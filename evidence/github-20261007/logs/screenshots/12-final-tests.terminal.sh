#!/bin/bash
cd /home/runner/work/os-2026-lab/os-2026-lab
exec > >(tee /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/12-final-tests.log) 2>&1
printf "OS LAB 1 | Wang Xusheng | 24281204 | Agent Linux run\n"
printf "Stage: 12-final-tests | UTC: "; date -u +%FT%TZ
printf "%s\n" '$ bash tests/verify.sh > logs/screenshots/verify-run.log 2>&1; rc=$?; tail -6 logs/final_test.log; if test "$rc" = 0; then cat logs/verification_summary.log; else tail -12 logs/screenshots/verify-run.log; fi; printf "verify_exit=%s\n" "$rc"; python3 tests/test_audit.py > logs/screenshots/additional.log 2>&1; ar=$?; tail -2 logs/screenshots/additional.log; test "$rc" = 0 && test "$ar" = 0'
bash /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/12-final-tests.command.sh
rc=$?
printf "\n[actual stage exit status: %s]\n" "$rc"
printf "%s" "$rc" > /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/12-final-tests.exit
touch /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/12-final-tests.ready
read -r -p "Screenshot capture point; terminal held open" unused
