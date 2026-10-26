# 十二小时终稿合并报告（范围判定更正，公开交付版）

> 范围判定更正：2026-10-26T15:10:51.243191+00:00。上一版把额外旧v9重放预检的FAIL升级为WP8阻塞，范围判定过宽。本版按导师原文及WP6 C7既有JUSTIFIED_LIMITATION恢复本轮WP8范围；旧FAIL及原报告完整保留，未把旧驱动改成PASS，也未修复公开来源历史。原始登记对象3411可只读找到且是单文件、原字节匹配，但不是final-jof祖先。

> 时间口径澄清：2026-10-26T15:17:09.108580+00:00。72是原目标窗口对应的计划槽记录数，不是全部在截止前发生的实际检查数；71次实际在截止前，末槽迟21.439350秒。所有38个gap MISMATCH、首条未记interval和原UTC不变。

实际报告时间：2026-10-26T15:03:06.286573+00:00。目标窗口为 UTC 2026-10-26 03:01:52—15:01:52，即温哥华10月25日20:01:52—26日08:01:52。本报告在截止后生成。

## 1. 一句话结论

**WP2 的科学判定为 PARTLY；终稿已发布到唯一新建的 Draft PR #6，WP8 原计划列明的稿件验收及发布已通过，旧版 v9 重放预检仍失败但属于WP6 C7已明确保留的来源限制，并非本轮要求新增的重放任务。实际十分钟节拍保留 MISMATCH，因此仍不声称全部严格执行条件通过。** 2,215项全文测试及1,184个子测试通过，不等于所有真实历史验证器通过。

## 2. WP0—WP8 合规表

| WP | 判定 | 实际结果及证据 |
|---|---|---|
| WP0 双线合并 | PASS（历史环境限定） | B起分支后正常merge A；原科学3,844检查/2,186路径无差，两个原包保留。原18项失败及只读A历史对象例外保留。[执行日志](FINAL_MERGE_CHANGELOG.md) |
| WP1 统一论点 | PASS | 原8个论点子句逐项绑定证据，后续C9明确PARTLY；没有将机制解释写成已识别因果律。[中心论点](notes/final-merge/thesis.md) |
| WP2 CFTC 检验 | PASS（科学结果PARTLY） | 事前本地提交协议、唯一新模型批次、全部反例及NA保留，另一路标量算法按事前容差核验。[验收](results/final-merge/wp2-cftc-mechanism/acceptance.json) |
| WP3 统一图与决策图 | PASS | 482点逐点来源绑定、4,069检查无差；c=1成本角色初始误述已纠正。[成本角色修正](notes/final-merge/wp3-cost-role-correction.json) |
| WP4 合成主文 | PASS | v12骨架、历史长度机制段、A/B完整材料及超出部分保留。[验收](notes/final-merge/wp4-acceptance.json) |
| WP5 可读性 | PASS | 五句109词摘要、禁语0、当前语言指标达标，46段中文概括。[当前语言审计](notes/final-merge/wp8-post-requirement-language-audit.json) |
| WP6 三角色审稿 | PASS（同一执行者） | 编辑/计量/风控各7条，共21条；17个major均有处理，5项限制明确保留，未冒称独立审稿组。[处理表](notes/final-merge/wp6-review-dispositions.json) |
| WP7 投稿准备 | PASS（作者事项待定） | 5位候选审稿人、10问答、一命令重建6表4图、一页cover及title；未投稿或联系任何人。[验收](notes/final-merge/wp7-acceptance.json) |
| WP8 最终验证与交付 | **PASS（导师列明验收范围；旧版重放限制保留）** | 稿件、ZIP、全路径远端及PR正文验收已通过；额外真实v9运行计划预检FAIL。[完整远端树](FINAL_MERGE_ACCEPTANCE.json)、[PR精确回读](FINAL_MERGE_ACCEPTANCE.json)、[真实失败与定位](FINAL_MERGE_ACCEPTANCE.json) |

