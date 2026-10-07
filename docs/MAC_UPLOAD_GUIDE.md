# Mac 手动上传与运行截图步骤

当前状态：Shell代码和历史运行证据齐全；本地已实际截取14张终端图并插入report-with-screenshots报告；GitHub工作流仍未执行；完整Agent聊天导出仍未加入。不要将此包描述为所有附件都已完成。

## 1 下载并解压

下载 os-2026-lab-manual-upload.zip，双击解压，打开 os-2026-lab-upload 文件夹。其内直接包含 src、tests、logs、docs、Makefile、README.md、history.bundle。

## 2 上传项目文件

用Safari或Chrome登录自己的GitHub，打开 https://github.com/wwwfirstsleep/os-2026-lab 。

空仓库首页点击 uploading an existing file；如果已经有文件，点击 Add file → Upload files。

第一批：把 src、tests、docs 三个文件夹及 Makefile、README.md、history.bundle 拖进网页上传区。注意拖的是这些内容，不是外层 os-2026-lab-upload 文件夹，也不是ZIP压缩包。等待文件加载完，点击 Commit changes（提交说明可写 Upload lab source reports and history bundle）。

日志需分批上传：先在仓库根目录用 Add file → Create new file 创建 logs/README-upload.md（写“实验原始日志”后提交），然后进入仓库的 logs 目录。点击 Add file → Upload files，先选择本地 logs 中直接可见的普通文件（不含子文件夹），提交；再分次上传 archive_initial、audit_20261007、screenshots_local 子文件夹，每次只拖一个子文件夹。一次不要超过100个文件。

上传后，首页应该直接出现 Makefile、README.md、src/、tests/、docs/、logs/ 和 history.bundle；不应多套一层 os-2026-lab-upload/。

网页上传不会导入本地.git提交图，原来的分阶段历史保存在history.bundle中。需要恢复时执行 git clone history.bundle restored-myshell；logs/git_history.log提供可直接阅读的历史清单。不能把网页上传生成的几次提交说成原始开发历史。若要远程也呈现完整提交图，需另用Git客户端推送；这不是本网页上传路径的结果。

## 3 可选 在GitHub重新采集截图（现有14张已在报告）

以下步骤3至5仅在你想补充另一环境的完整复验时执行；已有本地截图不需要等待GitHub。

添加截图工作流

Mac的Finder默认不显示 .github 文件夹，因此用网页创建文件更直接。

回到仓库根目录 → Add file → Create new file。
文件名框准确填写：.github/workflows/capture-evidence.yml
打开随包的 capture-evidence.yml.txt（Finder右键→打开方式→文本编辑），Command+A、Command+C，回到网页代码编辑区粘贴全部内容。不要粘贴Markdown代码围栏。
点击 Commit changes，提交到默认分支 main。如果你的默认分支名字不同，使用其实际名字。

## 4 在GitHub的Linux环境运行

点击仓库上方 Actions。
左侧选择 Capture real Linux terminal evidence。
点击 Run workflow，选择默认分支，再点绿色 Run workflow。
若页面要求启用Actions，按仓库页面提示启用；若运行受到账号/组织政策限制，保留实际错误，不视为通过。

等待运行结束。打开本次运行，查看各步骤。绿色仅表示流程退出成功，仍需检查实际截图是否清晰完整；红色表示流程有失败，请保留错误日志，不标记全部通过。

## 5 下载真实截图与日志

进入本次运行详情，下方 Artifacts 区域点击 linux-terminal-evidence 下载。
截图应在 docs/screenshots/ 下，共12张；logs/screenshots/保存原始输出和每阶段退出码。
若流程失败，仍可能有部分截图与日志可供排查；它们不等于完整验收成功。

将下载的整个artifact压缩包上传到当前对话，我会检查结果、修复需要调整的地方，并将合格的真实截图插入报告，重新输出Word/PDF。现在包里的report-with-screenshots.docx/pdf已经插入本地14张截图。

## 6 最终提交

优先提交仓库中的 docs/report-with-screenshots.docx 或同名PDF；将完整会话导出放入 docs/agent-interaction/。最后提交仓库链接，并确认老师能够访问。

截图流程在GitHub运行器中执行，不是在你的Mac本机执行；报告环境应按新日志记录，不能把GitHub运行器截图归为旧Linux环境。

官方操作文档：
https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository
https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow
https://docs.github.com/en/actions/how-tos/manage-workflow-runs/download-workflow-artifacts

## 最新截图补充

已取得14张真实xterm终端窗口截图，见docs/screenshots/；已插入24页报告docs/report-with-screenshots.docx及同名PDF。请优先使用这份带图报告，原report.docx/pdf是保留的17页历史底稿。截图10、14标明查看历史成功日志，12、13保留本次/proc和ptrace限制，不能声称本次完整验证成功。完整聊天导出与仓库上传仍未完成。
