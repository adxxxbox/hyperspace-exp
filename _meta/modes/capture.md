# Mode: capture

**Authority: author.** May read + write notes. May not touch structure (`_meta/`, renames, folder moves). May not run git. May invoke `vault-check` (read-only).

Loaded when the user wants to add or jot a new note.

Trigger phrases: "add", "new note", "jot", "capture", "quick note", "inbox", "journal entry", "today I", "remind me", or any request with no obvious admin/edit intent.

## The placement rule (one sentence)

> If you are not sure where it belongs, put it in `inbox.md`. If it's a dated reflection, put it in `journal/YYYY-MM-DD.md`. Otherwise pick the obvious top-level folder.

That's it. No decision tree. If the obvious folder is ambiguous, default to `inbox.md`.

## The folders, in one line each

- `inbox.md` — single-file quick-capture, append-only. Bullets or short paragraphs. No frontmatter.
- `journal/YYYY-MM-DD.md` — daily notes. Use Foam's "Open Daily Note" command.
- `1-projects/<slug>/` — multi-file ongoing work. Create a folder; the first note is usually called `README.md` or the project slug.
- `2-areas/` — ongoing areas of focus (fellowship, a rotation, a recurring topic). Single files, usually dated.
- `3-resources/` — externally-sourced reference material (imported books, chapter extracts).
- `4-atlas/` — MOCs and index pages (optional; empty-ok).
- `5-cards/` — atomic permanent notes, one idea each, ≤300 words (optional; empty-ok).

## Frontmatter

Optional. If you add it, use any of `title`, `created`, `type`, `tags`, `aliases`. Missing keys are fine.

For the three templated note types, use the templates in `.foam/templates/`:
- `daily-note.md` — used by `journal/`
- `new-note.md` — used for general notes

## What not to do

- Do not invent a new top-level folder.
- Do not reorganize existing folders — that's `admin` mode.
- Do not rename existing files — that's `admin` mode (it requires the wikilink sweep).
- Do not touch protected paths from `core/conventions.md §1`.

## When in doubt

Append to `inbox.md`. A later triage pass (also `capture` mode, or `admin` if links are involved) will move it.
