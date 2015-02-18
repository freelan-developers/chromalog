#!/bin/bash
HOOKS_DIR=${PWD##*/}

git config alias.runtests "!python '${HOOKS_DIR}/runtests.py'"
