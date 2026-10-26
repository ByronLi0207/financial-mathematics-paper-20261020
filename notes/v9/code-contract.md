# C0：PR #5 代码、数据与 Git 身份合同只读映射

核对时间：2026-10-24 18:06–18:14 UTC。对象是新 clone 的 `revision-v9`，起点 `0f1f066843e0c49cf3e24bce7d72032dc189603d`。本记录只做源文件、协议、归档 receipt、输入字节数/散列和 Git 对象存在性的读取；没有运行断点诊断、拟合、校准、模拟、预测、统计检验或 pytest。没有改动旧目录、旧 refs、源代码或归档结果。历史对象的本地导入由 root 统一处理，本审计未导入。

## 1. 可复用函数及边界

下列路径均相对本 v9 clone；所列行号为 C0 时的源文件行号。

| 路径/入口 | 可复用合同 | 注意事项 |
|---|---|---|
| `v8_mechanism_mc.py:35` `simulate_level_garch(z, phi, omega, alpha, beta, burn_in)` | 外部给定创新向量，生成常参数 level AR(1) 与 GARCH(1,1)，返回 burn 后 `position/variance/innovations` | 入口拒绝 `abs(phi)>=1`、非正 omega、负 alpha/beta、alpha+beta>=1；没有参数估计、截距、分段或 t 分布采样。首个方差固定为1，先前 level0。不能把它描述成已存在的 AR-GARCH-t 校准器。 |
| `v8_mechanism_mc.py:59` `repetition_normals(rep, design)` | `PCG64(SeedSequence(master_entropy,spawn_key=(rep,)))`；返回完整标准正态创新、初/终 RNG state | 固定32个rep，不能把新的 t 随机数说成该函数原样生成。 |
| `conditional_features.py:35` `build_features(...)` | 因果33特征，显式给 RMS 与 nominal gap；返回 `FeatureSeries(values,short_rms,valid_from)` | 无 I/O、无全样本标准化；valid=max(24,short,long)。 |
| `conditional_features.py:68/82/94/102/108` | 训练池标准化/查询变换、成熟训练索引、refit anchor、响应尺度 | 训练 origin 精确为 `r-H-W+1..r-H`；不得包含未完成标签。 |
| `study_core.py:70/80/229` `exact_rank/order_statistic/build_label_cache` | 整数修正秩、非插值次序统计量、含当前状态的完整峰值/头寸余量标签 | `peak[t]=max(abs(N[t:t+H+1]))`；`headroom=peak-abs(N[t])`；末端不完整标签不出现。 |
| `v8_mechanism_mc.py:95` `forecast_report(...)` | 同一完整连续 origins 网格上计算且仅计算 F、QR33、QR4；可传 checkpoint；返回 capacity、refit_indices、fit_diagnostics | 这是纯计算，无 I/O；传入真实数据会产生新的真实预测，C2 不应这样调用。合成序列可复用。 |
| `v8_mechanism_mc.py:70` `select_candidate(...)` | 两回归各自原有菜单、失败与 tie 规则 | QR33 与 QR4 不同，见下表。 |
| `conditional_quantile.py:166` `fit_quantile_ridge(...)` | 原始 ridge quantile ADMM solver，截距不惩罚 | 不修改容差/初始化/重试以救回失败。 |
| `conditional_study.py:205` `score_predictions(...)`；`study_core.py:403` `stable_mean(...)` | 最终 projected capacity 的 tau19/20 pinball 和严格 breach `peak>capacity`，完整 origins | 可按 WP3 closure 复用，而非调用含额外模型的原始 driver。 |
| `run_v8_wp3.py:376` `evaluate_method(...)` | 依次执行所有冻结验证候选，再执行一次所选参数评估；完整失败 receipt；无替换参数 | 这是带输出的编排函数，非纯函数；新 v9 须提供新输出位置和自己的设计身份，不能调用旧 `--run` 覆盖归档。 |
| `run_v8_wp3.py:344/367` `scalar_diagnostics/maturity_summary` | 只保存有限标量 fit/maturity 诊断；可回读训练成熟边界 | 非有限或非标量诊断不能伪装成完成。 |
| `v8_mechanism_mc.py:175` `summary_from_repetitions(...)` | 保留全部计划 rep，统计完成/失败/未尝试，缺任一rep则 full procedure NA | **它计算均值损失之比，不计算中位数**；不可将其 `relative_loss_percent` 用作 C2 N2/N3 所称中位数。 |
| `run_v8_wp3.py:209/234/242` `ResourceCheckpoint/kill_owned_worker/wait_owned_worker` | 同时检查本地与全局时钟，终止自己创建的进程组，节流真实线程探测 | 新墙钟预算必须在 v9 设计中明载；旧 RunGuard 内部540s是硬编码。 |
| `v8_daily_fx.py:39` `resample_closed_days(position,times)` | 确定性日频聚合，无 I/O、无拟合；返回不可写 `DailySeries` 及元数据指纹 | 只应复用聚合部分供新诊断；不必调用 WP4 预测 driver。 |
| `v8_daily_fx.py:82` `daily_issue_geometry(n,h,w,design)` | 冻结日频验证/评估边界，样本不足时 NA | 不会移动cutoff、缩短W或填补日期。 |
| `conditional_sources.py:155` `load_source(path,source_id,expected_sha256=...,expected_bytes=...)` | 已有本地 FX/Treasury 字节散列和 schema 先验证后解析；返回不可写数组 | 只支持 fx_hourly/nyfed_weekly，Treasury行必须是PDPOSGS-B；无网络。 |
| `study_data.py:404` `load_source(...,fetch=False,...)` | WP4实际所用的严格FX pinned reader | 明确 `fetch=False`；不能因缺本地文件触发下载。 |
| `round2_panel_sources.py:11` `align_source(raw,key,grid)` | 对指定经济日期网格作一一匹配，拒重复、错key、非有限值、缺日期 | 该函数自身不检查SHA，调用者须先按清单验证raw bytes；不能用当前API重下载代替旧版本。 |

