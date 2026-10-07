printf "%s\n" 'OS LAB 1 | Wang Xusheng | 24281204 | 07-files'
printf "%s\n" 'CURRENT RUN'
date -u +%FT%TZ
printf "%s\n" '$ printf %s '"'"'touch tests/tmp/screenshot-demo.txt
echo data > tests/tmp/screenshot-demo.txt
cat tests/tmp/screenshot-demo.txt
rm tests/tmp/screenshot-demo.txt
cat tests/tmp/screenshot-demo.txt
echo alive
exit
'"'"' | script -q -e -c ./myshell /dev/null'
bash -c 'printf %s '"'"'touch tests/tmp/screenshot-demo.txt
echo data > tests/tmp/screenshot-demo.txt
cat tests/tmp/screenshot-demo.txt
rm tests/tmp/screenshot-demo.txt
cat tests/tmp/screenshot-demo.txt
echo alive
exit
'"'"' | script -q -e -c ./myshell /dev/null'
rc=$?
printf "\n[actual command status: %s]\n" "$rc"
exit "$rc"
