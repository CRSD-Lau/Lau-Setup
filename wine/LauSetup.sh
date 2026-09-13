#!/bin/sh
# Author, Creator, Last Modified By: Neil Mitchell
set -eu
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if ! command -v python3 >/dev/null 2>&1; then
    printf '%s\n' 'Lau Setup requires Python 3 for its Linux safety checks.' >&2
    exit 1
fi
exec python3 "$here/lau_wine.py" "$@"
