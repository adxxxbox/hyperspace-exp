# 📝 Task Manager — SKILL

> Nancy's skill for tracking every todo the executive has, organized by goal → broad task → specific task, with full attributes and a log of every communication about each item.

Governed by `/_secretary/NANCY.md`. This file only extends those rules; it never contradicts them.

---

## 🎯 Purpose

Maintain a single source of truth for what the executive needs to do, why, by when, and everything that has been discussed about it.

## 📥 Inputs (read-only unless noted)

- `notes/` (via Note Lookup) — may surface new tasks
- `_secretary/calendar_manager/calendar.md` — events that imply tasks (prep, follow-up)
- `_secretary/note_lookup/lookups.md` — proposals to adopt
- Direct executive messages: "remind me to…", "I need to…", "X is done", "snooze X", etc.

## 📤 Outputs (writes)

- `_secretary/task_manager/tasks.md` — the full task tree
- `logged_updates` lines on every affected task

Nancy does **not** write tasks anywhere else.

---

## 🗂️ File structure of `tasks.md`

Three heading levels, in this exact hierarchy:

| Level | Role             | Format                                 |
| ----- | ---------------- | -------------------------------------- |
| `##`  | Goal / project   | `## Goal name`                          |
| `###` | Broad task       | `### 🔲 Broad task name`                |
| `####`| Specific task    | `#### 🔲 Specific task name`            |

- Goals are umbrellas — no emoji, no attributes, no log. They just group.
- Broad tasks are multi-step efforts. They have full attributes and `logged_updates`.
- Specific tasks are atomic units. They have full attributes and `logged_updates`. They may specify `parent=<broad_task_id>`.
- Task names contain **letters and spaces only** — no symbols, punctuation, or emojis inside the name itself. The status emoji sits *before* the name; nothing else decorates it.
- Done tasks strike the title: `### ~~✅ Task name~~`.

### Heading level is semantic, not positional

Level is chosen by the **nature of the task**, never by what's above it:

| Case                                              | Heading level | Where it sits                                                     |
| ------------------------------------------------- | ------------- | ----------------------------------------------------------------- |
| Multi-step effort                                 | `###` broad   | Under its `##` goal.                                              |
| Atomic task with a broad parent                   | `####` specific | Under the `###` broad task. `parent=T####` in header.             |
| Atomic task with **no broad parent** but a goal   | `####` specific | **Directly under the `##` goal** — skipping the `###` level is fine. `parent=—`. |
| Atomic task with **no goal** either               | `####` specific | Under the standing `## Miscellaneous` goal (see below). `parent=—`. |
| Broad task with no specific children yet          | `###` broad   | Stands alone under its goal; children added later.                |

**Why skip the `###` level visually?** Because `^####` must always mean "atomic specific task" and `^###` must always mean "broad multi-step task" for grep to stay honest. If we promoted standalone specifics to `###`, grep patterns would lie. Visual skipping is cheaper than semantic drift.

### Ordering inside a goal (avoiding false nesting)

Markdown renderers, folding editors, and TOC generators treat every `####` that appears *after* a `###` as a child of that `###`. To prevent orphan specifics from visually belonging to an unrelated broad task:

- **Within a goal, place orphan `####` tasks (those with `parent=—`) *before* any `###` broad task.** Document order inside a goal is therefore: `##` goal → orphan `####`s → `###` broads (each with its own `####` children) → next `###` broad.
- When a new `###` broad task is added to a goal that already has orphan specifics below it, **reshuffle**: orphans move above the new `###`. Log the reshuffle on each moved task (`context=reshuffle action=moved_above_broad`).

### Metadata is authoritative, headings are cosmetic

Every task entry carries **two mandatory placement fields** in its header comment:

- `goal=<slug>` — which `##` goal it belongs to. Slug = lowercase letters and underscores, matching the `##` heading text (e.g. `## Relocation planning` → `goal=relocation_planning`). The standing catch-all is `goal=miscellaneous`.
- `parent=<T####|—>` — which `###` broad task it belongs to. `—` means orphan (sits directly under the goal).

These two fields are the **single source of truth** for hierarchy. Headings (`##` / `###` / `####`) are navigation aids for humans and markdown renderers; they echo the metadata but never override it.

