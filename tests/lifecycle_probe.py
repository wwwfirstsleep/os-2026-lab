import os
fds = []
for name in os.listdir('/proc/self/fd'):
    try:
        os.fstat(int(name))
        fds.append(int(name))
    except OSError:
        pass
assert sorted(fds) == [0, 1, 2], fds
parent = os.getppid()
parent_fds = sorted(int(n) for n in os.listdir(f'/proc/{parent}/fd'))
assert parent_fds == [0, 1, 2], parent_fds
print('FD_OK')
