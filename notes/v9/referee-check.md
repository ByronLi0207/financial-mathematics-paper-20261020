# C5：42 项内部模拟审稿意见的实际处置核对

核读时间：2026-10-24；C4 提交 `e6a3c98` 后、C5 写法补充后。这里的“已改”只表示当前文件确有对应文字或产物，不表示科学缺口已经解决。没有把旧 response 的 ACCEPTED/PASS 当作本轮事实，也没有启动新审稿、Claude/跨模型审查、外部接触或新实验。

## 1. 来源、固定版本和判定规则

两套意见均为 **同一模型内部角色模拟**。V8 的三角色各五项为 M1–M5/F1–F5/E1–E5，共 15 项；P5 的 A/B/C 各九项，共 27 项（原分级 20 MAJOR、7 MINOR）。原 V8 15 项未逐项分 MAJOR/MINOR，本记录不补造分级。合计 **42 项全部保留**。

实际读取六份角色原文，再读取两份合表对齐 ID：

|来源|路径及原项起始行|SHA256|
|---|---|---|
|V8 M|旧 v8 `notes/v8/mock-methodology.md`；1–5 项起于 5/7/9/11/13 行|`24ba27b17b8891dea1365c0abd06f448c17e82d822aaa089b63270a207fb1438`|
|V8 F|旧 v8 `notes/v8/mock-finance.md`；起于 5/7/9/11/13 行|`a6a33d5a390a3e48cb428f7ec502d58019393b97fe191d42e53849c92fe65e1e`|
|V8 E|旧 v8 `notes/v8/mock-editor.md`；起于 5/7/9/11/13 行|`f59d1a095fa57f14155ca2b603c8291ecd687010667dc7a6800dee2b68a11d9b`|
|V8 合表|旧 v8 `notes/v8/mock-referees.md`|`8bcafcbcb7f8ef922ccee88199d7c47e9d31f6019f595b618c203185a85edc4c`|
|P5 A|当前 `notes/revision-v8/review-A-editor.md`；起于 5/13/21/29/37/45/53/61/69 行|`ccddcb21c75ad7c6ba2340fcea5a1717cfa3f390a5f692a45038a53730bfe5bd`|
|P5 B|当前 `notes/revision-v8/review-B-econometrics.md`；起于 7/15/23/31/39/47/55/63/71 行|`ded2bf701fcf03d11dbc19d4d3a0c3eddc6b8ba8aac0f2dc12cc26a8d52a6418`|
|P5 C|当前 `notes/revision-v8/review-C-risk-manager.md`；起于 9/17/25/33/41/49/57/65/73 行|`7480f5e9124732711ed03e13d2aacc7d49635df97e2bb9e3b45239029a51cd23`|
|P5 合表|当前 `notes/revision-v8/internal-review-2.md`|`bd1a57f39f83f8c43c853d50363c19a04dbbf8b2b68f8c4fd5652f61c770941c`|

“旧 v8”唯一指 `/Users/bingyouli/Research/论文/金融数学论文-v8-20261024`，只读，原 `revision-v8`/`f151b830489917ab7abc5137f2ec6b4135f55d6e`。P5 角色原文自述审阅基线为 WP5 完成的 `831d5fc763dbf29eb12ce293c46803b96bb470fb`；其中的旧行号和待 WP7 要求不当作当前位置。

下表的 **M** = [当前主文](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/submission-jof/manuscript.tex)，SHA256 `83c611692ecba07dd155d9792aa71870f9f9040f88cc9143c7ea639dd9278993`；**S** = [当前补充材料](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/submission-jof/supplement.tex)，SHA256 `65b8ca7cb427c225a33d9ca2f52dcfecc62fcf22e5958065000455705ee14c22`。主文以 C5 实际文件重新锁定，包含已落实的验证/选择限制、default benchmark 和 F3 测量补句，已不再使用 C4 的旧 `4d138feb...` 哈希。所有行号均为该快照的一基源行号；表/图同时给 label，避免后续分页改变位置。

[AUTHOR-TODO](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/submission-jof/AUTHOR-TODO.md) 已核读当前九项，SHA256 `84ed68116cbf5f9f12bce15fff27eb0f5b9eb84d049cdcae2863d9ce8deaaa67`。本表沿用其真实编号：T1 作者声明/rights；T2 独立/前瞻；T3 周度验证；T4 机制/失败；T5 测量/运营/价值；T6 public provenance/replay；T7 title/JoF；T8 PR3/4/5；T9 cleanup。T 编号是保留事项，不表示已启动研究；“无新增 T”只表示该条的写法问题可以用现证据处理。

