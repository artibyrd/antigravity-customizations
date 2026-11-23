#!/usr/bin/env python3
"""Antigravity PreToolUse hook enforcing git safety guardrails.

Reads an Antigravity PreToolUse JSON payload from stdin, inspects
``toolCall.args.CommandLine``, and prints an Antigravity JSON decision:

- ``deny``: destructive git operations (force push, ``git reset --hard``,
  ``git clean -f``, ``git branch -D`` / ``--delete --force``,
  ``git checkout .``, and worktree-mutating ``git restore .``).
- ``force_ask``: standard non-force ``git push`` (always prompts the user,
  ignoring cached approvals).
- ``allow``: safe local git operations (including ``git commit``), non-git
  commands, and fail-open fallback on malformed stdin payloads.

Zero third-party dependencies (Python 3.10+ stdlib only).
"""

from __future__ import annotations

import json
import posixpath
import re
import sys

# Decision severity levels (higher takes precedence across compound commands).
_SEV_ALLOW = 0
_SEV_FORCE_ASK = 1
_SEV_DENY = 2

_ALLOW_RESULT: dict[str, str] = {"decision": "allow"}

_ENV_ASSIGN_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
_PATHSPEC_MAGIC_RE = re.compile(r"^:\(([^)]*)\)(.*)$")

_SHELL_KEYWORDS = {
    "if",
    "then",
    "elif",
    "else",
    "do",
    "while",
    "until",
    "!",
    "{",
    "coproc",
}

_SHELL_BINARIES = {
    "sh",
    "bash",
    "zsh",
    "dash",
    "ksh",
    "ash",
    "mksh",
    "fish",
    "csh",
    "tcsh",
}

# Git global options that consume the following token as a separate argument.
_GIT_GLOBAL_VALUE_OPTS = {
    "-C",
    "-c",
    "--git-dir",
    "--work-tree",
    "--namespace",
    "--super-prefix",
    "--config-env",
    "--attr-source",
}

# Git global options that print metadata and exit without dispatching a subcommand.
_GIT_GLOBAL_INFO_OPTS = {
    "-v",
    "--version",
    "-h",
    "--help",
    "--html-path",
    "--man-path",
    "--info-path",
}

_ANSI_C_SIMPLE = {
    "a": "\a",
    "b": "\b",
    "e": "\x1b",
    "E": "\x1b",
    "f": "\f",
    "n": "\n",
    "r": "\r",
    "t": "\t",
    "v": "\v",
    "\\": "\\",
    "'": "'",
    '"': '"',
    "?": "?",
}


def _basename_lower(token: str) -> str:
    """Return lowercase executable basename across POSIX and Windows separators."""
    return re.split(r"[/\\]", token)[-1].lower()


def _decode_ansi_c(raw: str) -> str:
    """Decode bash ANSI-C $'...' escape sequences."""
    out: list[str] = []
    i = 0
    n = len(raw)
    while i < n:
        ch = raw[i]
        if ch != "\\" or i + 1 >= n:
            out.append(ch)
            i += 1
            continue
        nxt = raw[i + 1]
        if nxt in _ANSI_C_SIMPLE:
            out.append(_ANSI_C_SIMPLE[nxt])
            i += 2
        elif nxt == "x":
            m = re.match(r"[0-9A-Fa-f]{1,2}", raw[i + 2 :])
            if m:
                out.append(chr(int(m.group(0), 16)))
                i += 2 + len(m.group(0))
            else:
                out.append("\\x")
                i += 2
        elif nxt in ("u", "U"):
            max_len = 4 if nxt == "u" else 8
            m = re.match(rf"[0-9A-Fa-f]{{1,{max_len}}}", raw[i + 2 :])
            if m:
                code = int(m.group(0), 16)
                out.append(chr(code) if 0 <= code <= 0x10FFFF else "")
                i += 2 + len(m.group(0))
            else:
                out.append("\\" + nxt)
                i += 2
        elif nxt in "01234567":
            m = re.match(r"[0-7]{1,3}", raw[i + 1 :])
            if m:
                out.append(chr(int(m.group(0), 8) & 0xFF))
                i += 1 + len(m.group(0))
            else:
                out.append(nxt)
                i += 2
        elif nxt == "c" and i + 2 < n:
            out.append(chr(ord(raw[i + 2].upper()) ^ 0x40))
            i += 3
        else:
            out.append("\\" + nxt)
            i += 2
    return "".join(out)


def _scan_backtick_sub(
    text: str, start: int, *, in_double_quotes: bool
) -> tuple[str, int]:
    """Scan a `...` command substitution starting right after the opening backtick."""
    inner: list[str] = []
    j = start
    n = len(text)
    while j < n:
        ch = text[j]
        if ch == "\\" and j + 1 < n:
            nxt = text[j + 1]
            if nxt == "\n":
                j += 2
                continue
            if nxt in ("$", "`", "\\") or (in_double_quotes and nxt == '"'):
                inner.append(nxt)
                j += 2
                continue
            inner.append("\\")
            j += 1
            continue
        if ch == "`":
            return "".join(inner), j + 1
        inner.append(ch)
        j += 1
    return "".join(inner), n


