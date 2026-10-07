#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
make
python3 tests/run_tests.py redirect 2>&1 | tee logs/redirect_test.log
