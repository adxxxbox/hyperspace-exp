# Hyperspace Agreement

This file captures the current working agreement for the Hyperspace restructure. It is descriptive, not yet the final rulebook.

## Core idea

Hyperspace is the vault as a personal operating environment. The structure should keep the executive-facing workspace simple while keeping operator instructions, logs, tools, and internal machinery separate.

The system should stay modular. A module exists only when it has a real purpose, owner, and boundary. Empty conceptual departments are avoided.

## Top-level concept

The future structure currently has two main zones:

```text
Workspace/
_exec/
```

`Workspace/` is where active work lives. It is readable, human-facing, and flexible.

`_exec/` is the internal execution layer. It is technical, operator-facing, and structured.

## Workspace

`Workspace/` is freeform. It may use folders, but no project/area/resource/card/journal backbone is imposed.

Folders inside `Workspace/` are created only when useful, such as for a specific project, topic, period, or workflow. Organization should rely on links, tags, context, and convenience rather than a fixed folder taxonomy.

Current Workspace backbone:

```text
Workspace/
  Home.md
  Inbox.md
  Tasks.md
  Outlines.md
  Workspace Overview.md
  Delegated/
    Tasks.DELEGATED.md
    Calendar.DELEGATED.md
```

`Home.md` is the main entry point.

`Inbox.md` is fast capture.

`Tasks.md` is the executive-facing task view.

`Outlines.md` is the executive-facing map of content.

`Delegated/` contains active executive-facing content that is managed by operators.

## Delegated content

Delegated content is still part of Workspace because it is about the executive's life and work. It is separated only because operators actively maintain it.

Current delegated files:

```text
Delegated/
  Tasks.DELEGATED.md
  Calendar.DELEGATED.md
```

There is no `Lookups.DELEGATED.md`.

Lookup work is an operator behavior. Its findings should be routed into delegated tasks or delegated calendar items. The lookup operator's own process history belongs in its operator log.

## _exec

`_exec/` is technical and internal. It should use lowercase kebab-case folder names and typed filenames.

Current `_exec` structure:

```text
_exec/
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
    note-lookup/
      note-lookup.OPERATOR.md
      note-lookup.LOG.md

  archive/
    overview.ARCHIVE.md
```

## _exec file naming

Files in `_exec/` follow:

```text
name.TYPE.ext
```

The base name is lowercase kebab-case. The type extension is uppercase. The final extension is the actual file format.

Examples:

```text
task-manager.OPERATOR.md
task-manager.LOG.md
conventions.CORE.md
registry.TOOL.jsonc
overview.ARCHIVE.md
```

Current type extensions:

| Type | Meaning |
|---|---|
| `CORE` | Shared rules, routing, permissions, context loading, and governance |
| `TOOL` | Tool registries or tool-related descriptions |
| `OPERATOR` | Instructions for one operator |
| `LOG` | Workflow history for one operator |
| `ARCHIVE` | Archive overview or archive-related notes |
| `DELEGATED` | Workspace content actively managed by operators |

## Operators

Operators are the agentic workers. They are not called employees, personas, or executives.

Each operator gets its own folder:

```text
_exec/operators/<operator-name>/
```

Each operator folder contains:

```text
<operator-name>.OPERATOR.md
<operator-name>.LOG.md
```

The `.OPERATOR.md` file defines how the operator behaves.

The `.LOG.md` file records workflow history, handoffs, decisions, and activity traces for that operator.

The operator log does not replace active delegated content. For example, task state lives in `Workspace/Delegated/Tasks.DELEGATED.md`, while the task manager's process history lives in `_exec/operators/task-manager/task-manager.LOG.md`.

## Current operators

Current operator placeholders:

```text
task-manager
calendar-manager
note-lookup
```

`task-manager` manages delegated tasks.

`calendar-manager` manages delegated calendar items.

`note-lookup` scans Workspace for signals that may become tasks or calendar items. It does not need its own delegated content file.

The name `note-lookup` may still be revisited if a clearer name emerges.

## Archive

There is one archive under `_exec/`:

```text
_exec/archive/
```

It is the single place for inactive, retired, superseded, or preserved material from anywhere in Hyperspace.

Archive organization can be added when actual archived material exists. The backbone does not prescribe archive subfolders yet.

## Boundaries

| Area | Owner | Purpose |
|---|---|---|
| `Workspace/` | Executive-facing | Active notes, maps, inbox, tasks view, and freeform work |
| `Workspace/Delegated/` | Executive-facing, operator-managed | Active tasks and calendar content maintained by operators |
| `_exec/core-rules/` | System/internal | Shared rules, routing, permissions, and tools |
| `_exec/operators/` | Operator/internal | Operator instructions and workflow logs |
| `_exec/archive/` | System/internal | Inactive or retired material from anywhere |

## Design principles

Keep Workspace free.

Keep `_exec` technical.

Prefer one real module over many imaginary departments.

Do not create a folder just because a category exists in theory.

Put active executive-facing content in Workspace.

Put operator behavior and history in `_exec`.

Put operator-managed active content in `Workspace/Delegated/`.

Use typed filenames where boundaries matter.

Keep archive unified unless a real need forces a split.
