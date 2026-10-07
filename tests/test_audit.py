#!/usr/bin/env python3
"""Additional coverage for documented semantics; no ptrace or /proc needed."""
import importlib.util
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('suite', root/'tests/run_tests.py')
suite = importlib.util.module_from_spec(spec)
spec.loader.exec_module(suite)
case, tmp = suite.case, suite.TMP

case('cat multiple files', 'echo alpha > multi-a\necho beta > multi-b\ncat multi-a multi-b\n', 'alpha\nbeta\n')
case('cat continues after missing file', 'cat audit-no-file multi-b\n', 'beta\n', code=1, error='audit-no-file:')
for name in ['multi-new-a', 'multi-new-b']:
    (tmp/name).unlink(missing_ok=True)
case('touch multiple files', 'touch multi-new-a multi-new-b\n', '')
assert all((tmp/name).read_bytes() == b'' for name in ['multi-new-a', 'multi-new-b'])
case('rm multiple files', 'rm multi-new-a multi-new-b\n', '')
assert all(not (tmp/name).exists() for name in ['multi-new-a', 'multi-new-b'])
space_home = tmp/'home with spaces'
space_home.mkdir(exist_ok=True)
case('HOME remains one argument', 'echo $HOME\ncd $HOME\npwd\n', f'{space_home}\n{space_home}\n', env=dict(os.environ, HOME=str(space_home)))
case('empty HOME preserved', 'echo $HOME\ncd\n', '\n', code=1, error='cd:', env=dict(os.environ, HOME=''))
case('empty PATH preserved', 'echo $PATH\n', '\n', env=dict(os.environ, PATH=''))
case('right pipeline input overrides pipe', 'echo ignored | cat < multi-a\n', 'alpha\n')
case('duplicate input rejected', 'cat < multi-a < multi-b\necho alive\n', 'alive\n', error='parse:')
case('external append', 'printf one > ext-append\nprintf two >> ext-append\ncat ext-append\n', 'onetwo')
noexec = tmp/'not-executable'
noexec.write_text('plain text\n')
noexec.chmod(0o644)
case('exec permission failure returns 126', './not-executable\n', '', code=126, error='./not-executable:')
for command in ['echo a;b', 'echo a&b', 'echo a\\b', "echo 'a'"]:
    case('unsupported syntax '+command, command+'\necho alive\n', 'alive\n', error='parse:')
case('other variable forms literal', 'echo ${HOME} $OTHER #comment\n', '${HOME} $OTHER #comment\n')
case('EOF returns last error', 'unknown_command\n', '', code=127, error='unknown_command:')
case('blank line resets status', 'unknown_command\n\n', '', error='unknown_command:')

terminal = subprocess.run(['script', '-q', '-c', suite.BIN, '/dev/null'],
    input='pwd\ncd /not_exist\ncat not_exist.txt\nrm not_exist.txt\nunknown_command\necho alive\nexit\n',
    text=True, capture_output=True, cwd=tmp, timeout=10)
print('PTY TRANSCRIPT:\n'+terminal.stdout)
assert terminal.returncode == 0
assert terminal.stdout.count('[OS-LAB1] myshell$ ') == 7
assert 'alive' in terminal.stdout
assert all(s in terminal.stdout for s in ['cd:', 'not_exist.txt:', 'unknown_command:'])
print(f'TOTAL PASS {suite.count} additional subprocess cases + PTY check')
