printf "%s\n" 'OS LAB 1 | Wang Xusheng | 24281204 | 02-build'
printf "%s\n" 'CURRENT RUN'
date -u +%FT%TZ
printf "%s\n" '$ make clean all'
bash -c 'make clean all'
rc=$?
printf "\n[actual command status: %s]\n" "$rc"
exit "$rc"
