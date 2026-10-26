# C3 final-text PDF visual delta

**C3中间稿局部终稿检查；C4会换图/Table6，C7会复检最终版。**

只读逐页提取两个PDF文字以找变化页，随后仅渲染并打开变化页。未改源、未重新编译；上一轮17页检查记录完整保留。

## 固定输入

- Before: `/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-build/manuscript.pdf`；SHA256 `6fca841ef006dbbcc3b8a334eeca4b400b3120d9b989a9dc8dc43bc26552c516`。
- After: `/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-final-build/manuscript.pdf`；SHA256 `d741e17dff2fbda4b6726c44afa9731eeb9f4e2f806a2d4b408d604206345c9b`。
- 两版页数均为17。逐页原始extract_text及空白标准化比较得到同一变化集：1、5、10、14、16、17。
- 其余页2、3、4、6、7、8、9、11、12、13、15文字逐页相同；本轮按请求不重复渲染这些页，沿用上一轮固定PDF视觉记录的基础，并留待C7最终全页复检。
- pypdf只用于文字差异定位；变化页另用Poppler `pdftoppm -r 140 -f N -l N -png`生成，并逐页view_image以original detail打开。

## 变化页视觉 manifest

|Page|Opened PNG|文字差异与视觉观察|PNG size|PNG SHA256|
|---:|---|---|---|---|
|1|[page-01.png](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-final-render/page-01.png)|摘要加入absolute、同一hourly FX record的daily聚合，以及history52/full regression/median across series口径。目视：标题、145词摘要、keywords、引言与图1布局清晰，无裁切或重叠。|1158 x 1638|`07c7e869e1811219d469f65379b446d7e551420634f87c29f165eca11b7603d4`|
|5|[page-05.png](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-final-render/page-05.png)|one-standard-error说明增加Hastie等(2009)出处。目视：新增引用和后续换行正常，方法段未溢出，Table2仍留在下一页。|1158 x 1638|`63f232b11891981d494c7999dc5ba474f3b8e82277b761d2b1d2f21ff39e3d17`|
|10|[page-10.png](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-final-render/page-10.png)|FX图注由primary改为main comparison。目视：图注、Murphy图和Table5两panel均清晰，无图注碰撞。|1158 x 1638|`e1a28f712f242cf34b6905b1f07dc1653b936a1841c845486ea3cf5660b2b7d6`|
|14|[page-14.png](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-final-render/page-14.png)|结论补入history52下116.2%/121.4%与median口径，删去重复长历史总结。目视：结论和availability段落仍完整在页内，URLs换行正常。|1158 x 1638|`694cd57ccf47b18d085dadbeb24efad31ac198de479f56041e03b97205171db1`|
|16|[page-16.png](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-final-render/page-16.png)|新增Hastie书目；原Petrunia条目移到下一页。目视：新书目、DOI和其余参考文献可读，页底Newey-West条目未裁切或碰页码。|1158 x 1638|`ba2ca4734869cd61b2f143cd9d86a1900c44eb9c50b8ae23c835760385188c0b`|
|17|[page-17.png](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/c3-final-render/page-17.png)|原Petrunia完整条目移入页首，其余四条参考文献顺延。目视：无断裂条目、缺字或越界；仍是正常参考文献尾页。|1158 x 1638|`a72540f9861027824246f7d4d07de8d50928e7416c3bbc42e2b2c9417cd1a838`|

## Section 7.4与后续边界

- 两版从“7.4 Does sample size explain the low-frequency losses?”至Section8前的整段提取文字，去页脚和空白后完全相同。页11/12的逐页文字本身也相同；没有发现根本内容变化。
- 因此沿用前次观察：7.4从第11页中部开始，文字在第12页上部结束；含当前图4和图注延伸至第12页下部，约在1.5正文页高附近。C4替换图后必须重新确认。
- C4原待办仍在：图4当前仍为旧controlled-grid图，Table6仍待更新；Figure1千分位轴格式仍待C4处理。本轮没有把这些预先声明的待办认定为已解决。
- 六个变化页均未见裁切、重叠、缺字黑块或不可读图表；没有新出现的空白页或正文孤标题页。此结论仅覆盖本次差异视觉检查，不是最终投稿包通过。
- 原检查文件 `notes/v9/c3-visual-review.md` 与原 `.scratch/v9/c3-render/` 未覆盖或删除。
