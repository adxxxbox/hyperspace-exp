# Hyperspace

This document explains the current perspective of the Hyperspace project. It should be understandable without reading the existing vault, the old secretary files, or the current migration scaffold.

This is not yet the final rulebook. It is a continuously evolving design document: what Hyperspace is trying to become, how its main parts relate to each other, and what boundaries should stay clear as the structure evolves.

## What Hyperspace is

Hyperspace is a personal operating environment built out of notes, tasks, calendars, logs, and agent instructions.

The User is the center of the system. The User's life, work, projects, ideas, responsibilities, notes, and decisions are what Hyperspace exists to support.

Operators are agentic workers that help manage parts of the system. They are not the center. They do not own the User's work. They maintain selected workflows on the User's behalf.

Hyperspace should feel like an organized virtual office, but it should not become bureaucratic. Structure exists only where it helps.

## Goals

Hyperspace should make it easy to:

- Capture ideas, tasks, notes, and commitments quickly.
- Keep active work visible without forcing a rigid folder taxonomy.
- Let operators manage tasks, calendar items, and similar workflows without mixing their instructions into the User's notes.
- Keep operator behavior, rules, tools, and logs modular.
- Add future operators without redesigning the whole vault.
- Make boundaries obvious from filenames and folder locations.
- Preserve retired material in one archive.
- Keep communication simple: a person should be able to say where something belongs without reading a long manual.

## Main zones

The future structure currently has two main zones plus one root routing file:

```text
Workspace/
_agentic/
AGENTS.md
```

`Workspace/` is the User-facing work area.

`_agentic/` is the internal agentic layer.

`AGENTS.md` is the root routing table for all agents.

The distinction is the most important boundary in Hyperspace.

## Root routing

`AGENTS.md` sits at the root of Hyperspace.

It is not an operator and it is not a workspace note. It is the first routing table agents should read so they can identify the correct operator, the correct core rules, and the smallest useful context for the current request.

## Workspace

`Workspace/` contains the active material the User directly uses: notes, maps, inbox items, active views, and freeform working folders.

Workspace is intentionally flexible. It may contain folders, but no fixed project/area/resource/card/journal backbone is imposed.

Folders inside Workspace should be created by convenience. A folder can exist for a project, topic, period, person, workflow, or anything else that makes sense at the time.

Workspace organization should be supported by:

- links,
- tags,
- context,
- search,
- lightweight maps,
- and folders only where helpful.

Current Workspace backbone:

```text
Workspace/
  home.md
  inbox.md
  tasks-capture.md
  map.md
  workspace-overview.md
  Managed/
    Tasks.MANAGED.md
    Calendar.MANAGED.md
```

Workspace top-level filenames use kebab-case for consistency with `_agentic` and to keep filenames script-friendly. The `Managed/` folder retains its capitalization to mark the ownership boundary visually.

`home.md` is the main entry point into active work.

`inbox.md` is for fast capture of notes and free-form thoughts before routing. It is not for tasks.

`tasks-capture.md` is the User-facing capture queue for tasks. The User writes tasks here in any quick form. The task-manager operator drains entries into `Managed/Tasks.MANAGED.md` and clears them from this file. The User reads the active task list in `Managed/Tasks.MANAGED.md`, which means managed files must be human-readable, not opaque internal artifacts.

There is no `calendar-capture.md`. Calendar items normally arrive via import (Epic, email invites, etc.) into `Managed/Calendar.MANAGED.md`. Rare freeform calendar mentions can be written into `inbox.md` and routed by the signal-router.

`map.md` is the User-facing map of content. It helps navigate Workspace through links and context.

`workspace-overview.md` briefly explains the purpose of Workspace.

`Managed/` contains active content that is still owned by the User, but is actively maintained by operators.

## Managed

`Workspace/Managed/` exists because some active content belongs in Workspace but is maintained by operators.

Tasks and calendar items are examples. They are User-facing and about real life/work, but an operator may maintain them.

Current managed files:

```text
Workspace/
  Managed/
    Tasks.MANAGED.md
    Calendar.MANAGED.md
```

`Tasks.MANAGED.md` is the operator-maintained task source or working task file.

`Calendar.MANAGED.md` is the operator-maintained calendar source or working calendar file.

There is intentionally no separate managed signal file.

Signal routing is behavior, not a separate User-facing content category. The signal router scans Workspace for signals and routes findings into managed tasks or managed calendar items. Its process history belongs in its own operator log.

## \_agentic