| Question                                       | Grep                                                                |
| ---------------------------------------------- | ------------------------------------------------------------------- |
| All tasks for a goal                           | `grep 'goal=relocation_planning' _secretary/task_manager/tasks.md`  |
| All children of a broad task                   | `grep 'parent=T0007' _secretary/task_manager/tasks.md`              |
| All true orphans (no broad parent)             | `grep 'parent=—' _secretary/task_manager/tasks.md`                  |
| All broad tasks                                | `grep 'level=broad' _secretary/task_manager/tasks.md`               |
| All specific tasks                             | `grep 'level=specific' _secretary/task_manager/tasks.md`            |

**Conflict rule.** If heading position and `goal=` / `parent=` ever disagree, reshuffle the document to match the metadata. Never the reverse.

### The `## Miscellaneous` standing goal

Every task must live under some `##`. If a task has no natural goal, it goes under a permanent `## Miscellaneous` heading at the bottom of `tasks.md`. When the executive later says *"that actually belongs to project X"*, move the task under the correct goal and log the move with `context=regrouped action=moved_goal`.

---

## 🛠️ Workflow

### Creating a task

1. Ask (or infer) the goal. If none exists, create a new `##` goal section.
2. Decide broad vs specific:
   - Atomic, one-shot → specific (`####`).
   - Multi-step effort → broad (`###`), and create its specific children as they're identified.
3. Allocate the next ID: `grep -oE 'id=T[0-9]{4}' _secretary/task_manager/tasks.md | sort -u | tail -1` → increment.
4. Write the entry using the format in `WRITING_RULES` below.
5. Append the creation event to `logged_updates`.

### Updating a task

- **Status change:** update the emoji in the title, update `status=` in the header, update `- **status**:` attribute, append a `logged_updates` line.
- **Date change:** preserve history by striking the old value — `~~2026-05-01~~ 2026-05-08`. Log the change.
- **Snooze:** increment `snoozed=`, change `due=` (strike old), set `status=snoozed`, log with `context=snooze advised=<new_date> response=<executive_ok>`.
- **Mark done:** title → `~~✅ Task name~~`, `status=done`, add `- **done**: YYYY-MM-DD` attribute, log with `action=marked_done`.
- **Cancel:** `status=cancelled`, keep the entry (never delete), log why.

### Promoting risk

Nancy upgrades status automatically based on the clock:

| Condition                                     | New status  | Emoji |
| --------------------------------------------- | ----------- | ----- |
| `due < today` and not done                    | `overdue`   | 🔴    |
| `due - today <= 2 days` and not done          | `at_risk`   | 🟡    |
| everything else open                          | `pending`   | 🔲    |

When promoting, log the promotion: `context=clock action=promoted_status advised=<next_step> risk=🔴:past_due`.

### Logging a conversation about a task

Every time the executive discusses a task — reminder, update, question, deferral — append one line to that task's `logged_updates` block. Never more than one line per exchange unless truly separate topics. Single-token values, no prose, no repetition.

---

## 🧾 Logging

- **Per-task logs** live in each task's `logged_updates` block.
- **Task-creation logs** also live there (first line of the block).
- No separate task log file.
- If something happens that relates to tasks generally but not any one task, log to `_secretary/temp_unspecified_log.md`.

---

<!-- WRITING_RULES:START -->

### ✍️ WRITING RULES (self-sufficient — any skill may follow these to write a task)

**1. Location.** All tasks live in `_secretary/task_manager/tasks.md`. Nowhere else.

**2. Heading hierarchy (semantic, not positional).**
- `##` = Goal / project (no emoji, no attributes). Required — every task must live under some `##`.
- `###` = Broad (multi-step) task.
- `####` = Specific (atomic) task. May sit directly under a `##` goal if it has no broad parent — the `###` level is skipped, never faked.
- If a task has no real goal, place it under the standing `## Miscellaneous` heading (create it at the bottom of `tasks.md` if it does not yet exist).
- Append new tasks under the correct `##` goal. Create the goal if missing.
- **Within a goal, orphan `####` tasks (`parent=—`) must sit before any `###` broad task.** If adding a `###` to a goal with orphans below, move the orphans above it and log the reshuffle.
- The `parent=` field in each entry header is authoritative. If rendering and `parent=` disagree, reshuffle the document to match the metadata — never the reverse.