## 2. 必须纠正的旧模拟前提

旧 M5/E3 的角色原文要求保留 17 complete/7 failed、P1/P3 未支持及 P2/P4 不可评估，这些要求仍有效。但其旧回应“平稳模拟未重现周度损失”只描述旧校准设计的完成格，**不能推广成两批平稳模拟都不产生大损失**。

当前 M `sec:intro` L39、`sec:extensions` L268/L272/L276/L278 已按事实改写：P5 受控 QR33/H6 在 W52 原已有 +113.5–135.5%，W260 有 +21.3–36.3%；新 C2 恒定控制 W52 为 +116.2%，切换为 +121.4%。旧校准设计在另一菜单/weekly clock 下的近持平不能替换它们。D0 准确名称为 **constant-variance AR(1) levels, where the peak depends on the current position**，不是无信号 null。

当前判断必须并列：N1 原始拒绝 7/13、Holm13 后 2/13；N2 `UNASSESSABLE`（W260 每 arm 一条必需 QR33 重复失败）；N3 `NOT_SUPPORTED`（恒定控制并非近持平）；N4 `UNASSESSABLE`（daily `NONREGULAR_NULL`、hourly `GARCH_OPTIMIZATION_FAILED`）。M L274–278、S `sup:v9-stability` L1607–1661 和 Tables `tab:v9-stability-diagnostics`/`-w52`/`-w260`/`-f` 已承载这些事实。不能说 C2 证明不稳定性造成实际损失，不能用 31 次成功重复或 12 条来源补成完整中位数。

## 3. V8 十五项：逐条实际处置

