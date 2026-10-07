#!/usr/bin/env python3
"""Capture live xterm windows on Linux; never render saved output as fake screenshots.
Requires DISPLAY, xterm and ImageMagick import. Intended for manual GitHub Actions.
Not yet run in the author's restricted workspace: see docs/SCREENSHOT_RUNNER.md.
"""
from pathlib import Path
import json
import os
import shlex
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/screenshots'
LOG = ROOT / 'logs/screenshots'


def shell_session(lines):
    return 'printf %s ' + shlex.quote('\n'.join(lines) + '\n') + ' | script -q -e -c ./myshell /dev/null'


def stages():
    return [
        ('01-environment', 'uname -a; cat /etc/os-release; gcc --version | head -1; make --version | head -1; strace --version | head -1; git --version'),
        ('02-build', 'make clean all'),
        ('03-prompt', shell_session(['echo OS-LAB1-started', 'exit'])),
        ('04-builtins', shell_session(['pwd', 'echo hello', 'echo $HOME', 'echo $PATH', 'exit'])),
        ('05-external', shell_session(['ls -l src', 'whoami', 'uname -a', 'exit'])),
        ('06-cd', shell_session(['pwd', 'cd /tmp', 'pwd', 'cd /not_exist', 'pwd', 'exit'])),
        ('07-files', shell_session(['touch screenshot-demo.txt', 'echo data > screenshot-demo.txt', 'cat screenshot-demo.txt', 'rm screenshot-demo.txt', 'cat screenshot-demo.txt', 'echo alive', 'exit'])),
        ('08-redirection', shell_session(['echo hello > screenshot-out.txt', 'echo world >> screenshot-out.txt', 'cat < screenshot-out.txt', 'cat screenshot-out.txt', 'exit'])),
        ('09-pipe', shell_session(['ls | wc -l', 'printf hello | wc -c', 'cat screenshot-out.txt | wc -w', 'exit'])),
        ('10-strace', 'bash tests/trace.sh > logs/screenshots/trace-run.log 2>&1; rc=$?; if test "$rc" = 0; then sed -n 1,39p logs/strace_key.log; grep -E "pipe2|clone|wait4" logs/strace.log | head -8; else tail -25 logs/screenshots/trace-run.log; fi; exit "$rc"'),
        ('11-git', 'git log --oneline --reverse'),
        ('12-final-tests', 'bash tests/verify.sh > logs/screenshots/verify-run.log 2>&1; rc=$?; tail -6 logs/final_test.log; if test "$rc" = 0; then cat logs/verification_summary.log; else tail -12 logs/screenshots/verify-run.log; fi; printf "verify_exit=%s\\n" "$rc"; python3 tests/test_audit.py > logs/screenshots/additional.log 2>&1; ar=$?; tail -2 logs/screenshots/additional.log; test "$rc" = 0 && test "$ar" = 0'),
    ]


def main():
    assert os.environ.get('DISPLAY'), 'Requires a real or virtual X display'
    for tool in ['xterm', 'import', 'bash', 'script']:
        assert shutil.which(tool), f'Missing dependency: {tool}'
    OUT.mkdir(parents=True, exist_ok=True)
    LOG.mkdir(parents=True, exist_ok=True)
    results = []
    for name, command in stages():
        done, ready = LOG/(name+'.exit'), LOG/(name+'.ready')
        done.unlink(missing_ok=True)
        ready.unlink(missing_ok=True)
        inner, outer = LOG/(name+'.command.sh'), LOG/(name+'.terminal.sh')
        inner.write_text('#!/bin/bash\n'+command+'\n')
        # Tee preserves raw bytes while xterm displays the same live execution.
        outer.write_text('#!/bin/bash\n'
            + 'cd '+shlex.quote(str(ROOT))+'\n'
            + 'exec > >(tee '+shlex.quote(str(LOG/(name+'.log')))+') 2>&1\n'
            + 'printf "OS LAB 1 | Wang Xusheng | 24281204 | Agent Linux run\\n"\n'
            + 'printf "Stage: '+name+' | UTC: "; date -u +%FT%TZ\n'
            + 'printf "%s\\n" '+shlex.quote('$ '+command)+'\n'
            + 'bash '+shlex.quote(str(inner))+'\nrc=$?\n'
            + 'printf "\\n[actual stage exit status: %s]\\n" "$rc"\n'
            + 'printf "%s" "$rc" > '+shlex.quote(str(done))+'\n'
            + 'touch '+shlex.quote(str(ready))+'\n'
            + 'read -r -p "Screenshot capture point; terminal held open" unused\n')
        proc = subprocess.Popen(['xterm', '-geometry', '155x57+0+0', '-fa', 'DejaVu Sans Mono', '-fs', '11', '-bg', '#ffffff', '-fg', '#111111', '-title', name, '-e', 'bash', str(outer)], cwd=ROOT)
        try:
            deadline = time.monotonic()+180
            while not ready.exists():
                if proc.poll() is not None:
                    raise RuntimeError(f'{name}: xterm closed before capture')
                if time.monotonic() > deadline:
                    raise TimeoutError(name)
                time.sleep(0.1)
            time.sleep(0.4)
            subprocess.run(['import', '-window', 'root', str(OUT/(name+'.png'))], check=True, timeout=20)
            rc = int(done.read_text())
            results.append({'stage': name, 'exit': rc, 'image': name+'.png'})
            print(name, 'exit', rc, flush=True)
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill(); proc.wait()
        (LOG/'manifest.json').write_text(json.dumps(results, indent=2)+'\n')
    if any(r['exit'] for r in results):
        raise SystemExit('Some stages failed; preserve screenshots and investigate, do not claim full PASS')


if __name__ == '__main__':
    main()
