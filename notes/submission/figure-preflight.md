# H2 图表只读预检与成本图复查

结论：**当前10张图均已直接查看彩色和灰度，按当前主文/补充材料实际规格全部达到保守7bp字体门槛。** 旧成本图6个下标F约6.22bp的失败已保留；根代理授权样式修正后，本代理直接复查新版，当前成本图最小字约8.396bp。其余仍需明确的只是两图history标题和两处caption释义。投稿TIFF/EPS及最终排版由根代理继续检查。

本代理没有改canonical图、论文或研究代码，没有运行拟合/评分/研究摘要，也未改任何显示数值。九图在审计中未变；成本图由根代理修正，旧/新版本明确分开。

## 方法与边界

- 主文A4/25mm边距，正文160mm；补充材料A4/20mm边距，正文170mm。逐张读取实际includegraphics宽度；成本图同时应用高度上限和keepaspectratio。
- 字体提取包含文本/图形矩阵和数学下标，再乘实际缩放。PDFbp=1/72inch，TeXpt=1/72.27inch；7bp门槛略严格于7TeXpt。
- 以下尺寸来自当前LaTeX几何规格，未冒充新编译稿逐字形实测。首次测量时manuscript.pdf不存在；若图宽或版心改变必须重测。
- 当前10图彩色/灰度整图均以150dpi直接查看，旧成本图另看一版，共11个图版本。150dpi是诊断预览，不是投稿TIFF。
- 单位仅核验标签清楚与否；没有从金融数据重算货币换算。

## 当前10图尺寸与字体

| 图 | 来源与规格 | 印刷尺寸mm | 原生最小bp | 印刷最小bp | 7bp | 彩色/灰度直接看过 |
|---|---|---:|---:|---:|---|---|
| v10-cftc-contract-changes.pdf | `submission-final/manuscript.tex:282` / `width=.97\linewidth` | 155.20x126.64 | 8.80 | 8.603 | PASS | 是/是 |
| v10-cost-regions.pdf | `submission-final/manuscript.tex:345` / `width=.98\linewidth,height=.87\textheight,keepaspectratio` | 156.80x180.63 | 8.50 | 8.396 | PASS | 是/是 |
| v10-menu-isolation.pdf | `submission-final/supplement.tex:1510` / `width=.98\linewidth` | 166.60x135.95 | 8.50 | 8.920 | PASS | 是/是 |
| v11-fx-history.pdf | `submission-final/manuscript.tex:240` / `width=.88\linewidth` | 140.80x51.81 | 9.00 | 7.982 | PASS | 是/是 |
| v12-decomposition.pdf | `submission-final/manuscript.tex:298` / `width=.98\linewidth` | 156.80x93.10 | 8.00 | 7.717 | PASS | 是/是 |
| v13-rp.pdf | `submission-final/manuscript.tex:357` / `width=.98\linewidth` | 156.80x49.00 | 8.00 | 7.717 | PASS | 是/是 |
| v13-validation-length.pdf | `submission-final/generated/v13-supplement.tex:33` / `width=.98\linewidth` | 166.60x148.38 | 7.50 | 7.686 | PASS | 是/是 |
| v7-murphy-fx_hourly.pdf | `submission-final/generated/v10-moved-diagnostics.tex:23` / `width=.94\linewidth` | 159.80x88.21 | 9.00 | 9.060 | PASS | 是/是 |
| v7-murphy-nyfed_weekly.pdf | `submission-final/generated/v10-moved-diagnostics.tex:27` / `width=.94\linewidth` | 159.80x88.21 | 9.00 | 9.060 | PASS | 是/是 |
| v9-endpoint-peak-example.pdf | `submission-final/manuscript.tex:28` / `width=.94\linewidth` | 150.40x78.21 | 9.00 | 8.527 | PASS | 是/是 |

## 旧成本图问题与当前复查

- 旧SHA256：`07067f94f72dfea207c722a0bd917e6c941bcaed57b87833e6ccf23132cb4e39`，下标源6.3bp、印刷6.223bp，FAIL。
- 新SHA256：`925396ec1781718f812aa9933b10a203ab60489d21a772a6bcd2dba84e58f263`，印刷最小字8.396bp，PASS。
- 根代理把Breach charge beta=b/m_F改为Normalized breach charge beta，并把色阶零端由白改浅灰；本代理没有执行改图。
- `notes/submission/cost-figure-style-check.json`的旧/新SHA与本检查相同。
- 本代理从固定v13旧PDF独立提取115个数值文字token，与当前图完全一致。source arrays相同是根代理回执的保全断言，此处未重算矩阵。
- 新版彩色/灰度直接重看：零端浅灰与页白可分，大区边界清楚；相邻微小比例仍是细微连续色调，可选细网格/现有水平描边增强精读。

## 每张观察与最小处理

### v10-cftc-contract-changes.pdf

