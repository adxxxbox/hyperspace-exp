# 📅 Master Calendar

> Structured per `_secretary/calendar_manager/SKILL.md`. All entries follow the homogeneity rules in `_secretary/NANCY.md`.

- ID prefix: `E####`
- Day headings: `## YYYY-MM-DD <Weekday>`
- Event statuses: 🔵 upcoming · ⚪ past · 🟡 at_risk · 🔴 missed · ⛔ cancelled

---

<!-- SYNC_STATUS:START -->
- source=google    last_synced=2026-04-23 21:30 method=api           status=🟢:fresh
- source=apple     last_synced=2026-04-23 22:10 method=sqlite        status=🟢:fresh
- source=notion    last_synced=2026-04-23 21:33 method=mcp           status=🟢:fresh
- source=outlook   last_synced=—                method=—             status=⛔:skipped_per_exec_2026_04_23
<!-- SYNC_STATUS:END -->

> **Sync notes (2026-04-23):** Google Calendar returned zero events for today through 2026-04-26 across primary, `A&H Family`, and `Family` calendars. Notion `CalendarAdx` contained 13 fellowship rotation blocks (no discrete events, tasks, meetings, or deadlines). Outlook skipped per executive directive. Apple Calendar now synced via direct SQLite read of `~/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb` (macOS 26 Tahoe location — the older `~/Library/Calendars/` is empty on this system). The Apple DB holds 673 items across 21 calendars (21 calendars includes three `adxxxbox@gmail.com` aliases mirroring the Google account we already sync via API, plus iCloud Home/Match/Family/Work, `A&H Family`, Scheduled Reminders, and US Holidays); the next 48h window returned zero events, confirming the executive genuinely has nothing booked through 2026-04-26. **Net: three sources agree — the next three days are clear.**

---

## 2026-04-13 Monday

### 🔵 Away Games rotation
<!-- entry: type=event id=E0008 source=notion created=2026-04-23 date=2026-04-13 time=all_day status=upcoming source_calendar=notion -->
- **description**: fellowship rotation block currently running; ends in three days
- **date**: 2026-04-13 to 2026-04-26
- **time**: all_day
- **source_calendar**: notion
- **last_synced**: 2026-04-23 21:33
- **location**: —
- **status**: 🔵 upcoming
- **related**: E0009

**logged_updates**:
- `2026-04-23 21:33` [L0022] context=sync action=event_imported_current_rotation advised=prepare_for_CV_handover response=— risk=🟢:in_progress

## 2026-04-27 Monday

### 🔵 CV rotation
<!-- entry: type=event id=E0009 source=notion created=2026-04-23 date=2026-04-27 time=all_day status=upcoming source_calendar=notion -->
- **description**: next fellowship rotation block; starts in four days
- **date**: 2026-04-27 to 2026-05-10
- **time**: all_day
- **source_calendar**: notion
- **last_synced**: 2026-04-23 21:33
- **location**: —
- **status**: 🔵 upcoming
- **related**: E0008

**logged_updates**:
- `2026-04-23 21:33` [L0023] context=sync action=event_imported_next_rotation advised=— response=— risk=🟢:upcoming

## 2026-05-11 Monday

### 🔵 Neuro rotation
<!-- entry: type=event id=E0010 source=notion created=2026-04-23 date=2026-05-11 time=all_day status=upcoming source_calendar=notion -->
- **description**: fellowship rotation block (Notion CalendarAdx)
- **date**: 2026-05-11 to 2026-05-24
- **time**: all_day
- **source_calendar**: notion
- **last_synced**: 2026-04-23 21:33
- **location**: —
- **status**: 🔵 upcoming
- **related**: —

**logged_updates**:
- `2026-04-23 21:33` [L0024] context=sync action=event_imported advised=— response=— risk=🟢:upcoming

## 2026-05-25 Monday

### 🔵 Ortho Regional rotation
<!-- entry: type=event id=E0011 source=notion created=2026-04-23 date=2026-05-25 time=all_day status=upcoming source_calendar=notion -->
- **description**: fellowship rotation block (Notion CalendarAdx)
- **date**: 2026-05-25 to 2026-06-07
- **time**: all_day
- **source_calendar**: notion
- **last_synced**: 2026-04-23 21:33
- **location**: —
- **status**: 🔵 upcoming
- **related**: —

**logged_updates**:
- `2026-04-23 21:33` [L0025] context=sync action=event_imported advised=— response=— risk=🟢:upcoming

## 2026-06-08 Monday

### 🔵 GPS rotation
<!-- entry: type=event id=E0012 source=notion created=2026-04-23 date=2026-06-08 time=all_day status=upcoming source_calendar=notion -->
- **description**: fellowship rotation block (Notion CalendarAdx)
- **date**: 2026-06-08 to 2026-06-21
- **time**: all_day
- **source_calendar**: notion
- **last_synced**: 2026-04-23 21:33
- **location**: —
- **status**: 🔵 upcoming
- **related**: —

**logged_updates**:
- `2026-04-23 21:33` [L0026] context=sync action=event_imported advised=— response=— risk=🟢:upcoming

## 2026-06-22 Monday

### 🔵 Acute Pain rotation
<!-- entry: type=event id=E0013 source=notion created=2026-04-23 date=2026-06-22 time=all_day status=upcoming source_calendar=notion -->
- **description**: fellowship rotation block (Notion CalendarAdx)
- **date**: 2026-06-22 to 2026-06-30
- **time**: all_day
- **source_calendar**: notion
- **last_synced**: 2026-04-23 21:33
- **location**: —
- **status**: 🔵 upcoming
- **related**: —

**logged_updates**:
- `2026-04-23 21:33` [L0027] context=sync action=event_imported advised=— response=— risk=🟢:upcoming
