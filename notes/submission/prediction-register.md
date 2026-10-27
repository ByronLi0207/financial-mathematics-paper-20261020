# H4 预测登记表：只读证据准备

此文件与同名 JSON 仅整理已保存预测、阈值、输出和判定；未修改论文，未运行研究脚本、拟合、评分、金融摘要或新判定。固定 v13 来源为 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`；WP2 固定来源为 `6192ec370d131c60d05e9fb103150e0e9db6aa23`。

共 **36 行**：任务指定的 **29 行主/次预测**（含 WP2 方法分行），另加 **7 行 QR4 敏感性**，防止主 QR33 汇总遮蔽失败或无法判定。原保存判定对应 **20 成立、11 不成立、5 无法判定**。这只是登记行数，不能解释成独立检验或成功概率。

## 完整登记

| 行 ID | 方法/角色 | 预测与原阈值 | 实际保存输出 | 判定（原状态） |
|---|---|---|---|---|
| E5.P1.QR33+ | QR33+ / primary | QR33+ strictly improves original QR33 loss within the45 originally adverse panel cells. At least40 of fixed45 cells. | 30/45 successes; required40. | 不成立 (`False`) |
| E5.P2.QR33+ | QR33+ / primary | QR33+ excess loss against F lies within inclusive[-10%,+10%]. At least36 of fixed48 cells within[-10,+10]%. | 24/48 successes; required36. | 不成立 (`False`) |
| E5.P3.QR33+ | QR33+ / primary | Selected ridge penalty is at least1. At least25 of fixed48 cells (more than half). | 33/48 successes; required25. | 成立 (`True`) |
| R6.S1.R2 | R2 / primary | All26 retrospective weekly R2 cells complete with bounded worst and median excess. 26/26 complete; worst<=+25%; median<=+5%. | 26/26 complete; worst181.39452368014167%; median5.374072481175762%. | 不成立 (`NOT_MET`) |
| R6.S2.R2 | R2 / primary | R2 retains at least half of each negative R0 FX H6 gain. For each eligible R0<0 cell, R2<=0.5*R0; at least one eligible cell required. | One eligible cell W2880: R0=-16.62356533682211%; R2=-6.2754532709491055%; half_gain_retained=false. W720 not eligible. | 不成立 (`NOT_MET`) |
| R6.S3.R2 | R2 / primary | R2 weekly median excess is strictly lower than R0. Both rules complete26 cells; median(R2)<median(R0). | R0 median4.1510024714803695%; R2 median5.374072481175762%; both26 complete. | 不成立 (`NOT_MET`) |
| E1.M1.QR33 | QR33 / primary | Constant-arm W52 QR33 median is near parity with F. Inclusive[-5,+5]%. | 0.2069371499562489%. | 成立 (`SUPPORTED`) |
| E1.M2.QR33 | QR33 / primary | Switching-arm W52 QR33 median exceeds constant-arm median by5pp. Switching minus constant>=+5pp. | -0.43471629487539243pp; constant0.2069371499562489%; switching-0.22777914491914353%. | 不成立 (`NOT_SUPPORTED`) |
| E1.M3.QR33 | QR33 / primary | Both arm medians improve and at least12 of13 sources improve in both arms. Both group arm medians strictly lower; joint improvement>=12/13. | Both group arms improve; joint_improved_sources=13/13. | 成立 (`SUPPORTED`) |
| E2.T1.QR33 | QR33 / primary | Realized better historical report min(F,I) strictly beats QR33. At least60% of all2K cells; no missing operand deletion. | 29/34; fraction0.8529411764705882. | 成立 (`SUPPORTED`) |
| E2.T2.QR33 | QR33 / primary | Each W QR33 median excess against F lies near parity. Inclusive[-10,+10]% at both W52 and W260. | W52=19.334715757564624%; W260=10.34828178946443%. | 不成立 (`NOT_SUPPORTED`) |
| E2.T3.QR4 | QR4 / primary | QR4 median excess is strictly lower with W260 than W52. W260 median < W52 median. | W52=10.280676300222424%; W260=0.2174917571722501%; change=-10.063184543050173pp. | 成立 (`SUPPORTED`) |
| F1.D1.QR33 | QR33 / primary | Strictly positive finite-menu oracle gap G in more than half of fixed41 short-weekly cells. Fixed41 denominator; positive G share>1/2, using missing bounds. | support=29/41; complete=41; unavailable=0; bounds=0.7073170731707317,0.7073170731707317. | 成立 (`SUPPORTED`) |
| F1.D2.QR33 | QR33 / primary | Positive actual excess E and selection component S>E/2 in more than half of fixed41 cells. Fixed41 denominator; share of E>0 and S>E/2 >1/2, using missing bounds. | support=27/41; complete=41; unavailable=0; bounds=0.6585365853658537,0.6585365853658537. | 成立 (`SUPPORTED`) |
| F1.D3.QR33 | QR33 / primary | Both original long-history FX horizons have negative finite-menu gap. G<0 at H6 and H24; conjunction of both original FX cells. | H6 G=-14.917351765503492%; H24 G=-3.7577697957958254%;2/2 support. | 成立 (`SUPPORTED`) |
| F1.D1.QR4 | QR4 / sensitivity | Strictly positive finite-menu oracle gap G in more than half of fixed41 short-weekly cells. Fixed41 denominator; positive G share>1/2, using missing bounds. | support=26/41; complete=39; unavailable=2; bounds=0.6341463414634146,0.6829268292682927. | 成立 (`SUPPORTED`) |
| F1.D2.QR4 | QR4 / sensitivity | Positive actual excess E and selection component S>E/2 in more than half of fixed41 cells. Fixed41 denominator; share of E>0 and S>E/2 >1/2, using missing bounds. | support=27/41; complete=39; unavailable=2; bounds=0.6585365853658537,0.7073170731707317. | 成立 (`SUPPORTED`) |
| F1.D3.QR4 | QR4 / sensitivity | Both original long-history FX horizons have negative finite-menu gap. G<0 at H6 and H24; conjunction of both original FX cells. | H6 G=-4.2893706508927965%; H24 G=-3.1505838975205966%;2/2 support. | 成立 (`SUPPORTED`) |
| F2.V1.QR33 | QR33 / primary | Longer CFTC validation reduces each W across-contract QR33 arm median by at least5pp. For each W52/W260: median(V156)-median(V52)<=-5pp; both required. | W52: delta=-15.304032374564795pp, pairs=17/17, missing=0; W260: delta=-9.82319311344436pp, pairs=17/17, missing=0. | 成立 (`SUPPORTED`) |
| F2.V2.QR33 | QR33 / primary | Longer CFTC validation raises empirical-limit selection frequency at each W. At each W52/W260: infinity count(V156)>count(V52); both required. | W52: infinity V52/V156=4/10, missing_pairs=0; W260: infinity V52/V156=4/5, missing_pairs=0. | 成立 (`SUPPORTED`) |
| F2.V1.QR4 | QR4 / sensitivity | Longer CFTC validation reduces each W across-contract QR4 arm median by at least5pp. For each W52/W260: median(V156)-median(V52)<=-5pp; both required. | W52: delta=Nonepp, pairs=16/17, missing=1; W260: delta=Nonepp, pairs=16/17, missing=1. | 无法判定 (`UNDETERMINED`) |
| F2.V2.QR4 | QR4 / sensitivity | Longer CFTC validation raises empirical-limit selection frequency at each W. At each W52/W260: infinity count(V156)>count(V52); both required. | W52: infinity V52/V156=2/7, missing_pairs=1; W260: infinity V52/V156=2/4, missing_pairs=1. | 无法判定 (`UNDETERMINED`) |
| F3.Q1.QR33 | QR33 / primary | At tau.99 F strictly beats QR33 in at least29 fixed CFTC cells. At least29/34; strict wins only; fixed denominator with unknown bounds. | 28 supports,5 complete nonsupports (4 exact ties),1 unknown; support bounds[0.8235294117647058,0.8529411764705882]. | 无法判定 (`UNDETERMINED`) |
| F3.Q2.QR33 | QR33 / primary | At tau.99 QR33 improves matched F in both FX periods. Relative excess<0 in original and early2015; both required. | Both period inputs FAILED;0 supports,2 unknown; both relative_loss_pct=null. | 无法判定 (`UNDETERMINED`) |
| G2.V3.QR33 | QR33 / primary | Longer NY Fed validation reduces each horizon across13 arm median by at least5pp. At each H6/H24: median(V156)-median(V52)<=-5pp; both required. | H6: -7.812971755453957pp (SUPPORTED); H24: -35.45092255436495pp (SUPPORTED). | 成立 (`SUPPORTED`) |
| G2.V4.QR33 | QR33 / primary | Longer NY Fed validation increases empirical-limit selections at each horizon. At each H6/H24: infinity count(V156)>count(V52); both required. | H6: 6 to 9 (SUPPORTED); H24: 3 to 9 (SUPPORTED). | 成立 (`SUPPORTED`) |
| G2.V3.QR4 | QR4 / sensitivity | Longer NY Fed validation reduces each horizon across13 arm median by at least5pp. At each H6/H24: median(V156)-median(V52)<=-5pp; both required. | H6: -4.2150390061995235pp (NOT_SUPPORTED); H24: -18.670087236167987pp (SUPPORTED). | 不成立 (`NOT_SUPPORTED`) |
| G2.V4.QR4 | QR4 / sensitivity | Longer NY Fed validation increases empirical-limit selections at each horizon. At each H6/H24: infinity count(V156)>count(V52); both required. | H6: 5 to 7 (SUPPORTED); H24: 4 to 9 (SUPPORTED). | 成立 (`SUPPORTED`) |
| G3.R1.RP | RP / primary | Protocol median excess is small across all60 eligible weekly cells. Full-universe median<=+1%; any eligible missing outcome=>UNDETERMINED. | All60 complete; median0.0%; ordinary-regression median14.627467605779144%. | 成立 (`SUPPORTED`) |
| G3.R2.RP | RP / primary | At most5% of eligible weekly cells lose more than10% against F. Adverse defined excess>10%; adverse fraction<=0.05; at most3 of60. | 8/60 adverse; worst80.98396986931891%; no unavailable cells. | 不成立 (`NOT_SUPPORTED`) |
| G3.R3.RP | RP / primary | Retain at least half of ordinary QR gain in every eligible FX period. If ordinary excess<0, RP excess<=0.5*ordinary; every eligible gain period and at least1 required. | Original ordinary/RP=-14.766762552613882% (threshold-7.383381276306941%); early2015 ordinary/RP=-16.623565336822104% (threshold-8.311782668411052%); both SUPPORTED. | 成立 (`SUPPORTED`) |
| WP2.P1_QR4.QR4 | QR4 / primary | Low-region QR4 strictly loses against matched F. At least80% of fixed17 low-region cells; combined P1 requires both methods. | 15/17;0.8823529411764706; SUPPORT. | 成立 (`SUPPORT`) |
| WP2.P1_QR33.QR33 | QR33 / primary | Low-region QR33 strictly loses against matched F. At least80% of fixed34 low-region cells; combined P1 requires both methods. | 29/34;0.8529411764705882; SUPPORT. | 成立 (`SUPPORT`) |
| WP2.P2_QR4.QR4 | QR4 / primary | High-region W520 QR4 strictly beats matched F. At least60% of fixed17 high-region cells. | 10/17;0.5882352941176471 below0.6; NOT_SUPPORT. | 不成立 (`NOT_SUPPORT`) |
| WP2.P2_QR33.QR33 | QR33 / primary | QR33 high-region comparison requires observed c>2r*. No registered high-region cell exists; structurally NOT_TESTABLE by design. | planned=0; NO_REGISTERED_REGION_CELL; NOT_TESTABLE. | 无法判定 (`NOT_TESTABLE`) |
| WP2.P3_QR4.QR4 | QR4 / secondary | QR4 excess loss strictly decreases at both successive history steps. At least70% of fixed17 markets satisfy Delta52>Delta260>Delta520. | 6/17;0.35294117647058826 below0.7; NOT_SUPPORT. | 不成立 (`NOT_SUPPORT`) |

## 设计、结果与文稿精确绑定

下面逐行列出文件、完整 SHA256、JSON Pointer 或准确 Markdown 行。JSON 中另存原字段值与每个文稿锚点的完整文件 SHA256，供后续 H4 生成 LaTeX 总表。E5 与 WP2 的原设计没有阈值 JSON；其原文行号/逐字引文就是设计绑定，不能虚构 JSON Pointer。

### E5.P1.QR33+

- 设计：
  - `protocol/supervisor-20261023/e5-panel-prediction.md` — `Markdown line 42`; SHA256 `c9f82b37ee82dc000e6bf2590b1ef29195a0c442e7d3128536b6658d36f16d87`；原文：- **P1:** Among the **45 fixed cells** whose archived original QR33 loss exceeds F, at least **40** will have new QR33+ mean loss strictly below original QR33.
- 结果：
  - `results/supervisor-20261023/e5/prediction-assessment.json` — `/predictions/P1/supported`; SHA256 `5a2b4d370d34b571f661110d8bb30c3e0609cda47443dde7ee9bf60b0d786a46`
  - `results/supervisor-20261023/e5/prediction-assessment.json` — `/predictions/P1`; SHA256 `5a2b4d370d34b571f661110d8bb30c3e0609cda47443dde7ee9bf60b0d786a46`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:258`；`tab:weekly`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:512`；`sup:panel`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:628`；The expanded-menu selection precedes its evaluation；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：Predictions were fixed before new E5 fits, after original panel outcomes were inspected; post-result exploratory. Related series are not independent dealers. Original design Git object is unavailable here; do not upgrade saved chronology to verified original-object proof.