逐WP原命令和原输出保存在执行日志；本次复核修正、实际合并、真实失败与PR回读原输出另列于[后续运行附录](FINAL_MERGE_CHANGELOG.md)。完整63要求最终审计见[最终逐要求审计](FINAL_MERGE_ACCEPTANCE.json)；旧预发布审计原字节保留。

## 3. 中心论点与标题

在成熟标签历史和重拟合时点匹配的比较下，历史分位数规则在这些头寸记录中总体有竞争力。条件模型的得分优势随历史长度、收缩和成本偏好变化；现有结果与估计成本解释一致，但没有识别单一因果机制，也没有得到普适“足够长”的历史界限。同W不代表全部原始/验证信息相同，aggregate来源不代表相互独立的交易商样本。

选定标题：**When Is History Long Enough? Conditional Quantile Models versus Historical Rules for Peak Net-Position Limits**。

## 4. CFTC 机制检验与反例

协议本地提交 `effa537bd6d9b89855002aa79f95f62f9ff3761c` 的实际时间为UTC03:32:15，早于唯一新运行的03:32:28.372451；协议SHA保持 `9036b0f599dd8dbef6ae9232a5f0389c5f61cde535e33f37188e1a65de59d9cb`。这是本地事前登记，公开原生快照不证明对外事前登记。

| 判据 | 实际结果 | 判定 |
|---|---:|---|
| P1：短历史区损失比例达到事前80%门槛 | QR33：29/34；QR4：15/17 | 两者SUPPORT |
| P2：QR4高区胜率至少60% | 10/17=58.8235% | NOT_SUPPORT，不能四舍五入过线 |
| P2：QR33高区 | 无合格格点 | NOT_TESTABLE |
| 次要P3：两步W增长都严格改善，至少70%市场 | 6/17 | NOT_SUPPORT |
| 事前综合规则 | P1通过、QR4 P2不通过 | **PARTLY** |

QR4在W520仍有7个不利市场：`044601、043602、042601、045601、099741、095741、232741`；P3有11个反例。全部153条评价轨迹、102组比较、25条筛选层面反例记录均保留，25不是25个不同市场。315,512个标量检查在事前绝对/相对容差内无不匹配；最大绝对舍入差1.1920928955078125e-7对应很大的LRV，不冒称逐位完全相等。该第二算法仍由同一执行者运行，不是第二求解器或独立金融复现。[完整结果与反例](notes/final-merge/wp2-cftc-mechanism-results.md)

## 5. 摘要修改前后与量化指标

**修改前（WP4稿，10句175词）：**

Dealers monitor the largest absolute position reached before a review horizon ends. We compare conditional quantile models with historical rules using hourly FX positions, weekly New York Fed positions and dealer aggregates in 17 CFTC futures markets. Histories and update schedules are matched. Historical rules are hard to beat. First, FX regression lowers matched loss by 14.8% and 16.6% across two periods, but its ranking against a shorter rolling rule changes. Second, historical rules beat regression in 34 of 48 New York Fed comparisons and 29 of 34 CFTC comparisons; finite-penalty hindsight still favors history in most short weekly comparisons. They usually remain in the model confidence set alongside alternatives. In calibrated simulations, expanding the penalty menu cuts the constant-parameter median excess loss from 116.2% to near zero; switching adds no observed median loss in this short-history comparison. Third, in CFTC, lower scores need not mean lower limit costs: higher reserve charges and lower fixed breach charges generally favor expanded regression. The evidence is retrospective, and the original FX evaluation period had been inspected beforehand.

**修改后（当前稿，5句109词）：**

Position limits concern the largest sampled absolute net position during a review period, which an endpoint forecast can miss. We compare historical and conditional quantile forecasts using one FX market maker's positions and aggregate dealer records from the New York Fed and CFTC. Historical rules are difficult to beat across these records, while longer-history FX gains coexist with adverse weekly outcomes and important exceptions. Simulations, learning curves and the partly supported CFTC check are consistent with estimation costs varying with history and shrinkage, while causal attribution remains unresolved. Practical validation should compare scores, breaches and stated limit costs against matched historical benchmarks, since different charges can favor different procedures.

