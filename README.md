# myshell：Linux 命令解释程序实验

依据上传的《实验课题1_Linux命令解释程序设计与实现》（2022 年 3 月修订）和本次教师补充要求实现。目的是理解命令解析、进程创建/替换/回收、环境变量及文件描述符。此项目为 **AI 协助开发的真实运行成果**，不能宣称学生独立编写。报告位于 `docs/report.pdf` 和 `docs/report.docx`，已填写上传模板中的个人信息，并以 Agent 的真实运行日志为证据。完整聊天导出仍待用户提供，详见 `docs/AGENT_DISCLOSURE.md`。

## 环境

Ubuntu 24.04.3 LTS；Linux 6.18.44；x86_64；gcc 13.3.0；GNU Make 4.3；strace 6.8；Git 2.51.1。详见 `logs/environment.log` 和 `logs/verification_environment.log`。自动化测试还需要 Python 3、util-linux 的 script、常见 GNU coreutils。

环境初始沙箱不提供 `/tmp`、`/proc`，且禁用 ptrace；最终综合测试与 strace 在获准的沙箱外环境执行，发行版、内核和工具版本一致。失败日志保留，没有假装沙箱内 strace 成功。

## 编译与启动

```bash
make
./myshell
make clean
```

使用 `-std=c11 -Wall -Wextra -Wpedantic -O2 -g`，最终清理重编译无 warning。在当前 Shell 内启动本程序即可完成“启用”测试，不需要 chsh 或替换系统登录 Shell。交互输入时显示 `[OS-LAB1] myshell$ `（输出到 stderr）；批处理时不显示提示符。

## 已实现基础功能

| 命令 | 本项目语义 | 主要接口 |
|---|---|---|
| cd [目录] | 主进程切换目录；无参数使用 HOME | chdir |
| pwd | 不接受参数，显示实际当前目录 | getcwd |
| echo [参数…] | 空格分隔并换行；`-n` 也是普通文本 | fputs/putchar，最终 write |
| cat [文件…] | 读取文件；无参数读取 stdin | open/read/write/close |
| touch 文件… | 创建空文件；已有文件不截断、不更新时间戳 | open/close |
| rm 文件… | 删除文件，不递归删目录 | unlink |
| exit | 无参数退出，状态 0 | 主循环标志 |

外部命令使用 `fork + execvp + waitpid`，不调用 `system`/`popen`。execvp 在命令名不含 `/` 时搜索 PATH，包含 `/` 时直接执行相应路径。HOME、PATH 继承启动环境；仅当不存在时初始化为 `/`、`/usr/bin:/bin`（空字符串不替换）。支持独立参数 `$HOME`、`$PATH` 展开，不做字段分割，因此包含空格的环境值仍是一个参数。没有 export 内部命令，可由启动它的 Bash 设置环境。

## 已实现扩展功能

- `>` 截断输出、`>>` 追加输出、`<` 输入重定向，支持内外部命令，操作符可不加空格。
- 每条命令最多一个输入、一个输出重定向；重复同类重定向报语法错误。
- 单个 `|`，两边可用内部或外部命令；先启动两端再等待。显式重定向覆盖该端的管道连接。
- 管道里的 cd/exit 只影响对应子进程。管道状态取右端状态，不提供 pipefail。
- 非法命令、文件错误、常见语法错误可报错后继续；参数数量、token 数量和行长设上限。

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

上述重定向真正修改命令 fd 0/1。`strace -o logs/strace.log` 是 **strace 自身日志输出选项**，测试程序的 `tee` 是 **测试日志采集**，都不是本 Shell 的重定向实现。

## 未实现功能与已知限制

不支持多级管道、通配符展开、引号、转义、带空格的字面路径、`;`、`&`、`&&`、`||`、脚本注释、命令替换、波浪号、`${HOME}`、其他变量展开、数字 fd 重定向、`2>`、历史记录、行编辑、后台作业、作业控制和完整信号管理。引号、反斜杠、`;`、`&` 被拒绝；`*`、`#`、未支持的变量写法为普通字符。`2>` 不按 stderr 重定向解释，请勿使用。

这不是 Bash 的替代品。不要依赖 Ctrl-C 保留本 Shell，会话也可能收到信号退出；无参数 cat 在批处理模式会消费后续输入直到 EOF。单命令最多 127 个 argv 项（含命令名），每行最多 256 个 token、65536 字节；getline 会先读入整行，再检查长度，不是固定内存防护。空行状态为 0；EOF 返回最近一次处理状态；exit 不接受状态码。测试目录路径必须不含空格。没有故障注入覆盖 OOM、fork 资源耗尽、恢复 dup2 失败等所有系统错误。