|ID|原质疑与当前处置|当前精确落点|仍存科学缺口 / 作者事项|
|---|---|---|---|
|M1|**已改标签。** 14.8/16.6 为 matched，rolling 与 later 双方 wrapped 15.0 分开；没有把早期原三惩罚回归写成 one-SE 规则。|M `sec:evaluation` L159–163；`tab:fx` L184–193；`sec:results` L175/L177/L198。|比较标签问题有实际回应；不因此取得覆盖或外部复制。无新增 T；相关科学外推见 T2/T5。|
|M2|**已保留推断分层。** 原 72-contrast Holm、two-main Bonferroni 和新 raw-HAC 族各自具名。Treasury 0.00761/0.320 未混用。|M `tab:diagnostics` L235–253（尤其 L240/L242）；S `sup:implementation` L1376–1384；`sup:v8-backcast` L1553–1569。|HAC 正则性、重叠和完整研究选择误差没有因多重调整而解决；T2/T3，非新增确认性检验。|
|M3|**已改并限定。** “recurring”只承载同记录匹配收益；2015 规则后于原结果，full-prefix 仍含旧窗口和旧 scoring。|M `sec:intro` L35；`sec:limitations` L311；S `sup:v8-backcast` L1524–1539。|独立交易商、真正前瞻 first-release 证据仍无；T2。|
|M4|**已明示短验证和负面。** 52 个重叠 validation origins、33 predictors+intercept、paired-HAC one-SE 及 181.4 最差格均可核。C5 又在 Limits 集中写了长验证未测。|M `sec:methods` L132/L136、`sec:evaluation` L159、`tab:weekly` L223、`sec:limitations` L319；S `sup:selection` L834–841/L867/L899–905。|不能证明该选参规则稳定或保住 F；更长 outer validation 仍未做，T3。|
|M5|**已纠正前提，保留失败。** 七个 D1 全格失败不是低准确率；旧 weekly 完成格不能支持“所有平稳设计近持平”。P5 和 C2 constant 大损失、N3 未支持、N2/N4 未知均明说。|M `sec:extensions` L268–278；S `sup:v9-legacy-mc` L1571–1605（Table `tab:v9-legacy-mc`/`-failures`）；`sup:v9-stability` L1652–1661。|频率/菜单/时钟/验证/创新律未解耦；机制未识别，数值资格和缺格未补；T4。|
|F1|**已限定报告用途；不建立政策。** 在观测路径上评分 passive reports，图表的动作是 validation benchmark。|M `sec:evaluation` L163；`sec:implications` L288–302；`sec:limitations` L317；S `sup:implementation` L1372–1374。|干预会改变路径、真实政策收益和生产连续性未测；T5。|
|F2|**不扩大外推。** 单 FX market-maker client-flow 与相关 public categories 保留不同单位和数据角色。|M `sec:data` L116–122；`tab:weekly` L211；`sec:limitations` L311/L313。|13 类不是 13 位独立交易商；T2。|
|F3|**定义与集中限制已改。** Data 明确 fair-value/long-minus-short；Limits 保留 gross/net 边界，并已补 valuation/reporting-composition changes 未与 trading 分开的句子。|M `sec:data` L118；`sec:limitations` L313/L317；AUTHOR-TODO T5。|估值/净额/报告组成没有被实际分解。补句回应了报告要求，不能把此科学缺口判作解决；T5。|
|F4|**已说明记录钟。** H 是 subsequent source records，FX gaps 改变 elapsed span，weekly/daily 是不同区间。|M `sec:methods` L128、`tab:methods` L152；`sec:limitations` L313；S `sup:v8-daily` L1492–1519。|未观测记录间峰值，不能映射成普遍运营 review interval；T5。|
|F5|**保留 joint-validation 边界。** score、strict hits、error amounts 分开，19:1 是评价偏好；不估资金或干预成本。|M `sec:methods` L128；`sec:results` L228–253；`sec:implications` L292；`sec:limitations` L317；S `sup:preference` L457–501。|实际货币效用、safe limits、交易/资金收益仍未评价；T5。|
|E1|**定位已改，标题保留有理由。** 主线是 bounded comparative peak forecasting；初等地板和 classical bound 为背景，非新方法。|M `sec:intro` L23/L31/L33–41；`sec:literature` L47–72；`sec:target` L92/L99。|标题选择/JoF 门槛归作者和外部编辑，T7；C6 letter 尚待本轮验收，不能算已完成。|
|E2|**不把 breadth 当独立复制。** 单 FX、相关 weekly system、同源 daily/重叠窗口均有实际限定。|M `sec:data` L116–122；`sec:limitations` L311–315。|新增独立 dealer/前瞻证据仍是 T2，不因增加表行而解决。|
|E3|**已改为正确第三条。** 保留旧 17/7/P1–P4 的局部结果，同时改掉“两个平稳模拟都没损失”的过时解释；当前第三条是 stationary short-history losses。|M `sec:intro` L39；`sec:extensions` L270–278；`fig:mechanism` L280–281；`tab:map` L302；S `sup:v9-legacy-mc`/`sup:v9-stability`。|N3 未支持；N2/N4 不可评估，constant 116.2 与 switching 121.4 不识别实际机制。T4；不得恢复旧“样本短本身无害”结论。|
|E4|**已压缩与分流，旧页/词数快照不继承。** Introduction 有三点；Related literature 未再重复三点清单。详细 grids 已在独立 Supplement 节，图源已换为 v9 文件。|M `sec:intro` L33–41；`sec:literature` L47–72；`fig:example` L27–28；`fig:mechanism` L280–281；S `sup:v9-legacy-mc`/`sup:v9-stability`；`notes/v9/c4-supp-layout.md`。|旧 132-word/15-page/25-page 不是当前统计。最终 writing counts/全包视觉与页限由 C7 再验，stage pending；T6/T7。|
|E5|**部分落地，阶段待办。** 当前 availability 指 revision-v9，restricted-input replay 与 document compilation 分开，五项个人占位符仍在。|M unnumbered Data and code availability L331–343；S `sup:reproduction` L1664–1705；AUTHOR-TODO T1/T6。|C6 README/letter/metadata 一致性及 C7 fresh-clone/remote equality 未在本表验收。T1/T6；原旧包 PASS 不迁作本轮 PASS。|

## 4. P5 二十七项：逐条实际处置

