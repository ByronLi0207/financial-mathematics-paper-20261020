# v8 中文交付报告：研究窗口结束快照

状态：WINDOW_ENDED_PUBLICATION_PENDING。排程研究窗口已于2026-10-24T17:55:15Z结束，最后实际自检为17:55:52.403967Z。该文件是最终本地提交前的冻结快照，不能证明其自身之后才发生的发布。正式完成状态、最终远端commit和整树结论由PR5及最终对话报告的实际回读给出。以下数字回读已接受资料；没有新增金融分析。

1. 一句话结论

稿件已形成一篇保留失败证据的应用与模型验证研究，条件预测收益具有参照规则敏感性；新增研究没有证明普遍的窄条件机制、纯频率效应或独立第三时期。目标 Journal of Forecasting；现有证据不保证录用或具体发表档次。

2. 逐条合规表

表内 PASS 指工作包的执行及证据门槛，不等于原科学假说获得支持。

| 工作包 | 执行状态 | 证据及实质边界 |
|---|---|---|
| WP0 | PASS | wp0-gate-status.json、wp0-sync-output.json、wp0-three-commit-treatment.md：v7 底稿一致，新分支；三写作提交逐条处理。 |
| WP1 | PASS | wp1-before-after.md、wp1-rounding-green.json；最终写作指标见 review-r33-writing-metrics.json。 |
| WP2 | PASS | wp2-acceptance.json、逐图逐表清单；当前页核查链见 review-current-page-provenance.json。 |
| WP3 | PASS；科学判据 MISMATCH | wp3-acceptance.json、wp3-scientific-mismatch.json、冻结设计提交039f6f1；完整72格/方法与失败记录保留。 |
| WP4 | PASS；因果频率识别未达成 | wp4-acceptance.json、wp4-mismatches.json、冻结设计提交1427dc0。 |
| WP5 | PASS；独立第三时期 FAIL/MISMATCH | wp5-acceptance.json、wp5-mismatches.json、冻结设计提交467a995。 |
| WP6 | PASS | internal-review-2.md、wp6-acceptance.json：三内部角色27项意见，20 major逐条回应或明确限制；未用 Claude。 |
| WP7 | PASS；宣传性要求 MISMATCH | wp7-acceptance.json、wp7-cover-letter-response.md：按证据收窄摘要、贡献、解释图和结论，没有写成机制与频率识别成功。 |
| WP8 | PASS；公开金融复算 BLOCKED | review-r35-acceptance.json、完整pytest输出和资源收据、数字/编译/逐页/ZIP证据；REPRODUCING.md解释公开历史缺口。 |
| WP9 | 初次发布PASS，终版核对待实际完成 | wp9-acceptance.json和两次历史整树记录只证明各自切点；最终整树/保护引用证据待窗口结束后另附。 |

未删除文件、未合并main、未改PR3、未安装新软件；已冻结金融设计、原有两个primary、原结果与不利值均保留。收尾将再次核对。

3. WP3 模拟

每方法72格、每格32次；预设目标区为H6、W≥720、波动持续性≥0.9。支持判据要求目标12格至少6格达到清晰收益，且区外60格没有清晰收益。QR33、QR4均为目标区2/12、区外6/60，因此两方法均不满足。热力图显示同方差或较长期限也能出现收益，不能把原数据中的窄模式提升为普适机制。完整格、MC标准误和一次未收敛候选保留；判据是预设描述性pointwise MC筛查，不是家族错误率控制检验。主图/完整热力图由 results/revision-v8/wp3/ 拥有。

4. WP4 日频对照

固定同一FX来源，实际得到930个非空日、501个评估起点，历史F赢7/8。唯一QR4、W260/H6的约3%分数改善，破线37次，F为30次。观察图因此加入日频例外和各控制的破线要求，而不是“日频全部失败”。物理历史长度、期限、估计节奏、特征、评估跨度和目标随重采样共同变化；这是同来源聚合对照，仍不能单独归因于频率，也不是第二dealer独立验证。

5. WP5 三窗口

以下均为H6、原QR33；负损失变化表示该参照下分数更低。