`_agentic/` is the technical internal layer. It contains the mechanics of Hyperspace: shared rules, tool descriptions, operator instructions, operator logs, and archive.

`_agentic/` should feel different from Workspace. Workspace names may be friendly and human-facing. `_agentic` names should be technical, explicit, and consistent.

Current `_agentic` structure:

```text
_agentic/
  core-rules/
    overview.CORE.md
    router.CORE.md
    org-chart.CORE.md
    conventions.CORE.md
    permissions.CORE.md
    context-loading.CORE.md
    registry.TOOL.jsonc
    overview.TOOL.md

  operators/
    overview.OPERATOR.md
    task-manager/
      task-manager.OPERATOR.md
      task-manager.LOG.md
    calendar-manager/
      calendar-manager.OPERATOR.md
      calendar-manager.LOG.md
    signal-router/
      signal-router.OPERATOR.md
      signal-router.LOG.md

  archive/
    overview.ARCHIVE.md
```

## core-rules

`_agentic/core-rules/` contains the shared operating layer.

It holds rules and technical definitions that may be used by multiple operators. It also holds the tool registry or tool-related descriptions.

Current core-rule files:

```text
overview.CORE.md
router.CORE.md
org-chart.CORE.md
conventions.CORE.md
permissions.CORE.md
context-loading.CORE.md
registry.TOOL.jsonc
overview.TOOL.md
```

`router.CORE.md` will describe how requests are routed to the correct operator or workflow.

`org-chart.CORE.md` will describe the operator map and authority boundaries.

`conventions.CORE.md` will describe always-on system conventions.

`permissions.CORE.md` will describe read/write boundaries.

`context-loading.CORE.md` will describe what an operator should read for a given task.

`registry.TOOL.jsonc` will map tool-like capabilities or triggers to implementation details.

## Operators

Operators are the agentic workers in Hyperspace.

They are called operators, not employees or personas. The User is the person Hyperspace serves; operators are workers inside the system.

Operators live here:

```text
_agentic/operators/
```

Each operator gets one folder:

```text
_agentic/operators/<operator-name>/
```

Each operator folder contains:

```text
<operator-name>.OPERATOR.md
<operator-name>.LOG.md
```

The `.OPERATOR.md` file defines what the operator does, what it can read, what it can write, and how it should behave.

The `.LOG.md` file records the operator's workflow history: handoffs, decisions, activity traces, and notable changes.

The operator log is not the same as the active content the operator manages. For example, the task manager's process history belongs in:

```text
_agentic/operators/task-manager/task-manager.LOG.md
```

But the active task content belongs in:

```text
Workspace/Managed/Tasks.MANAGED.md
```

## Current operators

Current operator placeholders:

```text
task-manager
calendar-manager
signal-router
```

`task-manager` maintains managed tasks.

`calendar-manager` maintains managed calendar items.

`signal-router` scans Workspace for signals that may become tasks or calendar items.

The name `signal-router` reflects its current job: read allowed notes or sources, identify actionable signals, and route those signals into tasks or calendar items.

## Archive

There is one archive:

```text
_agentic/archive/
```

The archive is the single place for inactive, retired, superseded, or preserved material from anywhere in Hyperspace.

It may contain retired User material, but only because that material is inactive or preserved. Active User material belongs in Workspace or Workspace/Managed, not archive.

The archive is inside `_agentic` because it is part of the system's storage and maintenance layer, not part of active Workspace.

Archive organization should be added when real archived material exists. The backbone does not prescribe archive subfolders yet.

## File naming

Workspace top-level files use kebab-case so naming is consistent with `_agentic`, friendly to scripts and search, and free of spaces.

Examples:

```text
home.md
inbox.md
tasks-capture.md
map.md
workspace-overview.md
```

Managed files use a type extension because they have a special ownership boundary:

```text
Tasks.MANAGED.md
Calendar.MANAGED.md
```

Files in `_agentic/` use:

```text
name.TYPE.ext
```

The base name is lowercase kebab-case.

The type extension is uppercase.

The final extension is the real file format.

Examples:

```text
task-manager.OPERATOR.md
task-manager.LOG.md
conventions.CORE.md
registry.TOOL.jsonc
overview.ARCHIVE.md
```

Current type extensions:

| Type        | Meaning                                                             |
| ----------- | ------------------------------------------------------------------- |
| `CORE`      | Shared rules, routing, permissions, context loading, and governance |
| `TOOL`      | Tool registries or tool-related descriptions                        |
| `OPERATOR`  | Instructions for one operator                                       |
| `LOG`       | Workflow history for one operator                                   |
| `ARCHIVE`   | Archive overview or archive-related notes                           |
| `MANAGED`   | User-owned Workspace content actively maintained by operators        |

