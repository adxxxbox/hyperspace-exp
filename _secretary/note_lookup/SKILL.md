# 🔍 Note Lookup — SKILL

> Nancy's skill for reading the executive's notes (and, when available, emails) deeply and thoughtfully — to surface forgotten commitments, overdue items, and candidate tasks/events to propose into the other skills.

Governed by `/_secretary/NANCY.md`. This file only extends those rules; it never contradicts them.

---

## 🎯 Purpose

Treat `notes/` (and email, when accessible) as a signal source. Read with intent — not skimming. Turn findings into concrete proposals written into Task Manager or Calendar Manager, each tagged `source=note_lookup` so their origin is always traceable.

## 📥 Inputs (read-only — no writes outside `_secretary/`)

- `notes/` — the executive's note space. Nancy reads deeply; never writes.
- Email (Gmail via MCP, when authorized) — read only.
- `_secretary/task_manager/tasks.md` — to avoid creating duplicates.
- `_secretary/calendar_manager/calendar.md` — to avoid creating duplicates.

## 📤 Outputs (writes)

- `_secretary/note_lookup/lookups.md` — one entry per lookup session with what was read, what was found, what was proposed, and outcomes.
- **Proposals** written into other skills' data files, always with `source=note_lookup` in the entry header. See each skill's `WRITING_RULES` block.

Nancy **never** writes inside `notes/`, and never writes elsewhere outside `_secretary/`.

---

## 🗂️ File structure of `lookups.md`

- Each lookup session is a `##` heading by date: `## 2026-04-23 Morning lookup`.
- Each specific lookup pass within the session is a `###` entry: `### 🔍 <scope phrase>`.
- Scope phrases follow the letters-and-spaces-only rule.

---

## 🛠️ Workflow

### A lookup session

1. Decide scope — everything, or a subset (`notes/relocation/*.md`, all new-since-last, email thread subject X, etc.).
2. Read deeply. Engage with the content; don't glance.
3. For each finding:
   - Duplicate check: `grep -i "<key phrase>" _secretary/task_manager/tasks.md _secretary/calendar_manager/calendar.md`.
   - If new: **propose** by writing an entry into the correct skill's data file, using that skill's `WRITING_RULES` and `source=note_lookup`.
   - If ambiguous: write to `_secretary/temp_unspecified_log.md` instead of guessing.
4. Record the lookup session in `lookups.md` with everything found and every proposal made (by id).
5. On the next daily brief, Nancy raises these proposals with the executive: *"I found these in your notes — keep, adjust, or drop?"*

### Proposal lifecycle

Every proposal has three states, tracked in the lookup entry's `logged_updates`:
- `action=proposed` — created the task/event with `source=note_lookup`.
- `action=accepted` — executive confirmed; no further action on the lookup entry (the downstream task/event continues its own life).
- `action=rejected` — executive rejected; Nancy sets the downstream task/event to `status=cancelled` and logs.

---

## 🧾 Logging

- **Per-session log** in `_secretary/note_lookup/lookups.md`.
- **Per-proposal log** as `logged_updates` lines on the session entry.
- Downstream writes (tasks/events) each carry their own `logged_updates` too, with `source=note_lookup` in the header — so you can always trace a task back to the lookup that spawned it.

---

<!-- WRITING_RULES:START -->

### ✍️ WRITING RULES (self-sufficient — any skill may follow these to record a lookup session)

**1. Location.** All lookup sessions live in `_secretary/note_lookup/lookups.md`. Nowhere else.

**2. Heading hierarchy.**
- `##` = session, dated: `## YYYY-MM-DD <label>` (e.g. `## 2026-04-23 Morning lookup`).
- `###` = one scoped pass within the session: `### 🔍 <scope phrase>`.

**3. Title format.** Letters and spaces only in names. Emoji 🔍 for active, ✅ for accepted-by-executive, ⛔ for rejected.

**4. Entry header (after each `###` title).**

```
<!-- entry: type=lookup id=N#### source=note_lookup created=<YYYY-MM-DD> status=<open|accepted|rejected> scope=<path_glob_or_token> [related=<T####,E####>] -->
```

Mandatory: `type`, `id`, `source`, `created`, `status`, `scope`.

**5. Attribute block**:

```
- **scope**: <path glob or description>
- **inputs_read**: <comma-separated file list or token>
- **findings**: <one short line — or a sub-bulleted list if multiple>
- **proposals**: <comma-separated downstream ids: T####, E####, U####>
- **status**: <emoji> <status>
```

**6. `logged_updates` block** (same format as everywhere):

```
**logged_updates**:
- `YYYY-MM-DD HH:MM` [L####] context=<token> action=<proposed|accepted|rejected|follow_up> [advised=<token>] [response=<token>] risk=<🟢|🟡|🔴>:<one_word_reason>
```

**7. ID allocation.** New lookup id: `grep -oE 'id=N[0-9]{4}' _secretary/note_lookup/lookups.md | sort -u | tail -1` → increment.

**8. Cross-skill writes.** When creating a task or event from a lookup, write into the target skill's data file using **its** `WRITING_RULES`, with `source=note_lookup` in the task/event entry header. Record the downstream id in this lookup's `proposals` attribute.

**9. Never write outside `_secretary/`.** Notes and email are read-only inputs. If you feel the need to edit a note, stop: log the suggestion in the lookup entry and surface it at brief.

**10. Ambiguity.** If a finding is too vague to turn into a task/event, record it in the lookup entry's `findings` and log it in `_secretary/temp_unspecified_log.md`.

<!-- WRITING_RULES:END -->

---

## 🧪 Example (for reference only — not real data)

```markdown
## 2026-04-23 Morning lookup

### 🔍 Daycare research in notes
<!-- entry: type=lookup id=N0001 source=note_lookup created=2026-04-23 status=open scope=notes/relocation/** related=T0002 -->
- **scope**: notes/relocation/**
- **inputs_read**: notes/relocation/home_search.md, notes/relocation/kids.md
- **findings**: executive mentioned daycare needs by April 30; no task existed.
- **proposals**: T0002
- **status**: 🔍 open

**logged_updates**:
- `2026-04-23 08:40` [L0008] context=scan action=proposed advised=create_task response=— risk=🟡:deadline_close
```
