# AGENTS

This is the root registry for Hyperspace. It is the only place that answers the question: **what operators are active, and where do they live?** Routing logic for any request begins here.

When an operator is added, removed, or renamed, this file is updated. There is no other registry.

## How to use this file

1. Identify the operator that owns the request, using the table below.
2. Read that operator's `*.OPERATOR.md` for behaviour and permissions.
3. Read the relevant managed files in `Workspace/Managed/` if the operator maintains user-facing content.
4. Read `_agentic/conventions.CORE.md` once for shared conventions; do not re-read on subsequent requests in the same session.

If no operator owns the request, the request is User-direct: it does not need an operator at all.

## Active operators

| Operator | Owns | Reads | Writes | Folder |
| --- | --- | --- | --- | --- |
| `task-manager` | Active task list | `Workspace/Task Capture.md`, `Workspace/Managed/Tasks.md` | `Workspace/Managed/Tasks.md`, own log | [`_agentic/operators/task-manager/`](_agentic/operators/task-manager/) |
| `calendar-manager` | Active calendar items | `Workspace/Managed/Calendar.md`, calendar imports | `Workspace/Managed/Calendar.md`, own log | [`_agentic/operators/calendar-manager/`](_agentic/operators/calendar-manager/) |
| `signal-router` | Routing freeform signals into managed files | `Workspace/Inbox.md`, other Workspace notes | `Workspace/Managed/Tasks.md`, `Workspace/Managed/Calendar.md`, own log | [`_agentic/operators/signal-router/`](_agentic/operators/signal-router/) |

## Routing examples

- "Add task: follow up with cards on the d-TGA case." → `task-manager` (operates on `Task Capture.md` → `Managed/Tasks.md`).
- "What is on my calendar this week?" → `calendar-manager` (reads `Managed/Calendar.md`).
- "I dumped some thoughts in `Inbox.md`, please process." → `signal-router` (scans `Inbox.md`, routes findings into managed tasks/calendar).
- "Edit this project note." → User-direct, no operator.

## Adding an operator

1. Create the folder: `_agentic/operators/<operator-name>/`.
2. Create `<operator-name>.OPERATOR.md` and `<operator-name>.LOG.md` inside it.
3. Add one row to the **Active operators** table above.

That is the entire registration process. No other file needs to be edited.
