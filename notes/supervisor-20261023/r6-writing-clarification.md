# R6 写作限定与两项归档 HAC 核算

范围：只改写作并读取既存逐点损失做两项描述性 HAC；未重新拟合、选参、生成标签或修改旧结果。

改动：摘要、引言贡献段、第二节总结、第五节原样本带宽限定、第七节 R6 及 Table 10、第八节第二条、结论、CONTRIBUTIONS.md 创新点 2、文档复现说明。

两项均为同一原三点菜单 QR（λ=.01、也等于 R0）对不同 F，不是 R2；n=1440、H=6、L=7。匹配 frozen F2880/d24：−16.623565%、p=0.00002937322779608827；原 primary rolling F720/d1：+3.168199%、p=0.5735832734537913。p 值为事后、双侧标准正态、未调整的描述性核算，不控制整个选参和检视过程错误率。见新 HAC 目录和 r6-writing-provenance.json；既有结果均未改。

S1：T-bill H24 决定最差值 +181.4%，但中位数 +5.374% 也超 +5%；不能称唯一由一个格子导致失败。

验证：Tectonic 编译退出 0；正文含参考文献 15 页，附录 5 页。正文重新排版的第 1–15 页均逐页渲染目检，无裁切、表格越界或文字叠压。参考文献有一处已有的 underfull hbox 提示，不影响内容；无 overfull、未定义引文或交叉引用。既有统计夹具测试 7/7 通过（0.025 秒），未运行实验。544 个受保护的数据、协议、结果与核心路径逐字节未变，附录各页文本相同，无文件删除。

命令：
```text
python3 -B -m unittest test_supervisor_inference -v
# Ran 7 tests in 0.025s; OK
python3 -B build_supervisor_r6_writing.py
# 源绑定文档 reader；不重算统计量
/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic -X compile main.tex --outdir ../../.scratch/r6-writing-20261023/compile-delivery --keep-logs
# exit 0; PDF 15+5 pages
```

## 待用户决定

本轮没有新增待定事项。沿用 CONTRIBUTIONS.md 中未采纳的标题备选，正式标题未改。

## 摘要（本轮全文）

Three findings qualify conditional forecasts of two-sided absolute holding-period position peaks: FX gains depend on the historical reference and period. Against matched frozen $F_{2880}$, QR lowers loss by 14.8% in the inspected period and 16.6% in the 2015 block with no prior evaluation role found in the repository audit, but earlier loss rises by 3.2% against the original primary's rolling $F_{720}$, so that primary's gain direction does not recur; the Treasury $W=52$ analogue raises loss by 144.3%. Across 12 additional weekly series, expanding the ridge menu reduces median excess loss from 92.6% to 9.2%, yet 34 of 48 cells still lose. On short weekly samples, validation selection, including a conservative one-standard-error rule, does not reliably protect the historical benchmark. Finally, the original FX primary lowers loss by 12.7% while breaches rise from 332 to 376; the 1.83% 24-step legacy gain reverses above an underprediction/overprediction weight ratio of 20.6, and both primary Murphy curves cross. Inventory-limit comparisons therefore require error amounts and breach counts alongside pinball loss. The evidence remains retrospective: prior FX inspection, downloaded-vintage Treasury aggregates and shared panel reporting limit generalization.

## 结论（本轮全文）

Three findings qualify conditional forecasts of two-sided absolute holding-period peaks. History- and update-matched six-step regression lowers FX loss by 14.8% but raises Treasury loss by 50.8%. In the earlier 2015 FX block with no prior evaluation role found in the repository audit, QR lowers loss by 16.6% against matched frozen $F_{2880}$ but raises it by 3.2% against the original primary's rolling $F_{720}$, whose gain direction does not recur; the Treasury $W=52$ analogue raises loss by 144.3%. Expanded ridge menus reduce the 12-series weekly panel's median excess from 92.6% to 9.2%, but 34/48 cells still lose. Shrinkage mitigates losses, yet short-sample weekly validation selection, including conservative one-SE selection, does not stably protect the historical benchmark. Finally, the original FX primary's 12.7% score gain accompanies breaches rising from 332 to 376; the 1.83% 24-step legacy gain reverses above weight ratio 20.6, and both primary Murphy curves cross. Inventory-limit selection therefore requires underprediction amounts, overprediction amounts and breach counts alongside pinball loss.

These retrospective comparisons apply established estimators to a sampled peak. Prior FX inspection, downloaded-vintage Treasury aggregates, post-result menu expansion and shared panel reporting limit generalization. They establish neither conditional-coverage guarantees nor benefits from actual inventory or funding decisions.

## 第 8 节第 2 条（本轮全文）

**Default to conservative historical reports in short samples.** R6 shows that adding ordinary intercept-only $I$ to the menu and applying one-SE selection still permits large weekly losses: R2 selects $I$ in 17/26 cells, yet its worst excess over $F$ is +181.4%. For short samples of this kind, use the historical rule by default and switch to a conditional model only when validation evidence is sufficiently strong; this study establishes no such sufficiency threshold. Prefer conservative corrected-rank $F$ at short windows: earlier-period $I$ itself loses by as much as +36.5% relative to $F$. An intercept-only option and a larger penalty do not establish evaluation protection.