## 2. PR #5 WP3 的精确冻结设定

权威文件：`protocol/revision-v8/wp3-mechanism-design.md` 和 `.json`；归档 manifest `results/revision-v8/wp3/manifest.json`。WP3 是**没有从真实序列估计参数的正态创新平稳机制网格**。

- DGP：`N_t=phi*N_(t-1)+epsilon_t`，`epsilon=sqrt(v)*z`，`v=omega+alpha*epsilon_prev^2+beta*v_prev`；phi为0.7/0.9/0.98；p为0/.9/.98。显式参数分别 `(omega,alpha,beta)=(1,0,0),(.1,.05,.85),(.02,.05,.93)`，不能重新做二进制差值计算替换常数。
- 初始化：previous level0，第一方差1；burn-in20,000，retained3,264；是长burn近似平稳，不是精确平稳抽样。保留时钟从2000-01-03T00:00，每条记录3600秒。
- 网格：W52/260/720/2880，H6/24，共72 DGP/W/H格。方法仅F、QR33、QR4。C2指定W52/260、H6是新设计子集，不应重跑旧72格。
- 特征：signed levels lag0..24，abs(current)，increment RMS24/168，hour sin/cos，weekday sin/cos，gap>3600；valid_from168。QR4列 `[25,0,26,27]`，没有更早特征有效期的特权。规则适用于原WP3；周度真实实验自身的RMS6/26、refit13属于另一合同，不能悄悄替换。
- 训练/更新：在refit r用精确W条成熟origin `r-H-W+1..r-H`。refit_step24，验证与评估各自在段首重新anchor。训练池、transform、response scale和系数在块内冻结；查询特征与floor始终使用当前issue。早先已成熟的评估标签可进入后续refit。
- 验证3072..3143，共72 issue/3 blocks；评估3168..3239，共72 issue/3 blocks；最长验证标签H24结束于3167。W2880/H24最早训练origin169，超过valid168。
- 32次rep，master entropy2026102408；每rep完整normal vector被phi/p/W/H共用，rep间分开；保存初/终RNG state。函数库存rep0..31，不能动态增加。
- solver：max_iter10000，atol1e-6，rtol1e-5，gap_rtol1e-6，rho=1/n，截距不惩罚；同时满足ADMM primal/dual residual与可行dual Fenchel gap。初始化beta全0、截距为训练响应tau分位 `inverted_cdf`，residual=y-Xbeta，scaled_dual0；没有warm-start选项。
- QR33使用训练池均值/总体SD；重复常数列center为重复值、scale1。QR4保持原C-order `[25,0,26,27].copy()` 算法；response scale为 `max(mean(headroom),1e-6*mean(abs(anchor)),1e-12)`。最后capacity为 `abs(N_issue)+max(0,predicted_headroom)`，非有限预测报失败。
- F使用 `ceil(19*(W+1)/20)` 的成熟own-anchor headroom，非ordinary rank；W52为51，W260为248。F的headroom在refit block内冻结，floor当前更新。

