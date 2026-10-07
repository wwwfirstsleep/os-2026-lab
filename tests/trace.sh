#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p logs tests/tmp/trace
root=$(pwd)
{
  printf 'pwd\ncd /tmp\npwd\ncd %s/tests/tmp/trace\npwd\n' "$root"
  printf 'touch test.txt\necho trace-data > test.txt\ncat test.txt\nls -l\necho hello > out.txt\necho world >> out.txt\ncat < out.txt\nls | wc -l\nprintf hello | wc -c\nrm test.txt\nexit\n'
} > logs/strace_commands.txt
# Shell stdin comes from this file; -o is strace's log destination, not shell redirection.
strace -f -o logs/strace.log ./myshell < logs/strace_commands.txt > logs/strace_stdout.log 2> logs/strace_stderr.log
python3 tests/extract_trace.py
