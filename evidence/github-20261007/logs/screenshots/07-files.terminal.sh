#!/bin/bash
cd /home/runner/work/os-2026-lab/os-2026-lab
exec > >(tee /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/07-files.log) 2>&1
printf "OS LAB 1 | Wang Xusheng | 24281204 | Agent Linux run\n"
printf "Stage: 07-files | UTC: "; date -u +%FT%TZ
printf "%s\n" '$ printf %s '"'"'touch screenshot-demo.txt
echo data > screenshot-demo.txt
cat screenshot-demo.txt
rm screenshot-demo.txt
cat screenshot-demo.txt
echo alive
exit
'"'"' | script -q -e -c ./myshell /dev/null'
bash /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/07-files.command.sh
rc=$?
printf "\n[actual stage exit status: %s]\n" "$rc"
printf "%s" "$rc" > /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/07-files.exit
touch /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/07-files.ready
read -r -p "Screenshot capture point; terminal held open" unused