def _scan_heredoc_delim(text: str, pos: int) -> tuple[str, int]:
    """Read a heredoc delimiter token starting at ``pos`` (skipping spaces/tabs)."""
    n = len(text)
    while pos < n and text[pos] in (" ", "\t"):
        pos += 1
    chars: list[str] = []
    while pos < n and text[pos] not in (" ", "\t", "\r", "\n", ";", "|", "&", "(", ")", "<", ">"):
        ch = text[pos]
        if ch == "'":
            pos += 1
            while pos < n and text[pos] != "'":
                chars.append(text[pos])
                pos += 1
            if pos < n:
                pos += 1
        elif ch == '"':
            pos += 1
            while pos < n and text[pos] != '"':
                if text[pos] == "\\" and pos + 1 < n and text[pos + 1] in ('"', "\\", "$", "`"):
                    chars.append(text[pos + 1])
                    pos += 2
                else:
                    chars.append(text[pos])
                    pos += 1
            if pos < n:
                pos += 1
        elif ch == "\\" and pos + 1 < n:
            chars.append(text[pos + 1])
            pos += 2
        else:
            chars.append(ch)
            pos += 1
    return "".join(chars), pos


def _skip_heredoc_bodies(
    text: str, pos: int, pending: list[tuple[str, bool]]
) -> int:
    """Advance ``pos`` past the bodies of all pending heredocs."""
    n = len(text)
    for delim, strip_tabs in pending:
        while pos < n:
            nl = text.find("\n", pos)
            if nl == -1:
                line = text[pos:]
                pos = n
            else:
                line = text[pos:nl]
                pos = nl + 1
            check = line.rstrip("\r")
            if strip_tabs:
                check = check.lstrip("\t")
            if check == delim:
                break
    pending.clear()
    return pos


def _scan_paren_sub(text: str, start: int) -> tuple[str, int]:
    """Scan a $(...), <(...), or >(...) body starting right after the opening '('."""
    depth = 1
    j = start
    n = len(text)
    at_word_start = True
    pending_heredocs: list[tuple[str, bool]] = []
    while j < n:
        ch = text[j]
        if ch == "\n":
            j += 1
            at_word_start = True
            if pending_heredocs:
                j = _skip_heredoc_bodies(text, j, pending_heredocs)
            continue
        if ch == "<" and j + 1 < n and text[j + 1] == "<" and text[j : j + 3] != "<<<":
            strip_tabs = text[j : j + 3] == "<<-"
            j += 3 if strip_tabs else 2
            delim, j = _scan_heredoc_delim(text, j)
            if delim:
                pending_heredocs.append((delim, strip_tabs))
            at_word_start = False
            continue
        if ch == "'":
            j += 1
            while j < n and text[j] != "'":
                j += 1
            if j < n:
                j += 1
            at_word_start = False
        elif ch == "$" and j + 1 < n and text[j + 1] == "'":
            j += 2
            while j < n:
                if text[j] == "\\" and j + 1 < n:
                    j += 2
                elif text[j] == "'":
                    j += 1
                    break
                else:
                    j += 1
            at_word_start = False
        elif ch == '"':
            j += 1
            while j < n:
                if text[j] == "\\" and j + 1 < n:
                    j += 2
                elif text[j] == "$" and j + 1 < n and text[j + 1] == "(":
                    _, j = _scan_paren_sub(text, j + 2)
                elif text[j] == "`":
                    _, j = _scan_backtick_sub(text, j + 1, in_double_quotes=True)
                elif text[j] == '"':
                    j += 1
                    break
                else:
                    j += 1
            at_word_start = False
        elif ch == "\\" and j + 1 < n:
            j += 2
            at_word_start = False
        elif ch == "`":
            _, j = _scan_backtick_sub(text, j + 1, in_double_quotes=False)
            at_word_start = False
        elif ch == "#" and at_word_start:
            while j < n and text[j] != "\n":
                j += 1
        elif ch == "(":
            depth += 1
            j += 1
            at_word_start = True
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return text[start:j], j + 1
            j += 1
            at_word_start = True
        else:
            at_word_start = ch in " \t\r\n;|&"
            j += 1
    return text[start:], n


def _extract_heredoc_substitutions(body: str) -> list[str]:
    """Extract unescaped $(...) and `...` substitutions from an unquoted heredoc."""
    subs: list[str] = []
    j = 0
    n = len(body)
    while j < n:
        ch = body[j]
        if ch == "\\" and j + 1 < n:
            if body[j + 1] in ("$", "`", "\\", "\n"):
                j += 2
            else:
                j += 1
            continue
        if ch == "$" and j + 1 < n and body[j + 1] == "(":
            inner, j = _scan_paren_sub(body, j + 2)
            subs.append(inner)
            continue
        if ch == "`":
            inner, j = _scan_backtick_sub(body, j + 1, in_double_quotes=False)
            subs.append(inner)
            continue
        j += 1
    return subs


