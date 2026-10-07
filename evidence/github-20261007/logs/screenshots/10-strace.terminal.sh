#!/bin/bash
cd /home/runner/work/os-2026-lab/os-2026-lab
exec > >(tee /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/10-strace.log) 2>&1
printf "OS LAB 1 | Wang Xusheng | 24281204 | Agent Linux run\n"
printf "Stage: 10-strace | UTC: "; date -u +%FT%TZ
printf "%s\n" '$ bash tests/trace.sh > logs/screenshots/trace-run.log 2>&1; rc=$?; if test "$rc" = 0; then sed -n 1,39p logs/strace_key.log; grep -E "pipe2|clone|wait4" logs/strace.log | head -8; else tail -25 logs/screenshots/trace-run.log; fi; exit "$rc"'
bash /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/10-strace.command.sh
rc=$?
printf "\n[actual stage exit status: %s]\n" "$rc"
printf "%s" "$rc" > /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/10-strace.exit
touch /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/10-strace.ready
read -r -p "Screenshot capture point; terminal held open" unused
