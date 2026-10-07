printf "%s\n" 'OS LAB 1 | Wang Xusheng | 24281204 | 10-strace-history'
printf "%s\n" 'HISTORICAL TRACE FILE VIEW - NOT A NEW TRACE'
date -u +%FT%TZ
printf "%s\n" '$ grep -E '"'"'chdir\(|execve\("/usr/bin/ls"|out.txt.*O_|pipe2\('"'"' logs/strace.log; cat logs/strace_reaping.log'
bash -c 'grep -E '"'"'chdir\(|execve\("/usr/bin/ls"|out.txt.*O_|pipe2\('"'"' logs/strace.log; cat logs/strace_reaping.log'
rc=$?
printf "\n[actual command status: %s]\n" "$rc"
exit "$rc"
