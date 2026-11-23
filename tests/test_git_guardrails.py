"""Unit tests for the git-guardrails Antigravity PreToolUse hook."""

from __future__ import annotations

import importlib.util
import json
import os
import stat
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_DIR = REPO_ROOT / "plugins" / "git-guardrails"
HOOKS_JSON = PLUGIN_DIR / "hooks.json"
HOOK_SCRIPT = PLUGIN_DIR / "hooks" / "guard_git.py"


def _load_guard_module():
    prev = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec = importlib.util.spec_from_file_location("guard_git", HOOK_SCRIPT)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.dont_write_bytecode = prev


guard_git = _load_guard_module()


def _make_payload(command_line: str, tool_name: str = "run_command") -> str:
    return json.dumps(
        {
            "conversationId": "test-conv-001",
            "hookEventName": "PreToolUse",
            "toolCall": {
                "id": "toolu_01",
                "name": tool_name,
                "args": {"CommandLine": command_line},
            },
        }
    )


def _run_hook_subprocess(raw_stdin: str, direct: bool = False) -> dict[str, str]:
    cmd = [str(HOOK_SCRIPT)] if direct else [sys.executable, str(HOOK_SCRIPT)]
    proc = subprocess.run(
        cmd,
        input=raw_stdin,
        text=True,
        capture_output=True,
        cwd=PLUGIN_DIR,
        check=False,
    )
    if proc.returncode != 0:
        raise AssertionError(
            f"Hook exited with {proc.returncode}; stderr={proc.stderr!r}"
        )
    return json.loads(proc.stdout)


class TestPluginStructure(unittest.TestCase):
    def test_hooks_json_at_plugin_root(self) -> None:
        self.assertTrue(HOOKS_JSON.is_file(), "hooks.json must live at plugin root")
        self.assertFalse(
            (PLUGIN_DIR / "hooks" / "hooks.json").exists(),
            "hooks/hooks.json must not exist in native Antigravity plugins",
        )
        data = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))
        self.assertIn("git-guardrails", data)
        groups = data["git-guardrails"]["PreToolUse"]
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0]["matcher"], "run_command")
        handler = groups[0]["hooks"][0]
        self.assertEqual(handler["type"], "command")
        self.assertEqual(handler["command"], "python3 ./hooks/guard_git.py")
        self.assertEqual(handler["timeout"], 5)

    def test_hook_script_is_executable(self) -> None:
        self.assertTrue(HOOK_SCRIPT.is_file())
        mode = os.stat(HOOK_SCRIPT).st_mode
        self.assertTrue(mode & stat.S_IXUSR, "guard_git.py must have executable bit set")


class TestSubprocessContract(unittest.TestCase):
    def test_cli_deny_decision_schema(self) -> None:
        res = _run_hook_subprocess(_make_payload("git push --force origin main"))
        self.assertEqual(res["decision"], "deny")
        self.assertIsInstance(res.get("reason"), str)
        self.assertTrue(res["reason"].strip())

    def test_cli_force_ask_decision_schema(self) -> None:
        res = _run_hook_subprocess(_make_payload("git push origin main"))
        self.assertEqual(res["decision"], "force_ask")
        self.assertIsInstance(res.get("reason"), str)
        self.assertTrue(res["reason"].strip())

    def test_cli_allow_decision_schema(self) -> None:
        res = _run_hook_subprocess(_make_payload("git commit -m 'feat: safe'"))
        self.assertEqual(res["decision"], "allow")

    def test_direct_shebang_execution(self) -> None:
        res = _run_hook_subprocess(_make_payload("git reset --hard"), direct=True)
        self.assertEqual(res["decision"], "deny")

    def test_cli_malformed_stdin_fails_open(self) -> None:
        for bad_input in [
            "",
            "{not-valid-json",
            "[]",
            '"git push --force"',
            "{}",
            '{"toolCall": "not-an-object"}',
            '{"toolCall": {"name": "run_command"}}',
            '{"toolCall": {"name": "run_command", "args": {}}}',
            '{"toolCall": {"name": "run_command", "args": {"CommandLine": 42}}}',
        ]:
            with self.subTest(bad_input=bad_input):
                res = _run_hook_subprocess(bad_input)
                self.assertEqual(res, {"decision": "allow"})

    def test_non_run_command_tool_is_allowed(self) -> None:
        res = _run_hook_subprocess(
            _make_payload("git reset --hard", tool_name="view_file")
        )
        self.assertEqual(res, {"decision": "allow"})

    def test_payload_without_tool_name_still_evaluates(self) -> None:
        payload = json.dumps({"toolCall": {"args": {"CommandLine": "git reset --hard"}}})
        res = _run_hook_subprocess(payload)
        self.assertEqual(res["decision"], "deny")