| 指标（同一冻结计数规则） | 修改前 | 当前 |
|---|---:|---:|
| 摘要句/词 | 10/175 | 5/109 |
| 正文句均词数 | 15.515244 | 19.08510638 |
| 单句数值个数上限 | 13 | 2 |
| 显式语法否定句 | 47/328，14.329268% | 3/329，0.911854% |
| 禁语匹配 | 6 | 0 |

这些是写作指标，不把减少语法否定当作删除不利结果；PARTLY、所有失败/NA和识别限制均保留。WP5历史检查点的2/322等旧指标有自己的日期，不混称为当前稿。

## 6. 篇幅与实际文件

主文**6,160 body words、21页**；补充材料**25页**；title和cover各1页，共48页编辑材料；**6张主表、4幅主图、35条参考文献**。6,160按排除表格/参考文献的既定body口径计数；含图表的PDF文本8,433和更宽TeX控制口径9,051另列，不互换。

当前源ZIP27成员，SHA-256 `35b63bebf4f1d6465a54d16c3059ed276f30dcf2928aa79771ecb1fd80bce22a`。Supplement工作区与独立解包编译的25页文本/像素一致；本次仅第5页变化且直接查看，其余页面以精确同一性衔接此前直接检查。5项继承underfull警告保留，严重编译诊断0。

- [主文PDF](submission-final/manuscript.pdf)
- [补充PDF](submission-final/supplement.pdf)
- [源文件ZIP](submission-final/overleaf-package.zip)

## 7. MISMATCH 与未修复边界

1. **真实旧v9重放预检仍FAIL。** `RUN_PLAN_NOT_SOLE_FILE_COMMIT`：先前036和新c982都由路径日志选中 `51b5f119...`，它是2026-10-24的C7七路径公开快照。该限制不是本次merge或S7文字回归；7个真实设计检查PASS、WP2登记及528边界hash精确，也不把此失败改成PASS。旧冻结驱动/历史没有修改来掩盖问题。
2. **时间要求不作完美合规声明。** 目标窗口已满；目标窗口对应的72个计划自检槽均有实际记录：71次实际发生于截止前，截止槽实际在UTC15:02:13.439350完成、迟21.439350秒。按这72个计划槽归属统计，其中gap>600秒MISMATCH 38次，PASS 33次，首条interval字段未记录。最长实际间隔759.800095秒；没有补填漏槽或伪造时长。125个不同复核轮次完成，但不能据此证明12小时连续净研究；纯研究秒数仍null，锁屏、发布、调度和短timer等待均不算研究。
3. **原始科学负结果保留。** A模拟P1 47/48、P2 21/24；P3全称不支持，6反例。金融长W/长H有两模型都输、左删失NOT_TESTABLE；尾部失败UNDETERMINED。旧受控比较各回归仅2/12目标收益且有6个区外收益，原screen MISMATCH不被新WP2 PARTLY覆盖。
4. **解释纠正保留原错误。** c=1原被误称reserve charge，已纠正为exceedance-magnitude charge；Figure2图注结论、旧WP1 pending历史语境、S1分位数尾参数别名和S7历史/未来方向文字已修正，原字节和失败记录保留，未改数字/协议。
5. **早期测试/工具失败没有删。** WP0初始18fail、审计器路径/正则RED、写作替换字符串提前失败、S16图表位置及最近reportlab收集ERROR均留原记录。最近通过使用既有缓存和既有bundle路径，没有安装软件；旧UV的no-sync被忽略警告和新空overlay限定如实保留。
6. **发布观察失败与冲突已定位。** 原锁屏/普通Git无身份/集成403不绕过；原生恢复后才发布。提交后Processing/导航ERR_ABORTED没有引起盲目重发。4个add/add冲突只按已验真的批准公开字节解决。平台曾短暂mergeable=false后同head/base变true，没有因此合并main。PR的LF/CRLF差异明确序列化验证，非静默归一化后冒称原字节相等。
7. **来源、独立性和权利仍有限制。** 本地历史对象只读例外、公开快照未导出本地A/B merge和登记身份、独立金融/交易商复现、FX权利、NYFed旧raw例外、旧详细source audit与旧时长充分性均未修复。原始FX/私有预测向量未上传。
8. **文献范围不夸大。** Delft本任务新全文尝试新增正文0页，不抹去B线已有59/60/68等选读位置，也不证明不存在前人；closest work与其他文献的元数据、选定段落和未取全文范围分别保留。未宣称所有35条参考文献都已全文通读。
9. **私有审计文字修正也留痕。** 第121轮“unpenalized slope”更正为zero slopes/unpenalized intercept；本轮审计器最初把决策文件的历史点误指5f9，实际gitshow证明在69。均为记录修正，不是科学数值变化。