def _lex_shell(text: str) -> tuple[list[list[str]], list[str]]:
    """Lex a POSIX/bash command line into simple commands and embedded substitutions.

    Preserves quoting semantics so strings inside single/double quotes or quoted
    heredocs are not misparsed as separate commands, while still extracting
    executable command/process substitutions ($(...), `...`, <(...), >(...)).
    """
    commands: list[list[str]] = []
    substitutions: list[str] = []
    current_cmd: list[str] = []
    buf: list[str] = []
    in_word = False
    word_quoted = False
    expect_redir_target: str | None = None
    pending_heredocs: list[tuple[str, bool, bool]] = []

    def flush_word() -> None:
        nonlocal in_word, word_quoted, expect_redir_target
        if not in_word:
            return
        word = "".join(buf)
        buf.clear()
        was_quoted = word_quoted
        in_word = False
        word_quoted = False
        if expect_redir_target is not None:
            kind = expect_redir_target
            expect_redir_target = None
            if kind in ("heredoc", "heredoc_strip"):
                pending_heredocs.append((word, kind == "heredoc_strip", not was_quoted))
        else:
            current_cmd.append(word)

    def flush_cmd() -> None:
        nonlocal current_cmd, expect_redir_target
        flush_word()
        expect_redir_target = None
        if current_cmd:
            commands.append(current_cmd)
            current_cmd = []

    def consume_heredocs(pos: int) -> int:
        n_text = len(text)
        for delim, strip_tabs, expand in pending_heredocs:
            body_lines: list[str] = []
            while pos < n_text:
                nl = text.find("\n", pos)
                if nl == -1:
                    line = text[pos:]
                    pos = n_text
                else:
                    line = text[pos:nl]
                    pos = nl + 1
                check = line.rstrip("\r")
                if strip_tabs:
                    check = check.lstrip("\t")
                if check == delim:
                    break
                body_lines.append(line)
            if expand and body_lines:
                substitutions.extend(
                    _extract_heredoc_substitutions("\n".join(body_lines))
                )
        pending_heredocs.clear()
        return pos

    i = 0
    n = len(text)
    while i < n:
        ch = text[i]

        # Horizontal whitespace ends the current word.
        if ch in (" ", "\t", "\r"):
            flush_word()
            i += 1
            continue

        # Newline terminates the current command and consumes pending heredocs.
        if ch == "\n":
            flush_cmd()
            i += 1
            if pending_heredocs:
                i = consume_heredocs(i)
            continue

        # Comments begin only when '#' starts a new word.
        if ch == "#" and not in_word:
            while i < n and text[i] != "\n":
                i += 1
            continue

        # Process substitution: <(...) or >(...)
        if ch in ("<", ">") and i + 1 < n and text[i + 1] == "(":
            inner, i = _scan_paren_sub(text, i + 2)
            substitutions.append(inner)
            in_word = True
            buf.append("/dev/fd/procsub")
            continue

        # Redirections: &>> and &> must be checked before the '&' operator.
        if ch == "&" and i + 1 < n and text[i + 1] == ">":
            flush_word()
            expect_redir_target = "normal"
            i += 3 if text[i : i + 3] == "&>>" else 2
            continue

        # Command separator / grouping operators.
        if text[i : i + 3] == ";;&":
            flush_cmd()
            i += 3
            continue
        if text[i : i + 2] in ("&&", "||", "|&", ";;", ";&"):
            flush_cmd()
            i += 2
            continue
        if ch in (";", "|", "&", "(", ")"):
            flush_cmd()
            i += 1
            continue

        # Redirections starting with '<' or '>' (with optional numeric FD prefix).
        if ch in ("<", ">"):
            if in_word and not word_quoted and buf and all(c.isdigit() for c in buf):
                buf.clear()
                in_word = False
            else:
                flush_word()
            if text[i : i + 3] == "<<-":
                expect_redir_target = "heredoc_strip"
                i += 3
            elif text[i : i + 3] == "<<<":
                expect_redir_target = "normal"
                i += 3
            elif text[i : i + 2] == "<<":
                expect_redir_target = "heredoc"
                i += 2
            elif text[i : i + 2] in (">>", ">|", ">&", "<&", "<>"):
                expect_redir_target = "normal"
                i += 2
            else:
                expect_redir_target = "normal"
                i += 1
            continue

        # Single quotes: completely literal.
        if ch == "'":
            in_word = True
            word_quoted = True
            i += 1
            while i < n and text[i] != "'":
                buf.append(text[i])
                i += 1
            if i < n:
                i += 1
            continue

        # ANSI-C quotes: $'...'
        if ch == "$" and i + 1 < n and text[i + 1] == "'":
            in_word = True
            word_quoted = True
            i += 2
            raw_chars: list[str] = []
            while i < n:
                if text[i] == "\\" and i + 1 < n:
                    raw_chars.append(text[i])
                    raw_chars.append(text[i + 1])
                    i += 2
                elif text[i] == "'":
                    i += 1
                    break
                else:
                    raw_chars.append(text[i])
                    i += 1
            buf.append(_decode_ansi_c("".join(raw_chars)))
            continue

        # Double quotes ("...") or locale quotes ($"...").
        if ch == '"' or (ch == "$" and i + 1 < n and text[i + 1] == '"'):
            in_word = True
            word_quoted = True
            i += 2 if ch == "$" else 1
            while i < n:
                c = text[i]
                if c == '"':
                    i += 1
                    break
                if c == "\\" and i + 1 < n:
                    nxt = text[i + 1]
                    if nxt == "\n":
                        i += 2
                    elif nxt in ('"', "\\", "$", "`"):
                        buf.append(nxt)
                        i += 2
                    else:
                        buf.append("\\")
                        buf.append(nxt)
                        i += 2
                elif c == "$" and i + 1 < n and text[i + 1] == "(":
                    inner, i = _scan_paren_sub(text, i + 2)
                    substitutions.append(inner)
                    buf.append("$(" + inner + ")")
                elif c == "`":
                    inner, i = _scan_backtick_sub(text, i + 1, in_double_quotes=True)
                    substitutions.append(inner)
                    buf.append("`" + inner + "`")
                else:
                    buf.append(c)
                    i += 1
            continue

        # Unquoted command substitution: $(...)
        if ch == "$" and i + 1 < n and text[i + 1] == "(":
            in_word = True
            inner, i = _scan_paren_sub(text, i + 2)
            substitutions.append(inner)
            buf.append("$(" + inner + ")")
            continue

        # Unquoted backtick substitution: `...`
        if ch == "`":
            in_word = True
            inner, i = _scan_backtick_sub(text, i + 1, in_double_quotes=False)
            substitutions.append(inner)
            buf.append("`" + inner + "`")
            continue

        # Unquoted backslash escape / line continuation.
        if ch == "\\":
            if i + 1 < n:
                if text[i + 1] == "\n":
                    i += 2
                else:
                    in_word = True
                    word_quoted = True
                    buf.append(text[i + 1])
                    i += 2
            else:
                i += 1
            continue

        # Regular unquoted character.
        in_word = True
        buf.append(ch)
        i += 1

    flush_cmd()
    return commands, substitutions


