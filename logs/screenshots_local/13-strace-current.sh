printf "%s\n" 'OS LAB 1 | Wang Xusheng | 24281204 | 13-strace-current'
printf "%s\n" 'CURRENT RUN - PERMISSION CHECK'
date -u +%FT%TZ
printf "%s\n" '$ strace -f -o logs/screenshots_local/strace-probe.log /bin/true'
bash -c 'strace -f -o logs/screenshots_local/strace-probe.log /bin/true'
rc=$?
printf "\n[actual command status: %s]\n" "$rc"
exit "$rc"