| 窗口（均为H6／原QR33） | 起点数 | 对matched F损失变化 | 对rolling F720损失变化 | QR／matched F／rolling F破线次数 | 原始DM p：matched／rolling |
|---|---:|---:|---:|---|---|
| 原后期窗口 | 6625 | -14.77% | -12.66% | 376／360／332 | 4.47296e-09／2.19507e-07 |
| 既有较小早期窗口 | 1440 | -16.62% | +3.17% | 20／16／NA | 2.93732e-05／0.573583 |
| 扩展前缀窗口 | 7368 | -12.17% | -5.30% | 416／282／387 | 0.000435442／0.0550587 |


旧的rolling破线缺字段保留NA。扩展前缀包含既有1440起点，且旧H24目标区覆盖该前缀；三个窗口不能称为三个独立时期。扩展H24的QR33对matched F改善17.54%，却对rolling F720恶化2.73%，破线470对matched F275；H24 QR4对matched改善21.03%，破线355对275。这些结果要求把“只在短期限/小时频率有收益”改成参照敏感的记录内比较。新增8项normal-HAC DM为描述性事后比较，未校正完整选择过程；不拿raw p值认证独立、前瞻或全家族显著性。

6. 摘要与引言首段前后

展示仅将源文的LaTeX百分号和Figure引用转换成读者形式；原文逐字来源 wp7-before-after.md，已与v7/current源文核对。

摘要修改前：

> Risk limits on dealer positions concern the largest magnitude reached before a review horizon ends, rather than the position at its endpoint. We compare historical and conditional quantile forecasts of sampled absolute-position peaks for an FX market maker and weekly primary-dealer position aggregates. Simple historical rules prove difficult to beat. Long-history FX regression changes matched loss by -14.77% and -16.62% in the later and earlier periods. Its later advantage survives the evaluated finite delayed coverage correction. Before correction, however, regression breaches more frequently, while its ranking against a shorter-history rolling rule changes across periods. After stronger regularization, regression still loses 34 of 48 additional-panel comparisons. We formalize the known-floor target and apply a classical endpoint-to-peak bound under explicit assumptions. The results support joint validation of accuracy, breach behavior, and stability across reference rules, periods, and related series.

摘要修改后：

> Risk limits on dealer positions concern the largest magnitude reached before a review horizon ends, rather than the position at its endpoint. We compare historical and conditional quantile forecasts of sampled absolute-position peaks for an FX market maker and weekly primary-dealer position aggregates. Simple historical rules prove difficult to beat. At the shorter horizon, long-history FX regression lowers matched loss by 14.8% and 16.6% in the previously reported later and earlier windows. Its later advantage survives a delayed adaptive coverage adjustment (ACI). Before correction, however, regression breaches more frequently, while its ranking against a shorter-history rolling rule changes across periods. After stronger regularization, regression still loses 34 of 48 additional-panel comparisons. We formalize the known-floor target and apply a classical endpoint-to-peak bound under explicit assumptions. The results support joint validation of accuracy, breach behavior, and stability across reference rules, periods, and related series. A controlled simulation rejects a universal narrow-regime explanation, while aggregation and the overlapping backcast further qualify the empirical pattern.

引言首段修改前：

> A position can finish inside its limit after exceeding that limit during the intervening period, as Figure 1 illustrates. For a market maker, the relevant forecast therefore concerns the largest exposure before the next review, rather than the endpoint alone. The distinction changes the response variable, the observations available for training, and the interpretation of successful prediction. We study how established historical and conditional forecasts perform when every method targets this same sampled absolute-position peak.

引言首段修改后：

> A dealer's recorded net position can finish inside its limit after exceeding it earlier in the monitoring period, as Figure 1 illustrates. The forecasting question concerns the largest sampled exposure before the next review, rather than the endpoint alone. This changes the response and when its training label becomes available. We ask whether additional conditioning improves that peak forecast once historical information is matched, and whether the gain survives alternative references and breach assessment.

7. 写作量化指标

| 项目 | v7基稿 | 当前v8主文 |
|---|---:|---:|
| 摘要词数 | 139 | 164 |
| 统计口径内正文句数 | 215 | 244 |
| 平均句长 | 19.83 | 19.04 |
| 超过35词的句子 | 0 | 0 |
| 否定句比例 | 2.33% | 4.51% |
| 每句最多数字 | 2 | 2 |
| 超过1位小数的正文百分比 | 15 | 0 |
| changes … by | 5 | 0 |


