#!/bin/bash
cd /home/runner/work/os-2026-lab/os-2026-lab
exec > >(tee /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/05-external.log) 2>&1
printf "OS LAB 1 | Wang Xusheng | 24281204 | Agent Linux run\n"
printf "Stage: 05-external | UTC: "; date -u +%FT%TZ
printf "%s\n" '$ printf %s '"'"'ls -l src
whoami
uname -a
exit
'"'"' | script -q -e -c ./myshell /dev/null'
bash /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/05-external.command.sh
rc=$?
printf "\n[actual stage exit status: %s]\n" "$rc"
printf "%s" "$rc" > /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/05-external.exit
touch /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/05-external.ready
read -r -p "Screenshot capture point; terminal held open" unused
