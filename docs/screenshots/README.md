# 14张真实终端截图

由Agent在Linux中启动Xvfb与xterm，连接真实PTY，执行tests/capture_local_terminal.py后直接截取窗口。没有把日志文字绘制成终端外观，没有使用生成式图片。截图中姓名为拼音Wang Xusheng，学号24281204。

01至09：本次实际环境、编译、提示符、内外部命令、cd、文件操作、I/O重定向和管道。
10：在终端查看历史成功strace原始文件，图片明确标注历史；不是本次新的跟踪。
11：截图当时的实际Git历史。
12：本次测试68项后因/proc不可见失败，18项追加测试与独立PTY、4项解析回归通过。
13：本次strace被ptrace权限拒绝的真实错误。
14：查看历史完整成功日志并验证当前源码/Makefile/二进制哈希；图片明确标注历史。

原始命令、输出与退出码见logs/screenshots_local/。14张已插入docs/report-with-screenshots.docx和同名PDF，第18至24页。原report.docx/pdf保留为17页历史底稿。