### E5.P2.QR33+

- 设计：
  - `protocol/supervisor-20261023/e5-panel-prediction.md` — `Markdown line 43`; SHA256 `c9f82b37ee82dc000e6bf2590b1ef29195a0c442e7d3128536b6658d36f16d87`；原文：- **P2:** At least **36 of all 48 cells** will have `100*(QR33+ loss - F loss)/F loss` in the **inclusive interval [-10%,+10%]**.
- 结果：
  - `results/supervisor-20261023/e5/prediction-assessment.json` — `/predictions/P2/supported`; SHA256 `5a2b4d370d34b571f661110d8bb30c3e0609cda47443dde7ee9bf60b0d786a46`
  - `results/supervisor-20261023/e5/prediction-assessment.json` — `/predictions/P2`; SHA256 `5a2b4d370d34b571f661110d8bb30c3e0609cda47443dde7ee9bf60b0d786a46`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:258`；`tab:weekly`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:512`；`sup:panel`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:628`；The expanded-menu selection precedes its evaluation；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：Predictions were fixed before new E5 fits, after original panel outcomes were inspected; post-result exploratory. Related series are not independent dealers. Original design Git object is unavailable here; do not upgrade saved chronology to verified original-object proof.

### E5.P3.QR33+

- 设计：
  - `protocol/supervisor-20261023/e5-panel-prediction.md` — `Markdown line 44`; SHA256 `c9f82b37ee82dc000e6bf2590b1ef29195a0c442e7d3128536b6658d36f16d87`；原文：- **P3:** More than half of all 48 cells, meaning at least **25**, will select **lambda >= 1**.
- 结果：
  - `results/supervisor-20261023/e5/prediction-assessment.json` — `/predictions/P3/supported`; SHA256 `5a2b4d370d34b571f661110d8bb30c3e0609cda47443dde7ee9bf60b0d786a46`
  - `results/supervisor-20261023/e5/prediction-assessment.json` — `/predictions/P3`; SHA256 `5a2b4d370d34b571f661110d8bb30c3e0609cda47443dde7ee9bf60b0d786a46`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:258`；`tab:weekly`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:512`；`sup:panel`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:628`；The expanded-menu selection precedes its evaluation；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：Predictions were fixed before new E5 fits, after original panel outcomes were inspected; post-result exploratory. Related series are not independent dealers. Original design Git object is unavailable here; do not upgrade saved chronology to verified original-object proof.

### R6.S1.R2

- 设计：
  - `protocol/supervisor-20261023/r6-design.md` — `/success/S1`; SHA256 `de301f131426ed9b185451d87e3aee1726d978dd2d55ffd322efc02477b6bbae`
- 结果：
  - `results/supervisor-20261023/r6/assessment.json` — `/S1/status`; SHA256 `2c5d3d668b00bc27cc294fef7c2cf9633bb87e602d9bef814b3c7a3fbfe0b5f4`
  - `results/supervisor-20261023/r6/assessment.json` — `/S1`; SHA256 `2c5d3d668b00bc27cc294fef7c2cf9633bb87e602d9bef814b3c7a3fbfe0b5f4`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:270`；one-standard-error worst excess；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:674`；`sup:selection`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:750`；All three recorded success criteria；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:756`；`sup:selection-failures`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：R2 is the predesignated rule; retrospective repository-role audit is bounded. S1/S2/S3 all NOT_MET. R3 rule-cell failures remain failures, and Treasury W52 is a structural analogue rather than exact W260 primary replication.

### R6.S2.R2

- 设计：
  - `protocol/supervisor-20261023/r6-design.md` — `/success/S2`; SHA256 `de301f131426ed9b185451d87e3aee1726d978dd2d55ffd322efc02477b6bbae`
- 结果：
  - `results/supervisor-20261023/r6/assessment.json` — `/S2/status`; SHA256 `2c5d3d668b00bc27cc294fef7c2cf9633bb87e602d9bef814b3c7a3fbfe0b5f4`
  - `results/supervisor-20261023/r6/assessment.json` — `/S2`; SHA256 `2c5d3d668b00bc27cc294fef7c2cf9633bb87e602d9bef814b3c7a3fbfe0b5f4`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:270`；one-standard-error worst excess；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:674`；`sup:selection`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:750`；All three recorded success criteria；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:756`；`sup:selection-failures`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：R2 is the predesignated rule; retrospective repository-role audit is bounded. S1/S2/S3 all NOT_MET. R3 rule-cell failures remain failures, and Treasury W52 is a structural analogue rather than exact W260 primary replication.

### R6.S3.R2

