#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
make
python3 tests/run_tests.py basic 2>&1 | tee logs/basic_test.log
