printf "%s\n" 'OS LAB 1 | Wang Xusheng | 24281204 | 12-tests'
printf "%s\n" 'CURRENT RUN - CHECK EXIT STATUS'
date -u +%FT%TZ
printf "%s\n" '$ make test > logs/screenshots_local/current-suite.log 2>&1; rc=$?; grep -c "^PASS$" logs/screenshots_local/current-suite.log; tail -9 logs/screenshots_local/current-suite.log; printf "make_test_exit=%s\n" "$rc"; python3 tests/test_audit.py > logs/screenshots_local/additional.log 2>&1; ar=$?; tail -2 logs/screenshots_local/additional.log; python3 tests/test_trace_parser.py; test "$rc" = 0 && test "$ar" = 0'
bash -c 'make test > logs/screenshots_local/current-suite.log 2>&1; rc=$?; grep -c "^PASS$" logs/screenshots_local/current-suite.log; tail -9 logs/screenshots_local/current-suite.log; printf "make_test_exit=%s\n" "$rc"; python3 tests/test_audit.py > logs/screenshots_local/additional.log 2>&1; ar=$?; tail -2 logs/screenshots_local/additional.log; python3 tests/test_trace_parser.py; test "$rc" = 0 && test "$ar" = 0'
rc=$?
printf "\n[actual command status: %s]\n" "$rc"
exit "$rc"