- 设计：
  - `protocol/supervisor-20261023/r6-design.md` — `/success/S3`; SHA256 `de301f131426ed9b185451d87e3aee1726d978dd2d55ffd322efc02477b6bbae`
- 结果：
  - `results/supervisor-20261023/r6/assessment.json` — `/S3/status`; SHA256 `2c5d3d668b00bc27cc294fef7c2cf9633bb87e602d9bef814b3c7a3fbfe0b5f4`
  - `results/supervisor-20261023/r6/assessment.json` — `/S3`; SHA256 `2c5d3d668b00bc27cc294fef7c2cf9633bb87e602d9bef814b3c7a3fbfe0b5f4`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:270`；one-standard-error worst excess；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:674`；`sup:selection`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:750`；All three recorded success criteria；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:756`；`sup:selection-failures`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：R2 is the predesignated rule; retrospective repository-role audit is bounded. S1/S2/S3 all NOT_MET. R3 rule-cell failures remain failures, and Treasury W52 is a structural analogue rather than exact W260 primary replication.

### E1.M1.QR33

- 设计：
  - `protocol/v10/menu-isolation-design.md` — `/M1`; SHA256 `f15d9ce114bd6675a4094aa4997cab5566766792beaad3a87c505814041279c7`
- 结果：
  - `results/v10/menu/summary.json` — `/predictions/M1/status`; SHA256 `e1ac79325e2f8ef60ede05378c70dbbe5f2fedfdbe5ff021d2ec1e58826689d5`
  - `results/v10/menu/summary.json` — `/predictions/M1`; SHA256 `e1ac79325e2f8ef60ede05378c70dbbe5f2fedfdbe5ff021d2ec1e58826689d5`
- 正文/补充材料：
  - `submission-v10/supplement.tex:1498`；`sup:v10-menu`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:1521`；The design preceded every new path calculation.；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:1511`；`fig:mechanism`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：New paired simulated paths reuse earlier calibrated laws; menu expansion jointly adds stronger finite penalties and ordinary I. Required old-menu W260 full-regression failures remain unavailable; do not substitute successful subsets.

### E1.M2.QR33

- 设计：
  - `protocol/v10/menu-isolation-design.md` — `/M2`; SHA256 `f15d9ce114bd6675a4094aa4997cab5566766792beaad3a87c505814041279c7`
- 结果：
  - `results/v10/menu/summary.json` — `/predictions/M2/status`; SHA256 `e1ac79325e2f8ef60ede05378c70dbbe5f2fedfdbe5ff021d2ec1e58826689d5`
  - `results/v10/menu/summary.json` — `/predictions/M2`; SHA256 `e1ac79325e2f8ef60ede05378c70dbbe5f2fedfdbe5ff021d2ec1e58826689d5`
- 正文/补充材料：
  - `submission-v10/supplement.tex:1498`；`sup:v10-menu`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:1521`；The design preceded every new path calculation.；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:1511`；`fig:mechanism`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：New paired simulated paths reuse earlier calibrated laws; menu expansion jointly adds stronger finite penalties and ordinary I. Required old-menu W260 full-regression failures remain unavailable; do not substitute successful subsets.

### E1.M3.QR33

- 设计：
  - `protocol/v10/menu-isolation-design.md` — `/M3`; SHA256 `f15d9ce114bd6675a4094aa4997cab5566766792beaad3a87c505814041279c7`
- 结果：
  - `results/v10/menu/summary.json` — `/predictions/M3/status`; SHA256 `e1ac79325e2f8ef60ede05378c70dbbe5f2fedfdbe5ff021d2ec1e58826689d5`
  - `results/v10/menu/summary.json` — `/predictions/M3`; SHA256 `e1ac79325e2f8ef60ede05378c70dbbe5f2fedfdbe5ff021d2ec1e58826689d5`
- 正文/补充材料：
  - `submission-v10/supplement.tex:1498`；`sup:v10-menu`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:1521`；The design preceded every new path calculation.；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:1511`；`fig:mechanism`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：New paired simulated paths reuse earlier calibrated laws; menu expansion jointly adds stronger finite penalties and ordinary I. Required old-menu W260 full-regression failures remain unavailable; do not substitute successful subsets.

### E2.T1.QR33

- 设计：
  - `protocol/v10/cftc-design.md` — `/T1`; SHA256 `a7aacd4180d27ab810284119b0e4d0cdef79e5d2b0d0c9e7ad2cef8037ab5d78`
- 结果：
  - `results/v10/cftc/summary.json` — `/predictions/T1/status`; SHA256 `f9366a57d864edd2107c140f679c46f19aec89eb0e547f48483ec3768a28f4ae`
  - `results/v10/cftc/summary.json` — `/predictions/T1`; SHA256 `f9366a57d864edd2107c140f679c46f19aec89eb0e547f48483ec3768a28f4ae`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:275`；This meets the pre-specified 60；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:1528`；`sup:v10-cftc`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：Retrospective aggregate-market universe and economic-date downloaded vintage; reporting-system independence is not independent dealer replication. T1 compares realized min(F,I), not a deployable selector. Ingestion clarifications followed acquisition before forecasting.

### E2.T2.QR33

- 设计：
  - `protocol/v10/cftc-design.md` — `/T2`; SHA256 `a7aacd4180d27ab810284119b0e4d0cdef79e5d2b0d0c9e7ad2cef8037ab5d78`
- 结果：
  - `results/v10/cftc/summary.json` — `/predictions/T2/status`; SHA256 `f9366a57d864edd2107c140f679c46f19aec89eb0e547f48483ec3768a28f4ae`
  - `results/v10/cftc/summary.json` — `/predictions/T2`; SHA256 `f9366a57d864edd2107c140f679c46f19aec89eb0e547f48483ec3768a28f4ae`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:275`；This meets the pre-specified 60；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:1528`；`sup:v10-cftc`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：Retrospective aggregate-market universe and economic-date downloaded vintage; reporting-system independence is not independent dealer replication. T1 compares realized min(F,I), not a deployable selector. Ingestion clarifications followed acquisition before forecasting.

### E2.T3.QR4

- 设计：
  - `protocol/v10/cftc-design.md` — `/T3`; SHA256 `a7aacd4180d27ab810284119b0e4d0cdef79e5d2b0d0c9e7ad2cef8037ab5d78`
- 结果：
  - `results/v10/cftc/summary.json` — `/predictions/T3/status`; SHA256 `f9366a57d864edd2107c140f679c46f19aec89eb0e547f48483ec3768a28f4ae`
  - `results/v10/cftc/summary.json` — `/predictions/T3`; SHA256 `f9366a57d864edd2107c140f679c46f19aec89eb0e547f48483ec3768a28f4ae`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:275`；This meets the pre-specified 60；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:1528`；`sup:v10-cftc`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：Retrospective aggregate-market universe and economic-date downloaded vintage; reporting-system independence is not independent dealer replication. T1 compares realized min(F,I), not a deployable selector. Ingestion clarifications followed acquisition before forecasting.

### F1.D1.QR33

- 设计：
  - `protocol/v12/loss-decomposition-design.md` — `/predictions/D1`; SHA256 `cf8a38f734fc22ffa0e8895c2ea34d698ec26c92c31a2835888c464161b858d1`
  - `protocol/v12/loss-decomposition-design.md` — `/predictions/missing`; SHA256 `cf8a38f734fc22ffa0e8895c2ea34d698ec26c92c31a2835888c464161b858d1`
- 结果：
  - `results/v12/decomposition/predictions.json` — `/D1/status`; SHA256 `551ec9f4ab05e38b28c436a7a2c765c095f29ac96a49c4fc6dd0ec18ba4977e4`
  - `results/v12/decomposition/predictions.json` — `/D1`; SHA256 `551ec9f4ab05e38b28c436a7a2c765c095f29ac96a49c4fc6dd0ec18ba4977e4`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:289`；`sec:v12-low-frequency`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/manuscript.tex:290`；Loss from penalty selection exceeds half；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/manuscript.tex:292`；both long-history FX horizons have negative finite-menu gaps；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:1647`；Additional empirical checks and complete results；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：Finite-menu evaluation oracle is a retrospective diagnostic; the ordinary empirical limit is excluded. Component medians need not add or define a component share. QR4 is a separate sensitivity; missing cells stay in fixed denominator.

### F1.D2.QR33

- 设计：
  - `protocol/v12/loss-decomposition-design.md` — `/predictions/D2`; SHA256 `cf8a38f734fc22ffa0e8895c2ea34d698ec26c92c31a2835888c464161b858d1`
  - `protocol/v12/loss-decomposition-design.md` — `/predictions/missing`; SHA256 `cf8a38f734fc22ffa0e8895c2ea34d698ec26c92c31a2835888c464161b858d1`
- 结果：
  - `results/v12/decomposition/predictions.json` — `/D2/status`; SHA256 `551ec9f4ab05e38b28c436a7a2c765c095f29ac96a49c4fc6dd0ec18ba4977e4`
  - `results/v12/decomposition/predictions.json` — `/D2`; SHA256 `551ec9f4ab05e38b28c436a7a2c765c095f29ac96a49c4fc6dd0ec18ba4977e4`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:289`；`sec:v12-low-frequency`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/manuscript.tex:290`；Loss from penalty selection exceeds half；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/manuscript.tex:292`；both long-history FX horizons have negative finite-menu gaps；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:1647`；Additional empirical checks and complete results；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：Finite-menu evaluation oracle is a retrospective diagnostic; the ordinary empirical limit is excluded. Component medians need not add or define a component share. QR4 is a separate sensitivity; missing cells stay in fixed denominator.