|ID / 原分级|原质疑与当前处置|当前精确落点|仍存科学缺口 / 作者事项|
|---|---|---|---|
|A1 MAJOR|**已改为反证。** 两个 regression 都只有 2/12 target gains、6/60 outside gains；没有另找 region 救回机制。|M `sec:extensions` L272、`fig:mechanism` L281；S `sup:v8-mc` L1457–1465、Tables `tab:v8-mc-full`/`-four`。|procedural completion 不等 scientific support；C2 constant 也有大损失，T4。|
|A2 MAJOR|**保留同源 daily 对照，不作纯频率识别。** 7/8 与 QR4 例外/多 breaches 同时出现。|M `sec:results` L208；`tab:map` L301；`sec:limitations` L315；S `sup:v8-daily` L1492–1519、`tab:daily-fx`。|history/horizon/cadence/features/target/span 联动仍在，T2/T5；C6 letter 的同口径检查 pending。|
|A3 MAJOR|**已披露重叠/检视。** full-prefix 不是第三次独立验证；1440 旧 origins 与旧 target exposure 均列出，旧缺项仍 NA。|M `sec:limitations` L311；S `sup:v8-backcast` L1532–1539/L1567–1569；Tables `tab:v8-backcast`/`tab:v8-backcast-complete`。|新独立时期事实上没有；T2。公开 replay 的验证另属 T6/C7 pending。|
|A4 MAJOR|**数学降为背景。** contribution 三条为经验发现；floor elementary，endpoint bound classical，命题/证明未删除。|M `sec:intro` L33–41、`sec:target` L92/L99/L106；S `sup:floor` L46、`sup:levy` L93。|方法新颖性不主张；编辑 adequacy 仍外部决定，T7。C6 letter 呼应 pending。|
|A5 MAJOR|**承认成熟评价工具。** endpoint/path-risk lineage、scores+coverage 前例、Murphy/quantiles 皆保留；dash 只表示未核实维度。|M `sec:literature` L47–53/L57–72；`tab:literature` L69。|部分文献阅读不证明不存在先例；T7。C6 letter 不得改称 first/new methodology，pending。|
|A6 MAJOR|**实证问题已前置。** conditioning 相对 matched history 的收益、reference 改变及 breaches 是主线，checklist 是后续含义。|M `sec:intro` L23–39；`sec:results` L175–208；`sec:implications` L286–303。|没有普遍机制、外部选模规则或录用保证；T2/T7。C6 的 JoF letter 尚待验收。|
|A7 MINOR|**反例未删。** daily QR4 例外和 H24 matched backcast gains、rolling reference-sensitive loss 均保留。|M `sec:results` L181/L208；`tab:map` L300–302；S `sup:v8-backcast` L1541–1550、Table `tab:v8-backcast-complete`。|不能将 H6 clearest pattern 写成 only-hourly/only-short-horizon 法则，也不救 P5 MISMATCH；T4/T5。|
|A8 MINOR|**实务限定已落实，位置依新规则集中。** sampled target 与真实运营对象分开，daily 自身 F breaches 仍可查。|M `sec:target` L78–89；`sec:data` L120；`sec:implications` L290–303；`sec:limitations` L313/L317；S `tab:daily-fx`（input L1510）。|不重复把八类限制塞回每个目标段；gross/cash/intraday/utility 仍未测，T5。|
|A9 MINOR|**主文/Supp 版本已改，发布链未偷判。** v9 新研究实际存在，不再写“本轮无新增研究”；个人字段保留。|M availability L336、author fields L338–343；S 导言 L28–33、`sup:v9-stability` L1607、`sup:reproduction` L1672–1689。|C6 README/letter/版本路线仍 pending；C7 exact public replay/remote bytes 仍 pending。T1/T6/T8。|
|B1 MAJOR|**成熟标签与未来选罚分开。** main 保留 i+H≤r；later-selected backcast penalties 和四个精确 penalty identities 在 S。|M `sec:evaluation` L159；`sec:limitations` L311；S `sup:implementation` L1345–1352；`sup:v8-backcast` L1524–1530。|fit 内 maturity 不修复整个程序当时不可得；real-time historical validity 未建立，T2。|
|B2 MAJOR|**两部分 frozen screen 都失败。** main 给 2/12 和 6/60；S 给 required ≥6/12 且 no outside，与 MISMATCH。|M `sec:extensions` L272；S `sup:v8-mc` L1457–1465；完整两张 72 行表 input L1469–1470。|不以新阈值/子集重画机制边界；T4。|
|B3 MAJOR|**不确定性单位与口径保留。** 32 streams、common innovations、72 overlapping issues、burn approximation、ratio-of-means MCSE 和 win bound 在完整 S。|S `sup:v8-mc` L1424–1455；M `fig:mechanism` L281 明确 left settings-range、right source-IQR；`sec:limitations` L319。|新主图不是原 MCSE 热图，完整估计/MCSE 仍在 S，未混成置信区间。有限精度/短段/固定 DGP 仍限制推断，T4。|
|B4 MAJOR|**local freeze 不作盲法保证；procedure contrast 不作 predictor 因果。** menu/selector/tie/failure 差异保留，research-stage selection 已在 C5 Limits 明写。|M `sec:evaluation` L167、`sec:limitations` L311/L319；S 导言 L28–33、`sup:v8-mc` L1436–1438、`sup:implementation` L1363–1384。|全研究选择调整和 feature-count identification 未建立；T2/T3/T4。|
|B5 MAJOR|**新八项 raw-HAC 单列。** 不继承旧 72-family Holm/HLN；0.055 不当 equivalence，也不声称确认性不显著。|M `sec:results` L181、`tab:diagnostics` L237–253；S `sup:v8-backcast` L1553–1569、Table `tab:v8-backcast-complete`。|依赖/HAC 正则性和 post-selection scope 未被 p 值解决；T2/T3。无新增重算或检验。|
|B6 MAJOR|**actual exposure 已披露。** 3071–10438 包含 8999–10438，旧 target scoring 覆盖 3071–10462；未把表块算独立 successes。|S `sup:v8-backcast` L1524–1539；M `sec:limitations` L311；Table `tab:v8-backcast`。|没有 fresh third period；T2。不能通过 narration 或选 gaps 创建它。|
|B7 MAJOR|**同源聚合及例外均保留。** 用实际 930/501 和 completed-day last-record clock，未采用规划约 780。|M `sec:data` L120；`sec:results` L208；`sec:limitations` L313/L315；S `sup:v8-daily` L1492–1519。|非 pure frequency effect，非新 dealer，非 intraday peak；T2/T5。C6 letter 同口径仍 pending。|
|B8 MINOR|**候选与程序状态已分别呈现。** 18431 COMPLETE+1 FAILED candidate、6912 complete methods 及 QR4 指定身份/选择机制均留。|S `sup:v8-mc` L1473–1485；`sup:implementation` L1363–1374；两张 MC 表完整分母。|不是“所有 fits 都成功”，也不是一次 selected procedure failure；无 retry。未证明执行规格外数值稳健/生产连续性，T4/T5。|
|B9 MINOR|**population bound、fitted hits 与 score 分开。** true quantile/independent symmetric increments 前提、atom/equality distinction 和 paired breaches 俱在。|M `sec:target` L92/L99/L106、`tab:diagnostics` L253、`sec:results` L177/L181/L208；S `sup:wp2` L946–953；M Limits L317。|拟合 report/F/ACI 无依赖下覆盖证书或安全运营保证；T5。|
|C1 MINOR|**实质边界已保留；不按旧位置重复。** sampled net-inventory 定义仍在，cash/gross/optimal operating 的限制按本轮规则集中 Limits。|M `sec:target` L78–89；`sec:evaluation` L163；`sec:limitations` L313/L317。|原建议“在 target 再加完整限制句”未照搬，有 v9 集中限制要求作为理由；真实运营对象/效用仍未测，T5。|
|C2 MINOR|**19:1 与成本解释已分清。** §5 首个 tau 设定旁给十九对一评价偏好；是否真实成本的限制集中 Limits，原 exact frontier 不改。|M `sec:methods` L128、`sec:results` L230、`sec:limitations` L317；S `sup:preference` L457–501、`sup:frontier-0`/`sup:frontier-8`。|并非估计 funding ratio、收益率或最优政策；不为重复旧位置要求而复制限制，T5。|
|C3 MAJOR|**新收益成对报 breaches。** full-prefix 416/282、daily 37/30 与 wrapped 329/328 各归实际比较；full H6/H24/QR33/QR4 表全在。|M `sec:results` L177/L181/L208；`tab:fx`；S `tab:v8-backcast`/`tab:v8-backcast-complete`（L1541–1542）、`tab:daily-fx`。|score 降低不转化为 safer limit；没有给新 backcast/daily 新做 wrapper。T5。|
|C4 MAJOR|**C5 已精准改为 default benchmark。** main 和 Table6 不再把 F 写成覆盖或生产默认；daily 行要求检查 F 自身 breaches。|M `sec:implications` L290/L301–302；`sec:limitations` L317；S `tab:daily-fx` 仍含 36/501、66/501 的 F 行。|不新增 formal coverage rejection，也不把较低 loss 当可部署；运营验证仍 T5。|
|C5 MAJOR|**same-source aggregation 不作频率因果。** physical histories/horizons/cadence/calendar/evaluation/target 联动一次集中说明。|M `sec:data` L120–122；`sec:limitations` L315；`tab:map` L301；S `sup:v8-daily`。|改变 reporting frequency 不能保证重现 ranking；T2/T5。C6 letter 的 source/frequency 措辞 pending。|
|C6 MAJOR|**clock 和 snapshot 已明确，位置依新规则。** Data 给非空日/partial boundaries/completed-day end，unknown timezone/vintage 与 close/intraday 差别留 Limits。|M `sec:data` L118–120；`sec:limitations` L313；S `sup:v8-daily` L1492–1508。|不从 fingerprint 推 first-release；不编时区/market close。finer actual exposures/vintage 仍 T5；没有因旧“挪回 Data”要求重复限制。|
|C7 MAJOR|**没有新增独立验证 credit。** nested inspected windows、later penalties 和 raw descriptive inference 都有位置，完整缺项继续 NA。|M `sec:limitations` L311；S `sup:v8-backcast` L1524–1569；Tables `tab:v8-backcast`/`tab:v8-backcast-complete`。|独立/前瞻证据 T2；公开精确 replay T6。C6 letter、C7 公开字节和最终包状态仍 pending。|
|C8 MAJOR|**按 method 分失败合同。** mandatory QR33 blocking、QR4 eligible-completed selection、failed selected evaluation 不替换及候选失败身份均明确。|S `sup:implementation` L1363–1374；`sup:v8-mc` L1473–1485；新 C2 complete/FAIL 表在 `sup:v9-stability` L1648–1655。|没有演示 future numerical failure 的 production fallback；原科研失败未修复、未重试，T4/T5。|
|C9 MAJOR|**map 为验证指南，不作普遍 eligibility rule。** main 新机制图/完整 screen 反证；daily 例外与 benchmark action、new constant/switching 欠完整结果同表。|M `sec:extensions` L268–281；`tab:map` L295–303；`sec:limitations` L315–319；S `sup:v8-mc` L1457–1465。|2/12+6/60 仍 MISMATCH；stationary loss 与 N3 未支持排除必要性叙述，实际机制仍未知，T4。无 deployment/volatility-necessity 保证，T5。|

