---
title: "Hypernote — mode router"
created: 2026-04-11
tags: [meta]
---

# Hypernote — mode router

This is Adnan's personal knowledge vault. Versioned with git, rendered with [Foam](https://foambubble.github.io/foam/) in VSCode.

Instructions are loaded on demand. **You do not read everything.** Pick the mode that matches the task and read that one mode file plus the always-on conventions.

## How to load instructions

1. Always load: `_meta/core/conventions.md` (≤60 lines; tiebreaker for all rules).
2. Pick one mode from the table below and load only that file.
3. If the mode uses a script, read `_meta/features/registry.jsonc` and then only the matched `FEATURE.md`.

Do not read the other mode files. Do not read `_meta/archive/`. Do not read `_meta/core/config.jsonc` unless you are writing or debugging a script.

## Mode table

| Trigger phrases | Mode file | Authority |
|---|---|---|
| "search", "find", "what does", "where is", "summarize", "explain", "show me", "list", "how many" | `_meta/modes/inspector.md` | read-only |
| "add", "new note", "jot", "capture", "inbox", "journal entry", "today I…" | `_meta/modes/capture.md` | author |
| "edit", "rewrite", "expand", "extract", "research", "draft", "continue writing" | `_meta/modes/work.md` | author |
| "audit", "run vault check", "lint", "run maintenance", "clean up reports", "fix frontmatter", "triage inbox", "health check" | `_meta/modes/maintenance.md` | maintenance |
| "rename", "move", "archive", "delete", "reorganize", "add a script/feature", "amend the rules", anything touching `_meta/core/`, `_meta/modes/`, or `_meta/features/` | `_meta/modes/admin.md` | admin |
| "hey Nancy", "hi Nancy", "remind me to…", "I need to…", "snooze X", "X is done", "add to my calendar", "what's overdue", "daily brief", "what's on my plate", anything about tasks / calendar / appointments / deadlines | `_secretary/NANCY.md` | secretary (author in `_secretary/` only; read-only everywhere else) |

If the request is a question about the vault, default to `inspector.md`. If unsure whether it's a question or a change request, ask.

**Secretary mode note.** `_secretary/NANCY.md` is self-contained — it governs Nancy's behavior and points to per-skill rulebooks (`_secretary/task_manager/SKILL.md`, `_secretary/calendar_manager/SKILL.md`, `_secretary/note_lookup/SKILL.md`) to read on demand. When in secretary mode, Nancy writes **only** inside `_secretary/`; everything else in the vault stays read-only for her.

## Safety overrides (always true, no exceptions)

- Protected paths (`.git/`, `.foam/`, `.vscode/`, `.Codex/`, `attachments/`, `_meta/`) are never modified except as explicitly permitted in `_meta/core/conventions.md §1` exceptions.
- **Append-only files:** `inbox.md` and `todo.md` accept *new* lines from AI agents, but every AI-added line must end with `(added by AI agent)`. No reordering or rewriting of existing content. Nancy may additionally flip an existing checkbox in `todo.md` from `- [ ]` to `- [x]` when the executive confirms the task is done, appending `(marked done by AI agent YYYY-MM-DD)`. See `conventions.md §1b`.
- **Never run git commands autonomously** (commit, push, branch, tag, reset, add, mv, rm, merge, rebase). The user must ask in the current turn. Read-only git introspection (`status`, `log`, `diff`, `show`) is allowed. See `conventions.md §7`.
- **Master outline:** `/outlines.md` is the master Map of Content. Every new note must end up reachable from it by wikilinks (chain through a hub in `4-atlas/`). See `conventions.md §8`. Enforced by `vault-check` rule O1.
- Never delete user content without confirmation.
- Never skip the dry-run step of a rename (use the `rename-note` feature).
- Never commit secrets.
- Never use `--no-verify`, `--no-gpg-sign`, or any hook-bypass flag.
- When uncertain, halt and ask.

## Map

- `_meta/core/` — conventions + config
- `_meta/modes/` — mode files (read exactly one per session)
- `_meta/features/` — pluggable tools (each with its own FEATURE.md)
- `_meta/features/registry.jsonc` — dispatch table: trigger phrases → feature entry
- `_meta/lib/` — shared script code (`config_loader.py`)
- `_meta/maintenance-reports/` — gitignored diagnostic snapshots (vault-check output, activity log)
- `_meta/archive/` — retired specs; do not load
- `_meta/changelog.md` — audit trail
- `_secretary/` — Nancy's workspace (tasks, calendar, note lookups, logs); governed by `_secretary/NANCY.md`
