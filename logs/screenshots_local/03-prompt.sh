printf "%s\n" 'OS LAB 1 | Wang Xusheng | 24281204 | 03-prompt'
printf "%s\n" 'CURRENT RUN'
date -u +%FT%TZ
printf "%s\n" '$ printf %s '"'"'echo OS-LAB1-started
exit
'"'"' | script -q -e -c ./myshell /dev/null'
bash -c 'printf %s '"'"'echo OS-LAB1-started
exit
'"'"' | script -q -e -c ./myshell /dev/null'
rc=$?
printf "\n[actual command status: %s]\n" "$rc"
exit "$rc"