def _is_dot_or_root_pathspec(token: str) -> bool:
    """Return True if a git pathspec targets '.' / './' or the repository root."""
    if not token:
        return False
    if token in (":/", ":/.", ":/./"):
        return True
    magic_match = _PATHSPEC_MAGIC_RE.match(token)
    if magic_match:
        magic = magic_match.group(1)
        remainder = magic_match.group(2)
        if not remainder:
            return "top" in {part.strip() for part in magic.split(",") if part.strip()}
        return posixpath.normpath(remainder) == "."
    if token.startswith(":/"):
        remainder = token[2:]
        return not remainder or posixpath.normpath(remainder) == "."
    return posixpath.normpath(token) == "."


def _check_git_push(args: list[str]) -> tuple[int, dict[str, str]]:
    """Evaluate `git push` arguments: deny force pushes, force_ask standard pushes."""
    value_opts = {
        "--repo",
        "--receive-pack",
        "--exec",
        "-o",
        "--push-option",
        "--recurse-submodules",
    }
    positionals: list[str] = []
    after_double_dash = False
    i = 0
    n = len(args)

    while i < n:
        arg = args[i]
        if after_double_dash:
            positionals.append(arg)
            i += 1
            continue
        if arg == "--":
            after_double_dash = True
            i += 1
            continue
        if arg == "--force":
            return (
                _SEV_DENY,
                {
                    "decision": "deny",
                    "reason": (
                        "Blocked by git-guardrails: force-pushing with 'git push --force' "
                        "can overwrite remote history. Push without force or ask the user "
                        "to run it manually."
                    ),
                },
            )
        if arg == "--force-with-lease" or arg.startswith("--force-with-lease="):
            return (
                _SEV_DENY,
                {
                    "decision": "deny",
                    "reason": (
                        "Blocked by git-guardrails: force-pushing with '--force-with-lease' "
                        "rewrites remote history. Push without force or ask the user to "
                        "run it manually."
                    ),
                },
            )
        if arg == "--force-if-includes":
            return (
                _SEV_DENY,
                {
                    "decision": "deny",
                    "reason": (
                        "Blocked by git-guardrails: force-pushing with '--force-if-includes' "
                        "rewrites remote history. Push without force or ask the user to "
                        "run it manually."
                    ),
                },
            )
        if arg in value_opts:
            i += 2
            continue
        if arg.startswith("--"):
            i += 1
            continue
        if arg.startswith("-") and len(arg) > 1:
            # Combined short flags: -o consumes the remainder (or next token).
            consumed_next = False
            for idx, ch in enumerate(arg[1:]):
                if ch == "o":
                    if idx == len(arg) - 2:
                        consumed_next = True
                    break
                if ch == "f":
                    return (
                        _SEV_DENY,
                        {
                            "decision": "deny",
                            "reason": (
                                "Blocked by git-guardrails: force-pushing with 'git push -f' "
                                "can overwrite remote history. Push without force or ask "
                                "the user to run it manually."
                            ),
                        },
                    )
            i += 2 if consumed_next else 1
            continue

        positionals.append(arg)
        i += 1

    for pos in positionals:
        if pos.startswith("+"):
            return (
                _SEV_DENY,
                {
                    "decision": "deny",
                    "reason": (
                        f"Blocked by git-guardrails: refspec '{pos}' uses the '+' force-push "
                        "prefix, which overwrites remote history. Push without '+' or ask "
                        "the user to run it manually."
                    ),
                },
            )

    return (
        _SEV_FORCE_ASK,
        {
            "decision": "force_ask",
            "reason": (
                "git-guardrails requires explicit confirmation before pushing to a remote "
                "repository with 'git push'."
            ),
        },
    )


