@echo off
set HOOKS_DIR=%~dp0

git config alias.runtests "!python '%HOOKS_DIR%\runtests.py'"
