"""Regression for the scheduler-dependent strace formatting that was misread."""
import re
from pathlib import Path
source = (Path(__file__).parent/'extract_trace.py').read_text()
# Reuse the exact literal in the extractor without executing its file side effects.
import ast
module = ast.parse(source)
pattern = next(ast.literal_eval(n.value) for n in module.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id=='reap_pattern' for t in n.targets))
samples = [
 ('12 wait4(13, [{WIFEXITED(s) && WEXITSTATUS(s) == 0}], 0, NULL) = 13', '13'),
 ('12 <... wait4 resumed>[{WIFEXITED(s) && WEXITSTATUS(s) == 0}], 0, NULL) = 13', '13'),
 ('12 wait4(13, <unfinished ...>', None),
 ('12 wait4(-1, 0x123, 0, NULL) = -1 ECHILD (No child processes)', None),
]
for line, expected in samples:
    match = re.search(pattern, line)
    assert (match.group(1) if match else None) == expected, line
print('PASS: 4 trace-parser regression samples (synthetic parser inputs, not runtime evidence)')
