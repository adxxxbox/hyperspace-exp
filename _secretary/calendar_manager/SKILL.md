# 📅 Calendar Manager — SKILL

> Nancy's skill for maintaining a single master calendar aggregated from all of the executive's calendar sources, with a full log of every communication about each event.

Governed by `/_secretary/NANCY.md`. This file only extends those rules; it never contradicts them.

---

## 🎯 Purpose

Give the executive one authoritative view of every commitment on their time — from Google, Apple, Notion, and Outlook — with explicit freshness stamps per source and per-event conversation logs.

## 📥 Inputs (read-only unless noted)

- **Google Calendar** — accessible via API / MCP if configured; otherwise user-supplied updates.
- **Apple Calendar** — user-supplied updates (copy, screenshot, or dictation).
- **Notion Calendar** — accessible via Notion MCP; otherwise user-supplied.
- **Outlook (work)** — **not AI-accessible**. Nancy must ask the executive for a screenshot or copy. Always surface the `last_synced` timestamp for Outlook at every brief so the executive knows how stale the view is.
- `_secretary/task_manager/tasks.md` — task due dates may be mirrored here when the executive wants them on the calendar.

## 📤 Outputs (writes)

- `_secretary/calendar_manager/calendar.md` — the master calendar
- `logged_updates` lines on every affected event

Nancy does **not** write calendar data anywhere else.

---

## 🗂️ File structure of `calendar.md`

The file has two regions:

### 1. `SYNC_STATUS` block (top of file, mandatory)

```
<!-- SYNC_STATUS:START -->
- source=google    last_synced=<YYYY-MM-DD HH:MM> method=<api|manual> status=<🟢|🟡|🔴>:<note>
- source=apple     last_synced=<YYYY-MM-DD HH:MM> method=<manual>     status=<…>
- source=notion    last_synced=<YYYY-MM-DD HH:MM> method=<mcp|manual> status=<…>
- source=outlook   last_synced=<YYYY-MM-DD HH:MM> method=<screenshot> status=<…>  (AI cannot access; ask executive)
<!-- SYNC_STATUS:END -->
```

- Update whenever Nancy refreshes from a source.
- At every daily brief, Nancy **must** mention the oldest `last_synced` and whether Outlook is stale.

### 2. Events, grouped by date

- Each day is an `##` heading: `## 2026-04-23 Thursday`.
- Each event is an `###` heading under the day: `### 🔵 Event name`.
- Events within a day are ordered by start time.
- Past events may be deleted once they end — no need to retain them for history. (The external calendars of record — Google, Apple, Notion, Outlook — hold the permanent record; `calendar.md` is a working view.) Until removed, an ended event's status flips to `past` (⚪) so the file stays internally consistent.
- Cancelled events likewise may be deleted once the cancellation is confirmed; until then, strike the title (see next line).
- Event names contain **letters and spaces only** — same rule as tasks.
- Cancelled events strike the title: `### ~~⛔ Event name~~`.

---

## 🛠️ Workflow

### Syncing from external sources — forward-only

When pulling events from Google, Apple, Notion, Outlook, or any future source:

- **Import only events whose `end_date` is today or later.** Do not import past events — `calendar.md` is a forward-looking working view, and the external calendar is the system of record for anything that already ended.
- For **multi-day or long-running events** (e.g. a fellowship rotation block spanning weeks): import if any part of its range is today or later. If the event is fully in the past, skip it.
- For **recurring events**: only materialize occurrences whose start is today or later.
- If a **past event is already in `calendar.md`** (e.g. from a previous sync under the old retention rule, or because it flipped to `past` naturally), apply the "Removing events" section below — don't re-import it, delete it instead.

Rationale: three external calendars agree on the past already; `calendar.md` exists to tell the executive what's next, not what's been.

### Adding an event

1. Verify the event is not already past (see "Syncing from external sources" above).
2. Allocate the next ID: `grep -oE 'id=E[0-9]{4}' _secretary/calendar_manager/calendar.md | sort -u | tail -1` → increment.
3. Find or create the `## YYYY-MM-DD <Weekday>` day-heading; insert the event in time order.
4. Write the entry using the `WRITING_RULES` below.
5. Append a creation line to `logged_updates`.
6. Update the `SYNC_STATUS` entry for the relevant source.

### Updating an event

- **Time change:** preserve history — `- **time**: ~~09:00–09:30~~ 10:00–10:30`. Log it.
- **Cancel:** title → `### ~~⛔ Event name~~`, `status=cancelled`. The entry may be deleted once the cancellation is acknowledged by the executive (the external calendar of record holds history).
- **Status flip to past:** done automatically on time check; append a log line `context=clock action=event_past`. The entry may be deleted at any point after the flip — no retention requirement.

### Removing events (new behavior)

Past and cancelled events are **disposable** once they've served their purpose in the daily-brief cycle. Options:

- **Immediate cleanup:** delete the event entry (and its `logged_updates` block) as soon as it flips to `past` / `cancelled`.
- **Grace window:** keep past events for a short retention window (a few days) so the executive can see what just happened during the next couple of briefs, then delete.
- **Retain on request:** only keep a past/cancelled event if the executive explicitly asks, or if another live event links to it via `related=`.

When deleting, also clean up any orphaned `## YYYY-MM-DD <Weekday>` day-headings that become empty. Do **not** delete the `SYNC_STATUS` block, and do **not** delete events whose `status` is `upcoming`, `at_risk`, or `missed` — those are still live.

