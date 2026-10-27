# v10b 图表显示与数值绑定报告

本次仅整理投稿显示副本。未运行预测、评分、bootstrap、研究驱动器、reducer 或新实验，未修改 results、data、protocol、模型或科学计算脚本；没有切换分支或提交。`submission-v10/manuscript.tex` 与 `supplement.tex` 由根任务及补充材料负责人拥有，本助手未编辑。

## 结论与实际输出

- 主稿所用四图与补充材料所用两张 Murphy 图已重绘为矢量 PDF，另有 PNG 预览；文件名与已有引用保持一致。
- 六图的所有绘图数值数组逐项相同，包括点坐标、连接线、误差线区间及热图矩阵；每图前后 PDF SHA、实际 artist 数组及数组 SHA 均在 `visual-style-report.json`。
- 三张主生成表的每个数据行、数值显示精度、缺失/NA 和可追溯方法身份均保留；CFTC 的 170 个数值格为两位小数，menu 的中位数与两个四分位数均为两位，MCS 百分数均为一位。
- 完整 MCS 表保留 976 个原 p 值显示项、全部 NA、损失类上标、方法列和原方法图例；只改表头与不可见排版间距。
- 最终 canonical 主稿为 19 页、补充材料为 32 页；实际 PDF 的六个图形调用矩阵均已读取，字号检查使用最终 PDF 的缩放值。

最终 PDF 测量记录：`visual-qa/final-pdf-scale-check.json`。其中主稿 SHA-256 为 `1cf6d4be5110d60a6e54bc5f2184bd7b0e022870eefff677aff9963479dade47`，补充材料为 `1e80ec35561c67796d2b0f2d7cd951e36b90d6b745444c599d278f5e36dfc8bf`。最终四文档统一编译的 owning receipt 为根任务的 `notes/v10b/final-native-build.json`。

## 成熟显示实践与统一语义

