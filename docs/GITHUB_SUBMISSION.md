# GitHub 提交状态

本地项目已准备好用于创建 GitHub 仓库，保留真实开发历史。建议仓库名：os-lab1-myshell。
用户现已指定仓库：https://github.com/wwwfirstsleep/os-2026-lab 。实际只读克隆确认仓库为空；写入预检查因缺少身份认证失败，尚未推送。仓库链接已取得，但实验内容还不在远程仓库。

连接 GitHub 之后可创建仓库并推送既有提交。仓库可见性、仓库所属账号和教师访问方式应在发布时确认；不可把一个未发布的本地路径当作 GitHub 链接提交。

建议提交材料：
1. docs/report.pdf 或 docs/report.docx（Agent 实际验证版报告）；
2. 整个源码仓库（src、Makefile、tests、logs、docs、README）；
3. docs/agent-interaction/ 中的完整会话导出（目前待用户提供）；
4. 仓库链接和教师可用的访问权限。

复现入口：在支持 ptrace、/proc 和伪终端的 Linux 主机执行 bash tests/verify.sh。
验证会重写 logs/ 下当前结果；本次初始结果已在 logs/archive_initial/ 保留，Git 也保存更早版本。
