printf "%s\n" 'OS LAB 1 | Wang Xusheng | 24281204 | 08-redirection'
printf "%s\n" 'CURRENT RUN'
date -u +%FT%TZ
printf "%s\n" '$ printf %s '"'"'echo hello > tests/tmp/screenshot-out.txt
echo world >> tests/tmp/screenshot-out.txt
cat < tests/tmp/screenshot-out.txt
cat tests/tmp/screenshot-out.txt
exit
'"'"' | script -q -e -c ./myshell /dev/null'
bash -c 'printf %s '"'"'echo hello > tests/tmp/screenshot-out.txt
echo world >> tests/tmp/screenshot-out.txt
cat < tests/tmp/screenshot-out.txt
cat tests/tmp/screenshot-out.txt
exit
'"'"' | script -q -e -c ./myshell /dev/null'
rc=$?
printf "\n[actual command status: %s]\n" "$rc"
exit "$rc"