def _check_git_reset(args: list[str]) -> tuple[int, dict[str, str]]:
    """Deny `git reset --hard`; allow soft/mixed/path resets."""
    value_opts = {"-U", "--unified", "--inter-hunk-context", "--pathspec-from-file"}
    i = 0
    n = len(args)
    while i < n:
        arg = args[i]
        if arg == "--":
            break
        if arg == "--hard":
            return (
                _SEV_DENY,
                {
                    "decision": "deny",
                    "reason": (
                        "Blocked by git-guardrails: 'git reset --hard' permanently discards "
                        "uncommitted working-tree and index changes. Use 'git stash', "
                        "'git reset --soft', or ask the user to run it manually."
                    ),
                },
            )
        if arg in value_opts:
            i += 2
            continue
        i += 1
    return _SEV_ALLOW, _ALLOW_RESULT


def _check_git_clean(args: list[str]) -> tuple[int, dict[str, str]]:
    """Deny `git clean` with `-f` / `--force` (including combined short flags)."""
    i = 0
    n = len(args)
    while i < n:
        arg = args[i]
        if arg == "--":
            break
        if arg == "--force":
            return (
                _SEV_DENY,
                {
                    "decision": "deny",
                    "reason": (
                        "Blocked by git-guardrails: 'git clean --force' permanently deletes "
                        "untracked files. Preview with 'git clean -n' or ask the user to "
                        "clean manually."
                    ),
                },
            )
        if arg in ("-e", "--exclude"):
            i += 2
            continue
        if arg.startswith("--"):
            i += 1
            continue
        if arg.startswith("-") and len(arg) > 1:
            consumed_next = False
            for idx, ch in enumerate(arg[1:]):
                if ch == "e":
                    if idx == len(arg) - 2:
                        consumed_next = True
                    break
                if ch == "f":
                    return (
                        _SEV_DENY,
                        {
                            "decision": "deny",
                            "reason": (
                                "Blocked by git-guardrails: 'git clean -f' permanently deletes "
                                "untracked files. Preview with 'git clean -n' or ask the user "
                                "to clean manually."
                            ),
                        },
                    )
            i += 2 if consumed_next else 1
            continue
        i += 1
    return _SEV_ALLOW, _ALLOW_RESULT


def _check_git_branch(args: list[str]) -> tuple[int, dict[str, str]]:
    """Deny `git branch -D` and `git branch --delete --force` / `-d -f`."""
    required_value_opts = {
        "-u",
        "--set-upstream-to",
        "--delete-merged",
        "--forked",
        "--sort",
        "--format",
    }
    optional_value_opts = {
        "--contains",
        "--no-contains",
        "--merged",
        "--no-merged",
        "--points-at",
    }
    has_delete = False
    has_force = False
    has_force_delete = False
    i = 0
    n = len(args)

    while i < n:
        arg = args[i]
        if arg == "--":
            break
        if arg == "--delete":
            has_delete = True
            i += 1
            continue
        if arg == "--force":
            has_force = True
            i += 1
            continue
        if arg in required_value_opts:
            i += 2
            continue
        if arg in optional_value_opts:
            if i + 1 < n and not args[i + 1].startswith("-"):
                i += 2
            else:
                i += 1
            continue
        if arg.startswith("--"):
            i += 1
            continue
        if arg.startswith("-") and len(arg) > 1:
            consumed_next = False
            for idx, ch in enumerate(arg[1:]):
                if ch == "u":
                    if idx == len(arg) - 2:
                        consumed_next = True
                    break
                if ch == "D":
                    has_force_delete = True
                elif ch == "d":
                    has_delete = True
                elif ch == "f":
                    has_force = True
            i += 2 if consumed_next else 1
            continue
        i += 1

    if has_force_delete or (has_delete and has_force):
        return (
            _SEV_DENY,
            {
                "decision": "deny",
                "reason": (
                    "Blocked by git-guardrails: force-deleting a branch ('git branch -D' "
                    "or '--delete --force') can discard unmerged commits. Use safe "
                    "'git branch -d' or ask the user to delete it manually."
                ),
            },
        )
    return _SEV_ALLOW, _ALLOW_RESULT


