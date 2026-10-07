#!/bin/bash
cd /home/runner/work/os-2026-lab/os-2026-lab
exec > >(tee /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/01-environment.log) 2>&1
printf "OS LAB 1 | Wang Xusheng | 24281204 | Agent Linux run\n"
printf "Stage: 01-environment | UTC: "; date -u +%FT%TZ
printf "%s\n" '$ uname -a; cat /etc/os-release; gcc --version | head -1; make --version | head -1; strace --version | head -1; git --version'
bash /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/01-environment.command.sh
rc=$?
printf "\n[actual stage exit status: %s]\n" "$rc"
printf "%s" "$rc" > /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/01-environment.exit
touch /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/01-environment.ready
read -r -p "Screenshot capture point; terminal held open" unused
