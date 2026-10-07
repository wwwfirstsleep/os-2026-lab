#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
make
python3 tests/run_tests.py pipe 2>&1 | tee logs/pipe_test.log