def _check_git_checkout(args: list[str]) -> tuple[int, dict[str, str]]:
    """Deny `git checkout .` / `git checkout -- .` / `git checkout <ref> -- .`."""
    value_opts = {
        "-b",
        "-B",
        "--orphan",
        "--conflict",
        "-U",
        "--unified",
        "--inter-hunk-context",
        "--pathspec-from-file",
    }
    positionals: list[str] = []
    after_double_dash = False
    i = 0
    n = len(args)

    while i < n:
        arg = args[i]
        if after_double_dash:
            positionals.append(arg)
            i += 1
            continue
        if arg == "--":
            after_double_dash = True
            i += 1
            continue
        if arg in value_opts:
            i += 2
            continue
        if arg.startswith("--"):
            i += 1
            continue
        if arg.startswith("-") and len(arg) > 1:
            consumed_next = False
            for idx, ch in enumerate(arg[1:]):
                if ch in ("b", "B", "U"):
                    if idx == len(arg) - 2:
                        consumed_next = True
                    break
            i += 2 if consumed_next else 1
            continue
        positionals.append(arg)
        i += 1

    for pos in positionals:
        if _is_dot_or_root_pathspec(pos):
            return (
                _SEV_DENY,
                {
                    "decision": "deny",
                    "reason": (
                        f"Blocked by git-guardrails: 'git checkout' targeting '{pos}' "
                        "discards all unstaged working-tree edits. Target a specific file, "
                        "use 'git stash', or ask the user to run it manually."
                    ),
                },
            )
    return _SEV_ALLOW, _ALLOW_RESULT


def _check_git_restore(args: list[str]) -> tuple[int, dict[str, str]]:
    """Deny worktree-mutating `git restore .` (allowing `git restore --staged .`)."""
    value_opts = {
        "-s",
        "--source",
        "--conflict",
        "-U",
        "--unified",
        "--inter-hunk-context",
        "--pathspec-from-file",
    }
    staged = False
    worktree: bool | None = None
    positionals: list[str] = []
    after_double_dash = False
    i = 0
    n = len(args)

    while i < n:
        arg = args[i]
        if after_double_dash:
            positionals.append(arg)
            i += 1
            continue
        if arg == "--":
            after_double_dash = True
            i += 1
            continue
        if arg == "--staged":
            staged = True
            i += 1
            continue
        if arg == "--no-staged":
            staged = False
            i += 1
            continue
        if arg == "--worktree":
            worktree = True
            i += 1
            continue
        if arg == "--no-worktree":
            worktree = False
            i += 1
            continue
        if arg in value_opts:
            i += 2
            continue
        if arg.startswith("--"):
            i += 1
            continue
        if arg.startswith("-") and len(arg) > 1:
            consumed_next = False
            for idx, ch in enumerate(arg[1:]):
                if ch in ("s", "U"):
                    if idx == len(arg) - 2:
                        consumed_next = True
                    break
                if ch == "S":
                    staged = True
                elif ch == "W":
                    worktree = True
            i += 2 if consumed_next else 1
            continue
        positionals.append(arg)
        i += 1

    # By default git restore modifies the worktree unless only --staged is given.
    affects_worktree = worktree if worktree is not None else (not staged)
    if affects_worktree:
        for pos in positionals:
            if _is_dot_or_root_pathspec(pos):
                return (
                    _SEV_DENY,
                    {
                        "decision": "deny",
                        "reason": (
                            f"Blocked by git-guardrails: 'git restore' targeting '{pos}' "
                            "discards all unstaged working-tree changes. Restore specific "
                            "files, use 'git stash', or ask the user to run it manually."
                        ),
                    },
                )
    return _SEV_ALLOW, _ALLOW_RESULT


_GIT_SUBCOMMAND_RULES = {
    "push": _check_git_push,
    "reset": _check_git_reset,
    "clean": _check_git_clean,
    "branch": _check_git_branch,
    "checkout": _check_git_checkout,
    "restore": _check_git_restore,
}


def _evaluate_git_tokens(tokens: list[str], depth: int) -> tuple[int, dict[str, str]]:
    """Parse git global options and dispatch to the matching subcommand rule."""
    aliases: dict[str, str] = {}
    i = 1
    n = len(tokens)
    subcommand: str | None = None
    sub_args: list[str] = []

    while i < n:
        tok = tokens[i]
        if tok in _GIT_GLOBAL_INFO_OPTS:
            return _SEV_ALLOW, _ALLOW_RESULT
        if tok in _GIT_GLOBAL_VALUE_OPTS:
            if tok == "-c" and i + 1 < n:
                cfg = tokens[i + 1]
                if cfg.startswith("alias.") and "=" in cfg:
                    name, val = cfg[len("alias.") :].split("=", 1)
                    aliases[name] = val
            i += 2
            continue
        if tok.startswith("-c") and len(tok) > 2:
            cfg = tok[2:]
            if cfg.startswith("alias.") and "=" in cfg:
                name, val = cfg[len("alias.") :].split("=", 1)
                aliases[name] = val
            i += 1
            continue
        if tok.startswith("-C") and len(tok) > 2:
            i += 1
            continue
        if tok == "--":
            return _SEV_ALLOW, _ALLOW_RESULT
        if tok.startswith("-"):
            i += 1
            continue
        subcommand = tok
        sub_args = tokens[i + 1 :]
        break

    if subcommand is None:
        return _SEV_ALLOW, _ALLOW_RESULT

    # Handle inline `git -c alias.<name>=<def> <name>` invocations.
    if subcommand in aliases and depth < 5:
        alias_val = aliases[subcommand].strip()
        if alias_val.startswith("!"):
            return _evaluate_script(alias_val[1:], depth + 1)
        alias_cmds, alias_subs = _lex_shell(alias_val)
        best = (_SEV_ALLOW, _ALLOW_RESULT)
        for sub in alias_subs:
            best = _pick_stricter(best, _evaluate_script(sub, depth + 1))
        if alias_cmds:
            expanded = ["git", *alias_cmds[0], *sub_args]
            best = _pick_stricter(best, _evaluate_git_tokens(expanded, depth + 1))
        return best

    checker = _GIT_SUBCOMMAND_RULES.get(subcommand)
    if checker is None:
        return _SEV_ALLOW, _ALLOW_RESULT
    return checker(sub_args)


