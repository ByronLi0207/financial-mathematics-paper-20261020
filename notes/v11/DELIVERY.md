# v11 定稿交付与边界

本轮以 v10b `de1a1cf` 为底，只在 `revision-v11` 整合原已计算证据；来源固定 `60e03b8`。目标窗口为2026-10-25 05:01:20–07:01:20 UTC，完成1–5项后的时间只用于英文与APA校对。最终远端提交和整树一致性由发布后读取确认，不在本文件内自引用自己的提交SHA。

## 导入裁定

- WP2：原设计早于正式运行，30,536个成员通过本来源自己的回执校验；静态导入Table S47。47/48、21/24两条支持，以及42/48未满足的普遍排序预测全部保留，候选失败与反例不删除。
- WP3：设计早于正式运行，保存结果回执通过；用户指定的两位小数锚点−2.12%和−14.77%完全一致，导入正文Figure 2。未舍入百分比受聚合次序影响在binary64末位不逐位相同；严格初稿FAIL保留，底层损失均值、配对均差与破线数相同，不修补结果、不声称百分比bitwise一致。
- WP4：自己的数据/图指纹通过，但制图合同23:49:08晚于首次渲染23:42:24和所选v5渲染23:46:39，按本轮门槛不导入。不绘替代图。
- PR5标题、摘要、主线不导入。详见[来源核查](import-audit.md)、[逐数字绑定](imported-number-bindings.json)及[原始提交证明](original-commit-proofs.json)。

## 新正文小节

### How much history does FX regression need?

The fixed-period, short-horizon learning curve shows that more history helps only over part of the tested range (Figure 2). Full regression moves from higher loss at the shortest history to its largest matched gain at an intermediate history. The gain is smaller at the longest history, while the four-feature curve changes sign within the tested range. Both curves use the original FX period and their original penalty menus; regression is compared with its own matched historical reference at each history length. Supplement Section S35 retains the full contrasts and synthetic confirmation summary. Together, the history and menu comparisons link conditional gains to history length and the availability of strong shrinkage.

## 贡献第1条

First, matched FX gains recur, but rankings against a shorter rolling rule change. The period comparisons separate conditioning gains from the reference procedure (Table 3). Delayed calibration preserves the later matched gain while changing breach behavior. Within the original FX period, the full-regression learning curve improves at intermediate histories but gives back part of the gain at the longest history (Figure 2).

## 文档、校对和核验

摘要与标题保持v10b字节一致，摘要161词、8个数字。正文/补充/标题页/投稿信页数分别为20/34/1/1；新小节连同图注约占半页，低于0.75页。为守住正文页数，原全前缀稳健性段和组合结果句逐字移至补充S26与S18，所有数值保留。

|写法指标|v10b|v11|
|---|---:|---:|
|保守措辞句占比|3.48%|3.44%|
|平均句长|12.24|12.55|
|超过40词句子|0|0|

共记录148组、164处编辑：英文106、APA/书目同步50、排版/交叉引用/显示镜像8处。计数包括源文、书目和显示文字同步，并非互异的可见句子数。一个未使用、未跟踪的旧显示文件曾漏做写前备份，已恢复原SHA；其初次记录和恢复收据保留，不计入最终编辑、不发布。详见[逐处校对日志](proofreading-log.md)和[排除恢复记录](proofreading-rollbacks.json)。

34篇参考文献的作者/年/卷期/页码/DOI按原始出处核对；未改变科学数字或书目数字字段。作者及AI声明全部占位保留。[APA 1](APA-review-part1.md)、[APA 2](APA-review-part2.md)。

四份PDF全部重编译，56页均有实际看图证据；最后12个变化页重新逐页查看，44张字节相同图像复用此前实际审阅。[最终构建](final-native-build.json)、[正文闭合审阅](visual-closure-main.json)、[补充闭合审阅](visual-closure-supplement.json)。完整原环境测试最终再次通过1,715项和1,181子测试；命令和原始输出摘要见[closure-tests.json](closure-tests.json)。

数字审计覆盖2,077个受保护科学文件、18个原样导入文件、76条JSON数值绑定、15张既有生成表、4个正文内表、6个原图PDF及全部34条书目数字字段，均通过且没有新实验。[闭合完整性收据](integrity-closure.json)。

公开裸克隆的30项旧历史对象缺失失败原样保留；补齐三份原始历史对象后不改测试的全套复跑通过。公开原生源码包可独立编译；这两种复现范围分开披露，见[TESTING.md](TESTING.md)。

## 版本管理建议

[CANONICAL.md](CANONICAL.md)指定v11为唯一投稿入口。旧分支只读保留/归档，PR3/4/5建议待作者确认v11后关闭但保留证据分支；main是否合入另由作者决定。所有操作都只是建议，本轮没有开PR、关闭PR、合并或删除。

候选标题“When Is History Long Enough?”、作者/AI信息、WP3未舍入百分比解释、WP4缺少事先合同、Wisniewski论文年份来源及安全公开历史对象路线，全部列在[待用户决定](PENDING.md)。

比较入口：[v10b…v11](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/compare/revision-v10b...revision-v11)。

最后一轮公开源码包独立编译的56张图像和文字均与已审阅定稿一致，见[最终公开源码包回执](public-source-package-closure.json)。最后的全文逐页英文复读未再改源文，见[语言闭合记录](language-closure.json)；拼写检查通过，见[拼写回执](spelling-closure.json)。