| 方法 | lambda菜单 | 验证失败政策 | 精确tie |
|---|---|---|---|
| F | 无 | 不调参 | 无 |
| QR33 | .001/.01/.1 | 任一mandatory候选失败则该procedure INELIGIBLE | 较大lambda |
| QR4 | .001/.01/.1/1/10 | 可在完成候选中选；全部失败才INELIGIBLE；失败候选保留 | 递增菜单首个lambda |

I不是WP3菜单之一。`empirical_headroom.py:26/36` 是同时计算ordinary I与corrected F的原始双报告helper；不能为了只取F而悄悄多算I。WP3的 `forecast_report(...,'F')` 是只计算修正F的既有入口。原始 `conditional_study.historical_forecasts` 还会计算S/K等，不适合C2限定菜单。

WP3的summary是 `100*(mean(A)/mean(B)-1)`；delta MCSE为 `100*sd(A-rB,ddof1)/(sqrt(R)*mean(B))`。win严格A<B。任一计划rep的所选评估不完整，full-procedure cell NA；可用配对值仅能标成conditional on completion。C2的“某格失败整格失败”如何定义到source/state/W/method/rep应由新设计明载，不能误把旧QR4候选允许失败政策理解成重试。

## 3. Runtime 与编排合同

WP3：rep升序，再phi、p列表序，W升序、H6再24，F/QR33/QR4；一个worker处理一rep/phi/p，共288 worker blocks，每块8个W/H、24 method reports。32*72*3=6912计划method reports，candidate库存始终完整。`run_v8_wp3.py:269` 在生成任何随机数前先验证Git设计、写manifest并封code/protocol hashes；worker再次核对sealed bytes。

原预算：数值线程1、实际OS threads<=2，内部RSS1.5GiB/公开cap2GiB，内部worker540s/hard600s，全局3600s且中断在途worker。`run_study.RunGuard`只在Darwin上可验证资源，非Darwin会RESOURCE_UNVERIFIED；array单个64MiB/总128MiB也有限制。root的新C2预算和2rep试跑/降阶规则必须在新设计中冻结，旧runtime receipt只是规划参考。

`notes/revision-v8/wp3-original-runtime-fields.json` 的六条旧真实实验receipt仅供参考：QR33 W2880 H6/H24验证11.057/7.752秒，评估15.827/13.328秒；QR4每格包含5候选+所选评估，54.004/49.732秒，不能直接横比速度。这不是本轮计时。