否定句比例增加，不能报告成该指标下降。与篇幅预算不同，这组指标采用继承的prose排除口径；没有把4646个统计口径词误报成完整正文预算。

8. 篇幅与文件

完整正文4994词、摘要164词、合计预算5158；主PDF20页（含参考文献及未填作者字段；叙述/数据可用性止于17页），补充30页，独立作者模板1页；主图4、主表6。当前提交ZIP18成员，可单独编译文档并实际重建51页；不需要私人FX数据来编译文档。

- PDF：submission-jof/manuscript.pdf；补充：submission-jof/supplement.pdf。
- LaTeX：submission-jof/manuscript.tex、submission-jof/supplement.tex；包：submission-jof/overleaf-package.zip。
- 最新本地pytest完整发现：1335 passed，另1068 subtests passed，99.93s；外层100.350012917s、峰值RSS345292800B。原始输出review-r35-pytest-output.txt，未删去原始空格或改写测试输出。
- 主文535数字/32数字词、补充4983数字/109数字词，当前数字核对零失败/未解决/歧义；编译零error、未定义引用和缺字，补充保留28条underfull版面提示。

9. MISMATCH 清单

- 科学与前提：WP3窄条件筛查失败；WP4实际930而非约780、日频有例外且只能移植观察索引切分；WP5旧评估覆盖/窗口重叠、H24也有matched收益；cover letter不能声称机制已说明和频率已分离。
- 已纠正的表达/交付差异：WP0原比较家族72与旧报告71、陈旧页数；WP1避免两次四舍五入；WP7随机种子显示精度；WP8分数表重叠改排后补充30页；ZIP实际18成员；R9 penalty-menu、R30混合权重a、R33方法表指引、R35局部q/α/B符号定义。原失败材料保留。
- 时间：十分钟严格实际间隔未完全做到，11:55排程实际12:03:27，较上一实际自检间隔17分26.6秒；另有延迟，最终计时审计为60/60排程时点均有实际记录，无漏排程或重复；最大实际间隔1046.605892秒，最大迟到492.388881秒。严格实际十分钟间隔不达标，不能称十小时连续阅读/计算；没有补造或重写日志。
- 提交限频：此前本地切点与网页镜像分别限频，原文没有该双轨例外；合并时间线存在一小时内多次提交。本项不完全合规，保留实际commit与间隔，不改历史。现改用一个合并时钟，因此后续必要发布已排至10小时研究窗口之后，最终以真实回读为准；等待不计研究时长。
- 能力：公开浏览器分支是相同文件字节、不同Git历史，缺原本地冻结设计对象。公开clone完整金融复算及依赖这些对象的测试仍BLOCKED；未导出私人本地身份或削弱guard。

10. 待作者决定

兼容独立dealer与真正未见未来样本、公开安全的金融重放/设计历史方案、数据使用权、投稿新颖性定位和目标期刊适合度；真实运营成本与决策价值均待后续研究。摘要/结论中的“rejects”需作者考虑是否改成“does not support”，避免把MC描述性筛查读成家族控制的正式拒绝。作者身份、资金/利益冲突及期刊要求的个人字段必须由本人核实填写。未代作者撰写或填写AI声明；v7底稿已有的 `AI statement: [TO BE COMPLETED BY AUTHOR]` 未填占位仍在作者信息区，v8未新增该栏目。未替作者签署或投稿；缓存清理待另行授权。表中“Hourly / either history”与backcast适用配置、daily行“both controls”的具体对象，仍列为作者可进一步明确的两项标签问题；本轮没有据此新增模型、扩大配置覆盖或改结论。本轮不保证录用。

11. 发布

新PR： https://github.com/ByronLi0207/financial-mathematics-paper-20261020/pull/5 。最终commit、整树字节与main/PR3保护引用实证必须在最后发布后实际生成，不能预填在该冻结快照中。截至此草稿更新，九文档已核对远端224a2ee与本地f17f42c；两说明文件已在远端0f1f066逐文件验明，父提交及受保护分支均相符（review-rootguides-remote.json）。最后审计笔记、本地终切点与终版整树证明仍待实际完成。下一次任何提交不得早于18:01:01.942807Z，之后网页镜像还需统一时钟间隔。十小时研究窗口仍止于17:55:15Z，目标保持ACTIVE，后续必要发布不计额外研究时长。
