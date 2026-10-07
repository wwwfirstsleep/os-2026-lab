#!/bin/bash
cd /home/runner/work/os-2026-lab/os-2026-lab
exec > >(tee /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/08-redirection.log) 2>&1
printf "OS LAB 1 | Wang Xusheng | 24281204 | Agent Linux run\n"
printf "Stage: 08-redirection | UTC: "; date -u +%FT%TZ
printf "%s\n" '$ printf %s '"'"'echo hello > screenshot-out.txt
echo world >> screenshot-out.txt
cat < screenshot-out.txt
cat screenshot-out.txt
exit
'"'"' | script -q -e -c ./myshell /dev/null'
bash /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/08-redirection.command.sh
rc=$?
printf "\n[actual stage exit status: %s]\n" "$rc"
printf "%s" "$rc" > /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/08-redirection.exit
touch /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/08-redirection.ready
read -r -p "Screenshot capture point; terminal held open" unused