## 5. 已通知 root 的集中限制补句与阶段状态

1. **已落实**：旧 M4/B4 的“短重叠验证/完整研究阶段选择”原先只在 methods/Supp 说明。Root 在当前 M `sec:limitations` L319 加了 short overlapping validation、research-stage selection 和 longer weekly windows untested；因此本表按实际改动记录，不再列为将来完成。
2. **已落实**：旧 C4/C9 的默认操作风险，root 将 M L290/L302 改成明确的 **default benchmark**。科学 coverage/operating-value 缺口仍 T5，不因措辞修改而关闭。
3. **已落实**：F3 的 valuation/reporting-composition channel 已由 root 在现 M Limits313 段补入“Valuation and reporting-composition changes are not separated from trading.”，T5 保留对应未来数据/识别缺口。该句已在上列固定主文哈希中，不再列为未来承诺；没有新增计算。

**C6 stage pending**：one-page letter、README、metadata/版本路线及作者信息/rights 的本轮一致性，尚不能用旧 v8 package PASS 代替。矩阵中 E1/E5/A4/A5/A6/A9/B7/C5/C7 涉及 letter/package 的部分均只记录待本轮验收。

**C7 stage pending**：最终数字绑定/引用/写法门槛、主文和 Supplement 的新终编、全页视觉、测试、package/fresh-clone 和实际远端字节核对，均未在本 C5 note 宣称完成。C4 本地 PDF 观察不是 C7 或 publication PASS。此 note 不授权 merge、关闭旧 PR、投稿或清理；分别仍有 T8/T1/T9。

**当前 coverage：PASS，42/42。** 六份原始角色文本和两份合表均已核读，42 个 ID 各有 issue、实际 disposition、当前 source/label/行号及 Limitations/TODO 或阶段待办定位，无漏项。该 PASS 只检查意见覆盖和处置可追溯性，**不表示 42 个科学缺口全部解决、C6/C7 已通过或期刊/外部审稿已通过**。已实施的文字回应、未解科学问题和未到的交付阶段分别保留。

## C6 后续实际收口

本表第5节的C6 pending为C5提交时点；C6现已完成letter/README/metadata/snapshots/ZIP本地验收，见`notes/v9/c6-metadata.md`及`c6-package.json`。上述42行的科学处置不变；C7最终全页/全测试/远端发布仍待实际执行。
