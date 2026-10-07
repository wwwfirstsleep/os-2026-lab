# 功能 → 代码 → 命令 → 结果 → 证据

所有源码均在 src/myshell.c。下列测试名可在 tests/run_tests.py 与日志中查找；日志保留真实 stdout、stderr、退出码和断言 PASS。原始跟踪包含 PID，可区分 Shell 主进程与子进程。

| 功能 | 代码函数 | 测试命令/用例 | 已观察结果 | 证据 |
|---|---|---|---|---|
| 编译、启动 | main / Makefile | make clean all、PTY | 无 warning；7 次提示符 | final_build.log；final_test.log 末尾 |
| 提示符与异常恢复 | main | cd /not_exist、cat/rm not_exist.txt、unknown_command | 报错后再次显示提示符并输出 alive | final_test.log：PTY TRANSCRIPT |
| 参数解析/边界 | lex / parse | 参数超限、token 超限、超长行、缺失目标 | parse 错误后继续 | final_test.log |
| cd 主进程 | builtin | pwd、cd /tmp、pwd | 实际 /tmp；同 PID chdir 和 getcwd | strace_stdout.log；strace_cd_pwd.log |
| cd HOME | builtin / main | cd、pwd（指定 HOME） | 指定目录 | basic_test.log：HOME PATH expansion |
| pwd | builtin | pwd、pwd extra | 真实路径；参数错误 | basic_test.log；strace_cd_pwd.log |
| echo | builtin | echo one two、空 echo、参数超限 | one two、空行、拒绝超限 | basic_test.log；strace_read_write.log |
| cat 文件/stdin | builtin | cat 文件、cat < out.txt | 内容一致；read/write | basic_test.log；redirect_test.log；strace_files/read_write.log |
| touch | builtin | touch new.txt / 已有文件 | 空文件产生；旧数据保留 | basic_test.log；strace_files.log |
| rm | builtin | rm remove.txt / 不存在文件 | 文件消失；合理错误 | basic_test.log；strace_files.log 的 unlink |
| exit | builtin | exit、exit bad、exit 管道 | 正常退出；错误后继续；管道不退出父 Shell | basic_test.log；pipe_test.log |
| HOME/PATH 初始化与展开 | main / lex | echo $HOME、echo $PATH | 与传入环境一致；缺失时默认值 | basic_test.log：environment defaults |
| PATH 查找与外部命令 | execute | ls -l、whoami、uname -a、lab-probe | 输出正确；自定义 PATH 成功 | basic_test.log；strace_exec.log 成功 execve |
| > | redirect / run_command | echo hello > out.txt | 文件真实出现，内容 hello 换行 | redirect_test.log；strace_key.log O_TRUNC/dup2/write |
| >> | redirect | echo world >> out.txt | 保留前文并追加 | redirect_test.log；strace_key.log O_APPEND |
| < | redirect | cat < out.txt | hello 和 world | redirect_test.log；strace_key.log openat/read |
| 单管道 | run_line / pipeline_child | printf hello \| wc -c | 5 | pipe_test.log；strace_pipe.log |
| 内部命令管道 | pipeline_child | echo hello \| cat | hello | pipe_test.log |
| 重定向与管道组合 | redirect / pipeline_child | cat < pipe-input \| wc -w > words.txt | 文件中为 2 | pipe_test.log |
| 大数据/提前关闭 | run_line | seq 1 100000 \| wc -l；yes \| head -n 1 | 100000；y；未超时 | pipe_test.log |
| fd 与进程回收 | run_command / wait_child | 100 轮管道与重定向 | 父子仅 fd 0/1/2；代表性跟踪子进程均 wait4 回收 | final_test.log：FD_OK；strace_reaping.log |

日志路径均以 logs/ 为前缀。strace_key.log 是少量关键原始行；分组文件更全面；strace.log 是完整底稿。测试结果不等于覆盖所有硬件、内核、资源耗尽场景。

## 后续补充验证

`tests/test_audit.py` 的18项用例补查多文件cat/touch/rm、cat遇错后继续、含空格HOME作为一个参数、空HOME/PATH保留、管道右侧输入覆盖、重复输入拒绝、外部追加、exec权限错误126、未支持语法与字面变量、EOF/空行状态；结果见 `logs/audit_20261007/additional_test.log`，包含输入、输出、退出码、PASS及独立PTY转录。该文件是本次追加测试，不应将18项直接加入上一轮69项的历史计数。