**3. Title format.**
- Broad: `### <emoji> Task name`
- Specific: `#### <emoji> Task name`
- Name = letters and spaces only. No symbols, punctuation, digits, or emojis inside the name.
- Emoji matches status (see NANCY.md §3).
- If `status=done`: strike the title → `### ~~✅ Task name~~`.

**4. Entry header (HTML comment immediately after the title).**

```
<!-- entry: type=task level=<broad|specific> id=T#### source=<skill> created=<YYYY-MM-DD> status=<status> goal=<slug> parent=<T####|—> [due=<YYYY-MM-DD>] [priority=<low|med|high|critical>] [snoozed=<int>] [related=<T####,E####>] [done=<YYYY-MM-DD>] -->
```

Mandatory: `type`, `level`, `id`, `source`, `created`, `status`, `goal`, `parent`.

- `goal=<slug>` — lowercase letters + underscores, matches the `##` heading text. Catch-all is `goal=miscellaneous`.
- `parent=<T####>` for specific tasks nested under a broad task; `parent=—` for orphans and for broad tasks themselves.

**5. Attribute block** (bulleted list, immediately after the header). Include only those that apply:

```
- **description**: <short one-line description>
- **created**: <YYYY-MM-DD>
- **due**: <YYYY-MM-DD>            (preserve history via strikethrough when changed)
- **priority**: <low|med|high|critical>
- **status**: <emoji> <status>
- **snoozed**: <count>
- **goal**: <slug>                   (matches goal= in header and the `##` heading)
- **parent**: <T#### | — >           (matches parent= in header)
- **related**: <T####, E####, N####, …>
- **done**: <YYYY-MM-DD>            (only when status=done)
```

**6. `logged_updates` block** (immediately after attributes). Required on every task, even newly created (the first line is the creation event).

```
**logged_updates**:
- `YYYY-MM-DD HH:MM` [L####] context=<token> action=<token> [advised=<token>] [response=<token>] risk=<🟢|🟡|🔴>:<one_word_reason>
```

- One line per update. Single-token values (underscore for spaces).
- Allocate `L####` globally: `grep -rhoE 'L[0-9]{4}' _secretary/ | sort -u | tail -1` → increment.
- Never delete a logged update.

**7. ID allocation.** New task id: `grep -oE 'id=T[0-9]{4}' _secretary/task_manager/tasks.md | sort -u | tail -1` → increment → zero-pad to 4 digits. IDs are never reused.

**8. Cross-skill writes.** Always set `source=<your_skill_name>` in the entry header. Example: a task proposed by Note Lookup uses `source=note_lookup`.

**9. Ambiguity.** If any mandatory field cannot be determined, do **not** create the task here — write to `_secretary/temp_unspecified_log.md` instead with a note describing the ambiguity.

<!-- WRITING_RULES:END -->

---

## 🧪 Example entry (for reference only — not real data)

```markdown
## Relocation planning

### 🟡 Planning relocation
<!-- entry: type=task level=broad id=T0001 source=nancy created=2026-04-10 status=at_risk goal=relocation_planning parent=— due=2026-06-01 priority=high snoozed=0 related=E0003 -->
- **description**: coordinate move to new neighborhood by summer
- **created**: 2026-04-10
- **due**: ~~2026-05-15~~ 2026-06-01
- **priority**: high
- **status**: 🟡 at_risk
- **snoozed**: 1
- **goal**: relocation_planning
- **parent**: —
- **related**: E0003

**logged_updates**:
- `2026-04-10 09:15` [L0001] context=created action=broad_task_opened advised=break_into_subtasks response=agreed risk=🟢:fresh
- `2026-04-20 08:40` [L0007] context=morning_brief action=promoted_to_at_risk advised=start_daycare_search response=will_tomorrow risk=🟡:deadline_close

#### 🔲 Daycare lookup
<!-- entry: type=task level=specific id=T0002 source=note_lookup created=2026-04-20 status=pending goal=relocation_planning parent=T0001 due=2026-05-01 priority=high snoozed=0 -->
- **description**: find a daycare within 10 minutes of the new home
- **created**: 2026-04-20
- **due**: 2026-05-01
- **priority**: high
- **status**: 🔲 pending
- **goal**: relocation_planning
- **parent**: T0001
- **related**: —

**logged_updates**:
- `2026-04-20 08:40` [L0008] context=note_lookup_proposal action=task_created advised=begin_research response=— risk=🟢:fresh
```
