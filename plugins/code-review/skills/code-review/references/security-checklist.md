# Security Axis Checklist

Use this checklist when running the **Axis 3 — Security** subagent in `code-review`. Focus on concrete, exploitable weaknesses or broken trust boundaries introduced or exposed by the diff—never pad the report with theoretical boilerplate.

## Applicability Gate

If the diff touches **only** documentation, comments, changelogs, or static prose with zero runtime code, templates, scripts, hooks, CI workflows, or infrastructure/config changes, return:
> `No security-sensitive surface touched in this diff.`

## What to Inspect

1. **Auth, Authorization & Trust Boundaries**
   - Unauthenticated or under-authorized endpoints, missing tenant/object ownership checks (IDOR), or trusting caller-supplied identity/role/family/text fields that must be derived or fetched server-side.
   - Fail-open guards where a parse error, empty value, or depth limit silently grants privilege or skips validation.
2. **Injection & Unsafe Sinks**
   - Shell/command injection (`shell=True`, unescaped interpolation, wrapper/heredoc/subshell bypasses in command guards), SQL/NoSQL injection, path traversal (`../` escaping intended root), template injection, or unsafe deserialization (`pickle`, `yaml.load`).
   - Unsafe web/DOM sinks: interpolating untrusted or API-controlled fields into `.innerHTML`, `insertAdjacentHTML`, `document.write`, or inline `onclick="..."` handlers; unvalidated `<a href>` schemes (`javascript:`, `data:`) instead of `http:`/`https:` allowlists.
3. **SSRF & Untrusted Ingestion**
   - Outbound HTTP fetches of user-supplied URLs without blocking private/loopback/link-local/cloud-metadata IPs (`169.254.169.254`, `127.0.0.1`, `::1`, RFC 1918), enforcing redirect re-validation, response size caps, and timeouts.
   - Untrusted XML/HTML/archive parsing (XXE, zip bombs, unbounded recursion).
4. **Secrets & Cryptography**
   - Hardcoded API keys, tokens, private keys, or credentials committed in code, fixtures, or scripts; secrets logged or echoed into errors/artifacts without `<REDACTED>` scrubbing.
   - Signature/MAC verification flaws (non-constant-time comparison, unverified payload fields, signing untrusted remote input with a server's sovereign key, weak RNG for security tokens).
5. **Concurrency, Atomicity & Resource Limits**
   - Check-then-act races on leases, locks, quotas, or file creation; missing rate limits or unbounded memory/CPU amplification on public inputs.
6. **CI/CD, Hooks & Supply-Chain Boundaries**
   - Untrusted PR input interpolated into GitHub Actions `run:` blocks, overly broad workflow permissions, or `PreToolUse` hooks that accidentally auto-approve unrelated unsandboxed commands.

## Reporting Rules

- Cite exact `file:line` hunks and describe the **concrete exploit path or failure mode**, not vague advice.
- Label severity clearly: **Critical / High / Medium / Low**.
- Stay under **400 words**.