### Daily brief duty

On the brief, Nancy reports:

1. 📅 Today's events in order.
2. 🔵 Next 48 hours of events.
3. 🟡 Any events flagged `at_risk` (conflicts, prep missing).
4. 🔴 Any events the executive missed or is late for.
5. ⏱️ The staleness of each calendar source (from `SYNC_STATUS`).
6. 📨 An explicit ask if Outlook hasn't been synced in > 24h: *"I don't have a fresh Outlook view — can you share a screenshot?"*

### Conflict detection

When two events overlap: mark both `status=at_risk` with a log line `context=conflict action=flagged related=<other_event_id> risk=🟡:overlap` and surface at the next brief.

---

## 🧾 Logging

- **Per-event logs** live in each event's `logged_updates` block — same format as Task Manager.
- **Sync actions** are logged in `SYNC_STATUS` (by updating `last_synced`) **and** as a `logged_updates` line on any event created/modified by that sync.
- If a sync happens but no event changes, add a single line to `_secretary/temp_unspecified_log.md` noting the sync — we never want a sync event untracked.

---

<!-- WRITING_RULES:START -->

### ✍️ WRITING RULES (self-sufficient — any skill may follow these to write a calendar entry)

**1. Location.** All events live in `_secretary/calendar_manager/calendar.md`. Nowhere else.

**2. Day grouping.** Under an `## YYYY-MM-DD <Weekday>` heading. Create the day heading if missing. Keep events in chronological order.

**3. Title format.**
- `### <emoji> Event name`
- Name = letters and spaces only.
- Emoji matches status: 🔵 upcoming · ⚪ past · 🟡 at_risk · 🔴 missed · ⛔ cancelled.
- If `status=cancelled`: strike the title → `### ~~⛔ Event name~~`.

**4. Entry header (HTML comment immediately after the title).**

```
<!-- entry: type=event id=E#### source=<google|apple|notion|outlook|nancy|task_manager|note_lookup> created=<YYYY-MM-DD> date=<YYYY-MM-DD> time=<HH:MM-HH:MM|all_day> status=<upcoming|past|at_risk|missed|cancelled> [source_calendar=<google|apple|notion|outlook>] [related=<E####,T####>] -->
```

Mandatory: `type`, `id`, `source`, `created`, `date`, `time`, `status`.

Note: `source=` is the skill that wrote the entry. `source_calendar=` is which external calendar it came from. Keep both.

**5. Attribute block** (bulleted list, immediately after the header):

```
- **description**: <short one-line description>
- **date**: <YYYY-MM-DD>               (preserve history via strikethrough when changed)
- **time**: <HH:MM–HH:MM | all_day>    (preserve history via strikethrough when changed)
- **source_calendar**: <google|apple|notion|outlook>
- **last_synced**: <YYYY-MM-DD HH:MM>
- **location**: <token_or_—>
- **status**: <emoji> <status>
- **related**: <T####, E####, … | —>
```

**6. `logged_updates` block** (required, same format as everywhere):

```
**logged_updates**:
- `YYYY-MM-DD HH:MM` [L####] context=<token> action=<token> [advised=<token>] [response=<token>] risk=<🟢|🟡|🔴>:<one_word_reason>
```

- Allocate `L####` globally: `grep -rhoE 'L[0-9]{4}' _secretary/ | sort -u | tail -1` → increment.

**7. `SYNC_STATUS` updates.** Whenever you write an event that came from a sync, update the matching `source=<calendar>` line inside the `<!-- SYNC_STATUS:START -->...<!-- SYNC_STATUS:END -->` block with the new `last_synced` timestamp.

**8. ID allocation.** New event id: `grep -oE 'id=E[0-9]{4}' _secretary/calendar_manager/calendar.md | sort -u | tail -1` → increment → zero-pad to 4 digits.

**9. Cross-skill writes.** Set `source=<your_skill>` in the entry header. For example, Note Lookup proposing an event uses `source=note_lookup` but `source_calendar=` is whichever (or omitted if unknown — then log the ambiguity in `temp_unspecified_log.md` too).

**10. Ambiguity.** If any mandatory field is unknown, do **not** create the event here — write to `_secretary/temp_unspecified_log.md` instead.

<!-- WRITING_RULES:END -->

---

## 🧪 Example (for reference only — not real data)

```markdown
<!-- SYNC_STATUS:START -->
- source=google    last_synced=2026-04-23 08:00 method=api        status=🟢:fresh
- source=apple     last_synced=2026-04-22 19:00 method=manual     status=🟡:14h_old
- source=notion    last_synced=2026-04-23 08:05 method=mcp        status=🟢:fresh
- source=outlook   last_synced=2026-04-21 17:30 method=screenshot status=🔴:stale_ask_exec
<!-- SYNC_STATUS:END -->

## 2026-04-23 Thursday

### 🔵 Team standup
<!-- entry: type=event id=E0001 source=google created=2026-04-22 date=2026-04-23 time=09:00-09:30 status=upcoming source_calendar=google -->
- **description**: weekly engineering sync
- **date**: 2026-04-23
- **time**: 09:00–09:30
- **source_calendar**: google
- **last_synced**: 2026-04-23 08:00
- **location**: zoom
- **status**: 🔵 upcoming
- **related**: —

**logged_updates**:
- `2026-04-23 08:00` [L0012] context=sync action=event_created advised=— response=— risk=🟢:fresh
```
