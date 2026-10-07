报告使用 Noto Sans SC（SIL Open Font License 1.1），字体及许可证下载自：
https://github.com/googlefonts/noto-cjk/tree/main/Sans

LabReportSans.ttf 是为当前报告文本裁剪、固定字重 400 的子集；字体嵌入 PDF，读者不必安装字体。仅用于报告，不影响 Shell 的编译和运行。
若修改报告加入当前子集没有的新汉字（例如个人姓名），请将此字体替换为覆盖相应字符的完整 TrueType 中文字体，再运行 docs/build_report.py，或在自己的文字处理器中使用 report.md 编辑排版。
PDF 再生成额外需要 Python reportlab；Shell 编译不需要这些文档依赖。