def _pick_stricter(
    current: tuple[int, dict[str, str]],
    candidate: tuple[int, dict[str, str]],
) -> tuple[int, dict[str, str]]:
    """Return the higher-severity decision (deny > force_ask > allow)."""
    return candidate if candidate[0] > current[0] else current


def _extract_shell_c_script(args: list[str]) -> str | None:
    """Extract the command_string operand from `sh/bash/zsh ... -c <script>`."""
    long_value_opts = {"--rcfile", "--init-file"}
    saw_c = False
    i = 0
    n = len(args)

    while i < n:
        arg = args[i]
        if arg == "--":
            i += 1
            break
        if arg in long_value_opts:
            i += 2
            continue
        if arg.startswith("--"):
            i += 1
            continue
        if arg in ("-o", "+o", "-O", "+O"):
            i += 2
            continue
        if (arg.startswith("-") or arg.startswith("+")) and len(arg) > 1:
            consumed_next = False
            for idx, ch in enumerate(arg[1:]):
                if ch == "c" and arg.startswith("-"):
                    saw_c = True
                elif ch in ("o", "O"):
                    if idx == len(arg) - 2:
                        consumed_next = True
                    break
            i += 2 if consumed_next else 1
            continue
        break

    if saw_c and i < n:
        return args[i]
    return None


_WRAPPER_SPECS: dict[str, tuple[set[str], bool, int]] = {
    # binary -> (flags_taking_separate_value, skip_env_assigns, extra_positionals)
    "builtin": (set(), False, 0),
    "nohup": (set(), False, 0),
    "exec": ({"-a"}, False, 0),
    "time": ({"-f", "-o", "--format", "--output"}, False, 0),
    "nice": ({"-n", "--adjustment"}, False, 0),
    "stdbuf": ({"-i", "-o", "-e", "--input", "--output", "--error"}, False, 0),
    "timeout": ({"-k", "-s", "--kill-after", "--signal"}, False, 1),
    "sudo": (
        {
            "-C", "-D", "-g", "-h", "-p", "-R", "-r", "-T", "-t", "-U", "-u",
            "--user", "--group", "--chdir", "--prompt",
        },
        True,
        0,
    ),
    "doas": ({"-C", "-u"}, True, 0),
    "xargs": (
        {
            "-a", "-d", "-E", "-e", "-I", "-L", "-l", "-n", "-P", "-s",
            "--arg-file", "--delimiter", "--eof", "--replace", "--max-lines",
            "--max-args", "--max-procs", "--max-chars", "--process-slot-var",
        },
        False,
        0,
    ),
}


def _skip_wrapper_opts(
    cur: list[str], value_opts: set[str], *, allow_env: bool = False
) -> int:
    """Return index of the wrapped command after skipping wrapper flags."""
    i = 1
    while i < len(cur):
        tok = cur[i]
        if tok == "--":
            return i + 1
        if tok in value_opts:
            i += 2
            continue
        if tok.startswith("-") and len(tok) > 1:
            i += 1
            continue
        if allow_env and _ENV_ASSIGN_RE.match(tok):
            i += 1
            continue
        break
    return i