class TestDenyDestructiveGit(unittest.TestCase):
    def _assert_deny(self, commands: list[str]) -> None:
        for cmd in commands:
            with self.subTest(cmd=cmd):
                res = guard_git.evaluate_command(cmd)
                self.assertEqual(res["decision"], "deny", f"Expected deny for: {cmd}")
                self.assertTrue(res.get("reason", "").strip())

    def test_deny_force_push_variants(self) -> None:
        self._assert_deny(
            [
                "git push --force",
                "git push --force origin main",
                "git push origin main --force",
                "git push -f",
                "git push -f origin main",
                "git push origin main -f",
                "git push -uf origin main",
                "git push -fu origin main",
                "git push -qvf origin main",
                "git push -fo ci.skip origin main",
                "git push -o ci.skip -f origin main",
                "git push --force-with-lease",
                "git push --force-with-lease origin main",
                "git push --force-with-lease=refs/heads/main:abc123 origin main",
                "git push origin main --force-with-lease",
                "git push --force-if-includes origin main",
                "git push origin +main",
                "git push origin +HEAD:main",
                "git push origin main +dev",
                "git push origin +refs/heads/main:refs/heads/main",
                "git push --repo=origin +main",
                "git push --repo origin +main",
                "git push origin -- +main",
            ]
        )

    def test_deny_reset_hard_variants(self) -> None:
        self._assert_deny(
            [
                "git reset --hard",
                "git reset --hard HEAD",
                "git reset --hard HEAD~1",
                "git reset --hard origin/main",
                "git reset HEAD~1 --hard",
                "git reset -q --hard",
            ]
        )

    def test_deny_clean_force_variants(self) -> None:
        self._assert_deny(
            [
                "git clean -f",
                "git clean --force",
                "git clean -fd",
                "git clean -df",
                "git clean -fx",
                "git clean -xf",
                "git clean -fX",
                "git clean -Xf",
                "git clean -fdx",
                "git clean -qdf",
                "git clean -d -f",
                "git clean -x -d -f",
                "git clean -d --force",
                "git clean --force -d -x",
                "git clean -ff -d",
                "git clean src/ -fd",
                "git clean -e '*.log' -f",
                "git clean --exclude='*.log' -fd",
                "git clean -fe '*.log'",
            ]
        )

    def test_deny_branch_force_delete_variants(self) -> None:
        self._assert_deny(
            [
                "git branch -D old-feature",
                "git branch old-feature -D",
                "git branch -D a b",
                "git branch -rD origin/old",
                "git branch --delete --force old-feature",
                "git branch --force --delete old-feature",
                "git branch -d -f old-feature",
                "git branch -f -d old-feature",
                "git branch -df old-feature",
                "git branch -fd old-feature",
                "git branch -d --force old-feature",
                "git branch --delete -f old-feature",
                "git branch --merged -D old-feature",
            ]
        )

    def test_deny_checkout_dot_variants(self) -> None:
        self._assert_deny(
            [
                "git checkout .",
                "git checkout ./",
                "git checkout ./.",
                "git checkout .//",
                "git checkout -- .",
                "git checkout -- ./",
                "git checkout HEAD -- .",
                "git checkout HEAD .",
                "git checkout main -- .",
                "git checkout main .",
                "git checkout origin/main -- README.md .",
                "git checkout -f .",
                "git checkout --ours .",
                "git checkout --conflict=merge -- .",
                "git checkout -- :/",
                "git checkout :/",
                "git checkout -- ':(top)'",
                'git checkout -- ":(top)."',
            ]
        )

    def test_deny_restore_dot_variants(self) -> None:
        self._assert_deny(
            [
                "git restore .",
                "git restore ./",
                "git restore ./.",
                "git restore -- .",
                "git restore -- ./",
                "git restore --worktree .",
                "git restore --worktree ./",
                "git restore -W .",
                "git restore --staged --worktree .",
                "git restore --worktree --staged ./",
                "git restore -S -W .",
                "git restore -SW .",
                "git restore -WS ./",
                "git restore --source=HEAD .",
                "git restore --source HEAD .",
                "git restore -s HEAD .",
                "git restore -sHEAD .",
                "git restore --source=HEAD --staged --worktree .",
                "git restore --source=HEAD -- README.md ./",
                "git restore -- :/",
                "git restore -- ':(top)'",
                'git restore -- ":(top)."',
            ]
        )