- 当前SHA256：`8e6f49c0f07bb7af7cb3bd95f071c532cb033d0c3067cea160198e8cfcc6ab2d`
- 单位：Relative loss change(%) is explicit; History52/260 is a count of completed weekly training labels, but that unit is implicit in the panel titles.
- 内部代号：The17 CFTC codes are real contract identifiers. Full regression is a readable method name.
- 直接观察：All17 codes, separate history panels, circle/diamond marks and zero lines are legible in color and grayscale. No clipping.
- 问题：History unit is implicit.
- 最小处理：
  - Replace History52/History260 by52-week training history/260-week training history. Preserve all points, literal codes and values.

### v10-cost-regions.pdf

- 当前SHA256：`925396ec1781718f812aa9933b10a203ab60489d21a772a6bcd2dba84e58f263`
- 单位：Normalized cost, reserve coefficient kappa, normalized breach charge beta and the fraction colorbar are dimensionless. The normalization formula remains defined in paper text.
- 内部代号：Mathematical kappa,beta,c are defined quantities, not internal method IDs.
- 直接观察：Current corrected six-panel graphic directly re-viewed in color and grayscale. All ticks, panel counts and common colorbar are clear. Pale-gray zero level separates from page white; adjacent tiny fractions remain subtle continuous tones.
- 问题：Minor low-end continuous-tone limitation remains; current font gate passes.
- 最小处理：
  - Keep the root-corrected Normalized breach charge beta axis label. No further font change is required at current width.
  - Optional thin cell boundaries or existing-level outlines can help exact low-fraction reading; preserve every matrix entry, coefficient and panel count.

### v10-menu-isolation.pdf

- 当前SHA256：`de159ec2d1701a73c0efb875a9e579761ba82de5b9a77576f4b70473070b9e04`
- 单位：Relative loss change(%) is explicit. History52/260 counts completed simulated labels under inherited hourly-index geometry despite weekly calibration parameters; it must not be relabelled literally as weeks.
- 内部代号：Old menu/Expanded menu and Full regression/Four-feature are descriptive names. NA(12/13) is explicit. IQR is a standard abbreviation.
- 直接观察：Open circles versus filled diamonds preserve the menu distinction in grayscale. All four panels and both unavailable long-history summaries remain visible. No clipping.
- 问题：Training-label count and inherited clock are implicit in titles.
- 最小处理：
  - Replace Constant | History52/260 with Constant |52/260training labels, and likewise Switching. Retain all NA(12/13), repetition counts and summaries.
  - Optionally expand source IQR to source interquartile range in the footer/caption.

### v11-fx-history.pdf

- 当前SHA256：`a9bec24c8b11a0aff59ddba8cc7cc6b0a64a4005e5c3ed93f33a6c259b420d6e`
- 单位：Completed hourly labels and relative loss change(%) are explicit.
- 内部代号：Full regression/Four-feature are readable names.
- 直接观察：All five histories, turning points, both paths and legend are clear in grayscale through circle/diamond markers.
- 问题：未发现需修正的字体、单位或灰度辨识问题。
- 最小处理：
  - Retain circle/diamond markers and zero line; no required unit/font/gray correction.

### v12-decomposition.pdf

- 当前SHA256：`25cd8de0928a72b42eaee570d864accecd2bfc48ca2ec2cdc461045e48baa2cc`
- 单位：Excess loss relative to history(%) and planned comparison index are explicit normalized quantities.
- 内部代号：Selection component/Finite-menu gap/Actual excess/Unavailable are descriptive. Panel and Bill are source-group abbreviations.
- 直接观察：Diagonal versus dotted hatches, black actual-excess dots and unavailable crosses survive grayscale. All groups, negative bars and90 comparison indices remain visible.
- 问题：Panel/Bill need a caption definition; expanding inside the narrow group spans can overlap.
- 最小处理：
  - Define Panel=12additional New York Fed series and Bill=Treasury bills in the caption; no figure rewrite is necessary.
  - Keep both hatches and every dot/cross. Link the full index map without dropping or reordering cells.

### v13-rp.pdf

- 当前SHA256：`144206b43234f8eed89d198f4802c03a6a3d0d87a20d6ce576c7f271c0f13561`
- 单位：Excess pinball loss(%) is explicit. CFTC/New York Fed/FX use deliberately separate y scales.
- 内部代号：Ordinary/Protocol are readable names without RP/R0/QR codes.
- 直接观察：Markers, x positions, boxes and whiskers remain distinguishable in grayscale. Extreme weekly losses and identical ordinary/protocol FX outcomes are retained.
- 问题：未发现需修正的字体、单位或灰度辨识问题。
- 最小处理：
  - Retain circles versus squares, separate scales and all adverse points; do not introduce visual FX gains.

### v13-validation-length.pdf

- 当前SHA256：`a35cf05a7e21a65b7219f0959b28cfa91fa40562d060aedc07420c736cdb7ef6`
- 单位：Validation52/156weeks, training52/260weeks, horizons6/24weeks and excess pinball loss(%) are explicit.
- 内部代号：CFTC codes are genuine identifiers; GS-B,CS-TOT,GSC-G2L3 and other NY Fed labels omit the common PDPOS prefix.
- 直接观察：All four panels, vertical labels, zero lines and circle/square validation markers are legible at current supplementary size and in grayscale.
- 问题：The shortened NY Fed keys need an explicit full-key mapping.
- 最小处理：
  - Add caption: New York Fed labels omit the common PDPOS prefix; for example GS-B=PDPOSGS-B. Preserve every source label/order and number.
  - Retain circle/square markers and inspect conversion glyphs; source contains embedded Type3 font programs.

