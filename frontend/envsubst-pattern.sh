#!/usr/bin/env sh

if [ "$1" != "--prefix" ]; then
  echo "Usage: $0 --prefix PREFIX [options passed to envsubst]"
  exit 1
fi

set -eu

PREFIX="$2"
VARIABLE_NAMES=$(env | grep ^"$PREFIX" | cut -d = -f1 | xargs -I % echo $% | xargs echo)

shift 2
envsubst "$@" "$VARIABLE_NAMES"