现有WP3 manifest记录Python3.12.14、NumPy2.3.5、SciPy1.18.1、pytest9.1.1。现有full-suite receipt以uv临时环境装pytest/arch/scikit-learn，UV_OFFLINE=1、单线程；`requirements.txt`只锁numpy2.3.5/reportlab4.4.9，不能据其推断完整研究环境。本机默认 `/Library/Developer/CommandLineTools/usr/bin/python3` 只读元数据检查显示numpy/scipy/statsmodels/arch/pytest/scikit-learn/matplotlib均缺失；不要往它装包。既有uv和bundled Python路径存在。

`notes/revision-v8/run_full_pytest.py` 会写入旧 `notes/revision-v8/<stage>-pytest-*` 且复制tracked files，不带.git；复制目录在repo下，Git会向上找到父repo.git。**不应直接用它覆盖v8归档输出**。新v9测试若复制tracked files，尚未tracked的新测试不会进入copy；新runner需如实处理。

## 4. WP4 日频聚合与截止点

权威设计 `protocol/revision-v8/wp4-daily-fx-design.md/json`；实际调用见 `run_v8_wp4.py:252–324`。先以pinned bytes加载原FX，再调用 `resample_closed_days`；不是从公开聚合结果反推原始序列。

- 原timestamp按source-naive `datetime64[D]` 分组，不转换时区，不宣称UTC/exchange time。严格原顺序；每个非空日取最后记录。日内最后一条的身份只有当日结束才知道，所以issue clock固定为该日23:59:59.999999。
- 空日没有行，不填周末、插值或零；边界不完整日也按同一最后记录规则保留。日频H表示后续H个非空观测日，目标不含已丢弃的日内excursion。
- 归档 `results/revision-v8/wp4/cells/W52_H6/worker-source.json` 记录18576 hourly rows →930 daily rows；第一/末issue是2014-02-05/2017-01-24日末；gap直方图86400秒774次、172800秒155次。
- 聚合复现必须匹配四个canonical little-endian向量的SHA及组合SHA；组合前缀是 `v8-daily-v1\x00`。归档combined SHA=`a8638f97370b14308212cbaa2d82defaf7152e0f240ff9f950414a035ae744d1`。每日position SHA=`6efa0b259b71f364cf747d3b32084eb1e1ea528dd63ba5c7f2344d4459a63668`。
- Treasury索引结构被迁移：validation329..380(52)；evaluation405..n_daily-25，共501条即405..905；不是按比例分割，也不是复制Treasury2021绝对日期。validation最后H24标签结束404。
- W52/260、H6/24，RMS6/26、valid26、nominal gap86400，refit13，验证/评估各自anchor。day-end的hour features是常数，由原训练池标准化处理。QR33/QR4与WP3相同菜单和selector政策。
- 全日频向量、selected source indices、per-issue traces继续private；公开只发布聚合meta/hash/score。day-end mapping在旧WP4 manifest.private_directory各cell的daily-series.npz，勿将其加入公开结果。

## 5. C2诊断应定位的原评估前范围与已有输入

这部分只定位合同，没有选择断点方法、阈值或分段拟合政策。

| 序列 | 原评估起点的拥有文件 | 严格pre-evaluation观测范围（0-based） |
|---|---|---|
| Treasury PDPOSGS-B | `protocol/revision-20261022/study-spec.json:55–77`；eval405，日期2021-01-06 | 0..404，共405；不使用eval405本身 |
| 12条weekly panel | `protocol/revision-20261023/round2-D3-panel.json` 的evaluation_indices405..681；与706条Treasury经济日期网格对齐 | 每条0..404，共405 |
| same-dealer daily FX | WP4 `sample.evaluation_first=405` 与`cell-geometry.json` | 聚合后0..404，共405；先按原日频规则形成序列，再用此边界 |
| hourly FX（供N4比较） | `protocol/revision-20261022/study-spec.json:33–53` eval11927..18551；原`protocol/study-spec.json:223` cutoff2016-01-01 | 0..11926，共11927；不是WP5或retro起点 |

WP5评估起点3071与较早retro起点8999是另一个历史窗口合同。若新设计选不同前缀，须明说；不能默认为“原评估前”而挪动。

