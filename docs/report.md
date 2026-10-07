# Linux 命令解释程序设计与实现

课程：操作系统；实验：一；学期：2026—2027 第一学期。
学院：网络空间安全学院；姓名：王旭升；学号：24281204；班级：保密2401。
编制日期：2026年10月2日（按用户当地日期）。

## 实验目的

理解 Linux 命令解释器如何读取、解析和执行命令，区分内部命令与外部命令；通过进程创建、程序替换、等待回收、环境变量和文件描述符操作，实现可实际编译运行的 Shell，并用测试代码、运行结果和 strace 建立证据链。
本项目按照教师允许的 Agent 开发方式完成。用户提供指导书与要求，Agent 在 Linux 中实际开发和测试。本报告不声称学生独立编写、已在 Mac 本机运行 Linux Shell，或已经完成个人终端截图。

## 实验任务

依据上传的《实验课题1_Linux命令解释程序设计与实现》（2022年3月修订）及教师补充要求，实现提示符、输入解析、五条以上内部命令、exec 系列执行外部程序、至少一个内部命令直接调用系统调用接口，以及 HOME/PATH 支持。
实际完成七条内部命令：cd、pwd、echo、cat、touch、rm、exit。扩展完成 I/O 重定向 >、>>、< 与单个管道 |。通配符、多级管道、引号转义、后台作业和完整作业控制未实现，不作为已支持功能申报。

## 开发运行与测试环境

实际验证环境为 Ubuntu 24.04.3 LTS、Linux 6.18.44、x86_64；gcc 13.3.0、GNU Make 4.3、strace 6.8、Git 2.51.1。测试还使用 Python 3、util-linux script 和 GNU coreutils。工具已存在，无需安装 gcc、make 或 strace。
最初的受限执行视图没有 /tmp、/proc，且 ptrace 被禁止；最终复验在允许这些能力的 Linux 环境执行。两种视图的版本信息与权限差异均留有记录。用户使用 Mac，但不是本项目的 Linux 测试平台，也没有通过未提供的 SSH 连接操作用户虚拟机。
编译命令为 make clean all，参数为 -std=c11 -Wall -Wextra -Wpedantic -O2 -g。最终编译成功且无 warning。运行 ./myshell 即完成启用测试，不替换系统登录 Shell。

## 实验步骤

第一阶段建立最小 Shell：交互提示符、getline、简单分词、exit、fork/execvp/waitpid。首次编译通过，ls、ls -l、whoami、uname -a、echo hello 等九项检查通过，PTY 中看到提示符。
第二阶段依次加入 cd、pwd、echo、cat、touch、rm。每加入一个内部命令，均重新编译、正常测试、异常测试和回归，并单独提交 Git。cd 最初因环境缺少 /tmp 测试失败，原日志保留，未伪造成功。
第三阶段验证 HOME/PATH 的继承、缺失初始化、整参数展开与自定义 PATH 搜索。累计三十三项通过。同时处理 stdio 与 read 混用的预读和刷新问题，增加 stdin 消费及输出顺序测试。
第四阶段加入输出截断、追加和输入重定向，验证真实文件内容、内外部命令、重定向失败后的恢复及 /dev/full 写入失败。累计四十八项通过。
第五阶段加入单管道，验证外部/内部命令组合、十万行数据、读端提前退出、管道中 cd/exit 的隔离语义。累计六十四项通过，未继续加入未经验证的额外功能。
最后使用真实 strace 跟踪并提取证据，加入边界、重复 fd 与 PTY 异常恢复测试。复查修复 wait4 提取器只识别 resumed 行的问题，增加四个解析回归样例，再运行 tests/verify.sh 完整复验。

## 关键数据结构与设计

Token 包含词文本和类型；Command 保存 argv、输入路径、输出路径和追加标志。Token 拥有动态字符串，Command 借用其地址；执行后统一 free_tokens。每命令最多127个 argv 项，每行最多256个 token、65536字节；行长检查在 getline 之后，不声称是固定内存防护。
主流程为 main → lex → parse/run_line → run_command 或 pipeline_child。交互提示符写入 stderr，批处理输入不显示提示符。lex 只展开独立参数 $HOME 和 $PATH，不做通配符或字段分割。
单命令由 run_command 保存必要 fd（带 CLOEXEC），redirect 使用 open/dup2/close 改变输入输出，execute 判断 builtin 或 fork/execvp。内部命令结束后 fflush，再恢复原描述符。普通 cd 在主进程执行，因为子进程 chdir 无法改变父 Shell 的当前目录。
管道由 pipe 返回读写两端，两次 fork 分别启动左右命令，左端接 stdout，右端接 stdin。显式重定向覆盖本端管道连接。父子进程均关闭不需要的端点，父进程等待两个孩子。必须先启动两端再等待，避免管道写满而死锁；保留额外写端则会阻止 EOF。
wait_child 对 EINTR 重试，并读取退出状态。普通未知命令返回127，其他 exec 失败返回126；管道取右端状态，不提供 pipefail。管道内 cd/exit 只影响对应子进程。

