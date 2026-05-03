# Mode: inspector

**Authority: read-only.** Loaded when the user asks a question *about* the vault without asking to change anything.

Trigger phrases: "search", "find", "what does", "where is", "summarize", "explain", "show me", "list", "how many", "is there a note about…".

## What you may do

- Read any note, any file (except inside protected paths, which stay verbatim even to read).
- Run `vault-check` (read-only by design).
- Grep, glob, walk the tree.
- Answer in plain text.

## What you may NOT do

- Write, create, delete, rename, or move any file.
- Invoke any feature whose `FEATURE.md` declares `modifies_git: true` or side effects on the vault.
- Run git commands beyond `status`, `log`, `diff`, `show` (per `conventions.md §7`).
- Auto-correct frontmatter, even if `frontmatter.agent_auto_correct` is `true` — that's an admin-authority operation.

## If the user asks for a change

Surface the intent and either ask them to confirm ("you want me to switch to author mode and do X?") or tell them to re-prompt with language that matches `capture` / `work` / `admin` triggers. Do not silently escalate.

## When your answer needs citations

Cite files by path and line number (e.g. `2-areas/fellowship-assistant/2026-04-14_case-classification.md:17`) so the user can jump to the source.
