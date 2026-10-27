# 两图历史标题澄清：完成回执

结论：**PASS**。只修改两张授权canonical PDF中的6个panel标题。新图彩色/灰度均直接查看，标题完整且不挤压；没有改caption、其他图、原绘图源码、results、data或protocol，没有导入模型/runner或执行研究摘要。

## 来源与保全

- 固定来源提交：`8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`。
- 从tracked原绘图脚本仅AST加载arr/figure_geometry/setup/base/cftc/menu；完全排除原untracked BEFORE缓存断言及original_fig动态导入。
- 绘图材料只来自tracked两个report-values.json和tracked visual-style-report.json。
- **先用原样标题重建，两图PDF均与原v13 PDF逐字节相同**，证明所用字体、配色、几何与现有版本一致；随后仅替换title文本。
- 原v13保存的艺术家数组与新数组逐项完全一致；颜色、线宽、marker、误差条、坐标限制、tick、panel位置、图例和非标题文字坐标全部精确相同。
- 两张canonical前图均已tracked，因此无需.bak；原v13与本次前图SHA均保存在回执中。

## 各图结果

### v10-cftc-contract-changes

- 原v13/本次前图SHA256：`8e6f49c0f07bb7af7cb3bd95f071c532cb033d0c3067cea160198e8cfcc6ab2d`
- 新图SHA256：`71e3acaa34c19a20b7a24f6e11dc1ea92d478d0a0af629ce16723af8e9c399d9`
- 原样重建与v13 PDF逐字节相同：true。
- 数值文字逐一比较：29项，全部相同（原顺序也相同，无需映射重排）。
- 保存数组位置：`notes/v10b/visual-style-report.json:/figures/1/after_artist_arrays`；原/新数组完全相同。
- 保存数组SHA256：`4dcb92f21457d346b2fea1dd2646e937945c4ace64a265cf6f0bcff02443e316`
- 非标题PDF文字及其坐标、完整protected艺术家样式/几何：全部相同。
- 印刷最小字体：8.603213bp，保守7bp门槛PASS。
- 彩色/灰度：新版本均已直接查看，标题无裁切、无碰撞；数值、点、NA、误差条及footer完整。
- 标题替换：
  - `History 52` → `52-week training history`
  - `History 260` → `260-week training history`

### v10-menu-isolation

- 原v13/本次前图SHA256：`de159ec2d1701a73c0efb875a9e579761ba82de5b9a77576f4b70473070b9e04`
- 新图SHA256：`cc7fcd490cbd904d3c75f29c712b638a72eec530b51c9be170bf882936143b5d`
- 原样重建与v13 PDF逐字节相同：true。
- 数值文字逐一比较：22项，全部相同（原顺序也相同，无需映射重排）。
- 保存数组位置：`notes/v10b/visual-style-report.json:/figures/2/after_artist_arrays`；原/新数组完全相同。
- 保存数组SHA256：`7bbb9c691b416ed000e8d8d86b313572b968ff841f72b56cb85c9a05c505dc00`
- 非标题PDF文字及其坐标、完整protected艺术家样式/几何：全部相同。
- 印刷最小字体：8.920315bp，保守7bp门槛PASS。
- 彩色/灰度：新版本均已直接查看，标题无裁切、无碰撞；数值、点、NA、误差条及footer完整。
- 标题替换：
  - `Constant | History 52` → `Constant | 52 training labels`
  - `Constant | History 260` → `Constant | 260 training labels`
  - `Switching | History 52` → `Switching | 52 training labels`
  - `Switching | History 260` → `Switching | 260 training labels`

## 边界

CFTC标题明确以周为训练标签单位。模拟图仅写training labels，不将其继承的小时索引几何错误改成weeks。数据数组、统计输出、数值、顺序、画法和既有科学边界全部保留。

原figure-preflight.json保留改图前快照；本回执只接续其中两张图的新SHA和直接查看结论，其他8张图未动。未提交。
