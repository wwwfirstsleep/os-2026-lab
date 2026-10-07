from pathlib import Path
import re
root = Path(__file__).resolve().parents[1]
text = (root/'logs/strace.log').read_text()
# strace can show a wait4 as one line or split entry/resume lines.
reap_pattern = r'wait4(?:\(|.*resumed>).*?= ([1-9][0-9]*)$'
groups = {
    'exec': r'\bexecve\(', 'cd_pwd': r'\b(chdir|getcwd)\(',
    'files': r'\b(open|openat|unlink)\(',
    'redirect': r'\b(dup2|fcntl|close)\(|out\.txt',
    'pipe': r'\b(pipe|pipe2|clone|fork|vfork|wait4|waitid|dup2)\(',
    'read_write': r'\b(read|write)\(',
}
for name, pattern in groups.items():
    lines = [line for line in text.splitlines() if re.search(pattern, line)]
    assert lines, name
    (root/f'logs/strace_{name}.log').write_text('\n'.join(lines)+'\n')
required = [r'chdir\("/tmp"\)\s+= 0', r'execve\("[^"\n]*/ls".*= 0$', r'\b(pipe|pipe2)\(', r'\bdup2\(', r'\b(open|openat)\(', r'\bread\(', r'\bwrite\(', r'\bunlink\(', r'\b(clone|fork|vfork)\(', r'\bwait4\(']
for pattern in required:
    assert re.search(pattern, text, re.MULTILINE), pattern
# Small annotated excerpt retains original PID and full syscall lines.
selected = []
for label, pattern in [('cd',r'chdir\("/tmp"'),('pwd',r'getcwd\('),('touch/cat',r'openat.*test.txt'),('rm',r'unlink\('),('external',r'execve\("[^"\n]*/ls".*= 0$'),('redirection open',r'openat.*out.txt'),('redirection dup2',r'\bdup2\('),('read',r'read\(0, "hello'),('write',r'write\(1, "hello'),('pipe',r'\bpipe2?\('),('fork wrapper',r'\bclone\('),('reaping',reap_pattern)]:
    matches=[l for l in text.splitlines() if re.search(pattern,l)]
    assert matches, label
    selected.append('## '+label+'\n'+'\n'.join(matches[:3]))
(root/'logs/strace_key.log').write_text('\n\n'.join(selected)+'\n')
(root/'logs/strace_check.log').write_text('PASS: required syscall families and successful cd /tmp observed\n')
print((root/'logs/strace_key.log').read_text())

reaped = [l for l in text.splitlines() if re.search(reap_pattern, l)]
reaped_pids = {re.search(reap_pattern, line).group(1) for line in reaped}
assert len(reaped_pids) == 5, reaped
(root/'logs/strace_reaping.log').write_text('\n'.join(reaped)+'\nPASS: all 5 representative child processes reaped\n')