## Where things go

Use this table when deciding where something belongs.

| Item                             | Location                                                   | Reason                                           |
| -------------------------------- | ---------------------------------------------------------- | ------------------------------------------------ |
| A normal project note            | `Workspace/` or a convenient Workspace subfolder           | It is User-facing active work                    |
| A fast captured note or thought  | `Workspace/inbox.md`                                       | It is freeform, not yet routed, and not a task   |
| A quick task to be organized later | `Workspace/tasks-capture.md`                             | It is a write-only capture queue drained by the task-manager |
| The main map of notes            | `Workspace/map.md`                                         | It is User-facing navigation                     |
| The active task list (read view) | `Workspace/Managed/Tasks.MANAGED.md`                       | It is the operator-maintained source of truth, kept human-readable |
| Operator-maintained calendar data | `Workspace/Managed/Calendar.MANAGED.md`                   | It is active User content maintained by an operator |
| Instructions for task management | `_agentic/operators/task-manager/task-manager.OPERATOR.md` | It defines operator behavior                     |
| Task manager history             | `_agentic/operators/task-manager/task-manager.LOG.md`      | It records what the operator did                 |
| Shared routing rules             | `_agentic/core-rules/router.CORE.md`                       | It affects multiple operators                    |
| Tool registry                    | `_agentic/core-rules/registry.TOOL.jsonc`                  | It is technical operator infrastructure          |
| Retired material                 | `_agentic/archive/`                                        | It is inactive or preserved                      |

## Boundaries

The main boundary is:

```text
Workspace = active User-facing material
_agentic = internal operator/system material
```

The second boundary is:

```text
Workspace/Managed = active User-owned material maintained by operators
_agentic/operators = operator behavior and history
```

Tasks and calendars belong in `Workspace/Managed/` when operators maintain their working data, because they are still about the User's real commitments.

When a managed file has a User-facing capture counterpart, keep the boundary explicit:

```text
Workspace/tasks-capture.md       = User-facing capture queue (write-only, drained by operator)
Workspace/Managed/Tasks.MANAGED.md = operator-maintained source of truth (User-readable)
Workspace/Managed/Calendar.MANAGED.md = operator-maintained source of truth (User-readable)
```

There is no User-facing `calendar.md` or `calendar-capture.md`. Calendar items enter `Calendar.MANAGED.md` through imports or via `inbox.md` plus the signal-router.

Operator instructions and operator logs belong in `_agentic/operators/` because they describe how the operator behaves and what it has done.

## Modularity rule

Do not create a module just because a category sounds useful.

A module should exist only when it has:

- a real function,
- a clear owner,
- a clear input/output boundary,
- and a reason to be separate from existing modules.

This prevents Hyperspace from becoming a maze of imaginary departments.

## Adding a future operator

When a new operator is genuinely needed, add one folder:

```text
_agentic/operators/<new-operator>/
```

Inside it, add:

```text
<new-operator>.OPERATOR.md
<new-operator>.LOG.md
```

If the operator maintains active User-facing content, create the relevant managed file under:

```text
Workspace/Managed/
```

Only create a managed file when there is real active content to maintain.

## Design principles

Keep Workspace free.

Keep `_agentic` technical.

Prefer one real module over many imaginary departments.

Do not create a folder just because a category exists in theory.

Put active User-facing content in Workspace.

Put operator-maintained active content in `Workspace/Managed/`.

Put operator behavior and history in `_agentic/operators/`.

Put shared rules and tools in `_agentic/core-rules/`.

Use typed filenames where boundaries matter.

Keep archive unified unless a real need forces a split.

Keep communication simple enough that a future reader can answer: "Who owns this, and where does it go?"

## Open questions

The exact format inside managed task and calendar files is not decided yet. Because the User reads `Tasks.MANAGED.md` directly, the chosen format must be human-readable, not opaque structured data.

The drain contract for `tasks-capture.md` is not yet written. It needs to specify trigger condition (on-demand, on-invocation, or scheduled), preservation behavior on parse failure, and a marker the operator leaves so an empty file is unambiguous (just-drained vs. never-used). Until this is written, the task-manager operator cannot be implemented. On drain, the original line should be moved to the operator log rather than deleted, so nothing is ever truly lost.

The exact archive organization is not decided yet.

The final migration from the old vault structure has not happened yet.