已验证旧目录 `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/` 中：

- `.scratch/data/1hourNetPositionsKaggle.csv` 存在，1286391 bytes，SHA=`b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa`；新clone没有这个private input。
- `data/nyfed-pdposgs-b-20261022/PDPOSGS-B.csv` 存在，23315 bytes，SHA=`9f9f942ea8775a15f2e839cfe489f2e5113659ac37b375282d93bd6379be7cdb`；新clone公开归档也有此文件。`provenance.json`记录706 economic observations，2013-04-03..2026-10-07。
- 12条panel raw全在旧目录`.scratch/round2/panel-data/<KEY>.csv`，逐一复核bytes/hash与 `results/revision-20261023/round2/panel/selection-manifest.json` 相同。备用清单 `results/supervisor-20261023/e5/inputs/panel/selection-manifest.json` 给同一12条eligible；另外G11L21/G21是skipped，不能补进13条。每条raw707行/到2026-10-14，但按Treasury固定网格align后706行/到2026-10-07。
- 不应从旧E5 `.scratch/supervisor-round2-20261023/e5/sources` 猜路径：该旧目录下这些备用copy当前不存在；拥有的原panel-data路径存在。

| Panel key | bytes | SHA-256 |
|---|---:|---|
| PDPOSMBS-TOT |25680|`2e493d17890870eff6eca247c62b9175fcf7564a70d87e63ee520561bb71efcb`|
| PDPOSCS-TOT |24713|`169fdb5201f6a34152936f0aa2b444d9ea0f8814d39750bfd4a4bc942a41fade`|
| PDPOSFGS-TOT |25495|`00f321abeebf1aaee1af68dc7ab41bb403eafe770c915f4229fc80e18e3586de`|
| PDPOSTIPS-L2 |24883|`dc3dd1ef3f9a364c25789523a5b2f0d46860681808005620055db4a47c996995`|
| PDPOSTIPS-G11 |25017|`810355b1cf4c93282dcc76fa6fdc41bbccc1ec7d3675024a2400e2c27c695d5d`|
| PDPOSTIPS-G2 |24761|`8e54675071813501a240c1ea3a2ca4fda0f2e2aa88b1ea1bb2852fe6a9f6c894`|
| PDPOSTIPS-G6L11 |26797|`1e3ee3a336be321f47a3f7481591b15650607baa3fb46be7da99968ccbea7845`|
| PDPOSGSC-L2 |24714|`7ab08e2b39534ca67f43006949a7504334d90b63034b9ed3cd5248e59c9126bf`|
| PDPOSGSC-G2L3 |25930|`10c35a9516154011c0821d12eb86052f7d4df01a4c7b0cddee4878b72868678c`|
| PDPOSGSC-G3L6 |26090|`453f1a2458a2c9c7049d9128ccc9d1945b5a61e469ab1c8112577b3ad7539fa5`|
| PDPOSGSC-G6L7 |25967|`429d542e2cda305d8d5c458592b57b4042c9f479ce4135e3ab3610951ae6b35d`|
| PDPOSGSC-G7L11 |26639|`0b102760c5e4cc181d438d9c8618f8990d047ac8ecb9bd85bac63851742199d0`|

## 6. Fresh public clone 的历史Git阻断

初始new clone是full非shallow public history；C0 `git cat-file -e` 确认下述三设计commit均不存在。旧原repo只读确认三者存在。`notes/revision-v8/REPRODUCING.md`、`wp8-package-audit.md:42–203` 和 `wp9-acceptance-scope-readback.md:33–41` 已披露浏览器上传造成的文件/历史差异；不能把本地验证成功冒充public clone开箱复现。

