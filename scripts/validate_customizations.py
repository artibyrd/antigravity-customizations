#!/usr/bin/env python3
"""Zero-dependency validator for Antigravity plugin & skill customizations.

Catches silent Antigravity loader pitfalls before they reach main:
- Unknown top-level fields in plugin.json (silently discarded by loader)
- Duplicate plugin names across plugins/ (silently shadowed by loader)
- Invalid kebab-case names, >3 suggestedPrompts, or broken relative logo paths
- Misplaced hooks/hooks.json (native plugins require hooks.json at plugin root)
- Missing/invalid YAML frontmatter in SKILL.md or broken relative markdown links
- Accidental machine-local absolute paths leaked into public files
- Catalog drift between plugins/ directories and root README.md
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGINS_DIR = REPO_ROOT / "plugins"
ROOT_README = REPO_ROOT / "README.md"

ALLOWED_PLUGIN_KEYS = {
    "$schema",
    "name",
    "displayName",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "logo",
    "suggestedPrompts",
    "disabled",
}

ALLOWED_LOGO_EXTS = {".png", ".svg", ".jpg", ".jpeg", ".webp"}
KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LOCAL_PATH_PATTERNS = [
    re.compile(r"/home/[A-Za-z0-9._-]+/"),
    re.compile(r"/Users/[A-Za-z0-9._-]+/"),
    re.compile(r"[A-Za-z]:\\Users\\[A-Za-z0-9._-]+\\"),
]
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def strip_jsonc_comments(text: str) -> str:
    """Strip // and /* */ comments and trailing commas for JSONC parsing."""
    result: list[str] = []
    i = 0
    n = len(text)
    in_string = False
    escape = False
    while i < n:
        ch = text[i]
        if in_string:
            result.append(ch)
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            i += 1
        elif ch == '"':
            in_string = True
            result.append(ch)
            i += 1
        elif ch == "/" and i + 1 < n and text[i + 1] == "/":
            i += 2
            while i < n and text[i] != "\n":
                i += 1
        elif ch == "/" and i + 1 < n and text[i + 1] == "*":
            i += 2
            while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                i += 1
            i += 2
        else:
            result.append(ch)
            i += 1
    no_comments = "".join(result)
    return re.sub(r",(\s*[}\]])", r"\1", no_comments)


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Minimal YAML frontmatter parser for SKILL.md (supports scalar & folded blocks)."""
    if not text.startswith("---\n"):
        return None
    end_idx = text.find("\n---", 4)
    if end_idx == -1:
        return None
    raw = text[4:end_idx]
    fields: dict[str, str] = {}
    current_key: str | None = None
    block_lines: list[str] = []

    def flush() -> None:
        nonlocal current_key, block_lines
        if current_key is not None and block_lines:
            fields[current_key] = " ".join(line.strip() for line in block_lines).strip()
        current_key = None
        block_lines = []

    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[0].isspace() and current_key is not None:
            block_lines.append(line)
            continue
        flush()
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        if val in {">", ">-", "|", "|-"}:
            current_key = key
            block_lines = []
        else:
            fields[key] = val.strip('"').strip("'")
    flush()
    return fields


def check_relative_links(md_path: Path, errors: list[str]) -> None:
    content = md_path.read_text(encoding="utf-8")
    # Remove fenced code blocks before scanning links.
    cleaned = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    for match in MD_LINK_RE.finditer(cleaned):
        target = match.group(1)
        if target.startswith(("http://", "https://", "mailto:", "#", "customization://", "file://")):
            continue
        clean_target = target.split("#", 1)[0]
        if not clean_target:
            continue
        resolved = (md_path.parent / clean_target).resolve()
        if not resolved.exists():
            errors.append(
                f"{md_path.relative_to(REPO_ROOT)}: broken relative link '{target}'"
            )


def check_local_path_leaks(plugin_dir: Path, errors: list[str]) -> None:
    for path in plugin_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".ico"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pat in LOCAL_PATH_PATTERNS:
            m = pat.search(text)
            if m:
                errors.append(
                    f"{path.relative_to(REPO_ROOT)}: machine-local path leak '{m.group(0)}'"
                )


def validate_plugin(plugin_dir: Path, seen_names: dict[str, Path], errors: list[str]) -> str | None:
    rel = plugin_dir.relative_to(REPO_ROOT)
    manifest_path = plugin_dir / "plugin.json"
    if not manifest_path.is_file():
        errors.append(f"{rel}: missing required plugin.json")
        return None

    try:
        manifest = json.loads(strip_jsonc_comments(manifest_path.read_text(encoding="utf-8")))
    except json.JSONDecodeError as exc:
        errors.append(f"{rel}/plugin.json: invalid JSON/JSONC ({exc})")
        return None

    if not isinstance(manifest, dict):
        errors.append(f"{rel}/plugin.json: root must be a JSON object")
        return None

    unknown_keys = sorted(set(manifest.keys()) - ALLOWED_PLUGIN_KEYS)
    if unknown_keys:
        errors.append(
            f"{rel}/plugin.json: unknown top-level key(s) silently ignored by loader: {', '.join(unknown_keys)}"
        )

    name = manifest.get("name", plugin_dir.name)
    if not isinstance(name, str) or not KEBAB_RE.match(name):
        errors.append(f"{rel}/plugin.json: 'name' must be lowercase kebab-case (got {name!r})")
    else:
        if name in seen_names:
            errors.append(
                f"{rel}/plugin.json: duplicate plugin name '{name}' (already defined in {seen_names[name].relative_to(REPO_ROOT)})"
            )
        else:
            seen_names[name] = plugin_dir

    desc = manifest.get("description")
    if not isinstance(desc, str) or not desc.strip():
        errors.append(f"{rel}/plugin.json: 'description' must be a non-empty string")

    prompts = manifest.get("suggestedPrompts")
    if prompts is not None:
        if not isinstance(prompts, list) or not all(isinstance(p, str) and p.strip() for p in prompts):
            errors.append(f"{rel}/plugin.json: 'suggestedPrompts' must be a list of non-empty strings")
        elif len(prompts) > 3:
            errors.append(f"{rel}/plugin.json: 'suggestedPrompts' has {len(prompts)} entries (max 3)")

    logo = manifest.get("logo")
    if logo is not None:
        if not isinstance(logo, str) or logo.startswith(("/", "http://", "https://")):
            errors.append(f"{rel}/plugin.json: 'logo' must be a relative path")
        else:
            logo_path = (plugin_dir / logo).resolve()
            if not logo_path.is_file():
                errors.append(f"{rel}/plugin.json: logo file '{logo}' does not exist")
            elif logo_path.suffix.lower() not in ALLOWED_LOGO_EXTS:
                errors.append(f"{rel}/plugin.json: unsupported logo extension '{logo_path.suffix}'")

    # Guardrail: native plugins must keep hooks.json at root, not hooks/hooks.json
    nested_hooks = plugin_dir / "hooks" / "hooks.json"
    if nested_hooks.exists():
        errors.append(
            f"{rel}: hooks/hooks.json is ignored by native plugin discovery; move to {rel}/hooks.json"
        )

    # Validate bundled skills
    skills_dir = plugin_dir / "skills"
    if skills_dir.is_dir():
        for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.is_file():
                errors.append(f"{skill_dir.relative_to(REPO_ROOT)}: missing SKILL.md")
                continue
            fm = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
            if fm is None:
                errors.append(f"{skill_md.relative_to(REPO_ROOT)}: missing or unclosed YAML frontmatter")
                continue
            skill_name = fm.get("name", "")
            skill_desc = fm.get("description", "")
            if not KEBAB_RE.match(skill_name):
                errors.append(
                    f"{skill_md.relative_to(REPO_ROOT)}: frontmatter 'name' must be lowercase kebab-case (got {skill_name!r})"
                )
            elif skill_name != skill_dir.name:
                errors.append(
                    f"{skill_md.relative_to(REPO_ROOT)}: frontmatter 'name' ({skill_name!r}) does not match directory ({skill_dir.name!r})"
                )
            if not skill_desc.strip():
                errors.append(f"{skill_md.relative_to(REPO_ROOT)}: frontmatter 'description' is required")
            check_relative_links(skill_md, errors)

    # Check links in plugin README.md if present
    plugin_readme = plugin_dir / "README.md"
    if plugin_readme.is_file():
        check_relative_links(plugin_readme, errors)

    check_local_path_leaks(plugin_dir, errors)
    return name if isinstance(name, str) else plugin_dir.name


def main() -> int:
    errors: list[str] = []
    seen_names: dict[str, Path] = {}

    if not PLUGINS_DIR.is_dir():
        print("ERROR: plugins/ directory not found", file=sys.stderr)
        return 1

    plugin_dirs = sorted(p for p in PLUGINS_DIR.iterdir() if p.is_dir() and not p.name.startswith("."))
    if not plugin_dirs:
        print("ERROR: no plugins found under plugins/", file=sys.stderr)
        return 1

    validated: list[str] = []
    for plugin_dir in plugin_dirs:
        name = validate_plugin(plugin_dir, seen_names, errors)
        if name:
            validated.append(name)

    # Check root README catalog parity & relative links
    if not ROOT_README.is_file():
        errors.append("README.md: missing root README.md")
    else:
        readme_text = ROOT_README.read_text(encoding="utf-8")
        check_relative_links(ROOT_README, errors)
        for plugin_dir in plugin_dirs:
            expected_link = f"plugins/{plugin_dir.name}"
            if expected_link not in readme_text:
                errors.append(
                    f"README.md: catalog missing reference to '{expected_link}'"
                )

    if errors:
        print("Validation FAILED:\n", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"Validation PASSED: {len(validated)} plugin(s) verified ({', '.join(validated)}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
