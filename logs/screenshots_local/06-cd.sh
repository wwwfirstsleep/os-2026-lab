printf "%s\n" 'OS LAB 1 | Wang Xusheng | 24281204 | 06-cd'
printf "%s\n" 'CURRENT RUN'
date -u +%FT%TZ
printf "%s\n" '$ printf %s '"'"'pwd
cd /workspace/scratch/876e69c55179/myshell/tests/tmp
pwd
cd /not_exist
pwd
exit
'"'"' | script -q -e -c ./myshell /dev/null'
bash -c 'printf %s '"'"'pwd
cd /workspace/scratch/876e69c55179/myshell/tests/tmp
pwd
cd /not_exist
pwd
exit
'"'"' | script -q -e -c ./myshell /dev/null'
rc=$?
printf "\n[actual command status: %s]\n" "$rc"
exit "$rc"