## 测试方法与实际结果

```bash
bash tests/verify.sh  # 一次执行编译、完整/分组测试及真实 strace
make test
bash tests/test_basic.sh
bash tests/test_redirect.sh
bash tests/test_pipe.sh
```

完整测试 `make test` 需要可访问的 `/proc` 和可用伪终端。阶段测试分别保存至 basic_test.log、redirect_test.log、pipe_test.log。最终结果：**69 个 subprocess 用例通过，额外 1 项伪终端提示符检查通过**；另有 4 个 strace 摘录解析回归样例通过（这些是解析器合成输入，不是额外 Shell 运行用例）。包括 cd/文件/未知命令异常、输出设备写满、10 万行管道、提前关闭读端、100 次管道/重定向后的父子 fd 检查。最终日志：`logs/final_test.log`。测试已编译的程序是真实 subprocess，不是模拟输出。

## strace 验证

```bash
bash tests/trace.sh
# 或在终端交互跟踪（先准备 test.txt）：
strace -f -o logs/strace.log ./myshell
# 可手工查看：
grep execve logs/strace.log
grep chdir logs/strace.log
grep openat logs/strace.log
grep read logs/strace.log
grep write logs/strace.log
grep dup2 logs/strace.log
grep pipe logs/strace.log
```

脚本使用相同的 `strace -f -o logs/strace.log ./myshell` 命令，以 `logs/strace_commands.txt` 供给可复现输入；工作文件写在 `tests/tmp/trace/`。`-f` 跟踪子进程；工具需要 ptrace 权限。原始日志和分组日志均保留，优先读 `logs/strace_key.log`，同时参见 `docs/evidence.md`。

## 主要设计

`lex` → `parse` → `run_line` 分辨单命令/管道；`builtin` 分发内部命令；`execute` 创建并替换外部进程；`redirect` 修改 fd；`run_command` 保存/恢复父进程 fd。Token 持有动态字符串，Command 借用 Token 文本，执行结束统一释放。父进程内执行 cd，管道内执行隔离的子进程 builtin。

C 接口名与内核跟踪名不必相同：本机 open 显示为 openat，fork 显示为 clone，pipe 显示为 pipe2，waitpid 显示为 wait4；execvp 的 PATH 搜索最终产生 execve。本项目直接调用系统调用的 C 包装接口（如 chdir/unlink/read/write），不是通过外部 cat/rm 代劳，也不要求手写汇编或 syscall(SYS_...)。

源码、测试、运行证据的对应表见 `docs/evidence.md`；12 个原理问题见 `docs/understanding.md`；原始失败和修复见 `docs/process.md`；截图清单见 `docs/screenshots.md`；验收见 `docs/acceptance.md`。

## Git 与报告

包内包含 `.git` 和可独立恢复的 `history.bundle`。用 `git log --oneline --reverse` 查看分阶段提交。身份标记为 AI-assisted，不代表学生身份。完整聊天记录仍需从本会话保存，过程摘要不冒充完整 Agent 交互导出。报告源码附录与当前源码对应；个人信息来自用户上传的模板。报告采用原始运行日志摘录，不声称包含学生个人终端截图。GitHub 发布尚待账号连接，详见 `docs/GITHUB_SUBMISSION.md`。

## 严格合规复查（2026-10-07 UTC）

详见 `docs/COMPLIANCE_AUDIT.md`。源代码和 Makefile 未改变；本次清理编译成功，原测试前68项通过，第69项因当前环境没有 /proc 而失败。独立复测 PTY 和新增18项语义测试通过，4个提取器回归通过；本次 ptrace 被禁止，未完成新的 strace 跟踪。历史完整成功日志保留，不把它们冒充本次结果。新增测试运行：`python3 tests/test_audit.py`。

**提交材料尚未齐全**：指导书规定的真实结果截图、完整 Agent 交互导出仍缺；若按 GitHub 方式提交，还缺实际仓库链接。教师允许 Agent 开发的说明并未明确取消截图要求。报告现有日志摘录不是截图。截图位置见 `docs/screenshots.md`，存放目录为 `docs/screenshots/`。现有17页报告记录上一轮验证，请与此次审查单一起阅读。

## 最新截图补充

已取得14张真实xterm终端窗口截图，见docs/screenshots/；已插入24页报告docs/report-with-screenshots.docx及同名PDF。请优先使用这份带图报告，原report.docx/pdf是保留的17页历史底稿。截图10、14标明查看历史成功日志，12、13保留本次/proc和ptrace限制，不能声称本次完整验证成功。完整聊天导出与仓库上传仍未完成。
