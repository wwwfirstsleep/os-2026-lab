#!/bin/bash
cd /home/runner/work/os-2026-lab/os-2026-lab
exec > >(tee /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/02-build.log) 2>&1
printf "OS LAB 1 | Wang Xusheng | 24281204 | Agent Linux run\n"
printf "Stage: 02-build | UTC: "; date -u +%FT%TZ
printf "%s\n" '$ make clean all'
bash /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/02-build.command.sh
rc=$?
printf "\n[actual stage exit status: %s]\n" "$rc"
printf "%s" "$rc" > /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/02-build.exit
touch /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/02-build.ready
read -r -p "Screenshot capture point; terminal held open" unused