### F1.D3.QR33

- 设计：
  - `protocol/v12/loss-decomposition-design.md` — `/predictions/D3`; SHA256 `cf8a38f734fc22ffa0e8895c2ea34d698ec26c92c31a2835888c464161b858d1`
  - `protocol/v12/loss-decomposition-design.md` — `/predictions/missing`; SHA256 `cf8a38f734fc22ffa0e8895c2ea34d698ec26c92c31a2835888c464161b858d1`
- 结果：
  - `results/v12/decomposition/predictions.json` — `/D3/status`; SHA256 `551ec9f4ab05e38b28c436a7a2c765c095f29ac96a49c4fc6dd0ec18ba4977e4`
  - `results/v12/decomposition/predictions.json` — `/D3`; SHA256 `551ec9f4ab05e38b28c436a7a2c765c095f29ac96a49c4fc6dd0ec18ba4977e4`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:289`；`sec:v12-low-frequency`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/manuscript.tex:290`；Loss from penalty selection exceeds half；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/manuscript.tex:292`；both long-history FX horizons have negative finite-menu gaps；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:1647`；Additional empirical checks and complete results；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：Finite-menu evaluation oracle is a retrospective diagnostic; the ordinary empirical limit is excluded. Component medians need not add or define a component share. QR4 is a separate sensitivity; missing cells stay in fixed denominator.

### F1.D1.QR4

- 设计：
  - `protocol/v12/loss-decomposition-design.md` — `/predictions/D1`; SHA256 `cf8a38f734fc22ffa0e8895c2ea34d698ec26c92c31a2835888c464161b858d1`
  - `protocol/v12/loss-decomposition-design.md` — `/predictions/missing`; SHA256 `cf8a38f734fc22ffa0e8895c2ea34d698ec26c92c31a2835888c464161b858d1`
- 结果：
  - `results/v12/decomposition/predictions.json` — `/methods/QR4/D1/status`; SHA256 `551ec9f4ab05e38b28c436a7a2c765c095f29ac96a49c4fc6dd0ec18ba4977e4`
  - `results/v12/decomposition/predictions.json` — `/methods/QR4/D1`; SHA256 `551ec9f4ab05e38b28c436a7a2c765c095f29ac96a49c4fc6dd0ec18ba4977e4`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:289`；`sec:v12-low-frequency`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/manuscript.tex:290`；Loss from penalty selection exceeds half；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/manuscript.tex:292`；both long-history FX horizons have negative finite-menu gaps；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:1647`；Additional empirical checks and complete results；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：Finite-menu evaluation oracle is a retrospective diagnostic; the ordinary empirical limit is excluded. Component medians need not add or define a component share. QR4 is a separate sensitivity; missing cells stay in fixed denominator.

### F1.D2.QR4

- 设计：
  - `protocol/v12/loss-decomposition-design.md` — `/predictions/D2`; SHA256 `cf8a38f734fc22ffa0e8895c2ea34d698ec26c92c31a2835888c464161b858d1`
  - `protocol/v12/loss-decomposition-design.md` — `/predictions/missing`; SHA256 `cf8a38f734fc22ffa0e8895c2ea34d698ec26c92c31a2835888c464161b858d1`
- 结果：
  - `results/v12/decomposition/predictions.json` — `/methods/QR4/D2/status`; SHA256 `551ec9f4ab05e38b28c436a7a2c765c095f29ac96a49c4fc6dd0ec18ba4977e4`
  - `results/v12/decomposition/predictions.json` — `/methods/QR4/D2`; SHA256 `551ec9f4ab05e38b28c436a7a2c765c095f29ac96a49c4fc6dd0ec18ba4977e4`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:289`；`sec:v12-low-frequency`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/manuscript.tex:290`；Loss from penalty selection exceeds half；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/manuscript.tex:292`；both long-history FX horizons have negative finite-menu gaps；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:1647`；Additional empirical checks and complete results；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：Finite-menu evaluation oracle is a retrospective diagnostic; the ordinary empirical limit is excluded. Component medians need not add or define a component share. QR4 is a separate sensitivity; missing cells stay in fixed denominator.

### F1.D3.QR4

- 设计：
  - `protocol/v12/loss-decomposition-design.md` — `/predictions/D3`; SHA256 `cf8a38f734fc22ffa0e8895c2ea34d698ec26c92c31a2835888c464161b858d1`
  - `protocol/v12/loss-decomposition-design.md` — `/predictions/missing`; SHA256 `cf8a38f734fc22ffa0e8895c2ea34d698ec26c92c31a2835888c464161b858d1`
- 结果：
  - `results/v12/decomposition/predictions.json` — `/methods/QR4/D3/status`; SHA256 `551ec9f4ab05e38b28c436a7a2c765c095f29ac96a49c4fc6dd0ec18ba4977e4`
  - `results/v12/decomposition/predictions.json` — `/methods/QR4/D3`; SHA256 `551ec9f4ab05e38b28c436a7a2c765c095f29ac96a49c4fc6dd0ec18ba4977e4`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:289`；`sec:v12-low-frequency`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/manuscript.tex:290`；Loss from penalty selection exceeds half；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/manuscript.tex:292`；both long-history FX horizons have negative finite-menu gaps；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:1647`；Additional empirical checks and complete results；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：Finite-menu evaluation oracle is a retrospective diagnostic; the ordinary empirical limit is excluded. Component medians need not add or define a component share. QR4 is a separate sensitivity; missing cells stay in fixed denominator.

### F2.V1.QR33

- 设计：
  - `protocol/v12/validation-length-design.md` — `/predictions/V1`; SHA256 `14192e8ccb8cf8cde9b53e65d20c871b93c537deb9cfdd39cac09e5cf6578819`
  - `protocol/v12/validation-length-design.md` — `/predictions/missing`; SHA256 `14192e8ccb8cf8cde9b53e65d20c871b93c537deb9cfdd39cac09e5cf6578819`
- 结果：
  - `results/v12/validation-length/predictions.json` — `/methods/QR33/V1/status`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR33/V1`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR33/by_window/52/median_relative_loss_by_validation`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR33/by_window/52/median_difference_pct_points`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR33/by_window/52/complete_pair_count`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR33/by_window/52/missing_pair_count`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR33/by_window/260/median_relative_loss_by_validation`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR33/by_window/260/median_difference_pct_points`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR33/by_window/260/complete_pair_count`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR33/by_window/260/missing_pair_count`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:290`；Extending validation lowers CFTC median；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:1647`；Additional empirical checks and complete results；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：Difference of arm medians is not median paired change. Related markets are not independent. QR4 missing required pairs leaves its formal V1/V2 UNDETERMINED; complete-pair subset summaries do not replace the universe.

### F2.V2.QR33

- 设计：
  - `protocol/v12/validation-length-design.md` — `/predictions/V2`; SHA256 `14192e8ccb8cf8cde9b53e65d20c871b93c537deb9cfdd39cac09e5cf6578819`
  - `protocol/v12/validation-length-design.md` — `/predictions/missing`; SHA256 `14192e8ccb8cf8cde9b53e65d20c871b93c537deb9cfdd39cac09e5cf6578819`
- 结果：
  - `results/v12/validation-length/predictions.json` — `/methods/QR33/V2/status`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR33/V2`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR33/by_window/52/known_infinity_count_by_validation`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR33/by_window/52/complete_pair_count`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR33/by_window/52/missing_pair_count`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR33/by_window/260/known_infinity_count_by_validation`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR33/by_window/260/complete_pair_count`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR33/by_window/260/missing_pair_count`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:290`；Extending validation lowers CFTC median；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:1647`；Additional empirical checks and complete results；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：Difference of arm medians is not median paired change. Related markets are not independent. QR4 missing required pairs leaves its formal V1/V2 UNDETERMINED; complete-pair subset summaries do not replace the universe.

### F2.V1.QR4

- 设计：
  - `protocol/v12/validation-length-design.md` — `/predictions/V1`; SHA256 `14192e8ccb8cf8cde9b53e65d20c871b93c537deb9cfdd39cac09e5cf6578819`
  - `protocol/v12/validation-length-design.md` — `/predictions/missing`; SHA256 `14192e8ccb8cf8cde9b53e65d20c871b93c537deb9cfdd39cac09e5cf6578819`
