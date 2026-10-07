# 用户提供的GitHub Actions运行产物

原始来源：用户上传os1.zip内linux-terminal-evidence.zip。截图显示运行时间2026-10-07 04:59 UTC。
logs/screenshots/manifest.json列出本次生成的12张截图，退出码均为0。产物还带有4张旧图片，来自仓库已有文件；未把它们算成本次12张新截图。
核验：69项完整用例+PTY、18项追加用例+PTY及4项解析回归均成功；实际strace创建PID集合与回收集合均为3775至3779。
截图10-strace底部有截断，判断成功依据其.exit文件和完整原始日志，不声称该截图显示了全部输出。截图10使用第一轮跟踪PID3281，完整strace.log被随后verify.sh再次生成、主PID3774；第一轮对应logs/screenshots/trace-run.log，两轮不要混用PID。
已读取指定GitHub仓库当前源码；src/myshell.c、Makefile、tests/run_tests.py、tests/test_audit.py与本地版本字节一致。这是当前仓库比较，不冒充运行时源文件哈希（产物未包含artifact_hashes.log）。
