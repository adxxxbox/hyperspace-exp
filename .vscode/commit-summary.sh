#!/usr/bin/env bash
# Stage all changes and commit with a summary of added/modified/deleted files.
set -e

git pull --rebase --autostash

git add -A

A=$(git diff --cached --name-only --diff-filter=A)
M=$(git diff --cached --name-only --diff-filter=M)
D=$(git diff --cached --name-only --diff-filter=D)

nA=$(printf '%s' "$A" | awk 'NF{c++} END{print c+0}')
nM=$(printf '%s' "$M" | awk 'NF{c++} END{print c+0}')
nD=$(printf '%s' "$D" | awk 'NF{c++} END{print c+0}')

fA=$(printf '%s\n' "$A" | awk 'NF{n=split($0,a,"/"); print a[n]}' | paste -sd ', ' -)
fM=$(printf '%s\n' "$M" | awk 'NF{n=split($0,a,"/"); print a[n]}' | paste -sd ', ' -)
fD=$(printf '%s\n' "$D" | awk 'NF{n=split($0,a,"/"); print a[n]}' | paste -sd ', ' -)

if [ "$nA" = 0 ] && [ "$nM" = 0 ] && [ "$nD" = 0 ]; then
  echo 'Nothing to commit.'
  exit 0
fi

git commit \
  -m "New files added $nA ($fA)" \
  -m "Files modified $nM ($fM)" \
  -m "Files deleted $nD ($fD)"

git push