def _unwrap_prefix(tokens: list[str], depth: int) -> tuple[list[str], list[str]]:
    """Strip shell keywords, env assignments, and transparent wrapper commands.

    Returns ``(remaining_tokens, extra_scripts_to_eval)``.
    """
    extra_scripts: list[str] = []
    cur = list(tokens)

    while cur:
        head = cur[0]
        if head in _SHELL_KEYWORDS or _ENV_ASSIGN_RE.match(head):
            cur = cur[1:]
            continue

        base = _basename_lower(head)

        if base == "command":
            i = 1
            while i < len(cur):
                tok = cur[i]
                if tok == "--":
                    i += 1
                    break
                if tok.startswith("-") and len(tok) > 1:
                    if "v" in tok[1:] or "V" in tok[1:]:
                        return [], extra_scripts
                    i += 1
                    continue
                break
            cur = cur[i:]
            continue

        if base == "env":
            i = 1
            split_str: str | None = None
            while i < len(cur):
                tok = cur[i]
                if tok == "--":
                    i += 1
                    break
                if tok in ("-u", "--unset", "-C", "--chdir"):
                    i += 2
                    continue
                if tok in ("-S", "--split-string"):
                    if i + 1 < len(cur):
                        split_str = cur[i + 1]
                    i += 2
                    continue
                if tok.startswith("--split-string="):
                    split_str = tok.split("=", 1)[1]
                    i += 1
                    continue
                if tok.startswith("-S") and len(tok) > 2:
                    split_str = tok[2:]
                    i += 1
                    continue
                if tok.startswith("-") and len(tok) > 1:
                    i += 1
                    continue
                if _ENV_ASSIGN_RE.match(tok):
                    i += 1
                    continue
                break
            if split_str is not None and depth < 5:
                tail = " ".join(cur[i:])
                extra_scripts.append(f"{split_str} {tail}".strip())
                return [], extra_scripts
            cur = cur[i:]
            continue

        spec = _WRAPPER_SPECS.get(base)
        if spec is not None:
            value_opts, allow_env, extra_pos = spec
            idx = _skip_wrapper_opts(cur, value_opts, allow_env=allow_env)
            cur = cur[idx + extra_pos :] if idx + extra_pos <= len(cur) else []
            continue

        break

    return cur, extra_scripts


def _evaluate_command_tokens(
    tokens: list[str], depth: int
) -> tuple[int, dict[str, str]]:
    """Evaluate a single parsed shell command argv."""
    best = (_SEV_ALLOW, _ALLOW_RESULT)
    cur, extra_scripts = _unwrap_prefix(tokens, depth)

    for script in extra_scripts:
        best = _pick_stricter(best, _evaluate_script(script, depth + 1))
        if best[0] == _SEV_DENY:
            return best

    if not cur:
        return best

    base = _basename_lower(cur[0])

    if base in ("git", "git.exe"):
        return _pick_stricter(best, _evaluate_git_tokens(cur, depth))

    if depth >= 5:
        return best

    if base == "eval":
        eval_args = cur[1:]
        if eval_args and eval_args[0] == "--":
            eval_args = eval_args[1:]
        if eval_args:
            best = _pick_stricter(
                best, _evaluate_script(" ".join(eval_args), depth + 1)
            )
        return best

    if base in _SHELL_BINARIES:
        script = _extract_shell_c_script(cur[1:])
        if script is not None:
            best = _pick_stricter(best, _evaluate_script(script, depth + 1))
        return best

    if base == "find":
        i = 1
        n = len(cur)
        while i < n:
            if cur[i] in ("-exec", "-execdir"):
                i += 1
                sub_tokens: list[str] = []
                while i < n and cur[i] not in (";", "+"):
                    sub_tokens.append(cur[i])
                    i += 1
                if sub_tokens:
                    best = _pick_stricter(
                        best, _evaluate_command_tokens(sub_tokens, depth + 1)
                    )
                    if best[0] == _SEV_DENY:
                        return best
            i += 1
        return best

    return best


def _evaluate_script(command_line: str, depth: int = 0) -> tuple[int, dict[str, str]]:
    """Lex and evaluate all commands and embedded substitutions in a shell string."""
    if not command_line or not command_line.strip():
        return _SEV_ALLOW, _ALLOW_RESULT

    commands, substitutions = _lex_shell(command_line)
    best = (_SEV_ALLOW, _ALLOW_RESULT)

    for cmd_tokens in commands:
        best = _pick_stricter(best, _evaluate_command_tokens(cmd_tokens, depth))
        if best[0] == _SEV_DENY:
            return best

    if depth < 5:
        for sub in substitutions:
            best = _pick_stricter(best, _evaluate_script(sub, depth + 1))
            if best[0] == _SEV_DENY:
                return best

    return best


def evaluate_command(command_line: str) -> dict[str, str]:
    """Return an Antigravity PreToolUse decision dict for ``command_line``."""
    _, decision = _evaluate_script(command_line, depth=0)
    return decision


def handle_payload(raw_input: str) -> dict[str, str]:
    """Parse an Antigravity PreToolUse JSON payload and return a decision dict.

    Fails open (``{"decision": "allow"}``) on malformed or non-object JSON.
    """
    try:
        payload = json.loads(raw_input)
    except Exception:
        return dict(_ALLOW_RESULT)

    if not isinstance(payload, dict):
        return dict(_ALLOW_RESULT)

    tool_call = payload.get("toolCall")
    if not isinstance(tool_call, dict):
        return dict(_ALLOW_RESULT)

    tool_name = tool_call.get("name", "")
    if isinstance(tool_name, str) and tool_name and tool_name != "run_command":
        return dict(_ALLOW_RESULT)

    args = tool_call.get("args")
    if not isinstance(args, dict):
        return dict(_ALLOW_RESULT)

    command_line = args.get("CommandLine")
    if not isinstance(command_line, str):
        return dict(_ALLOW_RESULT)

    return evaluate_command(command_line)


def main() -> int:
    raw = sys.stdin.read()
    decision = handle_payload(raw)
    print(json.dumps(decision))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
