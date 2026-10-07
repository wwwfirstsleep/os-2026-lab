printf "%s\n" 'OS LAB 1 | Wang Xusheng | 24281204 | 09-pipe'
printf "%s\n" 'CURRENT RUN'
date -u +%FT%TZ
printf "%s\n" '$ printf %s '"'"'ls | wc -l
printf hello | wc -c
cat tests/tmp/screenshot-out.txt | wc -w
exit
'"'"' | script -q -e -c ./myshell /dev/null'
bash -c 'printf %s '"'"'ls | wc -l
printf hello | wc -c
cat tests/tmp/screenshot-out.txt | wc -w
exit
'"'"' | script -q -e -c ./myshell /dev/null'
rc=$?
printf "\n[actual command status: %s]\n" "$rc"
exit "$rc"
