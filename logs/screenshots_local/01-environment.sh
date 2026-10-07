printf "%s\n" 'OS LAB 1 | Wang Xusheng | 24281204 | 01-environment'
printf "%s\n" 'CURRENT RUN'
date -u +%FT%TZ
printf "%s\n" '$ uname -a; cat /etc/os-release; gcc --version | head -1; make --version | head -1; strace --version | head -1; git --version'
bash -c 'uname -a; cat /etc/os-release; gcc --version | head -1; make --version | head -1; strace --version | head -1; git --version'
rc=$?
printf "\n[actual command status: %s]\n" "$rc"
exit "$rc"
