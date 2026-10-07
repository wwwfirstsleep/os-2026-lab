#!/usr/bin/env python3
"""Real subprocess tests, log commands, raw streams, exit codes and assertions."""
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BIN = str(ROOT / 'myshell')
TMP = ROOT / 'tests/tmp'
TMP.mkdir(exist_ok=True)
count = 0

def case(name, script, out=None, code=0, error=None, env=None):
    global count
    print(f'\nCASE {name}\nINPUT:\n{script}', flush=True)
    p = subprocess.run([BIN], input=script, text=True, capture_output=True,
                       cwd=TMP, env=env, timeout=10)
    print(f'STDOUT={p.stdout!r}\nSTDERR={p.stderr!r}\nEXIT={p.returncode}', flush=True)
    assert p.returncode == code, (name, 'exit', code)
    if out is not None:
        assert p.stdout == out, (name, 'stdout', out)
    if error is not None:
        assert error in p.stderr, (name, 'stderr', error)
    count += 1
    print('PASS', flush=True)
    return p

def minimal():
    for cmd in ['ls', 'ls -l', 'whoami', 'uname -a', 'echo hello']:
        expected = subprocess.check_output(cmd.split(), cwd=TMP, text=True)
        case(cmd, cmd + '\nexit\n', expected)
    case('unknown continues', 'unknown_command\necho alive\nexit\n', 'alive\n', error='unknown_command:')
    case('empty and EOF', '\n\t\n', '')
    case('exit arguments', 'exit bad\necho alive\nexit\n', 'alive\n', error='exit:')
    case('argument limit', 'echo ' + 'a ' * 130 + '\necho alive\nexit\n', 'alive\n', error='parse:')

def test_cd():
    case('cd parent', f'cd {ROOT}\n/bin/pwd\nexit\n', str(ROOT) + '\n')
    case('cd error', 'cd /not_exist\necho alive\nexit\n', 'alive\n', error='cd:')
    case('cd arity', 'cd a b\n', '', code=2, error='cd:')

def test_pwd():
    case('pwd', f'pwd\ncd {ROOT}\npwd\nexit\n', str(TMP) + '\n' + str(ROOT) + '\n')
    case('pwd arity', 'pwd extra\necho alive\nexit\n', 'alive\n', error='pwd:')

def test_echo():
    case('echo spaces', 'echo one two\necho\necho -n literal\nexit\n', 'one two\n\n-n literal\n')
    case('echo excessive arguments', 'echo ' + 'x ' * 130 + '\necho alive\nexit\n', 'alive\n', error='parse:')

def test_cat():
    (TMP / 'cat-input.txt').write_text('alpha\nbeta\n')
    case('cat file', 'cat cat-input.txt\nexit\n', 'alpha\nbeta\n')
    case('cat error', 'cat not_exist.txt\necho alive\nexit\n', 'alive\n', error='not_exist.txt:')
    case('cat directory', 'cat .\n', '', code=1, error='cat: read:')

def test_touch():
    (TMP / 'new.txt').unlink(missing_ok=True)
    case('touch create', 'touch new.txt\nexit\n', '')
    assert (TMP / 'new.txt').read_bytes() == b''
    case('touch preserve', 'touch cat-input.txt\ncat cat-input.txt\nexit\n', 'alpha\nbeta\n')
    case('touch error', 'touch missing-dir/file\necho alive\nexit\n', 'alive\n', error='missing-dir/file:')
    case('touch arity', 'touch\n', '', code=2, error='touch:')

def test_rm():
    case('rm file', 'touch remove.txt\nrm remove.txt\nexit\n', '')
    assert not (TMP / 'remove.txt').exists()
    case('rm error', 'rm not_exist.txt\necho alive\nexit\n', 'alive\n', error='not_exist.txt:')
    case('rm directory', 'rm .\n', '', code=1, error='.:')
    case('rm arity', 'rm\n', '', code=2, error='rm:')

def test_env():
    env = dict(os.environ, HOME=str(ROOT), PATH='/usr/bin:/bin')
    case('HOME PATH expansion', 'echo $HOME\necho $PATH\ncd\npwd\nexit\n', str(ROOT)+'\n/usr/bin:/bin\n'+str(ROOT)+'\n', env=env)
    custom = TMP / 'pathbin'
    custom.mkdir(exist_ok=True)
    exe = custom / 'lab-probe'
    exe.write_text('#!/bin/sh\nprintf PATH_OK\n')
    exe.chmod(0o755)
    case('custom PATH lookup', 'lab-probe\n', 'PATH_OK', env=dict(env, PATH=str(custom)))
    case('empty PATH lookup failure', 'whoami\n', '', code=127, error='whoami:', env=dict(env, PATH=''))
    missing = dict(env)
    missing.pop('HOME'); missing.pop('PATH')
    case('environment defaults', 'echo $HOME\necho $PATH\ncd\npwd\n', '/\n/usr/bin:/bin\n/\n', env=missing)
    case('cat stdin and no read ahead', 'cat\nremaining input\n', 'remaining input\n')
    (TMP / 'order.txt').write_text('second\n')
    case('stdio syscall ordering', 'echo first\ncat order.txt\n', 'first\nsecond\n')