| 入口 | 必需真实commit | guard |
|---|---|---|
| `run_v8_wp3.py:91` |`039f6f1b49d46610697bed5300cab687b37951df`| rev-parse commit、git show两协议原bytes，再核original module hashes；缺对象为DESIGN_UNVERIFIED |
| `run_v8_wp4.py:56` |`1427dc0b943ee77a82ee03a67ec9281c20e2cdf5`| 同上，再核sealed WP3模块/source spec/source设计一致；缺对象为DESIGN_OR_SOURCE_SPEC_UNVERIFIED |
| `run_v8_wp5.py:73` |`467a995b16a1c6446b5927992faec26b7f5f6276`| 同类协议、代码、source与参数hash guard |

这些driver guard没有`merge-base`/祖先门，也不要求v9变成旧local history的后代。新clone私下保留真实旧对象、维持原guard、保持v9公共base祖先是两回事。root已决定仅在NEW.git本地导入，旧repo只读、不改guard、不伪造祖先、不公开bundle/私有identity；本审计未执行导入。

**完整suite另有两个实际历史依赖**：

1. `test_v8_main_numbers.py` → `notes/revision-v8/check_wp8_main_numbers.py:21–22/107/158`，需 `b571f324a253480b4e39bc8a8096775ddbcc7017` 与 `642d6af9eaccdd27896fd7a2e265cddd6f7a91e5`；C0时new均缺，old均存在。
2. `notes/revision-v8/test_v8_supp_numbers.py` → `check_wp8_supp_numbers.py:234` 读取`wp7-supplement-integration.json.baseline_commit=642d6af`，需同一个完整642d对象。
3. `notes/v7/check_numbers_v7.py:33/603` 独立旧checker另需 `3d964af91679a03088f811d7f01f89495a3adf20`；静态搜索未找到default tests调用此旧checker；不要运行它来认证v9或覆盖v7输出。

三个真实WP3/4/5 audit入口也通过manifest.design_commit做git show/commit时间检查，所以真实归档audit缺设计对象会记录DESIGN_COMMIT_UNVERIFIED。与此不同，`test_v8_wp3/4/5_audit.py` 的unit tests自建临时fixture Git，不要求这些真实ID。大部分core/driver/package/plot测试只用构造输入；不能笼统说全部v8 tests都BLOCKED。

旧 `round2_panel_run.py:91` 的 `prepare()` 确实对 `8baa2f5b44327b3ba295927bd3db954f3475d35d` 有merge-base祖先门；它还含已存在输出和私有trace依赖。C2只需纯`align_source`，不应调用这个旧driver。不能为了让旧driver跑通把它的设计commit伪造成v9祖先。

公开隐私边界：三个设计commit本身含未在公开origin出现的machine-local author/committer身份。即使去掉父历史，仅发布精确commit对象也会发布该身份；改身份则SHA变化并非原对象。私下本机复用不等于允许推送历史bundle。只推v9公共lineage、勿push--all，按root统一操作。

## 7. 交给新C2设计明确、此处不替其决定的差异

- 用户要求每段AR(1)-GARCH(1,1)-t与全段对照；WP3没有拟合，也没有t。`round2_filtered.py:189`的既有 `_fit_garch` 拟合的是**增量**constant-mean GARCH-normal，不能直接当作level AR-GARCH-t复用；`ar1_replay.py:72`只有AR(1)拟合。
- 用户N2/N3说median；WP3 summary是ratio of means。应各给准确字段/公式，并冻结哪种median及跨rep/跨series的聚合层级。
- WP3原refit24/RMS24/168/72val+72eval，与真实周/daily refit13/RMS6/26/52val不相同。新设计须明确遵守“除断点外同WP3”的范围，不能混合而无记录。
- 参数估计失败、无断点、非平稳估计、短分段、t自由度、跨断点state/variance传递、burn和时钟映射都是新生成器需要冻结的接口。此处没有做选择，也没有读取这些诊断的结果。
- 不论局部失败或预算削减，保持完整计划库存、失败原因、选参候选和所有负面格；不得用旧v8归档输出充当新v9计算结果。
