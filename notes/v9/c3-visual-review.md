# C3 native PDF visual review

**状态：C3中间稿，C4会换图/Table6，C7会复检最终版。**

本轮仅渲染并逐页打开当前PDF的全部17页；未修改投稿源、图片源、研究结果，也未重新编译。视觉检查覆盖裁切、重叠、缺字/黑块、图表与脚注可读性、页尾和标题孤立。此记录不替代数字审计、研究有效性或最终C7验收。

## 固定输入与渲染

- PDF: `/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-build/manuscript.pdf`
- PDF bytes: `177411`
- PDF SHA256: `6fca841ef006dbbcc3b8a334eeca4b400b3120d9b989a9dc8dc43bc26552c516`
- Native PDF: 17 pages, A4 595.28 x 841.89 pt, PDF 1.5.
- Renderer: `/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm`, `-r 140 -png`.
- Render exit code: 0; stderr empty. Output directory was newly created; 17 PNGs were produced.
- Every page listed below was individually opened with `view_image` at original detail. This is visual inspection, not a text-only check.

## 逐页 manifest

|Page|Opened image|Observed content and visual result|PNG size|PNG SHA256|
|---:|---|---|---|---|
|1|[page-01.png](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-render/page-01.png)|Title, Abstract, keywords, Introduction, Figure 1. PASS; title and abstract clear, no text/figure clipping. Figure 1 is still the prior USD-billions version; C4 will replace its axis formatting.|1158 x 1638|`8e4fa73f045d549c58bdc3aa827f8ba53fb0190867f0305db66b87faceab6217`|
|2|[page-02.png](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-render/page-02.png)|Three empirical points; Related literature. PASS; italic lead sentences, citations and paragraph spacing are clear; no heading orphan or collision.|1158 x 1638|`9f96305dcca29cc6db81f2f96a9eba77a2d5641b486a5b75a69b05547cfd03fd`|
|3|[page-03.png](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-render/page-03.png)|Table 1 literature comparison. PASS; table-only float page. Seven columns and the footnote are readable, all rules stay inside margins.|1158 x 1638|`3dcc5ef875db3b4b0df7008073d54873e5984228b9279b39b746fbf681112308`|
|4|[page-04.png](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-render/page-04.png)|Target, four displays, two propositions; Data begins. PASS; mathematical glyphs, subscripts and inequality symbols render correctly; Data heading has following text.|1158 x 1638|`c89efb1fa3cada12dfaa1c313c4453546b4016d7606e55844b74d6c11ac184e1`|
|5|[page-05.png](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-render/page-05.png)|Data continuation; Forecasting methods. PASS; method text and mathematical notation are readable; no cropped lines or overlap.|1158 x 1638|`858649bc0b86eb86dfab6da790c42a73313df33d3ba9ce2f90bad36b617254ae`|
|6|[page-06.png](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-render/page-06.png)|Table 2 methods and menus. PASS with dense-layout note; table-only float page. All cells and footnote are visible. The final footnote lines approach the footer but do not collide.|1158 x 1638|`59ba1a00c3a2f9144151ca7f2081f73675e9ec5f430f32615461aebcbe9e2f27`|
|7|[page-07.png](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-render/page-07.png)|Evaluation design, transparency, Results 7.1. PASS; subsection hierarchy and paragraphs render cleanly, with normal bottom whitespace.|1158 x 1638|`3c2639b33d81e541c65c1c616bc09428ecd61da28fe283118969c02ba252ca2f`|
|8|[page-08.png](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-render/page-08.png)|Table 3; Results 7.2; start of 7.3. PASS; table headers, numbers and notes are legible. The 7.3 heading has a full paragraph below it; no orphan heading.|1158 x 1638|`cd67262edd6c6cf1ff57eeff4020bc78952e1a7de9357e9fac7066f04561bbf7`|
|9|[page-09.png](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-render/page-09.png)|Table 4; continuation of 7.3. PASS; rows and footnote fit. Multi-line labels are readable; no column collision.|1158 x 1638|`b2765b6df85a37ea0ac69f8c7cacf5f595cb84f48d2797e831c2bd6d28ca9e64`|
|10|[page-10.png](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-render/page-10.png)|Table 5 panels A/B; Figure 2. PASS; both statistical panels, their notes and the solid/dashed Murphy curves are readable, with no caption clipping.|1158 x 1638|`3365d84f58c5381cf11b2ea69e08b700cba1acaf9184cd8823258532090be8f7`|
|11|[page-11.png](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-render/page-11.png)|Figure 3; start of Section 7.4. PASS; figure axes/legend/caption clear. Section 7.4 starts in the middle part of this page and continues normally onto page 12.|1158 x 1638|`a6c29c8423d3a0c7a03421a9c3093fd25c13f8b7ad4b3ccc8b97000511727ba1`|
|12|[page-12.png](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-render/page-12.png)|Section 7.4 continuation; Figure 4; Section 8 starts. VISUAL PASS / KNOWN C4 PLACEHOLDER; narrative, grid annotations and caption fit. Figure 4 is still the prior controlled-grid figure, while the text anticipates the combined figure.|1158 x 1638|`25540c0c95dff3f4faea1896f8ad741a282dcd65202bd03f3b80c6c2272ee3fa`|
|13|[page-13.png](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-render/page-13.png)|Section 8 continuation; Table 6; Limitations begins. VISUAL PASS / KNOWN C4 TABLE UPDATE; current four-column table is readable and contained; C4 will update its evidence structure.|1158 x 1638|`fc2015dba5eab3ca8e9923228be8347f54e4a1ee96eda2261e663bb91cf2f675`|
|14|[page-14.png](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-render/page-14.png)|Limitations conclusion; Conclusion; Data/code availability. PASS; all headings and text fit, and long availability URLs wrap inside margins.|1158 x 1638|`7eda8052d702fd8ce89e08451de3109d7bb12d478ae6ed2651e5d55f3ee74e25`|
|15|[page-15.png](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-render/page-15.png)|Author placeholders; References begins. PASS; all five author fields remain visible as placeholders. References and URL lines are readable.|1158 x 1638|`855b62664b6143a519dd48deaed0d4bca0807044340473616fdef5ed7b8b4013`|
|16|[page-16.png](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-render/page-16.png)|References continuation. PASS; dense reference page but no overlap, cropped line or missing glyph. URL breaks remain inside margins.|1158 x 1638|`d605576590e226e1b8227bd5e8a72544b240407f0064a9a0ad1068743694ba40`|
|17|[page-17.png](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-render/page-17.png)|Final four references. PASS; legitimate references tail page with whitespace below; no blank page or isolated body heading.|1158 x 1638|`640594a0960b67c59654ab4fb622004428020c96fa72ed128bc3088a5eeca1bf`|

