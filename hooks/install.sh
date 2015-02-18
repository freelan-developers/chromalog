#!/bin/bash
HOOKS_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

git config alias.runtests "!python '${HOOKS_DIR}/runtests.py'"
