#!/usr/bin/env bash
# rename-note.sh — Atomic rename-with-wikilink-sweep for the Foam vault.
#
# Implements §N10 / §13.4 of the vault organization guideline. Performs:
#   1. Dry-run sweep to preview wikilink changes
#   2. Prompt for confirmation
#   3. `git mv` of the file itself
#   4. Apply wikilink sweep across the vault
#   5. Stage and commit everything as one atomic change
#
# Usage:
#     ./rename-note.sh <old-slug> <new-slug> [subfolder]
#
# Examples:
#     ./rename-note.sh old-note new-note
#     ./rename-note.sh old-note new-note 1-projects
#
# Must be run from anywhere inside the vault (resolves vault root via git).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY_SCRIPT="${SCRIPT_DIR}/rename_note.py"
LIB_DIR="${SCRIPT_DIR}/../../lib"
ACTIVITY_LOG="${LIB_DIR}/activity_log.py"

if [[ $# -lt 2 || $# -gt 3 ]]; then
    echo "Usage: $0 <old-slug> <new-slug> [subfolder]" >&2
    exit 1
fi

OLD_SLUG="$1"
NEW_SLUG="$2"
SUBFOLDER="${3:-}"

# Resolve vault root via git
VAULT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "${VAULT_ROOT}" ]]; then
    echo "error: not inside a git repository. rename-note.sh requires git." >&2
    exit 1
fi

cd "${VAULT_ROOT}"

# Locate the old file
if [[ -n "${SUBFOLDER}" ]]; then
    OLD_PATH="${SUBFOLDER}/${OLD_SLUG}.md"
else
    # Search vault for unique match (skipping protected dirs)
    MATCHES=$(find . -name "${OLD_SLUG}.md" \
        -not -path "./.foam/*" \
        -not -path "./.vscode/*" \
        -not -path "./attachments/*" \
        -not -path "./docs/*" \
        -not -path "./.git/*" \
        -not -path "./_meta/*" \
        2>/dev/null | sed 's|^\./||')
    COUNT=$(echo -n "${MATCHES}" | grep -c '^' || true)
    if [[ "${COUNT}" -eq 0 ]]; then
        echo "error: no file named '${OLD_SLUG}.md' found in vault." >&2
        exit 1
    elif [[ "${COUNT}" -gt 1 ]]; then
        echo "error: multiple files named '${OLD_SLUG}.md' found:" >&2
        echo "${MATCHES}" >&2
        echo "       specify the subfolder as the third argument." >&2
        exit 1
    fi
    OLD_PATH="${MATCHES}"
fi

if [[ ! -f "${OLD_PATH}" ]]; then
    echo "error: file '${OLD_PATH}' does not exist." >&2
    exit 1
fi

NEW_PATH="$(dirname "${OLD_PATH}")/${NEW_SLUG}.md"

if [[ -e "${NEW_PATH}" ]]; then
    echo "error: target '${NEW_PATH}' already exists." >&2
    exit 1
fi

# Ensure working tree is clean (no uncommitted changes)
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "error: working tree has uncommitted changes. Commit or stash first." >&2
    git status --short >&2
    exit 1
fi

echo "Plan:"
echo "  move:    ${OLD_PATH}"
echo "  to:      ${NEW_PATH}"
echo ""
echo "Dry-run sweep of wikilinks:"
echo "----------------------------------------"
python3 "${PY_SCRIPT}" "${OLD_SLUG}" "${NEW_SLUG}" --vault-root "${VAULT_ROOT}"
echo "----------------------------------------"
echo ""
read -p "Proceed? [y/N] " -n 1 -r REPLY
echo ""
if [[ ! "${REPLY}" =~ ^[Yy]$ ]]; then
    echo "Aborted. No changes made."
    exit 0
fi

# Execute
git mv "${OLD_PATH}" "${NEW_PATH}"
python3 "${PY_SCRIPT}" "${OLD_SLUG}" "${NEW_SLUG}" --apply --vault-root "${VAULT_ROOT}" --quiet
git add -A
git commit -m "rename: ${OLD_SLUG} -> ${NEW_SLUG} (sweep wikilinks)"

echo ""
echo "Done. Commit:"
git log -1 --oneline

# Append a compact event to the hidden activity log (failures swallowed).
if [[ -f "${ACTIVITY_LOG}" ]]; then
    python3 "${ACTIVITY_LOG}" rename-note \
        from="${OLD_SLUG}" \
        to="${NEW_SLUG}" \
        commit="$(git rev-parse HEAD)" \
        >/dev/null 2>&1 || true
fi