- 结果：
  - `results/v12/validation-length/predictions.json` — `/methods/QR4/V1/status`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR4/V1`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR4/by_window/52/median_relative_loss_by_validation`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR4/by_window/52/median_difference_pct_points`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR4/by_window/52/complete_pair_count`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR4/by_window/52/missing_pair_count`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR4/by_window/260/median_relative_loss_by_validation`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR4/by_window/260/median_difference_pct_points`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR4/by_window/260/complete_pair_count`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR4/by_window/260/missing_pair_count`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:290`；Extending validation lowers CFTC median；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:1647`；Additional empirical checks and complete results；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：Difference of arm medians is not median paired change. Related markets are not independent. QR4 missing required pairs leaves its formal V1/V2 UNDETERMINED; complete-pair subset summaries do not replace the universe.

### F2.V2.QR4

- 设计：
  - `protocol/v12/validation-length-design.md` — `/predictions/V2`; SHA256 `14192e8ccb8cf8cde9b53e65d20c871b93c537deb9cfdd39cac09e5cf6578819`
  - `protocol/v12/validation-length-design.md` — `/predictions/missing`; SHA256 `14192e8ccb8cf8cde9b53e65d20c871b93c537deb9cfdd39cac09e5cf6578819`
- 结果：
  - `results/v12/validation-length/predictions.json` — `/methods/QR4/V2/status`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR4/V2`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR4/by_window/52/known_infinity_count_by_validation`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR4/by_window/52/complete_pair_count`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR4/by_window/52/missing_pair_count`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR4/by_window/260/known_infinity_count_by_validation`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR4/by_window/260/complete_pair_count`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
  - `results/v12/validation-length/predictions.json` — `/methods/QR4/by_window/260/missing_pair_count`; SHA256 `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:290`；Extending validation lowers CFTC median；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/supplement.tex:1647`；Additional empirical checks and complete results；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：Difference of arm medians is not median paired change. Related markets are not independent. QR4 missing required pairs leaves its formal V1/V2 UNDETERMINED; complete-pair subset summaries do not replace the universe.

### F3.Q1.QR33

- 设计：
  - `protocol/v12/tau-design.md` — `/predictions/Q1`; SHA256 `366c56a57983cbe8c9569abf626f2d5947166b66fd0a2ca2fa23a444dcd8943c`
- 结果：
  - `results/v12/tau/predictions.json` — `/Q1/status`; SHA256 `a9adbb6d4e939df9ce596b7dbc2355b8c0a94435c9e65da01047a1723a23f654`
  - `results/v12/tau/predictions.json` — `/Q1`; SHA256 `a9adbb6d4e939df9ce596b7dbc2355b8c0a94435c9e65da01047a1723a23f654`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:305`；Tail-level sensitivity remains incomplete；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/manuscript.tex:308`；`tab:v12-tau`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/generated/v13-supplement.tex:13`；leaving both aggregate tail-level conditions undetermined；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：Original Q1/Q2 remain UNDETERMINED. Post-failure G1 repair failed the forecast-preservation gate (6/10 pass), so three failed original comparisons were not repaired or relabelled.

### F3.Q2.QR33

- 设计：
  - `protocol/v12/tau-design.md` — `/predictions/Q2`; SHA256 `366c56a57983cbe8c9569abf626f2d5947166b66fd0a2ca2fa23a444dcd8943c`
- 结果：
  - `results/v12/tau/predictions.json` — `/Q2/status`; SHA256 `a9adbb6d4e939df9ce596b7dbc2355b8c0a94435c9e65da01047a1723a23f654`
  - `results/v12/tau/predictions.json` — `/Q2`; SHA256 `a9adbb6d4e939df9ce596b7dbc2355b8c0a94435c9e65da01047a1723a23f654`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:305`；Tail-level sensitivity remains incomplete；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/manuscript.tex:308`；`tab:v12-tau`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/generated/v13-supplement.tex:13`；leaving both aggregate tail-level conditions undetermined；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：Original Q1/Q2 remain UNDETERMINED. Post-failure G1 repair failed the forecast-preservation gate (6/10 pass), so three failed original comparisons were not repaired or relabelled.

### G2.V3.QR33

- 设计：
  - `protocol/v13/nyfed-validation-length-design.md` — `/predictions/V3`; SHA256 `aeb733a56631fcbfc501660ee5290ac2cb50a99eaa6b7d8b8fb42f3e420068be`
- 结果：
  - `results/v13/nyfed-validation/summary.json` — `/methods/QR33/V3`; SHA256 `1a52f2bc14cdadf49be1ca2a6e31a42aa78fef92def0d2c25ded73cba07ee976`
  - `results/v13/nyfed-validation/summary.json` — `/methods/QR33/by_horizon/6/median_relative_loss_by_validation`; SHA256 `1a52f2bc14cdadf49be1ca2a6e31a42aa78fef92def0d2c25ded73cba07ee976`
  - `results/v13/nyfed-validation/summary.json` — `/methods/QR33/by_horizon/6/median_difference_pct_points`; SHA256 `1a52f2bc14cdadf49be1ca2a6e31a42aa78fef92def0d2c25ded73cba07ee976`
  - `results/v13/nyfed-validation/summary.json` — `/methods/QR33/by_horizon/6/V3`; SHA256 `1a52f2bc14cdadf49be1ca2a6e31a42aa78fef92def0d2c25ded73cba07ee976`
  - `results/v13/nyfed-validation/summary.json` — `/methods/QR33/by_horizon/24/median_relative_loss_by_validation`; SHA256 `1a52f2bc14cdadf49be1ca2a6e31a42aa78fef92def0d2c25ded73cba07ee976`
  - `results/v13/nyfed-validation/summary.json` — `/methods/QR33/by_horizon/24/median_difference_pct_points`; SHA256 `1a52f2bc14cdadf49be1ca2a6e31a42aa78fef92def0d2c25ded73cba07ee976`
  - `results/v13/nyfed-validation/summary.json` — `/methods/QR33/by_horizon/24/V3`; SHA256 `1a52f2bc14cdadf49be1ca2a6e31a42aa78fef92def0d2c25ded73cba07ee976`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:290`；The New York Fed medians fall；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/generated/v13-supplement.tex:10`；`sup:v13-checks`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/generated/v13-supplement.tex:19`；`tab:v13-validation`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/generated/v13-supplement.tex:24`；Four-feature & 6；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：QR33 is primary and QR4 separate sensitivity. At H6, longer validation also advances its endpoint18weeks and changes refit phase; no causal length-only claim. Arm-median changes are not paired-change medians.

### G2.V4.QR33

- 设计：
  - `protocol/v13/nyfed-validation-length-design.md` — `/predictions/V4`; SHA256 `aeb733a56631fcbfc501660ee5290ac2cb50a99eaa6b7d8b8fb42f3e420068be`
- 结果：
  - `results/v13/nyfed-validation/summary.json` — `/methods/QR33/V4`; SHA256 `1a52f2bc14cdadf49be1ca2a6e31a42aa78fef92def0d2c25ded73cba07ee976`
  - `results/v13/nyfed-validation/summary.json` — `/methods/QR33/by_horizon/6/infinity_count_by_validation`; SHA256 `1a52f2bc14cdadf49be1ca2a6e31a42aa78fef92def0d2c25ded73cba07ee976`
  - `results/v13/nyfed-validation/summary.json` — `/methods/QR33/by_horizon/6/V4`; SHA256 `1a52f2bc14cdadf49be1ca2a6e31a42aa78fef92def0d2c25ded73cba07ee976`
  - `results/v13/nyfed-validation/summary.json` — `/methods/QR33/by_horizon/24/infinity_count_by_validation`; SHA256 `1a52f2bc14cdadf49be1ca2a6e31a42aa78fef92def0d2c25ded73cba07ee976`
  - `results/v13/nyfed-validation/summary.json` — `/methods/QR33/by_horizon/24/V4`; SHA256 `1a52f2bc14cdadf49be1ca2a6e31a42aa78fef92def0d2c25ded73cba07ee976`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:290`；The New York Fed medians fall；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/generated/v13-supplement.tex:10`；`sup:v13-checks`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/generated/v13-supplement.tex:19`；`tab:v13-validation`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/generated/v13-supplement.tex:24`；Four-feature & 6；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：QR33 is primary and QR4 separate sensitivity. At H6, longer validation also advances its endpoint18weeks and changes refit phase; no causal length-only claim. Arm-median changes are not paired-change medians.

### G2.V3.QR4

- 设计：
  - `protocol/v13/nyfed-validation-length-design.md` — `/predictions/V3`; SHA256 `aeb733a56631fcbfc501660ee5290ac2cb50a99eaa6b7d8b8fb42f3e420068be`
