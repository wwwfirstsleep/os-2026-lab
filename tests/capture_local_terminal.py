#!/usr/bin/env python3
"""Real PTY-backed xterm screenshots; historical logs are explicitly labelled.
Set XVFB_BIN, XTERM_BIN and optionally XKB_ROOT, XFONT_ROOT for local tools.
"""
from pathlib import Path
import os, subprocess, time, socket, pty, termios, select, shlex, json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/screenshots'
LOG=ROOT/'logs/screenshots_local'
OUT.mkdir(exist_ok=True);LOG.mkdir(exist_ok=True)
env=dict(os.environ,DISPLAY='127.0.0.1:101')
xvfb=os.environ.get('XVFB_BIN','Xvfb')
xterm=os.environ.get('XTERM_BIN','xterm')
args=[xvfb,':101','-screen','0','1600x1100x24','-nolock','-nolisten','unix','-listen','tcp','-ac']
for variable,flag in [('XKB_ROOT','-xkbdir'),('XFONT_ROOT','-fp')]:
 if os.environ.get(variable):args += [flag,os.environ[variable]]
x=subprocess.Popen(args,cwd=Path(xvfb).resolve().parent,env=env,stdout=open(LOG/'display.log','w'),stderr=subprocess.STDOUT)

def session(lines):
 return 'printf %s '+shlex.quote('\n'.join(lines)+'\n')+' | script -q -e -c ./myshell /dev/null'

stages=[
 ('01-environment','CURRENT RUN', 'uname -a; cat /etc/os-release; gcc --version | head -1; make --version | head -1; strace --version | head -1; git --version'),
 ('02-build','CURRENT RUN','make clean all'),
 ('03-prompt','CURRENT RUN',session(['echo OS-LAB1-started','exit'])),
 ('04-builtins','CURRENT RUN',session(['pwd','echo hello','echo $HOME','exit'])),
 ('05-external','CURRENT RUN',session(['ls -l src','whoami','uname -a','exit'])),
 ('06-cd','CURRENT RUN',session(['pwd',f'cd {ROOT}/tests/tmp','pwd','cd /not_exist','pwd','exit'])),
 ('07-files','CURRENT RUN',session(['touch tests/tmp/screenshot-demo.txt','echo data > tests/tmp/screenshot-demo.txt','cat tests/tmp/screenshot-demo.txt','rm tests/tmp/screenshot-demo.txt','cat tests/tmp/screenshot-demo.txt','echo alive','exit'])),
 ('08-redirection','CURRENT RUN',session(['echo hello > tests/tmp/screenshot-out.txt','echo world >> tests/tmp/screenshot-out.txt','cat < tests/tmp/screenshot-out.txt','cat tests/tmp/screenshot-out.txt','exit'])),
 ('09-pipe','CURRENT RUN',session(['ls | wc -l','printf hello | wc -c','cat tests/tmp/screenshot-out.txt | wc -w','exit'])),
 ('10-strace-history','HISTORICAL TRACE FILE VIEW - NOT A NEW TRACE',"grep -E 'chdir\\(|execve\\(\"/usr/bin/ls\"|out.txt.*O_|pipe2\\(' logs/strace.log; cat logs/strace_reaping.log"),
 ('11-git','CURRENT HISTORY VIEW','git log --oneline --reverse'),
 ('12-tests','CURRENT RUN - CHECK EXIT STATUS', 'make test > logs/screenshots_local/current-suite.log 2>&1; rc=$?; grep -c "^PASS$" logs/screenshots_local/current-suite.log; tail -9 logs/screenshots_local/current-suite.log; printf "make_test_exit=%s\\n" "$rc"; python3 tests/test_audit.py > logs/screenshots_local/additional.log 2>&1; ar=$?; tail -2 logs/screenshots_local/additional.log; python3 tests/test_trace_parser.py; test "$rc" = 0 && test "$ar" = 0'),
 ('13-strace-current','CURRENT RUN - PERMISSION CHECK','strace -f -o logs/screenshots_local/strace-probe.log /bin/true'),
 ('14-test-history','HISTORICAL FULL PASS FILE VIEW - NOT A NEW TEST','tail -7 logs/final_test.log; cat logs/verification_summary.log; sha256sum -c logs/artifact_hashes.log'),
]
results=[]
try:
 deadline=time.monotonic()+10
 while True:
  try:s=socket.create_connection(('127.0.0.1',6101),timeout=.2);s.close();break
  except OSError:
   if time.monotonic()>deadline:raise RuntimeError('X display not ready')
   time.sleep(.1)
 for name,label,command in stages:
  master,slave=pty.openpty()
  attrs=termios.tcgetattr(slave);attrs[3]&=~termios.ECHO;termios.tcsetattr(slave,termios.TCSANOW,attrs)
  term=subprocess.Popen([xterm,'-S'+os.ttyname(slave)+'/'+str(master),'-geometry','120x35+0+0','-fa','DejaVu Sans Mono','-fs','14','-bg','white','-fg','black','-title',name],env=env,pass_fds=(master,),stdout=open(LOG/(name+'.xterm.log'),'w'),stderr=subprocess.STDOUT)
  try:
   assert select.select([slave],[],[],10)[0], 'no xterm window acknowledgement'
   window=os.read(slave,256).decode().strip().splitlines()[0]
   int(window,16)
   # Print the executed command, then stream its real stdout/stderr through tee into the PTY.
   body='printf "%s\\n" '+shlex.quote('OS LAB 1 | Wang Xusheng | 24281204 | '+name)+'\n'
   body+='printf "%s\\n" '+shlex.quote(label)+'\ndate -u +%FT%TZ\n'
   body+='printf "%s\\n" '+shlex.quote('$ '+command)+'\n'
   body+='bash -c '+shlex.quote(command)+'\nrc=$?\nprintf "\\n[actual command status: %s]\\n" "$rc"\nexit "$rc"\n'
   (LOG/(name+'.sh')).write_text(body)
   pipe='bash '+shlex.quote(str(LOG/(name+'.sh')))+' 2>&1 | tee '+shlex.quote(str(LOG/(name+'.log')))+'; exit "${PIPESTATUS[0]}"'
   run=subprocess.run(['/bin/bash','-c',pipe],cwd=ROOT,env=env,stdin=slave,stdout=slave,stderr=slave,timeout=120)
   time.sleep(.2)
   subprocess.run(['import','-window','0x'+window,str(OUT/(name+'.png'))],env=env,check=True,timeout=10)
   results.append(dict(stage=name,label=label,exit=run.returncode,image=name+'.png'))
   print(name,run.returncode,flush=True)
  finally:
   term.terminate();term.wait(timeout=5);os.close(master);os.close(slave)
 (LOG/'manifest.json').write_text(json.dumps(results,indent=2)+'\n')
finally:
 x.terminate();x.wait(timeout=5)