class TestForceAskStandardPush(unittest.TestCase):
    def _assert_force_ask(self, commands: list[str]) -> None:
        for cmd in commands:
            with self.subTest(cmd=cmd):
                res = guard_git.evaluate_command(cmd)
                self.assertEqual(
                    res["decision"], "force_ask", f"Expected force_ask for: {cmd}"
                )
                self.assertTrue(res.get("reason", "").strip())

    def test_standard_git_push_requires_confirmation(self) -> None:
        self._assert_force_ask(
            [
                "git push",
                "git push origin main",
                "git push -u origin feat/guardrails",
                "git push --set-upstream origin feat/guardrails",
                "git push --tags",
                "git push --no-force-with-lease origin main",
                "git push -o ci.skip origin main",
                "git push -ofoo origin main",
                "git push -o +custom origin main",
                "git push origin --delete merged-branch",
                "git push origin main >/tmp/push.log 2>&1",
                "git -C repo push origin main",
                "git --git-dir /tmp/r/.git --work-tree /tmp/r push origin main",
                "git add . && git commit -m 'ship it' && git push origin main",
            ]
        )


class TestGlobalFlagsWrappersAndCompoundShell(unittest.TestCase):
    def test_global_git_options(self) -> None:
        deny_cases = [
            "git -C repo reset --hard",
            "git -Crepo push -f",
            "git -C '/path/with spaces/repo' push --force",
            "git -c user.name=bot -c core.autocrlf=false push -f",
            "git -ccore.pager=cat clean -fd",
            "git --git-dir=/tmp/repo/.git --work-tree=/tmp/repo reset --hard",
            "git --git-dir /tmp/repo/.git --work-tree /tmp/repo checkout -- .",
            "git --no-pager branch -D stale",
            "git -P restore --worktree .",
            "git -p push origin +main",
            "git --bare --namespace=ns push --force-with-lease",
            "git --namespace ns reset --hard",
            "git --no-optional-locks --no-advice clean -df",
            "git --exec-path=/usr/lib/git-core push -f",
            "git -c alias.fp='push --force' fp origin main",
            "git -c alias.boom='!git reset --hard' boom",
            "/usr/bin/git push --force",
            "/usr/local/bin/git reset --hard",
            "git.exe clean -fd",
            r"\git push -f",
            "'git' reset --hard",
            'g""it clean -fd',
            "$'git' $'push' $'--force'",
            "$'\\x67it' reset --hard",
        ]
        for cmd in deny_cases:
            with self.subTest(cmd=cmd):
                self.assertEqual(guard_git.evaluate_command(cmd)["decision"], "deny")

    def test_compound_chains_subshells_and_substitutions(self) -> None:
        deny_cases = [
            "git status && git reset --hard",
            "false || git push --force",
            "echo ok; git clean -fd",
            "echo y | git branch -D old",
            "git status |& git reset --hard",
            "git reset --hard & echo bg",
            "git status\ngit checkout -- .",
            "git status\r\ngit restore .\r\n",
            "git \\\n  reset \\\n  --hard",
            "git commit -m 'ok'&&git push -f",
            "(cd repo && git reset --hard)",
            "{ git clean -fd; }",
            "if true; then git branch -D feat; fi",
            'for b in a b; do git branch -D "$b"; done',
            "case x in y) git reset --hard;; esac",
            "echo $(git reset --hard)",
            'echo "$(git push --force)"',
            "echo `git clean -fd`",
            'echo "`git branch -D foo`"',
            "echo ${FOO:-$(git reset --hard)}",
            "cat <(git push --force)",
            "cat <<EOF\n$(git reset --hard)\nEOF",
            "cat <<EOF && git push -f\nhello\nEOF",
            'git commit -m "$(cat <<\'EOF\'\ndon\'t break\nEOF\n)" && git push --force',
            "git reset --hard 2>&1 >/dev/null",
        ]
        for cmd in deny_cases:
            with self.subTest(cmd=cmd):
                self.assertEqual(guard_git.evaluate_command(cmd)["decision"], "deny")

    def test_wrappers_and_nested_shells(self) -> None:
        deny_cases = [
            "GIT_DIR=.git git reset --hard",
            "FOO=1 BAR='a b' git push -f",
            "env FOO=1 git push --force",
            "env -u BAR git push origin +main",
            'env -S "git push -f"',
            "command git reset --hard",
            "exec git clean -fd",
            "sudo git reset --hard",
            "sudo -u root git push --force",
            "nohup git push -f",
            "nice -n 5 git clean -fd",
            "time git reset --hard",
            "timeout 30 git push --force",
            "echo old | xargs git branch -D",
            "echo main | xargs -I{} git push -f origin {}",
            "find . -maxdepth 1 -exec git clean -fd {} \\;",
            "find . -maxdepth 1 -exec git clean -fd {} +",
            'sh -c "git reset --hard"',
            "bash -c 'git push --force'",
            '/bin/bash -lc "git clean -fd"',
            'bash -euo pipefail -c "git branch -D foo"',
            'bash -O extglob -c "git reset --hard"',
            'bash -c -e "git checkout ."',
            'zsh -c "git restore --worktree ."',
            'eval "git reset --hard"',
            "eval git push -f",
        ]
        for cmd in deny_cases:
            with self.subTest(cmd=cmd):
                self.assertEqual(guard_git.evaluate_command(cmd)["decision"], "deny")

    def test_wrappers_propagate_force_ask(self) -> None:
        force_ask_cases = [
            "GIT_SSH_COMMAND='ssh -i key' git push origin main",
            "timeout 30 git push origin main",
            'bash -euo pipefail -c "git push origin main"',
            "cat <(git push origin main)",
        ]
        for cmd in force_ask_cases:
            with self.subTest(cmd=cmd):
                self.assertEqual(
                    guard_git.evaluate_command(cmd)["decision"], "force_ask"
                )

    def test_deny_outranks_force_ask_in_compound_commands(self) -> None:
        for cmd in [
            "git push origin main && git reset --hard",
            "git reset --hard && git push origin main",
            "git push origin main; git clean -fd",
            "git push origin main && echo $(git branch -D old)",
        ]:
            with self.subTest(cmd=cmd):
                self.assertEqual(guard_git.evaluate_command(cmd)["decision"], "deny")