def test_redirect():
    case('output append input', 'echo hello>out.txt\necho world>>out.txt\ncat<out.txt\necho terminal\n', 'hello\nworld\nterminal\n')
    assert (TMP / 'out.txt').read_text() == 'hello\nworld\n'
    case('truncate', 'echo reset > out.txt\ncat out.txt\n', 'reset\n')
    case('external redirection', 'printf external > external.txt\nwc -c < external.txt\n', '8\n')
    case('input and output', 'cat < out.txt > copy.txt\ncat copy.txt\n', 'reset\n')
    case('redirect failure restores stdout', 'echo hidden > missing-dir/out\necho alive\n', 'alive\n', error='missing-dir/out:')
    case('input failure restores stdin', 'cat < missing-input\necho alive\n', 'alive\n', error='missing-input:')
    for cmd in ['echo >', 'cat <', 'echo > > x', 'echo > a > b', '> only-file', 'echo x |', 'echo "hi"']:
        case('syntax '+cmd, cmd+'\necho alive\n', 'alive\n', error='parse:')
    case('cd redirection remains parent', f'cd {ROOT} > cd-out\npwd\n', str(ROOT)+'\n')
    if Path('/dev/full').exists():
        case('echo write failure', 'echo hi > /dev/full\necho alive\n', 'alive\n', error='stdout:')

def test_pipe():
    case('pipe external', 'printf hello|wc -c\n', '5\n')
    case('pipe ls', 'ls | wc -l\n', str(len(os.listdir(TMP)))+'\n')
    (TMP / 'pipe-input').write_text('hello world\n')
    case('pipe builtin', 'cat pipe-input | wc -w\n', '2\n')
    case('pipe both builtins', 'echo hello | cat\n', 'hello\n')
    case('pipe with redirections', 'cat < pipe-input | wc -w > words.txt\ncat words.txt\n', '2\n')
    case('large pipe no deadlock', 'seq 1 100000 | wc -l\n', '100000\n')
    case('early reader exit', 'yes | head -n 1\n', 'y\n')
    case('pipe cd isolated', f'cd {ROOT} | cat\npwd\n', str(TMP)+'\n')
    case('pipe exit isolated', 'exit | cat\necho alive\n', 'alive\n')
    case('pipe unknown continues', 'unknown_command | cat\necho alive\n', 'alive\n', error='unknown_command:')
    case('right exit status', 'echo hi | unknown_command\n', '', code=127, error='unknown_command:')
    case('pipe redirection override', 'echo file > pipe-out | wc -c\ncat pipe-out\n', '0\nfile\n')
    for cmd in ['| cat', 'echo hi |', 'echo hi || cat', 'echo hi | cat | wc -c']:
        case('bad pipeline '+cmd, cmd+'\necho alive\n', 'alive\n', error='parse:')

def test_robust():
    case('line limit', 'echo ' + 'x'*65536 + '\necho alive\n', 'alive\n', error='parse: line too long')
    case('token limit', '>'*600 + '\necho alive\n', 'alive\n', error='parse: too many tokens')
    case('literal unsupported glob', 'echo *.txt\n', '*.txt\n')
    case('only whole parameter expands', 'echo prefix$HOME\n', 'prefix$HOME\n')
    script = ('echo hi > repeat.txt\ncat < repeat.txt | wc -c > count.txt\n') * 100
    script += f'{sys.executable} {ROOT}/tests/lifecycle_probe.py\n'
    case('parent and child fd leak after 100 pipelines', script, 'FD_OK\n')
    terminal = subprocess.run(['script', '-q', '-c', BIN, '/dev/null'],
                              input='pwd\ncd /not_exist\ncat not_exist.txt\nrm not_exist.txt\nunknown_command\necho alive\nexit\n',
                              text=True, capture_output=True, timeout=10, cwd=TMP)
    print('PTY TRANSCRIPT:\n'+terminal.stdout)
    assert terminal.returncode == 0
    assert terminal.stdout.count('[OS-LAB1] myshell$ ') == 7
    assert 'alive' in terminal.stdout
    for text in ['cd:', 'not_exist.txt:', 'unknown_command:']:
        assert text in terminal.stdout
    print('PASS prompt returns after errors')

if __name__ == '__main__':
    group = sys.argv[1] if len(sys.argv) > 1 else 'all'
    groups = {'basic': [minimal, test_cd, test_pwd, test_echo, test_cat, test_touch, test_rm, test_env],
              'redirect': [test_redirect], 'pipe': [test_pipe], 'robust': [test_robust]}
    assert group in [*groups, 'all']
    for name, functions in groups.items():
        if group in (name, 'all'):
            for fn in functions: fn()
    print(f'\nTOTAL PASS {count} subprocess cases; PTY checked in robust group')
