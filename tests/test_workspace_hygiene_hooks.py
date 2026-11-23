"""Unit tests for the workspace-hygiene-hooks PostToolUse and Stop hooks."""

from __future__ import annotations

import importlib.util
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_DIR = REPO_ROOT / "plugins" / "workspace-hygiene-hooks"
PLUGIN_JSON = PLUGIN_DIR / "plugin.json"
HOOKS_JSON = PLUGIN_DIR / "hooks.json"
AUTO_FORMAT_SCRIPT = PLUGIN_DIR / "hooks" / "auto_format.py"
CLEAN_CHECK_SCRIPT = PLUGIN_DIR / "hooks" / "check_workspace_clean.py"


def _load_module(name: str, path: Path):
    prev = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.dont_write_bytecode = prev


auto_format = _load_module("auto_format", AUTO_FORMAT_SCRIPT)
check_workspace_clean = _load_module("check_workspace_clean", CLEAN_CHECK_SCRIPT)


def _run_hook(
    script: Path,
    raw_stdin: str,
    *,
    env: dict[str, str] | None = None,
    direct: bool = False,
) -> dict[str, object]:
    cmd = [str(script)] if direct else [sys.executable, str(script)]
    proc = subprocess.run(
        cmd,
        input=raw_stdin,
        text=True,
        capture_output=True,
        cwd=PLUGIN_DIR,
        env=env,
        check=False,
    )
    if proc.returncode != 0:
        raise AssertionError(
            f"{script.name} exited with {proc.returncode}; "
            f"stdout={proc.stdout!r} stderr={proc.stderr!r}"
        )
    return json.loads(proc.stdout)


def _write_stub_binary(
    bin_dir: Path,
    name: str,
    log_path: Path,
    *,
    exit_code: int = 0,
    noisy: bool = False,
    sleep_seconds: float = 0.0,
) -> Path:
    stub = bin_dir / name
    code = f"""#!{sys.executable}
import json, os, sys, time
if {sleep_seconds!r} > 0:
    time.sleep({sleep_seconds!r})
if {noisy!r}:
    print("NOISY FORMATTER STDOUT")
    print("NOISY FORMATTER STDERR", file=sys.stderr)
entry = {{
    "bin": {name!r},
    "argv": sys.argv[1:],
    "cwd": os.getcwd(),
}}
with open({str(log_path)!r}, "a", encoding="utf-8") as fh:
    fh.write(json.dumps(entry) + "\\n")
sys.exit({exit_code!r})
"""
    stub.write_text(code, encoding="utf-8")
    stub.chmod(0o755)
    return stub


def _read_invocations(log_path: Path) -> list[dict[str, object]]:
    if not log_path.exists():
        return []
    lines = [
        line for line in log_path.read_text(encoding="utf-8").splitlines() if line.strip()
    ]
    return [json.loads(line) for line in lines]


class TestPluginStructure(unittest.TestCase):
    def test_hooks_json_at_plugin_root_with_two_independent_hooks(self) -> None:
        self.assertTrue(HOOKS_JSON.is_file(), "hooks.json must live at plugin root")
        self.assertFalse(
            (PLUGIN_DIR / "hooks" / "hooks.json").exists(),
            "hooks/hooks.json must not exist in native Antigravity plugins",
        )
        data = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))
        self.assertEqual(set(data.keys()), {"auto-format", "workspace-clean-check"})

        # Hook 1: auto-format (PostToolUse grouped structure)
        post_groups = data["auto-format"]["PostToolUse"]
        self.assertEqual(len(post_groups), 1)
        self.assertEqual(
            post_groups[0]["matcher"],
            "write_file|edit_file|replace_file_content|multi_replace_file_content|write_to_file",
        )
        post_handler = post_groups[0]["hooks"][0]
        self.assertEqual(post_handler["type"], "command")
        self.assertEqual(post_handler["command"], "python3 ./hooks/auto_format.py")
        self.assertEqual(post_handler["timeout"], 15)

        # Hook 2: workspace-clean-check (Stop flat list structure)
        stop_handlers = data["workspace-clean-check"]["Stop"]
        self.assertEqual(len(stop_handlers), 1)
        stop_handler = stop_handlers[0]
        self.assertEqual(stop_handler["type"], "command")
        self.assertEqual(
            stop_handler["command"], "python3 ./hooks/check_workspace_clean.py"
        )
        self.assertEqual(stop_handler["timeout"], 5)

    def test_hook_scripts_have_0755_permissions(self) -> None:
        for script in (AUTO_FORMAT_SCRIPT, CLEAN_CHECK_SCRIPT):
            with self.subTest(script=script.name):
                self.assertTrue(script.is_file())
                mode = stat.S_IMODE(os.stat(script).st_mode)
                self.assertEqual(
                    mode,
                    0o755,
                    f"{script.name} must have 0755 permissions (got {oct(mode)})",
                )

    def test_plugin_manifest_and_no_legacy_project_filenames(self) -> None:
        manifest = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "workspace-hygiene-hooks")
        self.assertLessEqual(len(manifest.get("suggestedPrompts", [])), 3)

        legacy_names = ("check_tables.py", "kill_stale_tests.py", "clear_pg_locks.py")
        for path in PLUGIN_DIR.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            for legacy in legacy_names:
                self.assertNotIn(
                    legacy,
                    text,
                    f"{path.relative_to(REPO_ROOT)} must not contain project-specific name {legacy!r}",
                )


