#!/bin/bash
bash tests/trace.sh > logs/screenshots/trace-run.log 2>&1; rc=$?; if test "$rc" = 0; then sed -n 1,39p logs/strace_key.log; grep -E "pipe2|clone|wait4" logs/strace.log | head -8; else tail -25 logs/screenshots/trace-run.log; fi; exit "$rc"
