#!/usr/bin/env python3
"""Antigravity Stop hook to detect stray scratch/debug files in workspace root.

Reads an Antigravity Stop JSON payload from stdin and checks ONLY top-level
regular files directly inside each directory listed in ``workspacePaths``
(never subdirectories, never symlinks, never ``artifactDirectoryPath``).

Infinite-loop prevention and fail-open rules:
1. If ``continuationActive`` is truthy -> immediately return ``{"decision": "allow"}``.
2. If ``terminationReason`` is present and not ``"NO_TOOL_CALL"`` (e.g.,
   ``"USER_CANCELED"``, ``"ERROR"``, ``"MAX_INVOCATIONS"``,
   ``"MAX_TOKEN_BUDGET_EXCEEDED"``, ``"TERMINAL_CUSTOM_HOOK"``) -> return
   ``{"decision": "allow"}``.
3. If ``error`` is non-empty or ``fullyIdle`` is explicitly ``false`` -> return
   ``{"decision": "allow"}``.
4. On malformed stdin JSON or missing/empty ``workspacePaths`` -> fail open
   with ``{"decision": "allow"}``.

Zero third-party dependencies (Python 3.10+ stdlib only).
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ALLOW_RESPONSE: dict[str, str] = {"decision": "allow"}

STRAY_PREFIXES: tuple[str, ...] = ("scratch_", "tmp_", "debug_")
STRAY_EXTENSIONS: frozenset[str] = frozenset({".py", ".sh", ".js", ".ts", ".txt", ".log"})
EXACT_STRAY_FILENAMES: frozenset[str] = frozenset(
    {
        "test_fail.log",
        "test_output.log",
        "debug.log",
        "output.tmp",
    }
)


def is_stray_filename(filename: str) -> bool:
    """Return True if ``filename`` matches a generic stray scratch/debug pattern."""
    lowered = filename.lower()
    if lowered in EXACT_STRAY_FILENAMES:
        return True
    if lowered.startswith(STRAY_PREFIXES):
        ext = Path(lowered).suffix
        if ext in STRAY_EXTENSIONS:
            return True
    return False


def _has_error(payload: dict[str, object]) -> bool:
    err = payload.get("error")
    if isinstance(err, str):
        return bool(err.strip())
    return bool(err)


def _is_same_or_within(path_realpath: str, directory_realpath: str) -> bool:
    try:
        common = os.path.commonpath([directory_realpath, path_realpath])
    except ValueError:
        return False
    return common == directory_realpath


def find_stray_root_files(
    workspace_paths: list[object],
    artifact_dir: str | None = None,
) -> list[str]:
    """Scan top-level regular files in each valid workspace root for stray files."""
    real_artifact_dir: str | None = None
    if (
        isinstance(artifact_dir, str)
        and artifact_dir.strip()
        and "\x00" not in artifact_dir
    ):
        try:
            real_artifact_dir = os.path.realpath(artifact_dir)
        except (OSError, ValueError):
            real_artifact_dir = None

    seen_roots: set[str] = set()
    found: list[str] = []

    for root in workspace_paths:
        if not isinstance(root, str) or not root.strip() or "\x00" in root:
            continue
        try:
            real_root = os.path.realpath(root)
        except (OSError, ValueError):
            continue
        if real_root in seen_roots:
            continue
        if real_artifact_dir is not None and _is_same_or_within(
            real_root, real_artifact_dir
        ):
            continue
        if not os.path.isdir(real_root):
            continue
        seen_roots.add(real_root)

        try:
            with os.scandir(root) as entries:
                for entry in entries:
                    try:
                        # Strictly top-level regular files: never directories, never symlinks.
                        if not entry.is_file(follow_symlinks=False):
                            continue
                    except OSError:
                        continue
                    if is_stray_filename(entry.name):
                        found.append(os.path.join(root, entry.name))
        except OSError:
            continue

    found.sort()
    return found


def evaluate_stop_payload(payload: object) -> dict[str, str]:
    """Evaluate a parsed Stop hook payload and return an Antigravity decision."""
    if not isinstance(payload, dict):
        return dict(ALLOW_RESPONSE)

    # CRITICAL: check continuationActive first to prevent infinite Stop loops.
    if payload.get("continuationActive"):
        return dict(ALLOW_RESPONSE)

    termination_reason = payload.get("terminationReason")
    if (
        termination_reason is not None
        and termination_reason != ""
        and termination_reason != "NO_TOOL_CALL"
    ):
        return dict(ALLOW_RESPONSE)

    if _has_error(payload):
        return dict(ALLOW_RESPONSE)

    if payload.get("fullyIdle") is False:
        return dict(ALLOW_RESPONSE)

    workspace_paths = payload.get("workspacePaths")
    if not isinstance(workspace_paths, list) or not workspace_paths:
        return dict(ALLOW_RESPONSE)

    artifact_dir = payload.get("artifactDirectoryPath")
    artifact_dir_str = artifact_dir if isinstance(artifact_dir, str) else None

    stray_files = find_stray_root_files(workspace_paths, artifact_dir=artifact_dir_str)
    if stray_files:
        listed = ", ".join(stray_files)
        return {
            "decision": "continue",
            "reason": (
                f"Stray scratch/log file(s) detected in workspace root: {listed}. "
                "Remove them or move them to your session scratch directory before finishing."
            ),
        }

    return dict(ALLOW_RESPONSE)


def main() -> int:
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            result = dict(ALLOW_RESPONSE)
        else:
            payload = json.loads(raw)
            result = evaluate_stop_payload(payload)
    except Exception:
        result = dict(ALLOW_RESPONSE)

    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