### v7-murphy-fx_hourly.pdf

- 当前SHA256：`9f07e1bb66630ecefe517a75e7d878c05dadd6fe2fc49e47c1ca5f635b294192`
- 单位：Threshold is labelled USD millions; mean elementary score is labelled dimensionless. No currency conversion recomputed.
- 内部代号：Full regression/Historical headroom are descriptive.
- 直接观察：Solid circles versus dashed squares remain clear in grayscale, including crossings and close segments. Axes and legend are clear.
- 问题：未发现需修正的字体、单位或灰度辨识问题。
- 最小处理：
  - Preserve curve samples/crossings, line/marker distinction and USD-millions unit.

### v7-murphy-nyfed_weekly.pdf

- 当前SHA256：`0ab26bbc6ad85479267d8e1dbb5c700911617b0c26fed71fa285be02210d7d07`
- 单位：Threshold is labelled USD billions; mean elementary score is dimensionless. No currency conversion recomputed.
- 内部代号：Full regression/Historical headroom are descriptive.
- 直接观察：Both paths, crossings, shape/dash encodings, axes and legend remain clear in grayscale. No clipping.
- 问题：未发现需修正的字体、单位或灰度辨识问题。
- 最小处理：
  - Preserve exact curves/crossings and USD-billions unit; retain solid circles versus dashed squares.

### v9-endpoint-peak-example.pdf

- 当前SHA256：`af428203394aeafcad636f00fb466b502217205456168789472605caf09b5ef6`
- 单位：Absolute position is labelled USD millions; economic date is labelled2021.
- 内部代号：Observed absolute position/Historical headroom limit are descriptive.
- 直接观察：Both intervening breaches, the final return below the limit, dated points and units remain clear in grayscale.
- 问题：未发现需修正的字体、单位或灰度辨识问题。
- 最小处理：
  - Keep solid circles versus dashed squares, all dated observations and exact limit. No smoothing or reduction.

## 剩余具体显示文字交接

| 文件/位置 | 现标签 | 建议 | 只改显示的可行办法 |
|---|---|---|---|
| v10-cftc-contract-changes.pdf两panel | History52 / History260 |52-week training history /260-week training history |改归档作图脚本的title字符串后输出新副本；或在标题空白区域覆盖文字。所有点和代码不变。 |
| v10-menu-isolation.pdf四panel | Constant or Switching, History52/260 | Constant or Switching,52/260training labels |只改title字符串。不要写weeks：该模拟继承小时索引几何。 |
| v12-decomposition.pdf对应caption | Panel / Bill |解释Panel=12additional New York Fed series; Bill=Treasury bills |只改caption，避免在狭窄group span里展开造成重叠。 |
| v13-validation-length.pdf对应caption | GS-B等短key |说明省略共同PDPOS前缀，例如GS-B=PDPOSGS-B |只补caption映射，无需改点或数值。 |

没有发现需要修正的USD millions/USD billions轴标签，也没有发现必须改写的内部QR/R0软件代号；现有方法名已为可读文字。

## TIFF/EPS与有效分辨率

ASMBI单独TIFF/EPS、线图最低600dpi/优先800dpi由根代理提供，本子任务未另行联网核实。此处不宣称根代理投稿格式已导出或检查完成。按最终印刷尺寸生成800dpi可以避免补充图放大后从原生800dpi降到约762-795有效dpi。像素向上取整。

| 图 | 最终印刷800dpi像素WxH | 原PDF画布需原生DPI以达800有效dpi | 原生800的有效dpi |
|---|---:|---:|---:|
| v10-cftc-contract-changes.pdf | 4889x3989 | 783 | 818.3 |
| v10-cost-regions.pdf | 4939x5690 | 791 | 809.9 |
| v10-menu-isolation.pdf | 5248x4282 | 840 | 762.3 |
| v11-fx-history.pdf | 4435x1632 | 710 | 902.0 |
| v12-decomposition.pdf | 4939x2933 | 772 | 829.4 |
| v13-rp.pdf | 4939x1544 | 772 | 829.4 |
| v13-validation-length.pdf | 5248x4674 | 820 | 780.6 |
| v7-murphy-fx_hourly.pdf | 5034x2779 | 806 | 794.7 |
| v7-murphy-nyfed_weekly.pdf | 5034x2779 | 806 | 794.7 |
| v9-endpoint-peak-example.pdf | 4738x2464 | 758 | 844.4 |

提高DPI不会增大物理字体。成本图通过来自标签样式处理；其余图无需为7bp门槛改变科学画法。根代理导出后应逐张直接查看，保留数学符号、NA、真实series/contract keys、全部极端点及灰度线型/标记。
