#!/bin/bash
cd /home/runner/work/os-2026-lab/os-2026-lab
exec > >(tee /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/09-pipe.log) 2>&1
printf "OS LAB 1 | Wang Xusheng | 24281204 | Agent Linux run\n"
printf "Stage: 09-pipe | UTC: "; date -u +%FT%TZ
printf "%s\n" '$ printf %s '"'"'ls | wc -l
printf hello | wc -c
cat screenshot-out.txt | wc -w
exit
'"'"' | script -q -e -c ./myshell /dev/null'
bash /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/09-pipe.command.sh
rc=$?
printf "\n[actual stage exit status: %s]\n" "$rc"
printf "%s" "$rc" > /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/09-pipe.exit
touch /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/09-pipe.ready
read -r -p "Screenshot capture point; terminal held open" unused
