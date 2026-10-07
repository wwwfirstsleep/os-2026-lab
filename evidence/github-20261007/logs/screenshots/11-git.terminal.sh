#!/bin/bash
cd /home/runner/work/os-2026-lab/os-2026-lab
exec > >(tee /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/11-git.log) 2>&1
printf "OS LAB 1 | Wang Xusheng | 24281204 | Agent Linux run\n"
printf "Stage: 11-git | UTC: "; date -u +%FT%TZ
printf "%s\n" '$ git log --oneline --reverse'
bash /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/11-git.command.sh
rc=$?
printf "\n[actual stage exit status: %s]\n" "$rc"
printf "%s" "$rc" > /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/11-git.exit
touch /home/runner/work/os-2026-lab/os-2026-lab/logs/screenshots/11-git.ready
read -r -p "Screenshot capture point; terminal held open" unused
