# myshell：Linux 命令解释程序设计与实现

《操作系统》实验课题1。姓名：王旭升；学号：24281204；班级：保密2401。

依据实验指导书（2022年3月修订）及教师补充要求，实现命令解析、内部命令、外部程序执行、环境变量、I/O重定向和单级管道，理解进程与文件描述符的工作方式。

我采用 **Agent 协助开发**：由 Agent 协助编写代码、执行测试和整理材料，我负责上传仓库并提供 GitHub Actions 运行产物。我的原理总结见[理解与体会](docs/personal-understanding.md)，重点是父子进程、文件描述符、重定向与管道，以及如何用测试和 strace 验证实现。

## 当前提交状态

- 仓库：<https://github.com/wwwfirstsleep/os-2026-lab>
- 最新报告：[PDF，26页](docs/report-final.pdf)；[可编辑Word](docs/report-final.docx)。第25页为理解与体会，第26页记录后续 GitHub 成功复验。
- GitHub 复验：12个截图阶段退出码均为0；69项命令用例与PTY检查、18项追加用例与PTY检查、4项日志解析回归均有成功记录；真实 strace 已执行。
- [GitHub运行产物](evidence/github-20261007/)已归档。原开发环境中的失败日志继续保留，不能将它们与后续成功复验混为同一次运行。
- [交互材料](docs/agent-interaction/)已附用户提供的Word与补充TXT，但存在中间对话缺失，**不是完整会话记录**。这一材料缺项尚未消除。

旧报告和审查文档记录各阶段状态；当前状态以上述26页报告及本README为准。

## 开发与验证环境

| 项目 | 初始开发环境 | 后续GitHub复验环境 |
|---|---|---|
| 发行版 | Ubuntu 24.04.3 LTS | Ubuntu 24.04.5 LTS |
| Linux内核 | 6.18.44 | 6.17.0-1022-azure |
| CPU架构 | x86_64 | x86_64 |
| gcc | 13.3.0 | 13.3.0 |
| GNU Make | 4.3 | 4.3 |
| strace | 6.8 | 6.8 |
| Git | 2.51.1 | 2.55.0 |

环境证据：[初始环境](logs/environment.log)、[GitHub环境](evidence/github-20261007/logs/verification_environment.log)。

用户使用Mac，但本项目的运行证据来自Linux，不能将其描述为macOS原生运行结果。完整测试另需Python 3、util-linux的`script`、常见GNU coreutils、可访问的`/proc`及PTY；strace需要ptrace权限。截图工作流另需Xvfb、xterm和ImageMagick，这些不是编译Shell的依赖。

开发阶段曾因执行环境缺少`/tmp`、`/proc`或禁止ptrace而失败，获准环境中的历史验证及后续GitHub完整复验均另有成功证据。失败与成功记录分别保留。

## 编译与运行

在Linux中进入仓库根目录：

```bash
make
./myshell
```

清理重新编译与删除生成程序：

```bash
make clean all
make clean
```

编译参数为`-std=c11 -Wall -Wextra -Wpedantic -O2 -g`。已归档的GitHub清理编译无错误、无warning：[编译日志](evidence/github-20261007/logs/final_build.log)。

运行`./myshell`即可进行启用测试，无需替换系统登录Shell。交互输入显示`[OS-LAB1] myshell$ `，提示符写入stderr；批处理时不显示提示符。

## 已实现基础功能

| 内部命令 | 本项目支持的语义 | 主要接口 |
|---|---|---|
| `cd [目录]` | 主进程切换目录；无参数使用HOME | chdir |
| `pwd` | 显示实际当前目录；不接受参数 | getcwd |
| `echo [参数…]` | 空格分隔并换行；`-n`作为普通文本 | fputs/putchar，最终write |
| `cat [文件…]` | 读取一个或多个文件；无参数读取stdin | open/read/write/close |
| `touch 文件…` | 创建空文件；已有文件不截断、不更新时间戳 | open/close |
| `rm 文件…` | 删除文件，不递归删除目录 | unlink |
| `exit` | 无参数退出，状态0 | 主循环退出标志 |

外部命令通过`fork + execvp + waitpid`执行，没有调用`system`或`popen`。命令名不含`/`时，execvp按PATH搜索；包含`/`时直接使用指定路径。

HOME和PATH继承启动环境；只有不存在时才分别初始化为`/`与`/usr/bin:/bin`，空字符串不替换。支持独立参数`$HOME`、`$PATH`展开，不做字段分割，环境值包含空格时仍为一个参数。没有export内部命令，可由启动本程序的Bash设置环境。

## 已实现扩展功能

- `>`截断输出、`>>`追加输出、`<`输入重定向，支持内外部命令，操作符可不加空格。
- 每条命令最多一个输入和一个输出重定向；重复同类重定向报语法错误。
- 单个`|`，两端可为内部或外部命令；先启动两端再等待。显式重定向覆盖对应端的管道连接。
- 管道内的cd/exit只影响对应子进程。管道状态取右端状态，不提供pipefail。
- 已测试的非法命令、文件错误和常见语法错误会报错后继续；参数数量、token数量及行长有上限检查。

在本Shell中可执行：

```text
echo $HOME
echo $PATH
touch demo.txt
echo hello > demo.txt
echo world >> demo.txt
cat < demo.txt
cat demo.txt | wc -w
printf hello | wc -c
rm demo.txt
exit
```

I/O重定向实际使用open、dup2、close修改命令的fd 0/1，输出文件内容有断言测试。`strace -o logs/strace.log`指定的是strace自身日志位置，`tee`用于采集测试日志；两者都不能代替本Shell的I/O重定向实现。

## 测试方法与结果

```bash
bash tests/verify.sh
python3 tests/test_audit.py
```