- 结果：
  - `results/v13/nyfed-validation/summary.json` — `/methods/QR4/V3`; SHA256 `1a52f2bc14cdadf49be1ca2a6e31a42aa78fef92def0d2c25ded73cba07ee976`
  - `results/v13/nyfed-validation/summary.json` — `/methods/QR4/by_horizon/6/median_relative_loss_by_validation`; SHA256 `1a52f2bc14cdadf49be1ca2a6e31a42aa78fef92def0d2c25ded73cba07ee976`
  - `results/v13/nyfed-validation/summary.json` — `/methods/QR4/by_horizon/6/median_difference_pct_points`; SHA256 `1a52f2bc14cdadf49be1ca2a6e31a42aa78fef92def0d2c25ded73cba07ee976`
  - `results/v13/nyfed-validation/summary.json` — `/methods/QR4/by_horizon/6/V3`; SHA256 `1a52f2bc14cdadf49be1ca2a6e31a42aa78fef92def0d2c25ded73cba07ee976`
  - `results/v13/nyfed-validation/summary.json` — `/methods/QR4/by_horizon/24/median_relative_loss_by_validation`; SHA256 `1a52f2bc14cdadf49be1ca2a6e31a42aa78fef92def0d2c25ded73cba07ee976`
  - `results/v13/nyfed-validation/summary.json` — `/methods/QR4/by_horizon/24/median_difference_pct_points`; SHA256 `1a52f2bc14cdadf49be1ca2a6e31a42aa78fef92def0d2c25ded73cba07ee976`
  - `results/v13/nyfed-validation/summary.json` — `/methods/QR4/by_horizon/24/V3`; SHA256 `1a52f2bc14cdadf49be1ca2a6e31a42aa78fef92def0d2c25ded73cba07ee976`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:290`；The New York Fed medians fall；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/generated/v13-supplement.tex:10`；`sup:v13-checks`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/generated/v13-supplement.tex:19`；`tab:v13-validation`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/generated/v13-supplement.tex:24`；Four-feature & 6；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：QR33 is primary and QR4 separate sensitivity. At H6, longer validation also advances its endpoint18weeks and changes refit phase; no causal length-only claim. Arm-median changes are not paired-change medians.

### G2.V4.QR4

- 设计：
  - `protocol/v13/nyfed-validation-length-design.md` — `/predictions/V4`; SHA256 `aeb733a56631fcbfc501660ee5290ac2cb50a99eaa6b7d8b8fb42f3e420068be`
- 结果：
  - `results/v13/nyfed-validation/summary.json` — `/methods/QR4/V4`; SHA256 `1a52f2bc14cdadf49be1ca2a6e31a42aa78fef92def0d2c25ded73cba07ee976`
  - `results/v13/nyfed-validation/summary.json` — `/methods/QR4/by_horizon/6/infinity_count_by_validation`; SHA256 `1a52f2bc14cdadf49be1ca2a6e31a42aa78fef92def0d2c25ded73cba07ee976`
  - `results/v13/nyfed-validation/summary.json` — `/methods/QR4/by_horizon/6/V4`; SHA256 `1a52f2bc14cdadf49be1ca2a6e31a42aa78fef92def0d2c25ded73cba07ee976`
  - `results/v13/nyfed-validation/summary.json` — `/methods/QR4/by_horizon/24/infinity_count_by_validation`; SHA256 `1a52f2bc14cdadf49be1ca2a6e31a42aa78fef92def0d2c25ded73cba07ee976`
  - `results/v13/nyfed-validation/summary.json` — `/methods/QR4/by_horizon/24/V4`; SHA256 `1a52f2bc14cdadf49be1ca2a6e31a42aa78fef92def0d2c25ded73cba07ee976`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:290`；The New York Fed medians fall；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/generated/v13-supplement.tex:10`；`sup:v13-checks`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/generated/v13-supplement.tex:19`；`tab:v13-validation`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/generated/v13-supplement.tex:24`；Four-feature & 6；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：QR33 is primary and QR4 separate sensitivity. At H6, longer validation also advances its endpoint18weeks and changes refit phase; no causal length-only claim. Arm-median changes are not paired-change medians.

### G3.R1.RP

- 设计：
  - `protocol/v13/recommended-protocol-design.md` — `/predictions/R1`; SHA256 `610a2d26c29ffab472618f5aaed186bd8b29f2a6d956bb1045c29c3588b2a126`
- 结果：
  - `results/v13/recommended-protocol/summary.json` — `/R1`; SHA256 `45814a8a31cfe55f229bf0b133c028a5b1ca238db61aae7b5179b7c90906308b`
  - `results/v13/recommended-protocol/summary.json` — `/weekly`; SHA256 `45814a8a31cfe55f229bf0b133c028a5b1ca238db61aae7b5179b7c90906308b`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:350`；`sec:v13-rp`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/manuscript.tex:351`；8 cases lose by over ten percent；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/generated/v13-supplement.tex:41`；The median condition therefore passes while the tail condition fails；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/generated/v13-supplement.tex:44`；`tab:v13-routing`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：Retrospective rule designed after earlier outcomes, using inspected evaluation periods. Zero weekly median reflects majority fallback; R2 fails. Gains in FX are retained, not increased.

### G3.R2.RP

- 设计：
  - `protocol/v13/recommended-protocol-design.md` — `/predictions/R2`; SHA256 `610a2d26c29ffab472618f5aaed186bd8b29f2a6d956bb1045c29c3588b2a126`
- 结果：
  - `results/v13/recommended-protocol/summary.json` — `/R2`; SHA256 `45814a8a31cfe55f229bf0b133c028a5b1ca238db61aae7b5179b7c90906308b`
  - `results/v13/recommended-protocol/summary.json` — `/weekly`; SHA256 `45814a8a31cfe55f229bf0b133c028a5b1ca238db61aae7b5179b7c90906308b`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:350`；`sec:v13-rp`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/manuscript.tex:351`；8 cases lose by over ten percent；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/generated/v13-supplement.tex:41`；The median condition therefore passes while the tail condition fails；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/generated/v13-supplement.tex:44`；`tab:v13-routing`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：Retrospective rule designed after earlier outcomes, using inspected evaluation periods. Zero weekly median reflects majority fallback; R2 fails. Gains in FX are retained, not increased.

### G3.R3.RP

- 设计：
  - `protocol/v13/recommended-protocol-design.md` — `/predictions/R3`; SHA256 `610a2d26c29ffab472618f5aaed186bd8b29f2a6d956bb1045c29c3588b2a126`
- 结果：
  - `results/v13/recommended-protocol/summary.json` — `/R3`; SHA256 `45814a8a31cfe55f229bf0b133c028a5b1ca238db61aae7b5179b7c90906308b`
  - `results/v13/recommended-protocol/summary.json` — `/FX`; SHA256 `45814a8a31cfe55f229bf0b133c028a5b1ca238db61aae7b5179b7c90906308b`
