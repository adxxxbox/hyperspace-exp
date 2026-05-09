# Conventions

The single governance file for Hyperspace. All shared rules every operator must obey live here.

Sections inside this file are allowed to grow. When a section becomes large enough to dominate the file or to change at a different cadence than the rest, that is the signal to split it into its own `*.CORE.md` next to this one. Until then, do not split.

## Growth rule

A new file or folder enters Hyperspace only when there is concrete pressure for it: a real workflow, a real duplication, a real permissions need, or a real navigation pain. "It might be useful later" is not pressure. The empty-placeholder pattern is forbidden.

This rule applies to everything: operators, tools, core-rule splits, archive subfolders, managed files, and Workspace folders.

## Operator activation

When activating an operator for a request:

1. Read the operator's folder: `_agentic/operators/<operator-name>/`.
2. Read its `<operator-name>.OPERATOR.md` for behaviour and permissions.
3. Read its `<operator-name>.LOG.md` only if prior history is relevant to the current task.
4. Read the managed files the operator owns (per `AGENTS.md`).
5. Do not read other operators' files unless the request explicitly crosses operators.

Minimal context loading is the default. Loading more than is needed is a violation.

## Routing

All routing decisions begin at `AGENTS.md`. The active-operators table there is the only source of truth for which operators exist.

If a request does not map to any operator, it is User-direct and no operator is loaded.

If a request spans operators, the first operator handles its part, then hands off via its log.

(Split into `router.CORE.md` when this section exceeds about fifty lines or routing changes start polluting the diff history of this file.)

## Permissions

Defaults:

- Every operator may read its own folder and the files listed under it in the `AGENTS.md` registry.
- Every operator may write only to the files listed under "Writes" for it in `AGENTS.md`, plus its own `*.LOG.md`.
- No operator may modify `AGENTS.md`, `Hyperspace Agreement.md`, this file, or any other operator's folder.
- No operator may delete files. Retired material moves to `_agentic/archive/`.
- The User may write anywhere.

(Split into `permissions.CORE.md` when the first sensitive tool exists, or when three or more operators have meaningfully different boundaries.)

## File naming

- `Workspace/` uses human style: first letter capitalised, spaces allowed, additional capitalisation as the name warrants. Example: `Task Capture.md`.
- `_agentic/` uses tech style: lowercase kebab-case base names with uppercase typed suffixes. Example: `task-manager.OPERATOR.md`.
- The `Managed/` folder inside Workspace marks the operator-ownership boundary; files inside it use the human style without an extra suffix.

Typed suffixes currently in use inside `_agentic/`:

| Suffix | Meaning |
| --- | --- |
| `CORE` | Shared governance file |
| `OPERATOR` | Behaviour spec for one operator |
| `LOG` | History log for one operator |
| `ARCHIVE` | Archive overview or archive-related notes |

New suffixes are added only when a new file class genuinely exists. They are not pre-declared.

## Archive

There is one archive: `_agentic/archive/`. Anything retired from anywhere in Hyperspace goes here. The archive has no internal structure until real archived material exists in volume.

## Logs

Each operator maintains its own `*.LOG.md` inside its own folder. Logs are append-only narrative: handoffs, decisions, notable changes, drained items.

Log rotation is not yet defined. When a log becomes hard to read, archive the older portion under `_agentic/archive/` and start a fresh log file. (Split into a dedicated rotation rule when this happens for the first time.)
