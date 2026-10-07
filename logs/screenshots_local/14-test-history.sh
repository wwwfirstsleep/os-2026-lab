printf "%s\n" 'OS LAB 1 | Wang Xusheng | 24281204 | 14-test-history'
printf "%s\n" 'HISTORICAL FULL PASS FILE VIEW - NOT A NEW TEST'
date -u +%FT%TZ
printf "%s\n" '$ tail -7 logs/final_test.log; cat logs/verification_summary.log; sha256sum -c logs/artifact_hashes.log'
bash -c 'tail -7 logs/final_test.log; cat logs/verification_summary.log; sha256sum -c logs/artifact_hashes.log'
rc=$?
printf "\n[actual command status: %s]\n" "$rc"
exit "$rc"