- 正文/补充材料：
  - `submission-v10/manuscript.tex:350`；`sec:v13-rp`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/manuscript.tex:351`；8 cases lose by over ten percent；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/generated/v13-supplement.tex:41`；The median condition therefore passes while the tail condition fails；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
  - `submission-v10/generated/v13-supplement.tex:44`；`tab:v13-routing`；固定来源 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`
- 解释边界：Retrospective rule designed after earlier outcomes, using inspected evaluation periods. Zero weekly median reflects majority fallback; R2 fails. Gains in FX are retained, not increased.

### WP2.P1_QR4.QR4

- 设计：
  - `protocol/final-merge/wp2-cftc-mechanism.md` — `Markdown lines 94-96`; SHA256 `9036b0f599dd8dbef6ae9232a5f0389c5f61cde535e33f37188e1a65de59d9cb`；原文：* **P1-QR4:** among the 17 planned low-region cells, at least 80% have Delta>0.   Combined P1 passes only if both method-specific screens pass. Report both   fractions and every failure/tie independently.
  - `protocol/final-merge/wp2-input-seal.json` — `/rstar/QR4`; SHA256 `94b03ca0c36767d08c4b12ddac79a8556c1cabb56d26cdfa70141959a72cfbe7`
- 结果：
  - `results/final-merge/wp2-cftc-mechanism/summary.json` — `/tests/P1_QR4/status`; SHA256 `fee6b8656345b97f72e121bc94303a35b9fd372ea5a5d78fc083e9acae16c166`
  - `results/final-merge/wp2-cftc-mechanism/summary.json` — `/tests/P1_QR4`; SHA256 `fee6b8656345b97f72e121bc94303a35b9fd372ea5a5d78fc083e9acae16c166`
  - `results/final-merge/wp2-cftc-mechanism/summary.json` — `/primary_verdict`; SHA256 `fee6b8656345b97f72e121bc94303a35b9fd372ea5a5d78fc083e9acae16c166`
- 正文/补充材料：
  - `submission-final/manuscript.tex:374`；`sec:history-mechanism`；固定来源 `6192ec370d131c60d05e9fb103150e0e9db6aa23`；Exists in final-jof source only; absent from pinned v13. Later H4 integration must assign the new submission location.
  - `submission-final/manuscript.tex:440`；`tab:cftc-mechanism`；固定来源 `6192ec370d131c60d05e9fb103150e0e9db6aa23`
  - `submission-final/generated/final-cftc-extension.tex:1`；`sup:final-cftc`；固定来源 `6192ec370d131c60d05e9fb103150e0e9db6aa23`
  - `submission-final/generated/final-cftc-extension.tex:7`；P3 is a secondary strict decrease；固定来源 `6192ec370d131c60d05e9fb103150e0e9db6aa23`
- 解释边界：Only W520 is prospective new forecast extension; W52/W260 outcomes were already known. Same-executor scalar audit is not another author/model, second solver fit or independent data replication. QR33 high region is structurally NOT_TESTABLE; primary verdict PARTLY.

### WP2.P1_QR33.QR33

- 设计：
  - `protocol/final-merge/wp2-cftc-mechanism.md` — `Markdown lines 92-93`; SHA256 `9036b0f599dd8dbef6ae9232a5f0389c5f61cde535e33f37188e1a65de59d9cb`；原文：* **P1-QR33:** among the 34 planned market/window cells with c<r*/2, at least   80% have Delta>0.
  - `protocol/final-merge/wp2-input-seal.json` — `/rstar/QR33`; SHA256 `94b03ca0c36767d08c4b12ddac79a8556c1cabb56d26cdfa70141959a72cfbe7`
- 结果：
  - `results/final-merge/wp2-cftc-mechanism/summary.json` — `/tests/P1_QR33/status`; SHA256 `fee6b8656345b97f72e121bc94303a35b9fd372ea5a5d78fc083e9acae16c166`
  - `results/final-merge/wp2-cftc-mechanism/summary.json` — `/tests/P1_QR33`; SHA256 `fee6b8656345b97f72e121bc94303a35b9fd372ea5a5d78fc083e9acae16c166`
  - `results/final-merge/wp2-cftc-mechanism/summary.json` — `/primary_verdict`; SHA256 `fee6b8656345b97f72e121bc94303a35b9fd372ea5a5d78fc083e9acae16c166`
- 正文/补充材料：
  - `submission-final/manuscript.tex:374`；`sec:history-mechanism`；固定来源 `6192ec370d131c60d05e9fb103150e0e9db6aa23`；Exists in final-jof source only; absent from pinned v13. Later H4 integration must assign the new submission location.
  - `submission-final/manuscript.tex:440`；`tab:cftc-mechanism`；固定来源 `6192ec370d131c60d05e9fb103150e0e9db6aa23`
  - `submission-final/generated/final-cftc-extension.tex:1`；`sup:final-cftc`；固定来源 `6192ec370d131c60d05e9fb103150e0e9db6aa23`
  - `submission-final/generated/final-cftc-extension.tex:7`；P3 is a secondary strict decrease；固定来源 `6192ec370d131c60d05e9fb103150e0e9db6aa23`
- 解释边界：Only W520 is prospective new forecast extension; W52/W260 outcomes were already known. Same-executor scalar audit is not another author/model, second solver fit or independent data replication. QR33 high region is structurally NOT_TESTABLE; primary verdict PARTLY.

### WP2.P2_QR4.QR4

- 设计：
  - `protocol/final-merge/wp2-cftc-mechanism.md` — `Markdown lines 97-98`; SHA256 `9036b0f599dd8dbef6ae9232a5f0389c5f61cde535e33f37188e1a65de59d9cb`；原文：* **P2-QR4:** among 17 planned W=520 cells with c>2r*, at least 60% have Delta<0.   P2-QR33 is structurally NOT_TESTABLE and is not counted as a failed primary.
  - `protocol/final-merge/wp2-input-seal.json` — `/rstar/QR4`; SHA256 `94b03ca0c36767d08c4b12ddac79a8556c1cabb56d26cdfa70141959a72cfbe7`
- 结果：
  - `results/final-merge/wp2-cftc-mechanism/summary.json` — `/tests/P2_QR4/status`; SHA256 `fee6b8656345b97f72e121bc94303a35b9fd372ea5a5d78fc083e9acae16c166`
  - `results/final-merge/wp2-cftc-mechanism/summary.json` — `/tests/P2_QR4`; SHA256 `fee6b8656345b97f72e121bc94303a35b9fd372ea5a5d78fc083e9acae16c166`
  - `results/final-merge/wp2-cftc-mechanism/summary.json` — `/primary_verdict`; SHA256 `fee6b8656345b97f72e121bc94303a35b9fd372ea5a5d78fc083e9acae16c166`
- 正文/补充材料：
  - `submission-final/manuscript.tex:374`；`sec:history-mechanism`；固定来源 `6192ec370d131c60d05e9fb103150e0e9db6aa23`；Exists in final-jof source only; absent from pinned v13. Later H4 integration must assign the new submission location.
  - `submission-final/manuscript.tex:440`；`tab:cftc-mechanism`；固定来源 `6192ec370d131c60d05e9fb103150e0e9db6aa23`
  - `submission-final/generated/final-cftc-extension.tex:1`；`sup:final-cftc`；固定来源 `6192ec370d131c60d05e9fb103150e0e9db6aa23`
  - `submission-final/generated/final-cftc-extension.tex:7`；P3 is a secondary strict decrease；固定来源 `6192ec370d131c60d05e9fb103150e0e9db6aa23`
- 解释边界：Only W520 is prospective new forecast extension; W52/W260 outcomes were already known. Same-executor scalar audit is not another author/model, second solver fit or independent data replication. QR33 high region is structurally NOT_TESTABLE; primary verdict PARTLY.

### WP2.P2_QR33.QR33

- 设计：
  - `protocol/final-merge/wp2-cftc-mechanism.md` — `Markdown lines 83-83`; SHA256 `9036b0f599dd8dbef6ae9232a5f0389c5f61cde535e33f37188e1a65de59d9cb`；原文：has no observed c>2r* cell and its P2 is NOT_TESTABLE by design.
  - `protocol/final-merge/wp2-input-seal.json` — `/rstar/QR33`; SHA256 `94b03ca0c36767d08c4b12ddac79a8556c1cabb56d26cdfa70141959a72cfbe7`
- 结果：
  - `results/final-merge/wp2-cftc-mechanism/summary.json` — `/tests/P2_QR33/status`; SHA256 `fee6b8656345b97f72e121bc94303a35b9fd372ea5a5d78fc083e9acae16c166`
  - `results/final-merge/wp2-cftc-mechanism/summary.json` — `/tests/P2_QR33`; SHA256 `fee6b8656345b97f72e121bc94303a35b9fd372ea5a5d78fc083e9acae16c166`
  - `results/final-merge/wp2-cftc-mechanism/summary.json` — `/primary_verdict`; SHA256 `fee6b8656345b97f72e121bc94303a35b9fd372ea5a5d78fc083e9acae16c166`
- 正文/补充材料：
  - `submission-final/manuscript.tex:374`；`sec:history-mechanism`；固定来源 `6192ec370d131c60d05e9fb103150e0e9db6aa23`；Exists in final-jof source only; absent from pinned v13. Later H4 integration must assign the new submission location.
  - `submission-final/manuscript.tex:440`；`tab:cftc-mechanism`；固定来源 `6192ec370d131c60d05e9fb103150e0e9db6aa23`
  - `submission-final/generated/final-cftc-extension.tex:1`；`sup:final-cftc`；固定来源 `6192ec370d131c60d05e9fb103150e0e9db6aa23`
  - `submission-final/generated/final-cftc-extension.tex:7`；P3 is a secondary strict decrease；固定来源 `6192ec370d131c60d05e9fb103150e0e9db6aa23`
- 解释边界：Only W520 is prospective new forecast extension; W52/W260 outcomes were already known. Same-executor scalar audit is not another author/model, second solver fit or independent data replication. QR33 high region is structurally NOT_TESTABLE; primary verdict PARTLY.

### WP2.P3_QR4.QR4

- 设计：
  - `protocol/final-merge/wp2-cftc-mechanism.md` — `Markdown lines 99-101`; SHA256 `9036b0f599dd8dbef6ae9232a5f0389c5f61cde535e33f37188e1a65de59d9cb`；原文：* **P3 (secondary):** Delta_QR4(52)>Delta_QR4(260)>Delta_QR4(520) strictly in   at least 70% of the 17 markets. A tie or reversal is a counterexample.   Do not substitute an endpoint-only decrease for both successive decreases.
  - `protocol/final-merge/wp2-input-seal.json` — `/rstar/QR4`; SHA256 `94b03ca0c36767d08c4b12ddac79a8556c1cabb56d26cdfa70141959a72cfbe7`
- 结果：
  - `results/final-merge/wp2-cftc-mechanism/summary.json` — `/tests/P3_QR4/status`; SHA256 `fee6b8656345b97f72e121bc94303a35b9fd372ea5a5d78fc083e9acae16c166`
  - `results/final-merge/wp2-cftc-mechanism/summary.json` — `/tests/P3_QR4`; SHA256 `fee6b8656345b97f72e121bc94303a35b9fd372ea5a5d78fc083e9acae16c166`
  - `results/final-merge/wp2-cftc-mechanism/summary.json` — `/primary_verdict`; SHA256 `fee6b8656345b97f72e121bc94303a35b9fd372ea5a5d78fc083e9acae16c166`
- 正文/补充材料：
  - `submission-final/manuscript.tex:374`；`sec:history-mechanism`；固定来源 `6192ec370d131c60d05e9fb103150e0e9db6aa23`；Exists in final-jof source only; absent from pinned v13. Later H4 integration must assign the new submission location.
  - `submission-final/manuscript.tex:440`；`tab:cftc-mechanism`；固定来源 `6192ec370d131c60d05e9fb103150e0e9db6aa23`
  - `submission-final/generated/final-cftc-extension.tex:1`；`sup:final-cftc`；固定来源 `6192ec370d131c60d05e9fb103150e0e9db6aa23`
  - `submission-final/generated/final-cftc-extension.tex:7`；P3 is a secondary strict decrease；固定来源 `6192ec370d131c60d05e9fb103150e0e9db6aa23`
- 解释边界：Only W520 is prospective new forecast extension; W52/W260 outcomes were already known. Same-executor scalar audit is not another author/model, second solver fit or independent data replication. QR33 high region is structurally NOT_TESTABLE; primary verdict PARTLY.

## 本地预先提交与公开上传时序

公开 Git 文件提交不是外部注册平台的预注册。E5 原始设计对象在当前 checkout 不可读取，回执给出的本地预先提交时间应明确标作“保存回执记载”，不能改称已核验原始提交对象。R6、E1、E2、WP2 的原始本地提交可核验且先于新增计算，而其公开文件上传在运行后。F1/F2/F3/G2/G3 的本地和公开设计提交均先于新增计算；它们仍继承已查看的研究背景及所列回顾性边界。

| 组 | 本地设计对象/UTC | 新增计算开始 UTC | 公开上传对象/UTC | 证据边界 |
|---|---|---|---|
| E5 | `8baa2f5b44327b3ba295927bd3db954f3475d35d` / 原对象缺失；E5回执记载 2026-10-23T11:27:50-07:00 | 2026-10-23T18:30:55.774398+00:00 | `7e623612e425c16d70ab403d074cc24c32ba6203` / 2026-10-24T07:30:36+00:00 | Saved receipt records a local pre-run design; original design object is unavailable; public file upload is after the recorded run. |
| R6 | `6c0eef44c46a0ff525264b13ae1dae9b821ad3c2` / 2026-10-23T20:22:37+00:00 | 2026-10-23T20:33:19.763225+00:00 | `7e623612e425c16d70ab403d074cc24c32ba6203` / 2026-10-24T07:30:36+00:00 | Verified local Git design before new calculation; public file upload after calculation. |
| E1 | `3c5f167632a1a21ded29731a773a85ab307d3a96` / 2026-10-24T22:18:54+00:00 | 2026-10-24T22:30:48.528337+00:00 | `3230c87ce5c200ed00c3d4e3418be11b24bbde22` / 2026-10-25T00:38:34+00:00 | Verified local Git design before new calculation; public file upload after calculation. |
| E2 | `acd567c1f58fbe7fbb4194be70ff7bebbdfb2baf` / 2026-10-24T22:45:31+00:00 | 2026-10-24T23:08:56.022441+00:00 | `3230c87ce5c200ed00c3d4e3418be11b24bbde22` / 2026-10-25T00:38:34+00:00 | Verified local Git design before new calculation; public file upload after calculation. |
| F1 | `9679e15824bf24bbcf06b645688ee5c030793c30` / 2026-10-25T10:58:15+00:00 | 2026-10-25T11:41:04.218844+00:00 | `4c5abeba018b22c39dbff57d16200934af6f6c39` / 2026-10-25T11:05:41+00:00 | Local and public Git design commits before new calculation; public Git posting is not an external preregistration registry. |
| F2 | `f8628dbf83ebeebf5fcd4e494985c11603f11eb5` / 2026-10-25T10:58:15+00:00 | 2026-10-25T11:55:28.834331+00:00 | `12e86a23f0be1ad55d6ab980473972442cd006f0` / 2026-10-25T11:07:13+00:00 | Local and public Git design commits before new calculation; public Git posting is not an external preregistration registry. |
| F3 | `185e1ae9a63046b56181a77bb031c6a7a24a0138` / 2026-10-25T10:58:15+00:00 | 2026-10-25T12:03:29.365026+00:00 | `9fa50a76e9b93fa26cb0931e9bde38a4fac27485` / 2026-10-25T11:09:40+00:00 | Local and public Git design commits before new calculation; public Git posting is not an external preregistration registry. |
| G2 | `d58464ee2bf87f01e7e2625b0888edcd2e442214` / 2026-10-26T03:13:44+00:00 | 2026-10-26T03:22:14.775734+00:00 | `2f4587a2ef4784956e57fd293bf65db95a6a4660` / 2026-10-26T03:14:45+00:00 | Local and public Git design commits before new calculation; public Git posting is not an external preregistration registry. |
| G3 | `99a912ccf6911da2f54627a7b4b57fb7541b6673` / 2026-10-26T03:24:05+00:00 | 2026-10-26T03:33:01.753154+00:00 | `fcc09c3a7ee303f212fdad969a709662525c0658` / 2026-10-26T03:25:07+00:00 | Local and public Git design commits before new calculation; public Git posting is not an external preregistration registry. |
| WP2 | `effa537bd6d9b89855002aa79f95f62f9ff3761c` / 2026-10-26T03:32:15+00:00 | 2026-10-26T03:32:28.372451+00:00 | `475788a5f0387164297579005e09582eedee549d` / 2026-10-26T07:51:56+00:00 | Verified local Git design before new calculation; public file upload after calculation. |

## 保留的失败及无法判定

以下行必须出现在后续总表；敏感性可单独成 panel，但不能删除：

- `E5.P1.QR33+`：不成立 (`False`)；30/45 successes; required40.
- `E5.P2.QR33+`：不成立 (`False`)；24/48 successes; required36.
- `R6.S1.R2`：不成立 (`NOT_MET`)；26/26 complete; worst181.39452368014167%; median5.374072481175762%.
- `R6.S2.R2`：不成立 (`NOT_MET`)；One eligible cell W2880: R0=-16.62356533682211%; R2=-6.2754532709491055%; half_gain_retained=false. W720 not eligible.
- `R6.S3.R2`：不成立 (`NOT_MET`)；R0 median4.1510024714803695%; R2 median5.374072481175762%; both26 complete.
- `E1.M2.QR33`：不成立 (`NOT_SUPPORTED`)；-0.43471629487539243pp; constant0.2069371499562489%; switching-0.22777914491914353%.
- `E2.T2.QR33`：不成立 (`NOT_SUPPORTED`)；W52=19.334715757564624%; W260=10.34828178946443%.
- `F2.V1.QR4`：无法判定 (`UNDETERMINED`)；W52: delta=Nonepp, pairs=16/17, missing=1; W260: delta=Nonepp, pairs=16/17, missing=1.
- `F2.V2.QR4`：无法判定 (`UNDETERMINED`)；W52: infinity V52/V156=2/7, missing_pairs=1; W260: infinity V52/V156=2/4, missing_pairs=1.
- `F3.Q1.QR33`：无法判定 (`UNDETERMINED`)；28 supports,5 complete nonsupports (4 exact ties),1 unknown; support bounds[0.8235294117647058,0.8529411764705882].
- `F3.Q2.QR33`：无法判定 (`UNDETERMINED`)；Both period inputs FAILED;0 supports,2 unknown; both relative_loss_pct=null.
- `G2.V3.QR4`：不成立 (`NOT_SUPPORTED`)；H6: -4.2150390061995235pp (NOT_SUPPORTED); H24: -18.670087236167987pp (SUPPORTED).
- `G3.R2.RP`：不成立 (`NOT_SUPPORTED`)；8/60 adverse; worst80.98396986931891%; no unavailable cells.
- `WP2.P2_QR4.QR4`：不成立 (`NOT_SUPPORT`)；10/17;0.5882352941176471 below0.6; NOT_SUPPORT.
- `WP2.P2_QR33.QR33`：无法判定 (`NOT_TESTABLE`)；planned=0; NO_REGISTERED_REGION_CELL; NOT_TESTABLE.
- `WP2.P3_QR4.QR4`：不成立 (`NOT_SUPPORT`)；6/17;0.35294117647058826 below0.7; NOT_SUPPORT.

另保留以下上下文，不能用预测层面成立掩盖单元缺失或技术失败：

- E1-W260-incomplete：Required old-menu full-regression repetition fails in both simulation arms at W260; no all13-source replacement summary.
- F1-QR4-unavailable：QR4 D1/D2 retain2 unavailable cells each in fixed41 denominator despite supported conservative bounds.
- F2-QR4-required-missing-pairs：Each QR4 window has16/17 complete pairs and1 missing required pair; both V1 and V2 remain UNDETERMINED.
- F3-original-three-failures-retained：One CFTC and both FX required tau.99 comparisons failed; post-failure G1 repair consistency gate FAIL leaves all3 original unavailable outcomes unchanged.
- R6-rule-cell-failures：R3 rule has four retained FX/W720 failures across retro/inspected and H6/H24; S1–S3 primary R2 criteria all remain NOT_MET.
- WP2-structural-missing-region：QR33 P2 is NOT_TESTABLE with planned0; combinedP1 support and overallPARTLY cannot erase this row.

## LaTeX 总表交接约定

- 使用 JSON `rows` 的完整36行及已给定顺序；29行主/次预测与7行方法敏感性可区分 panel。
- `saved_status` 是原结果，`decision_zh` 仅翻译原状态；不得从均值、中位数、成功子样本或四舍五入重作判定。
- 两个窗口/两个 horizon 的联合阈值必须保留；F2/G2 的变化是 arm medians 之差，不是成对变化的中位数。
- WP2 P1分别列 QR4/QR33，P2分别列 QR4/QR33，P3列 QR4；P2QR33 的计划数0和 NOT_TESTABLE 必须可见。
- WP2 整体主结论是 PARTLY。W52/W260 已知，只有 W520 是新增预测。
- 本表现有正文/补充材料定位是固定来源行号和 label。后续论文重排后，由根代理更新最终章节/表号；不得把 final-jof 的 WP2 来源位置当作当前 v13 已有章节。
