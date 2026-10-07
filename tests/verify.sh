#!/bin/bash
# One reproducible entry point for the teacher's Linux host.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p logs
{
  uname -a
  cat /etc/os-release
  gcc --version
  make --version
  strace --version
  git --version
} > logs/verification_environment.log 2>&1
make clean all > logs/final_build.log 2>&1
make test > logs/final_test.log 2>&1
bash tests/test_basic.sh > logs/basic_runner.log 2>&1
bash tests/test_redirect.sh > logs/redirect_runner.log 2>&1
bash tests/test_pipe.sh > logs/pipe_runner.log 2>&1
bash tests/trace.sh > logs/strace_extract_output.log 2>&1
sha256sum src/myshell.c Makefile myshell > logs/artifact_hashes.log
printf 'PASS: clean build, full suite, grouped tests and real strace completed\n' | tee logs/verification_summary.log
