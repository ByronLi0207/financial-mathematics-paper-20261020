# WP2–WP4 公开聚合结果独立回读

状态：PASS_PUBLIC_SCALAR_READBACK。此次仅核对公开 JSON 和原始公开
paired-comparisons.csv 的聚合标量；没有读取 raw source、私有 NPZ 或逐期金融
向量，没有重跑模型、HAC、DM/GW 或新增分析。输入当前 SHA-256、实际命令、
literal stdout/stderr 和算术核对明细保存在同目录 output JSON/TXT。

## WP4：分母、加权均值与原 primary 一致

| 来源 | low/middle/high 样本数 | 三组 mean new-minus-reference | 完整分母 | 加权分组均值 | 原 primary |
|---|---|---|---:|---:|---:|
| FX，USD | 1593 / 1816 / 3216 | -58761.2665 / -27839.4337 / -70387.9104 | 6625 | -55929.1515487561 | -55929.15154875609 |
| Treasury，USD millions | 9 / 25 / 243 | +6696.6609 / +5230.5926 / +810.8824 | 277 | +1401.0078517747918 | +1401.0078517747918 |

两行样本数均精确相加为完整分母。与原 paired-comparisons.csv 的 primary
mean difference 相比，FX 加权均值仅相差 -7.275957614183426e-12 USD，Treasury
相差 0，满足 rel_tol=1e-12、abs_tol=1e-8 的回读容差。GW 分母分别为
6619 和 271，均恰好 burn-in 6；完整分组汇总没有跟随 GW 缩短。

可支持的 FX 表述：三个状态的点估计均有负损失差，不能写成“只在高状态赢”。
高状态点估计最负；但组均值异质性 raw/Holm p 均为 0.1593833367，未提供
常用 5% 工作参考下的组间差异证据。joint GW raw p=1.4629751215e-6，
四槽 Holm p=5.8519004861e-6；该检验包含 intercept，拒绝可仅反映无条件
均值差，不是已证明的 RMS 依赖，也不能据此开发/宣称状态切换策略。

Treasury 三组点估计均为正，完整 primary 的 QR 劣势没有在任一状态反转。
low/middle 仅 9 和 25 个原期，须明确说明小组样本及依赖/HAC 参考限制。
异质性 raw p=0.0004267717546、Holm p=0.001280315264；joint GW raw
p=0.04848777760、Holm p=0.09697555519。不能把 raw < .05 写成四槽
family 调整后 joint GW 仍显著，也不能把 heterogeneity 拒绝写成有因果或
可部署的状态效果。状态是 position-increment RMS，不是价格/收益率波动率。

## raw、NA、Holm 的标量重算

| 家族 | 固定槽数 | raw NA 槽数 | raw p < .05 | 有 raw p 且 Holm p < .05 |
|---|---:|---:|---:|---:|
| WP2 | 56 | 5 | 18 | 6 |
| WP3 | 224 | 98 | 60 | 18 |
| WP4 | 4 | 0 | 3 | 2 |

逐槽检查 raw NA -> bookkeeping 1；独立排序并按 m-j 乘数重算整个既定家族的
Holm 数值，全部一致。bookkeeping 1 不是观察到有效 p=1；NA/identical-loss
槽不能被解释为校准、相等性或无差异的证据。coverage p 值仍是另外的未调整
诊断，不能借用 ranking family 的调整声称获得条件覆盖保证。

## WP2：ACI 的损失和覆盖必须成对表述

24 行中 22 COMPLETE、2 NA；ACI_F 与 ACI_QR 各 7 个 COMPLETE，SAV 为
8 个 COMPLETE。两个 NA 是 Treasury H24/W260 wrappers，不能删掉或补模型。

FX H6/W720：wrapped QR loss=439672.9121，wrapped F=472677.7727，QR
损失较低；但 strict hits 为 352/6625 versus 331/6625，QR 的绝对覆盖距离
反而更大（两者距离差 +0.003094339623）。FX H6/W2880：QR loss=393795.0578
versus F=463271.4663，strict hits 为 329 versus 328，QR 的覆盖距离略小
（距离差 -0.0001509433962）。不能用“更多 hits”单独判定更差覆盖：当两者
都低于 5% 时，更多 hits 可能更接近目标。

Treasury 原 primary 的 H6/W260：wrapped QR loss=3013.159658，wrapped
F=2792.912816，QR 仍较差；hits 为 6 versus 7 /277，QR 的绝对覆盖距离
也更大。因此不能概括为“覆盖校正后 QR 在所有地方都更好”。H24 和短窗口
也保留有利与不利结果，不根据 ACI 名称宣称校准改善或引入 canonical ACI
的保证。SAV 的 8 个数值 COMPLETE 也不代表全局最优或独立外部验证。

## WP3：组合结果保留对两个 constituent 的方向

公开 findings 的计数已从公开逐格聚合行重新核对：mean 全 56 格可用，14 格
损失低于两者、16 格低于 F、54 格低于 QR；median 仅原 8 格可用，3 格低于
两者、5 格低于 F、6 格低于 QR。48 个 panel median 是缺原 plain KNN 的 NA。
这些是依赖的 inspected cells，不是 56/8 次独立复现。

两个 median=EXACTLY_F 的格子为 Treasury H6/W52 和 H24/W52，其 loss、hits
和覆盖距离与 F 精确一致；该代数身份不能写成新增预测能力证据。

原 primary 对应的 source/H/W 情境中：

| 情境 | 方法 | loss 相对 matched F | loss 相对 QR | strict hits / n |
|---|---|---:|---:|---:|
| FX H6/W2880 | mean | -10.6138% | +4.8725% | 330/6625 |
| FX H6/W2880 | median | -11.1693% | +4.2207% | 327/6625 |
| Treasury H6/W260 | mean | +2.7731% | -31.8416% | 40/277 |
| Treasury H6/W260 | median | -3.9813% | -36.3211% | 28/277 |

因此 FX 这两种组合均低于 matched F 但高于 QR；Treasury median 在该格
低于两者，而 mean 仍高于 F。Treasury median hits 28/277 仍约 10.1%，
不能把分数改善写成达到 5% 覆盖目标。FX 的 matched F/W2880 组合控制
与 WP4 原 primary 的 rolling F/W720 明确不同，不能混写。

公开八条 Murphy 记录均为 CROSSING，positive/negative/zero breakpoint
计数精确加总到完整 breakpoint_count；findings 与组合主报告一致。积分
减 pinball 的公开残差最大绝对值为 7.275957614183426e-12，没有支持“整个
阈值域占优”的表述。这里仅回读已发布的 scalar event-sign 汇总，没有重读
曲线私有向量或重新做财务曲线计算。

## 证据与范围

- `wp2-4-public-readback.py`：仅 Python 标准库；明列五个允许读取的公开 JSON
  及一个原始公开 paired aggregate CSV，没有 NumPy、worker 或模型导入。
- `wp2-4-public-readback-output.json`：全部公开输入当前 hash 与核对结果。
- `wp2-4-public-readback-output.txt`：实际命令、完整 literal 输出、return code 0。
- 本回读证实这些公开汇总之间的算术和引用一致性；它不重新验证私有轨迹、
  raw source、历史信息可用性或所用参考分布的统计假设。