## 实际跨度与待办

- Section 7.4标题位于印刷页11中部；文字在印刷页12上部结束，正文文字本身少于一个完整正文页高。当前图4及图注继续占据页12中下部，Section 8随后在页12下部开始。含现图和图注的7.4整体约在1.5个正文页高附近；这是逐页图像观察的近似值，不是换图后的最终分页验收。
- 已知C4待办：图4仍是旧PR5 controlled-grid图，而7.4正文已经提及controlled与newly calibrated的组合比较。该不一致本轮没有修图或改文；C4必须完成预定合并图。
- 已知C4待办：Table 6当前仍是原四列结构；其本页视觉可读，后续扩列/换结构后需要重看列宽、换行及页数。
- Figure 1当前纵轴使用USD billions的旧样式；C4仍需完成要求的千分位普通数字轴。现图轴、图例和曲线均没有裁切。
- 页3、页6是表格浮动专页，不能等同于空白页。页17是参考文献尾页；没有发现仅含正文孤标题的页面。页6表2较密、脚注接近页脚，最终排版应继续关注余量。
- 未见裁切、文字/表格重叠、缺字黑块或不可辨的图例。现有图4虽然字密，但各格估计/MCSE和坐标在本次140dpi原图中可辨；C4替换后该观察不自动继承。

## 边界

本记录只确认上述固定SHA的C3中间稿视觉状态。C4改变图、Table6或分页后，C7须重新编译并渲染最终正文、Supplement及title page；本轮不能宣称投稿包最终通过。