class TestAllowAndFalsePositiveResistance(unittest.TestCase):
    def _assert_allow(self, commands: list[str]) -> None:
        for cmd in commands:
            with self.subTest(cmd=cmd):
                res = guard_git.evaluate_command(cmd)
                self.assertEqual(res["decision"], "allow", f"Expected allow for: {cmd}")

    def test_allow_safe_local_git_commands(self) -> None:
        self._assert_allow(
            [
                "git status",
                "git diff",
                "git diff --stat HEAD~1",
                "git log -n 10 --oneline",
                "git add .",
                "git add -A",
                "git commit -m 'feat: add git guardrails'",
                "git commit --amend --no-edit",
                "git branch",
                "git branch -a",
                "git branch -v",
                "git branch -d merged-branch",
                "git branch --delete merged-branch",
                "git branch -u origin/main",
                "git checkout -b feat/new-branch",
                "git checkout -B feat/reset-branch main",
                "git checkout main",
                "git checkout origin/main",
                "git checkout -",
                "git checkout HEAD -- README.md",
                "git checkout -- src/app.py",
                "git checkout -- ./README.md",
                "git checkout README.md",
                "git restore README.md",
                "git restore ./README.md",
                "git restore --worktree src/app.py",
                "git restore --source=HEAD src/app.py",
                "git restore --staged .",
                "git restore -S .",
                "git restore -S ./",
                "git restore --staged --no-worktree .",
                "git reset",
                "git reset --soft HEAD~1",
                "git reset --mixed HEAD~1",
                "git reset HEAD file.py",
                "git reset -- --hard",
                "git clean -n",
                "git clean --dry-run -d",
                "git clean -nd",
                "git clean -n -e -f",
                "git clean -n -ef",
                "git clean -n -- -f",
                "git stash",
                "git stash pop",
                "git switch -c feat/x",
                "git help push",
                "git --version",
                "git --help push",
                "git -C repo status",
            ]
        )

    def test_no_false_positives_on_quoted_strings_comments_and_heredocs(self) -> None:
        self._assert_allow(
            [
                'git commit -m "prevent git reset --hard"',
                "git commit -m 'never run git push --force or git clean -fd'",
                'git commit -m "Mention \\`git push --force\\` in README"',
                "git commit -m 'Mention $(git reset --hard) in docs'",
                'git commit -m "Safe sub: $(git rev-parse --short HEAD)"',
                'git commit -m "docs: guardrails\n\nBlocks git reset --hard and git push --force."',
                'git commit -m "$(cat <<\'EOF\'\n1) don\'t run "git reset --hard" or git push --force\nEOF\n)"',
                "git commit -F - <<'EOF'\nBlock git push --force and git reset --hard\nEOF",
                'echo "git push --force"',
                "echo 'git reset --hard && git clean -fd'",
                'printf "%s\\n" "git branch -D old"',
                'grep "git reset --hard" hooks/guard_git.py',
                "rg 'git push --force' .",
                'git log --grep="git reset --hard"',
                "git status # do not run git reset --hard",
                "sh -c \"echo 'git reset --hard'\"",
                "command -v git",
                "ls -la",
                "python3 -m unittest discover -s tests -v",
                "",
                "   ",
            ]
        )


if __name__ == "__main__":
    unittest.main()