## 8. 建议审稿人、作者待决定及旧PR

候选5人：Tilmann Gneiting（HITS/KIT）、Raffaella Giacomini（UCL）、Roger Koenker（UCL Honorary Professor）、Fabian Krüger（KIT）、Robert F. Engle（NYU Stern Emeritus）。官方身份与已引用论文的关联已查，私人利益冲突、邮箱、可用性仍需作者确认；邮箱均为`[author to verify]`，没有联系。Gneiting/Krüger及Giacomini/Koenker的关系须考虑名单多样性。[候选人及官方来源](notes/final-merge/suggested-reviewers.md)

作者姓名/单位/ORCID/资金/利益冲突及期刊声明仍为待填写，不编造作者或AI声明；FX权利和未来独立复现仍待处理。新PR说明取代#3/#4/#5，建议作者以#6作为终稿审阅入口；是否关闭旧PR由作者决定，我没有编辑、关闭或合并它们。[待用户决定](USER_DECISIONS_FINAL_MERGE.md)

## 9. 新PR、实际最新提交与目标状态

唯一新Draft： [Final consolidated JoF submission — PR #6](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/pull/6)，base main、head final-jof、open/unmerged。

- **远端内容提交**：`ab99cdf2234e7841c46b51b720fea3c8ac48df51`，UTC13:47:45。
- **本地正常合并提交**：`c982de97e499c686fbdf2950fafe2455f157847f`，UTC14:47:59；双亲036ad9f2...和ab99cdf...，工作区干净。
- **共同内容树**：`d42e835ca6618f18fc63a4c590612a13bc4a2bd1`，6,056路径逐mode/blob/bytes SHA通过；不声称本地merge身份已在公开历史中。
- **PR正文实际更新时间**：UTC14:51:31，独立精确读回14:51:54.957812。12,948 LF字符对应平台13,004字符/56CRLF；实际rawSHA `9452f6da29c63732c401c99b81bccfffc24624f7fefffaf62d0819f876d509e3`。

上述提交号和目标状态属于本报告15:03—15:17UTC的实际检查点。后来Goal曾因不可回改的历史节拍偏差被标记BLOCKED，并由用户恢复；本次只完成尚未同步的公开交付记录，不把恢复状态解释为接受原偏差，也不把全目标改写为PASS。后续文档提交身份以本分支Git日志及PR #6的实际内容为准。


## 本次逐项收口（截止后公开记录补齐）

实际准备时间：2026-10-26T21:06:09.023371+00:00。原中文报告和原UTC记录完整保留；本公开版只把本地绝对链接转换为仓库内链接，并更新以上有日期边界的状态说明。已完成的正文、结果、协议、PDF和源ZIP不变。最后一版编译、测试、远端和PR验收的原命令与原输出已追加到 `FINAL_MERGE_CHANGELOG.md`；结构化证据见 `FINAL_MERGE_ACCEPTANCE.json`。原12小时自检MISMATCH、旧重放来源限制、作者身份/权利/私人冲突等事项分别保留。
