# 指导书要求的截图清单（尚未补齐）

复查确认：指导书要求编译、运行和测试结果截图。教师允许 Agent 开发，但现有补充说明没有明确豁免截图；日志摘录不能直接替代截图。此前将本清单称为“可选”不够严格，现予纠正。请按本清单补齐真实截图，并将图片放在 docs/screenshots/，随后插入报告对应部分。这里建议截图。先在 **启动 myshell 的 Bash 终端** 输入下列信息，将方括号内容替换为本人真实值，不要在系统配置里修改用户名：

```bash
printf '操作系统实验1 | 姓名：[填写] | 学号：[填写]\n'
```

然后依次保留这些真实终端截图：

1. uname -a、cat /etc/os-release、gcc --version、make --version、strace --version。
2. make clean all 编译命令与成功结果。
3. ./myshell 启动后的 [OS-LAB1] 提示符。
4. pwd、echo、exit 等内部命令。
5. ls -l、whoami、uname -a 外部命令。
6. pwd → cd /tmp → pwd（本人的 Linux 确认 /tmp 存在）。
7. touch demo.txt → echo data > demo.txt → cat demo.txt → rm demo.txt。
8. echo hello > out.txt → echo world >> out.txt → cat < out.txt。
9. ls | wc -l、printf hello | wc -c。
10. bash tests/trace.sh 与 cat logs/strace_key.log。
11. git log --oneline --reverse。
12. make test 的最终 PASS 和异常恢复测试。

不要将本文档或程序生成的排版图冒充终端原生截图。当前包内保存了真实文字日志与 PTY 转录，尚未含用户本人姓名学号的原生终端截图。完整 AI/Agent 交互记录请另行保存当前聊天。

## 最新截图补充

已取得14张真实xterm终端窗口截图，见docs/screenshots/；已插入24页报告docs/report-with-screenshots.docx及同名PDF。请优先使用这份带图报告，原report.docx/pdf是保留的17页历史底稿。截图10、14标明查看历史成功日志，12、13保留本次/proc和ptrace限制，不能声称本次完整验证成功。完整聊天导出与仓库上传仍未完成。