`verify.sh`执行清理编译、完整及分组测试和真实strace。18项追加测试由第二条命令单独运行。也可分别执行：

```bash
make test
bash tests/test_basic.sh
bash tests/test_redirect.sh
bash tests/test_pipe.sh
```

这些命令需要前述Linux环境能力。部分脚本会重写根目录`logs/`中的当前结果；归档的GitHub产物位于`evidence/github-20261007/`，应保留作为本次运行底稿。

| 验证内容 | 已核验结果 | GitHub归档证据 |
|---|---|---|
| 完整命令测试 | 69项通过，另有PTY提示符与异常恢复检查 | [final_test.log](evidence/github-20261007/logs/final_test.log) |
| 追加语义测试 | 18项通过，另有PTY检查 | [additional.log](evidence/github-20261007/logs/screenshots/additional.log) |
| strace解析器 | 4项合成输入回归通过，不计为额外Shell运行用例 | [final_test.log](evidence/github-20261007/logs/final_test.log)末尾 |
| 完整复验脚本 | 成功 | [verification_summary.log](evidence/github-20261007/logs/verification_summary.log) |
| 子进程回收 | 代表性跟踪中5个创建的子进程均被回收 | [strace_reaping.log](evidence/github-20261007/logs/strace_reaping.log) |
| 截图采集阶段 | 清单列出的12个阶段退出码均为0 | [manifest.json](evidence/github-20261007/logs/screenshots/manifest.json) |

覆盖内容包括指定的cd/cat/rm/未知命令异常、真实文件内容、输出设备写满、10万行管道、读端提前退出、100轮管道/重定向后的fd检查，以及多文件操作、空环境变量、含空格的HOME等。测试通过只代表已测试的范围，不表示任意输入或资源耗尽场景都无问题。

## strace验证与截图来源

```bash
bash tests/trace.sh
```

或准备好输入文件后，交互执行：

```bash
strace -f -o logs/strace.log ./myshell
```

`-f`跟踪子进程。归档中的[完整strace](evidence/github-20261007/logs/strace.log)、[关键摘录](evidence/github-20261007/logs/strace_key.log)和[读写摘录](evidence/github-20261007/logs/strace_read_write.log)可用于核对chdir、execve、openat、read、write、dup2、pipe2、clone及wait4等调用。

GitHub截图流程先运行一次trace.sh，随后verify.sh再次跟踪；第10张截图对应第一轮主PID3281，最终归档strace.log对应第二轮主PID3774。第一轮输出保存在[trace-run.log](evidence/github-20261007/logs/screenshots/trace-run.log)，不要混用两轮PID。

[GitHub截图目录](evidence/github-20261007/docs/screenshots/)同时包含仓库原有图片，本次新生成的12张以manifest.json为准。第10张图底部有截断，完整结论依据原始日志及退出码，不能仅凭截图判断。原Agent环境的14张终端截图在[docs/screenshots](docs/screenshots/)，其中历史日志查看与当时的权限失败已明确标注。

## 主要设计思路

`main`读取输入，`lex`产生Token，`parse`生成Command，`run_line`选择单命令或管道；`builtin`分发内部命令，`execute`处理外部程序，`redirect`修改fd，`run_command`保存与恢复父进程fd。

Token持有动态字符串，Command借用文本，执行完成统一释放。普通cd必须在主进程执行，因为子进程chdir不能改变父Shell目录；管道中的cd在隔离子进程中执行。

父进程等待外部命令，waitpid遇EINTR重试。管道两端并发启动，父子进程关闭不用的端点，避免阻止EOF或产生大输出死锁。stdin禁用stdio预读；stdout在适当时机刷新，避免缓冲数据在fd恢复后才写出。备份fd带CLOEXEC，防止泄漏给外部程序。

C接口名与内核跟踪名不必相同：本次open显示为openat，fork为clone，pipe为pipe2，waitpid为wait4，execvp的PATH搜索最终进入execve。内部cat/cd/rm等直接使用系统调用的C接口，不是启动外部工具代劳。

## 未实现功能与已知限制

不支持多级管道、通配符展开、引号、转义、含空格的字面路径、`;`、`&`、`&&`、`||`、脚本注释、命令替换、波浪号、`${HOME}`、其他变量展开、数字fd重定向、`2>`、历史记录、行编辑、后台作业、作业控制和完整信号管理。

引号、反斜杠、`;`、`&`被拒绝；`*`、`#`和未支持的变量写法为普通字符。`2>`不按stderr重定向解释。不要依赖Ctrl-C保留本Shell；无参数cat在批处理时会消费后续输入直到EOF。

单命令最多127个argv项（含命令名），每行最多256个token、65536字节；getline先读整行再检查长度，不是固定内存防护。空行状态为0；EOF返回最近一次处理状态；exit不接受退出码参数。测试目录路径必须不含空格。未故障注入覆盖OOM、fork资源耗尽及恢复dup2失败等全部系统错误。

## Git历史与材料说明

当前仓库采用网页上传，GitHub提交列表主要反映上传过程。原Agent分阶段开发历史保存在[history.bundle](history.bundle)，不是由网页上传自动导入的提交图；不要把两者混称。需要查看原始历史时，可在有Git的环境执行：

```bash
git clone history.bundle restored-myshell
git -C restored-myshell log --oneline --reverse
```

bundle保存的是归档时的开发版本，不一定包含此后单独上传的最新版报告和证据；当前提交材料以本仓库文件为准。

[功能与证据映射](docs/evidence.md)、[原理说明](docs/understanding.md)、[开发过程摘要](docs/process.md)供理解和追溯使用。报告给出技术解释，但不能代替学生本人的理解与讲解。交互Word及补充TXT是已保存的部分记录，过程摘要也不能冒充完整聊天导出。