class TestAutoFormatHook(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_root = Path(self._tmp.name)
        self.workspace = self.tmp_root / "workspace"
        self.workspace.mkdir()
        self.outside = self.tmp_root / "outside"
        self.outside.mkdir()
        self.bin_dir = self.tmp_root / "bin"
        self.bin_dir.mkdir()
        self.empty_bin_dir = self.tmp_root / "empty_bin"
        self.empty_bin_dir.mkdir()
        self.log_path = self.tmp_root / "invocations.jsonl"

        for tool in ("ruff", "prettier", "gofmt", "rustfmt"):
            _write_stub_binary(self.bin_dir, tool, self.log_path)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _env_with_path(self, path_dir: Path) -> dict[str, str]:
        env = dict(os.environ)
        env["PATH"] = str(path_dir)
        return env

    def _make_post_payload(
        self,
        args: dict[str, object],
        *,
        workspace_paths: list[str] | None = None,
        error: object = None,
        cwd: str | None = None,
        artifact_dir: str | None = None,
        tool_name: str = "write_file",
    ) -> str:
        payload: dict[str, object] = {
            "conversationId": "test-conv-hygiene",
            "hookEventName": "PostToolUse",
            "toolCall": {
                "id": "toolu_01",
                "name": tool_name,
                "args": args,
            },
        }
        if workspace_paths is not None:
            payload["workspacePaths"] = workspace_paths
        if error is not None:
            payload["error"] = error
        if cwd is not None:
            payload["cwd"] = cwd
        if artifact_dir is not None:
            payload["artifactDirectoryPath"] = artifact_dir
        return json.dumps(payload)

    def test_formats_using_path_and_target_file_schemas(self) -> None:
        py_file = self.workspace / "module.py"
        py_file.write_text("x=1\n", encoding="utf-8")
        ts_file = self.workspace / "app.ts"
        ts_file.write_text("const x=1;\n", encoding="utf-8")

        # Antigravity 2.0 schema: Path
        res1 = _run_hook(
            AUTO_FORMAT_SCRIPT,
            self._make_post_payload(
                {"Path": str(py_file)},
                workspace_paths=[str(self.workspace)],
                tool_name="write_file",
            ),
            env=self._env_with_path(self.bin_dir),
        )
        self.assertEqual(res1, {})

        # IDE schema: TargetFile
        res2 = _run_hook(
            AUTO_FORMAT_SCRIPT,
            self._make_post_payload(
                {"TargetFile": str(ts_file)},
                workspace_paths=[str(self.workspace)],
                tool_name="replace_file_content",
            ),
            env=self._env_with_path(self.bin_dir),
        )
        self.assertEqual(res2, {})

        invocations = _read_invocations(self.log_path)
        self.assertEqual(len(invocations), 2)
        self.assertEqual(invocations[0]["bin"], "ruff")
        self.assertEqual(invocations[0]["argv"], ["format", os.path.realpath(py_file)])
        self.assertEqual(invocations[0]["cwd"], os.path.realpath(self.workspace))
        # Ensure ruff check --fix is never invoked.
        self.assertNotIn("check", invocations[0]["argv"])
        self.assertNotIn("--fix", invocations[0]["argv"])

        self.assertEqual(invocations[1]["bin"], "prettier")
        self.assertEqual(
            invocations[1]["argv"], ["--write", os.path.realpath(ts_file)]
        )

    def test_multi_language_formatter_dispatch(self) -> None:
        cases = [
            ("a.py", "ruff", ["format"]),
            ("a.js", "prettier", ["--write"]),
            ("a.jsx", "prettier", ["--write"]),
            ("a.ts", "prettier", ["--write"]),
            ("a.tsx", "prettier", ["--write"]),
            ("a.mjs", "prettier", ["--write"]),
            ("a.cjs", "prettier", ["--write"]),
            ("a.css", "prettier", ["--write"]),
            ("a.json", "prettier", ["--write"]),
            ("a.yaml", "prettier", ["--write"]),
            ("a.yml", "prettier", ["--write"]),
            ("a.go", "gofmt", ["-w"]),
            ("a.rs", "rustfmt", []),
        ]
        for filename, expected_bin, expected_prefix in cases:
            with self.subTest(filename=filename):
                target = self.workspace / filename
                target.write_text("// stub\n", encoding="utf-8")
                self.log_path.unlink(missing_ok=True)
                res = _run_hook(
                    AUTO_FORMAT_SCRIPT,
                    self._make_post_payload(
                        {"Path": str(target)},
                        workspace_paths=[str(self.workspace)],
                    ),
                    env=self._env_with_path(self.bin_dir),
                )
                self.assertEqual(res, {})
                invocations = _read_invocations(self.log_path)
                self.assertEqual(len(invocations), 1)
                self.assertEqual(invocations[0]["bin"], expected_bin)
                self.assertEqual(
                    invocations[0]["argv"],
                    [*expected_prefix, os.path.realpath(target)],
                )

    def test_skips_when_tool_error_present(self) -> None:
        py_file = self.workspace / "broken.py"
        py_file.write_text("x=1\n", encoding="utf-8")

        res = _run_hook(
            AUTO_FORMAT_SCRIPT,
            self._make_post_payload(
                {"Path": str(py_file)},
                workspace_paths=[str(self.workspace)],
                error="exit status 1",
            ),
            env=self._env_with_path(self.bin_dir),
        )
        self.assertEqual(res, {})
        self.assertEqual(_read_invocations(self.log_path), [])

        # Empty error string should NOT block formatting.
        res_empty = _run_hook(
            AUTO_FORMAT_SCRIPT,
            self._make_post_payload(
                {"Path": str(py_file)},
                workspace_paths=[str(self.workspace)],
                error="",
            ),
            env=self._env_with_path(self.bin_dir),
        )
        self.assertEqual(res_empty, {})
        self.assertEqual(len(_read_invocations(self.log_path)), 1)

    def test_workspace_confinement_rejects_outside_traversal_prefix_and_symlink(
        self,
    ) -> None:
        outside_file = self.outside / "secret.py"
        outside_file.write_text("x=1\n", encoding="utf-8")

        sibling_prefix_dir = self.tmp_root / "workspace-evil"
        sibling_prefix_dir.mkdir()
        sibling_file = sibling_prefix_dir / "evil.py"
        sibling_file.write_text("x=1\n", encoding="utf-8")

        symlink_escape = self.workspace / "escape_link.py"
        symlink_escape.symlink_to(outside_file)

        artifact_dir = self.workspace / ".gemini" / "antigravity" / "artifacts"
        artifact_dir.mkdir(parents=True)
        artifact_py = artifact_dir / "scratch.py"
        artifact_py.write_text("x=1\n", encoding="utf-8")

        traversal_abs = os.path.join(str(self.workspace), "..", "outside", "secret.py")
        traversal_rel = os.path.join("..", "outside", "secret.py")

        rejected_cases = [
            ("outside_abs", {"Path": str(outside_file)}, None),
            ("traversal_abs", {"Path": traversal_abs}, None),
            ("traversal_rel", {"Path": traversal_rel}, None),
            ("sibling_prefix", {"Path": str(sibling_file)}, None),
            ("symlink_escape", {"Path": str(symlink_escape)}, None),
            ("artifact_dir", {"Path": str(artifact_py)}, str(artifact_dir)),
        ]
        for label, args, art_dir in rejected_cases:
            with self.subTest(case=label):
                self.log_path.unlink(missing_ok=True)
                res = _run_hook(
                    AUTO_FORMAT_SCRIPT,
                    self._make_post_payload(
                        args,
                        workspace_paths=[str(self.workspace)],
                        cwd=str(self.workspace),
                        artifact_dir=art_dir,
                    ),
                    env=self._env_with_path(self.bin_dir),
                )
                self.assertEqual(res, {})
                self.assertEqual(
                    _read_invocations(self.log_path),
                    [],
                    f"Formatter must NOT run for rejected case {label}",
                )

    def test_missing_formatter_fails_open(self) -> None:
        py_file = self.workspace / "missing_tool.py"
        py_file.write_text("x=1\n", encoding="utf-8")

        res = _run_hook(
            AUTO_FORMAT_SCRIPT,
            self._make_post_payload(
                {"Path": str(py_file)},
                workspace_paths=[str(self.workspace)],
            ),
            env=self._env_with_path(self.empty_bin_dir),
        )
        self.assertEqual(res, {})
        self.assertEqual(py_file.read_text(encoding="utf-8"), "x=1\n")

    def test_noisy_failing_formatter_still_outputs_clean_empty_json(self) -> None:
        noisy_bin = self.tmp_root / "noisy_bin"
        noisy_bin.mkdir()
        _write_stub_binary(
            noisy_bin, "ruff", self.log_path, exit_code=2, noisy=True
        )
        py_file = self.workspace / "noisy.py"
        py_file.write_text("x=1\n", encoding="utf-8")

        res = _run_hook(
            AUTO_FORMAT_SCRIPT,
            self._make_post_payload(
                {"Path": str(py_file)},
                workspace_paths=[str(self.workspace)],
            ),
            env=self._env_with_path(noisy_bin),
        )
        self.assertEqual(res, {})
        self.assertEqual(len(_read_invocations(self.log_path)), 1)

    def test_formatter_timeout_fails_open(self) -> None:
        slow_bin = self.tmp_root / "slow_bin"
        slow_bin.mkdir()
        _write_stub_binary(slow_bin, "ruff", self.log_path, sleep_seconds=3.0)
        py_file = self.workspace / "slow.py"
        py_file.write_text("x=1\n", encoding="utf-8")

        prev_path = os.environ.get("PATH")
        try:
            os.environ["PATH"] = str(slow_bin)
            ok = auto_format.format_file(
                str(py_file), run_cwd=str(self.workspace), timeout=0.3
            )
            self.assertFalse(ok)
        finally:
            if prev_path is None:
                os.environ.pop("PATH", None)
            else:
                os.environ["PATH"] = prev_path

    def test_malformed_json_and_unsupported_extensions_fail_open(self) -> None:
        md_file = self.workspace / "notes.md"
        md_file.write_text("# hi\n", encoding="utf-8")

        bad_inputs = [
            "",
            "{invalid-json",
            "[]",
            "{}",
            '{"toolCall": "bad"}',
            '{"toolCall": {"args": "bad"}}',
            '{"toolCall": {"args": {"Path": 123}}}',
            '{"toolCall": {"args": {"Path": "/tmp/bad\\u0000.py"}}}',
            '{"workspacePaths": "not-a-list", "toolCall": {"args": {"Path": "/tmp/a.py"}}}',
            self._make_post_payload(
                {"Path": str(self.workspace / "does_not_exist.py")},
                workspace_paths=[str(self.workspace)],
            ),
            self._make_post_payload(
                {"Path": str(md_file)},
                workspace_paths=[str(self.workspace)],
            ),
        ]
        for raw in bad_inputs:
            with self.subTest(raw=raw[:40]):
                res = _run_hook(
                    AUTO_FORMAT_SCRIPT,
                    raw,
                    env=self._env_with_path(self.bin_dir),
                )
                self.assertEqual(res, {})
        self.assertEqual(_read_invocations(self.log_path), [])

    def test_direct_shebang_execution(self) -> None:
        res = _run_hook(AUTO_FORMAT_SCRIPT, "{}", direct=True)
        self.assertEqual(res, {})


class TestWorkspaceCleanCheckHook(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_root = Path(self._tmp.name)
        self.workspace = self.tmp_root / "workspace"
        self.workspace.mkdir()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _make_stop_payload(
        self,
        *,
        workspace_paths: list[str] | None = None,
        continuation_active: bool | None = False,
        termination_reason: str | None = "NO_TOOL_CALL",
        fully_idle: bool | None = True,
        error: str | None = None,
        artifact_dir: str | None = None,
    ) -> str:
        payload: dict[str, object] = {
            "conversationId": "test-conv-stop",
            "hookEventName": "Stop",
        }
        if workspace_paths is not None:
            payload["workspacePaths"] = workspace_paths
        if continuation_active is not None:
            payload["continuationActive"] = continuation_active
        if termination_reason is not None:
            payload["terminationReason"] = termination_reason
        if fully_idle is not None:
            payload["fullyIdle"] = fully_idle
        if error is not None:
            payload["error"] = error
        if artifact_dir is not None:
            payload["artifactDirectoryPath"] = artifact_dir
        return json.dumps(payload)

    def test_continuation_active_prevents_infinite_loop(self) -> None:
        (self.workspace / "scratch_repro.py").write_text("print(1)\n", encoding="utf-8")
        res = _run_hook(
            CLEAN_CHECK_SCRIPT,
            self._make_stop_payload(
                workspace_paths=[str(self.workspace)],
                continuation_active=True,
                termination_reason="NO_TOOL_CALL",
            ),
        )
        self.assertEqual(res, {"decision": "allow"})

    def test_non_no_tool_call_termination_reasons_allow(self) -> None:
        (self.workspace / "debug.log").write_text("trace\n", encoding="utf-8")
        reasons = [
            "USER_CANCELED",
            "ERROR",
            "MAX_INVOCATIONS",
            "MAX_FORCED_INVOCATIONS",
            "MAX_TOKEN_BUDGET_EXCEEDED",
            "TERMINAL_STEP_TYPE",
            "TERMINAL_CUSTOM_HOOK",
            "INJECTED_RESPONSE",
        ]
        for reason in reasons:
            with self.subTest(terminationReason=reason):
                res = _run_hook(
                    CLEAN_CHECK_SCRIPT,
                    self._make_stop_payload(
                        workspace_paths=[str(self.workspace)],
                        continuation_active=False,
                        termination_reason=reason,
                    ),
                )
                self.assertEqual(res, {"decision": "allow"})

    def test_error_and_not_fully_idle_allow(self) -> None:
        (self.workspace / "scratch_debug.py").write_text("pass\n", encoding="utf-8")

        res_err = _run_hook(
            CLEAN_CHECK_SCRIPT,
            self._make_stop_payload(
                workspace_paths=[str(self.workspace)],
                error="model timeout",
            ),
        )
        self.assertEqual(res_err, {"decision": "allow"})

        res_busy = _run_hook(
            CLEAN_CHECK_SCRIPT,
            self._make_stop_payload(
                workspace_paths=[str(self.workspace)],
                fully_idle=False,
            ),
        )
        self.assertEqual(res_busy, {"decision": "allow"})

    def test_detects_stray_prefix_and_exact_filenames(self) -> None:
        stray_names = [
            "scratch_probe.py",
            "scratch_run.sh",
            "tmp_check.js",
            "tmp_parse.ts",
            "debug_notes.txt",
            "debug_trace.log",
            "test_fail.log",
            "test_output.log",
            "debug.log",
            "output.tmp",
        ]
        for name in stray_names:
            with self.subTest(filename=name):
                ws = self.tmp_root / f"ws_{name.replace('.', '_')}"
                ws.mkdir()
                stray_path = ws / name
                stray_path.write_text("temp\n", encoding="utf-8")

                res = _run_hook(
                    CLEAN_CHECK_SCRIPT,
                    self._make_stop_payload(
                        workspace_paths=[str(ws)],
                        continuation_active=False,
                        termination_reason="NO_TOOL_CALL",
                    ),
                )
                self.assertEqual(res["decision"], "continue")
                reason = res.get("reason")
                self.assertIsInstance(reason, str)
                assert isinstance(reason, str)
                self.assertIn(name, reason)
                self.assertIn("session scratch directory", reason)

    def test_ignores_legitimate_files_and_legacy_project_names(self) -> None:
        clean_names = [
            "README.md",
            "main.py",
            "test_app.py",
            "test_scratch_utils.py",
            "scratch_notes.md",
            "debug_config.yaml",
            "package.json",
            "Justfile",
            # Legacy project-specific filenames must NOT be flagged generically
            "check_tables.py",
            "kill_stale_tests.py",
            "clear_pg_locks.py",
        ]
        for name in clean_names:
            (self.workspace / name).write_text("ok\n", encoding="utf-8")

        res = _run_hook(
            CLEAN_CHECK_SCRIPT,
            self._make_stop_payload(
                workspace_paths=[str(self.workspace)],
                continuation_active=False,
                termination_reason="NO_TOOL_CALL",
            ),
        )
        self.assertEqual(res, {"decision": "allow"})

    def test_ignores_subdirectories_and_nested_stray_files(self) -> None:
        # Subdirectory containing a stray file must NOT be traversed.
        subdir = self.workspace / "scripts"
        subdir.mkdir()
        (subdir / "scratch_inside.py").write_text("pass\n", encoding="utf-8")
        (subdir / "debug.log").write_text("log\n", encoding="utf-8")

        # Subdirectory whose own name matches a stray filename must NOT be flagged.
        (self.workspace / "scratch_dir.py").mkdir()
        (self.workspace / "debug.log").mkdir()

        res = _run_hook(
            CLEAN_CHECK_SCRIPT,
            self._make_stop_payload(
                workspace_paths=[str(self.workspace)],
                continuation_active=False,
                termination_reason="NO_TOOL_CALL",
            ),
        )
        self.assertEqual(res, {"decision": "allow"})

    def test_ignores_symlinks_including_broken_symlinks(self) -> None:
        outside_target = self.tmp_root / "real_target.py"
        outside_target.write_text("pass\n", encoding="utf-8")

        (self.workspace / "scratch_link.py").symlink_to(outside_target)
        (self.workspace / "debug.log").symlink_to(outside_target)
        (self.workspace / "tmp_broken.log").symlink_to(
            self.tmp_root / "nonexistent_target.log"
        )

        res = _run_hook(
            CLEAN_CHECK_SCRIPT,
            self._make_stop_payload(
                workspace_paths=[str(self.workspace)],
                continuation_active=False,
                termination_reason="NO_TOOL_CALL",
            ),
        )
        self.assertEqual(res, {"decision": "allow"})

    def test_skips_artifact_directory_and_deduplicates_roots(self) -> None:
        artifact_dir = self.tmp_root / "artifacts"
        artifact_scratch = artifact_dir / "scratch"
        artifact_scratch.mkdir(parents=True)
        (artifact_dir / "scratch_script.py").write_text("pass\n", encoding="utf-8")
        (artifact_scratch / "scratch_nested.py").write_text("pass\n", encoding="utf-8")

        res_art = _run_hook(
            CLEAN_CHECK_SCRIPT,
            self._make_stop_payload(
                workspace_paths=[str(artifact_dir), str(artifact_scratch)],
                artifact_dir=str(artifact_dir),
            ),
        )
        self.assertEqual(res_art, {"decision": "allow"})

        # Duplicate roots report the stray file once.
        stray = self.workspace / "scratch_once.py"
        stray.write_text("pass\n", encoding="utf-8")
        res_dup = _run_hook(
            CLEAN_CHECK_SCRIPT,
            self._make_stop_payload(
                workspace_paths=[str(self.workspace), str(self.workspace)],
            ),
        )
        self.assertEqual(res_dup["decision"], "continue")
        reason = str(res_dup["reason"])
        self.assertEqual(reason.count("scratch_once.py"), 1)

    def test_malformed_and_missing_workspace_paths_fail_open(self) -> None:
        bad_inputs = [
            "",
            "{invalid-json",
            "[]",
            "{}",
            '{"workspacePaths": []}',
            '{"workspacePaths": "not-a-list"}',
            '{"workspacePaths": [123, null]}',
            '{"workspacePaths": ["/nonexistent/path/that/does/not/exist"]}',
        ]
        for raw in bad_inputs:
            with self.subTest(raw=raw[:40]):
                res = _run_hook(CLEAN_CHECK_SCRIPT, raw)
                self.assertEqual(res, {"decision": "allow"})

    def test_direct_shebang_execution(self) -> None:
        (self.workspace / "output.tmp").write_text("tmp\n", encoding="utf-8")
        res = _run_hook(
            CLEAN_CHECK_SCRIPT,
            self._make_stop_payload(workspace_paths=[str(self.workspace)]),
            direct=True,
        )
        self.assertEqual(res["decision"], "continue")
        self.assertIn("output.tmp", str(res["reason"]))


if __name__ == "__main__":
    unittest.main()
