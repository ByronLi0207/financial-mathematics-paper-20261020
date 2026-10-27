# v10b 文档再生与边界

当前投稿源仍在submission-v10，分支revision-v10b，固定v10基线23fd9fa。原生源ZIP包含30文件，可独立解压后编译main.tex、supplement.tex、title-page.tex、cover-letter.tex；figure-legends.tex为完整图注列表支持文件。这里只编译保存的TeX/PDF图，不运行模型。

本轮使用的实际构建入口是notes/v10b/build_native_package.py，--run参数必须使用新的目录名，避免覆盖既有scratch检查。当前最终receipt为final-native-build.json；当前sourceZIP SHA是package-source-manifest.json。不可用旧notes/v10的prose builder覆盖v10b源。

read_cost_grid.py只读取原primary-regions.csv与cost-grid.csv.zip中的cheaper标记，输出cost-reading.json/.md；不调用成本计算器、不发预测。style_saved_displays.py只从固定v10显示基准和保存曲线生成图表副本，原before资产由23fd9fa拥有，完整逐项artist/数据值映射见visual-style-report.json。新图只覆盖submission副本，results/data/protocol全部封存不改。

full tests命令与环境在final-tests.json，原测试体系未修改；不把单元测试当作新的科学评估。final_check.py检查文档包/封存/正文结果行/作者占位/写法，旧S1/S2/S3字词规则与本轮精确Supplement引用的区分见checker-interpretation.md。

restricted原始FX/私有预测向量不在公开包。旧科学回放需要其原设计/输入许可，本文档不启动它。所有失败、负面及不可用结果保留。
