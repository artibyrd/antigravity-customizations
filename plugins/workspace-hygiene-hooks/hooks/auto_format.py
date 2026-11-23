#!/usr/bin/env python3
"""Antigravity PostToolUse hook for fail-open multi-language auto-formatting.

Reads an Antigravity PostToolUse JSON payload from stdin, extracts the edited
file path from ``toolCall.args.Path`` (Antigravity 2.0) or
``toolCall.args.TargetFile`` (IDE), verifies workspace confinement against
``workspacePaths`` (and excludes ``artifactDirectoryPath`` when present), and
runs an installed formatter for supported file extensions:

- ``.py`` -> ``ruff format <file>`` (formatting only; never ``ruff check --fix``)
- ``.js``, ``.jsx``, ``.ts``, ``.tsx``, ``.mjs``, ``.cjs``, ``.css``,
  ``.json``, ``.yaml``, ``.yml`` -> ``prettier --write <file>``
- ``.go`` -> ``gofmt -w <file>``
- ``.rs`` -> ``rustfmt <file>``

Always fails open: skips when ``error`` is present, when the path lies outside
``workspacePaths``, when no matching formatter is installed on ``PATH``, or on
malformed input / formatter timeouts. Always prints ``{}`` on stdout and exits 0.

Zero third-party dependencies (Python 3.10+ stdlib only).
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

FORMATTER_TIMEOUT_SECONDS = 10

FORMATTER_BY_EXT: dict[str, tuple[str, ...]] = {
    ".py": ("ruff", "format"),
    ".js": ("prettier", "--write"),
    ".jsx": ("prettier", "--write"),
    ".ts": ("prettier", "--write"),
    ".tsx": ("prettier", "--write"),
    ".mjs": ("prettier", "--write"),
    ".cjs": ("prettier", "--write"),
    ".css": ("prettier", "--write"),
    ".json": ("prettier", "--write"),
    ".yaml": ("prettier", "--write"),
    ".yml": ("prettier", "--write"),
    ".go": ("gofmt", "-w"),
    ".rs": ("rustfmt",),
}


def _has_error(payload: dict[str, object]) -> bool:
    err = payload.get("error")
    if isinstance(err, str):
        return bool(err.strip())
    return bool(err)


def is_within_directory(target_realpath: str, directory_realpath: str) -> bool:
    """Return True if ``target_realpath`` is strictly inside ``directory_realpath``."""
    try:
        common = os.path.commonpath([directory_realpath, target_realpath])
    except ValueError:
        return False
    return common == directory_realpath and target_realpath != directory_realpath


def _extract_raw_path(payload: dict[str, object]) -> str | None:
    tool_call = payload.get("toolCall")
    if not isinstance(tool_call, dict):
        return None
    args = tool_call.get("args")
    if not isinstance(args, dict):
        return None

    for key in ("Path", "TargetFile"):
        val = args.get(key)
        if isinstance(val, str) and val.strip():
            return val
    return None


def resolve_target_file(payload: dict[str, object]) -> tuple[str, str] | None:
    """Validate and resolve the target file path and formatter working directory.

    Returns ``(real_target_path, formatter_cwd)`` if the file should be
    formatted, or ``None`` if it must be skipped.
    """
    if _has_error(payload):
        return None

    raw_path = _extract_raw_path(payload)
    if raw_path is None or "\x00" in raw_path:
        return None

    workspace_paths_raw = payload.get("workspacePaths")
    if workspace_paths_raw is not None and not isinstance(workspace_paths_raw, list):
        return None
    workspace_paths: list[object] = (
        workspace_paths_raw if isinstance(workspace_paths_raw, list) else []
    )

    cwd_raw = payload.get("cwd")
    cwd = (
        cwd_raw
        if isinstance(cwd_raw, str)
        and cwd_raw.strip()
        and "\x00" not in cwd_raw
        and os.path.isabs(cwd_raw)
        else None
    )

    if os.path.isabs(raw_path):
        candidate = raw_path
    elif cwd is not None:
        candidate = os.path.join(cwd, raw_path)
    elif len(workspace_paths) == 1 and isinstance(workspace_paths[0], str):
        ws0 = workspace_paths[0]
        if not ws0.strip() or "\x00" in ws0 or not os.path.isabs(ws0):
            return None
        candidate = os.path.join(ws0, raw_path)
    else:
        return None

    try:
        real_target = os.path.realpath(candidate)
    except (OSError, ValueError):
        return None

    # Exclude files inside artifactDirectoryPath even if nested under workspacePaths.
    artifact_dir_raw = payload.get("artifactDirectoryPath")
    if (
        isinstance(artifact_dir_raw, str)
        and artifact_dir_raw.strip()
        and "\x00" not in artifact_dir_raw
    ):
        try:
            real_artifact_dir = os.path.realpath(artifact_dir_raw)
        except (OSError, ValueError):
            real_artifact_dir = None
        if real_artifact_dir and (
            real_target == real_artifact_dir
            or is_within_directory(real_target, real_artifact_dir)
        ):
            return None

    matched_root: str | None = None
    if workspace_paths:
        for ws in workspace_paths:
            if not isinstance(ws, str) or not ws.strip() or "\x00" in ws:
                continue
            try:
                real_ws = os.path.realpath(ws)
            except (OSError, ValueError):
                continue
            if is_within_directory(real_target, real_ws):
                matched_root = real_ws
                break
        if matched_root is None:
            return None

    if not os.path.isfile(real_target):
        return None

    run_cwd = matched_root if matched_root is not None else os.path.dirname(real_target)
    return real_target, run_cwd


def get_formatter_command(target_path: str) -> list[str] | None:
    """Return the resolved formatter command list for ``target_path``, or None."""
    ext = Path(target_path).suffix.lower()
    spec = FORMATTER_BY_EXT.get(ext)
    if spec is None:
        return None
    binary = shutil.which(spec[0])
    if binary is None:
        return None
    return [binary, *spec[1:], target_path]


def format_file(
    target_path: str,
    run_cwd: str | None = None,
    timeout: float = FORMATTER_TIMEOUT_SECONDS,
) -> bool:
    """Run the matching installed formatter on ``target_path`` (fail-open).

    Returns True if a formatter was invoked and completed with exit code 0,
    False otherwise.
    """
    cmd = get_formatter_command(target_path)
    if cmd is None:
        return False

    try:
        proc = subprocess.run(
            cmd,
            cwd=run_cwd or os.path.dirname(target_path),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout,
            check=False,
        )
        return proc.returncode == 0
    except (subprocess.TimeoutExpired, OSError, ValueError):
        return False


def handle_payload(payload: object) -> dict[str, object]:
    """Process a parsed PostToolUse payload; always returns ``{}``."""
    if isinstance(payload, dict):
        resolved = resolve_target_file(payload)
        if resolved is not None:
            real_target, run_cwd = resolved
            format_file(real_target, run_cwd=run_cwd)
    return {}


def main() -> int:
    try:
        raw = sys.stdin.read()
        if raw.strip():
            payload = json.loads(raw)
            handle_payload(payload)
    except Exception:
        pass

    print(json.dumps({}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