参照 [Okabe 与 Ito 的 Color Universal Design](https://jfly.uni-koeln.de/color/) 使用颜色加形状、线型、位置的冗余编码；模拟方式采用 [Colorspacious 官方教程](https://colorspacious.readthedocs.io/en/latest/tutorial.html) 的 CVD 色彩空间转换。包经临时 uv 环境调用，没有系统安装。模拟仅写 QA PNG，未变换投稿图。

| 语义 | 实际颜色 | 冗余识别 |
|---|---|---|
| 完整回归 | Okabe–Ito 蓝 `#0072B2` | Murphy 为实线/圆；CFTC 两历史列为圆/菱形；menu 固定在 Full regression 位置 |
| 四特征回归 | Okabe–Ito 紫 `#CC79A7` | 固定 Four-feature 位置与文字标签 |
| 历史 headroom | 灰黑 `#222222` | 虚线/方形，与回归实线/圆分开 |
| 原菜单 | 保留该方法颜色 | 空心圆 |
| 扩展菜单 | 保留该方法颜色 | 实心菱形 |
| 成本获胜比例 | 白到蓝的单调色阶 | 明确 0–1 色标；此颜色表示比例，不表示某个方法 |

已查看六图普通色彩、100% deuteranomaly、protanomaly、tritanomaly 及灰阶的完整 contact sheet。色彩接近时，菜单身份仍由空/实心与圆/菱形辨认，方法由固定位置及可读标签辨认，Murphy 曲线由线型/marker 辨认。图例均置于数据区域之外；无图例遮挡数据。菜单图行间距与 CFTC 图底注间距经过实际渲染后修正，成本图全部 beta 刻度保留并旋转以防相邻数字粘连。

## 最终 PDF 的实际字号

测量直接读取最终页面内容流的 `cm` 与 `Do` 矩阵，并合成图形的 `/Matrix`；不能用 pypdf 的内层文字 visitor 单独给出的原始字号代替外层缩放。测量脚本为 `measure_final_pdf.py`。

| 最终位置 | 图 | 实际缩放 | 最小普通文字字号 | 边界 |
|---|---|---:|---:|---|
| 主稿 p.1 | endpoint/peak 示例 | 0.94746 | 8.527 pt | 原坐标、日期、报告线不变 |
| 主稿 p.10 | CFTC 全合约 | 0.97769 | 8.604 pt | 全部 17 合约及原顺序保留 |
| 主稿 p.12 | 菜单隔离 | 0.98778 | 8.396 pt | NA 的 12/13 来源标注保留 |
| 主稿 p.14 | 成本区域 | 0.98778 | 8.396 pt | 数学下标自然缩至 6.223 pt；正文和刻度未缩至此值 |
| 补充 p.32 | FX Murphy | 1.00668 | 9.060 pt | USD millions |
| 补充 p.32 | Treasury Murphy | 1.00668 | 9.060 pt | USD billions，保留原实际显示的 0.001 比例 |

原主图生成宽度过大，缩进正文后 CFTC 最小普通字为约 5.31 pt，菜单 NA 字为约 4.83 pt；现在接近实际刊印宽度生成。原 Murphy 图本身字号已可读，其本次改进重点是统一方法颜色、添加 marker、移出图例并明确 elementary score 无量纲。

独立主表样张使用主稿 A4/25 mm 页边距，CFTC 正文约 8.535 pt，MCS/menu 正文约 8.966 pt，无 Overfull；数学下标在约 5.978 pt 属公式正常下标。最终整稿维持既定字号及缩放，未靠额外缩表压页。

## 逐项绑定的证据方法

1. **Endpoint**：核对旧 v9 PDF SHA 与 `results/v9/figures/scalars.json` 一致；其归档日期、七个绝对头寸与报告值逐项等于 `notes/v7/example-selection.json`。新图两条实际 Line2D 的 x/y 数组逐项比较，未换窗口或单位。
2. **CFTC/menu**：旧投稿 PDF 与对应 results 中已存 PDF 的 SHA 一致；使用旧 `report_v10_cftc.py` / `report_v10_menu.py` 的纯显示函数在内存建立原图，截获实际 artist 数组，与新图逐项比较。保存动作在内存拦截，不写 results。
3. **Cost**：旧投稿 PDF 与结果 PDF 的 SHA 一致；把三个已保存的聚合输入逐字节复制到 `notes/v10b/visual-qa/cost-original-reference/`，将旧 `report_v10_cost.py` 的显示输出目录改指向该 QA 目录；捕获旧显示函数的实际热图 artists，并与新图全部 7×9 矩阵比较。全部上下界、两轴网格、完成数亦保留。没有调用成本计算器或重新估算成本。
4. **Murphy**：发现 v7 原 TeX 使用原生 millions，但实际继承 PDF 曾在 revision-v8 中把 Treasury 横轴换成 billions。故没有拿旧 TeX 冒充实际 PDF 的 baseline。实际 baseline PDF SHA 精确匹配 `notes/revision-v8/wp2-figure-styling.json`，旧显示函数经输出重定向后截获实际 201 点曲线；FX 比例为 1，Treasury 为 0.001，新图完全保留。另行重建原 v7 TeX 与旧 TeX 逐字节相等，只作为原生归档的额外交叉核对。
5. **表格**：CFTC/menu 原 body 行逐格与 saved report-values 对照，MCS 主表保留所有原行内数值串。完整 MCS 新增不可见上标占位后先剥离占位校验全文相等，再仅改表头；所有 976 个原 p-value token 的序列仍完全相等，NA 数量不变。Legacy 表仅按已知 header 前缀替换，非表头数据行逐字节保留。

12 个读取输入的 SHA 在显示生成前后完全一致。完整输入路径、SHA、前后 artist 数组、输出 PDF SHA 和表格格级字符串对照都在 JSON；不是只记录“同一个来源”。

## 表格显示、表头及注释

- CFTC 用原生 `r@{.}l` 列按小数点对齐；表头为 Intercept only、Four-feature、Full regression、Calibrated history、Calibrated regression。方法 ID 只在说明中用于可追溯映射，I 未误写成 translated path。
- Menu 用等宽右齐盒分别排列中位数与两个四分位数，固定两位小数；方法行写 Full regression / Four-feature。
- MCS 主表按固定宽度排列计数比及一位小数百分比；其说明明确指向 Supplement Section S31，保留独立的 4/98 指标，并按根任务指示去掉注释中对 2/98 总行的重复复述。
- 完整 MCS 的 41 个列身份改用可读短名；最密块的两行短名旋转 90 度，保留原分块数及原 7.1 pt 正文。原 Mxx 别名只在科学损失类上标和方法图例 body 保留。带损失类上标的列为无上标 p 值添加等宽不可见占位，避免后缀把小数点向左挤；本身没有上标的列不增宽。
- 完整 menu 表增加 `endfirsthead`，首 caption/label 不再在续页重复执行；只重复可读列头。
- 九个 legacy 生成表的 header 已单独通俗化。五个原四句 caption 通过合并句子缩成三句，没有删除失败、重叠窗口、样本选择或科学限制。
- 补充材料其他原表的数字列已有右齐排版；固定小数位的列可直接对齐，复合的 loss/breach、IQR 或科学计数法单元格仍保留原显示精度，未为了排版改数值。补充材料正文表头及其核对由 `v10b_supplement` 负责人处理。

正式 caption 和三张主生成表的正式 note 均不超过三句。完整 MCS 前置方法说明和完整 legend 的若干普通科学段落较长：按根任务最终分类，它们是 S31 的科学说明段落，不作为 caption/note 计句；本助手已明确报告该分类，没有把长段落伪装成已通过三句 note 检查。

## 渲染与未解决项

- 已查看六图普通/CVD/灰阶 contact sheets、三主表完整样张、完整 menu+MCS 九页样张，以及最终尺寸的补充材料 p.27 密集 MCS 矩阵与 p.32 两张 Murphy 图。
- 当前整稿独立原生构建：主稿 19 页、补充 32 页，均无 Overfull；主稿无未解析引用，补充无 multiply-defined label。原有 Underfull 文本提示未当作科学或编译失败。
- 独立构建与最终 canonical PDF 的读取验收没有覆盖根任务的四 PDF 最终统一验收责任；根任务将完成全页检查与打包。
- 数学下标采用排版系统的自然小号；完整 MCS 的密集审计矩阵保留 7.1 pt 正文以保留全部检验及页数。该矩阵适合 PDF 放大阅读；没有声称它与主稿正文同字号。
- 没有未解决的数据、单位、图例遮挡或数值绑定问题。需要保留的范围边界是：重绘只验证已保存曲线与聚合读出，不构成独立重算或新的科学验证。

QA 文件包括 `visual-qa/all-figures-before.png`、`all-figures-after.png`、三种 CVD sheet、`all-figures-grayscale.png`、`tables-contact.png`、`supplement-tables-contact.png`、`render-font-qa.json` 及最终矩阵测量。所有 QA 图均位于 notes，未覆盖科学归档。

Root逐页复核后的最终间距修正：MCS主表列距2pt→4pt，命题编号后补词间空格，标题页禁标题断词并隐藏链接彩框，删除menu重复过渡句。均不改数据，final-native-r2已重新编译并逐页SHA比对/变化页重看通过；未变页面按渲染SHA复用逐页检查，变化页重新打开。
