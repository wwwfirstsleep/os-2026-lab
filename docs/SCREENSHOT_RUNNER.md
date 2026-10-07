# 真实截图运行流程（已准备，尚未执行）

用户指定目标仓库：https://github.com/wwwfirstsleep/os-2026-lab 。本次git clone成功，返回空仓库；git push --dry-run因没有GitHub认证而失败，没有上传文件。

已准备 .github/workflows/capture-evidence.yml：手动触发，在Ubuntu运行器安装编译、strace、Xvfb、xterm和截图工具，执行tests/capture_terminal.py。脚本将实际命令输出到xterm，再截取X显示画面，不将旧日志渲染成伪终端截图。12张图片含环境、编译、提示符、内外部命令、cd、文件操作、重定向、管道、strace、Git、综合测试；同时保存真实输出和退出码。

当前仅通过Python编译与12组Bash语法检查；没有声称工作流已经执行、图片已经生成或报告已经插图。实际运行后须检查图像没有截断、测试均通过，再由Agent插入报告并渲染检查。若运行失败，artifact仍保留失败证据，不能申报成功。

下一步需要GitHub认证且具备该仓库写入及Actions执行权限。用户不要把token或密码直接发到聊天。得到授权连接后，推送真实Git历史和此工作流，手动运行，下载linux-terminal-evidence artifact；随后完成报告插图。若连接权限不包含工作流操作，需要对应可用权限或用户在仓库Actions页执行一次。

此流程是待验证的采集工具，不属于已经实现/测试通过的Shell功能，也不改变之前的实验测试计数。源码及Makefile未修改。

## 最新截图补充

已取得14张真实xterm终端窗口截图，见docs/screenshots/；已插入24页报告docs/report-with-screenshots.docx及同名PDF。请优先使用这份带图报告，原report.docx/pdf是保留的17页历史底稿。截图10、14标明查看历史成功日志，12、13保留本次/proc和ptrace限制，不能声称本次完整验证成功。完整聊天导出与仓库上传仍未完成。
