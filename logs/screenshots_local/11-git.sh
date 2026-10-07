printf "%s\n" 'OS LAB 1 | Wang Xusheng | 24281204 | 11-git'
printf "%s\n" 'CURRENT HISTORY VIEW'
date -u +%FT%TZ
printf "%s\n" '$ git log --oneline --reverse'
bash -c 'git log --oneline --reverse'
rc=$?
printf "\n[actual command status: %s]\n" "$rc"
exit "$rc"
