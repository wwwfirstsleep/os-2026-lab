# 十二个原理问题（结合本实现）

1. **为什么 fork + exec？** fork 保留一个继续解释命令的父进程，同时创建子进程。execvp 把子进程替换成外部命令。若主 Shell 自己 exec 成功，它就不再是解释器。
2. **父子分别做什么？** execute 中子进程 execvp，失败 perror 后 _exit；父进程 wait_child 等待。管道中两个子进程分别读写，父进程关闭端点并等待两者。
3. **为什么 cd 在父进程？** 当前目录是进程属性。fork 后子进程继承目录，但 chdir 只更改调用进程；不能反向更改父进程。run_command 中 builtin 在父进程执行。管道中的 cd 则按隔离语义在子进程执行，已专门测试。
4. **exec 为什么成功不返回？** 内核用新可执行文件重建进程地址空间并进入新程序入口，PID 保持；原调用点不再存在。只有加载失败才返回 -1，因此 perror/_exit 放在 execvp 之后。
5. **PATH 做什么？** 是可执行文件目录列表。execvp 用无斜杠的命令名逐目录尝试，最终调用 execve；strace 中先出现若干 ENOENT 再出现 /usr/bin/ls 成功，是搜索过程，不等于命令失败。
6. **0/1/2 是什么？** 约定的 stdin/stdout/stderr 文件描述符，是进程描述符表的索引，不是固定文件。提示符走 fd 2，使 fd 1 的命令输出可重定向。FILE * stdout 是 C 库缓冲对象，与内核 fd 1 不同。
7. **open + dup2 为什么实现 >？** open 用 O_WRONLY|O_CREAT|O_TRUNC 创建/截断文件，dup2(fd,1) 让 fd 1 指向它。后续 write(1,...) 就进入文件。追加换成 O_APPEND。执行 builtin 前保存 fd，fflush 后恢复，避免输出在恢复后才被缓冲库写出。
8. **管道为何两个 fd？** pipe 返回读端和写端；数据从写端进入内核缓冲，从读端取出。左子进程把写端复制到 1，右子进程把读端复制到 0。
9. **为何关闭不用的端？** 只有所有写端关闭，读者才看见 EOF；多余读端会影响 SIGPIPE/EPIPE。父进程不传输数据，应关闭两端；子进程 dup2 后关闭原端点。要先启动两端再 wait，避免管道写满而无人读取。
10. **strace 如何看到调用？** 它利用 Linux ptrace 跟踪机制观察调用进入、返回和参数。-f 跟踪新子进程。沙箱可能禁止 ptrace，所以安装成功不等于能跟踪；本次先失败，再在获准环境中实际成功。
11. **C 库和系统调用什么关系？** puts/fputs 可先缓冲，最终经 write 写入内核；open/read/write/chdir/unlink 是系统调用的用户态 C 接口。glibc 可选择 openat/clone/pipe2/wait4 等内核入口，因此不能只按 C 函数同名搜索。至少 cat/rm/cd 明确直接使用这些接口，不是借助 system 启动外部工具。
12. **waitpid 为什么重要？** 读取退出状态并回收子进程内核记录，避免僵尸。wait_child 在 EINTR 时重试，run_line 对左右子进程均等待。右端决定管道状态；左端可能因读者提前关闭收到 SIGPIPE，这是管道机制的一部分。

补充：stdin 设置无缓冲，避免 getline 预读吞掉原本留给 cat 或外部程序的输入；每条内部命令输出及时 fflush，避免 puts 与 write 混用时顺序反转；备份 fd 设置 CLOEXEC，防止外部程序继承它们。