## 实验结果

本次 tests/verify.sh 实际完成清理编译、完整测试、分组测试和真实 strace，返回成功。69个 subprocess 用例与1项 PTY 检查通过；额外4个合成样例仅验证日志解析器，不算作额外 Shell 运行测试。详细结果见 logs/final_test.log。
基础33项、重定向15项、管道16项、健壮性5项。测试逐项打印输入、stdout、stderr、退出码并断言，不用预先编写的假输出替代运行。持续100次管道与重定向之后，父子 fd 均仅为0、1、2。
strace 跟踪中，cd /tmp 成功；外部 /usr/bin/ls 的 execve 成功；文件创建、读取、删除及重定向出现 openat/read/write/unlink/dup2；管道出现 pipe2/clone；五个代表性子进程均被 wait4 成功回收。完整原始日志与精简片段分别保存。
报告中的证据页是日志原文摘录，标明来源文件，不是个人终端截图。初始版本的成功证据复制在 logs/archive_initial/，更早失败日志与 Git 历史也保留。所有已声明功能均在 docs/evidence.md 中对应到代码、测试和证据。

## I/O 重定向与日志的区别

执行 echo hello > out.txt 时，Shell 解析 >，用 open(...O_TRUNC...) 打开目标，再用 dup2 将其接到 fd 1；命令写到 stdout 的内容真正进入 out.txt。>> 改用 O_APPEND，< 将目标接到 fd 0。这一语义由文件内容断言及 strace 双重验证。
strace -o logs/strace.log 只是指定 strace 自己的跟踪日志位置；测试脚本使用 tee 采集输出也只是测试日志。两者不能作为 Shell 已实现 I/O 重定向的证据，更不能在 README 中混称重定向功能。

## 讨论与问题处理

真实失败包括沙箱没有 /tmp、/proc 和禁止 ptrace。获准环境中完成了对应复验，但 /proc/PID/task/PID/children 接口仍不可用，因此改为 fd 检查与 strace 的 wait4 返回证据，不声称原检查通过。
日志提取曾把 PATH 搜索中失败的候选 execve 摘入结果，后要求成功 execve；修改时又出现正则 $ 未启用 MULTILINE 的误报，已修正并保留失败日志。进一步复查发现 wait4 可能完整打印或分段 resumed 打印，新解析器同时接受二者，拒绝未完成行与失败返回。
代码审查中，stdin 设置无缓冲以避免 getline 提前吞掉留给 cat/外部程序的数据；stdout 及时 fflush 以避免 puts 和 write 的输出顺序反转。备份 fd 设置 CLOEXEC，避免泄漏给外部程序。这些设计均有对应行为测试。
实际未遇到编译错误，不为营造开发过程而人为制造错误。当前测试没有覆盖全部资源耗尽、OOM、恢复 dup2 失败等情况，也不据此声称程序绝无 bug。

## 功能边界

cd 仅支持零或一个目录参数；pwd 不接受参数。echo 用空格连接参数并换行，-n 是普通文本。cat 无参数读取 stdin，在批处理下会消费后续输入直到 EOF。touch 只创建文件并保留已有数据，不更新时间戳；rm 不递归删除目录；exit 不接受状态码。
HOME/PATH 继承启动环境，缺失时分别初始化为 / 和 /usr/bin:/bin；空字符串不替换。支持独立 $HOME/$PATH，不支持 ${HOME} 等复杂写法。每命令最多一个输入和一个输出重定向，重复同类重定向报错。
不支持多级管道、通配符、引号、转义、含空格字面路径、分号、逻辑连接、命令替换、脚本注释、数字 fd 重定向、历史记录、后台运行或完整信号/作业控制。2> 不应当作 stderr 重定向使用；Ctrl-C 不保证保留本 Shell。

## 结论与提交说明

现有运行证据支持指导书基础要求和两个扩展功能（I/O 重定向、单管道）已实现并通过所列测试。可以使用本地项目或 Git 历史恢复源码，在具备 ptrace、/proc、伪终端的 Linux 中运行 bash tests/verify.sh 复现。
本报告说明设计原理和实际结果，不代替学生本人的理解或现场讲解。完整 AI/Agent 交互导出仍需从当前聊天界面取得，process.md 只是摘要。GitHub 远程发布尚待账号连接，没有虚构仓库 URL。代码和报告可交付，不等于上述提交附件已全部就绪。
