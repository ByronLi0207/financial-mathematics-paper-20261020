# Final prose - v9

English source: [current manuscript](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/submission-jof/manuscript.tex); SHA256 `83c611692ecba07dd155d9792aa71870f9f9040f88cc9143c7ea639dd9278993`.
Chinese source: [thesis](/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/notes/v9/thesis.md); SHA256 `ec07d6f63523cc4fdc94c5c0d9d1356a2451e6a759eb946918536a1ec3a400e7`.

The Chinese thesis is copied in full. The English abstract, three complete First/Second/Third paragraphs and complete conclusion are copied from the manuscript without rewriting. Only TeX escapes, italics and cross-reference display are converted to Markdown; Table 3, Table 4 and Section 7.4 are the current references.

## Chinese thesis (full)

### v9共同主线（C2结果后定稿）

预测交易商头寸峰值时，简单的历史规则很难打败。小时级FX上，长历史分位数回归相对匹配历史规则的损失在两个时期分别降低14.8%和16.6%；延迟校准后，后期优势仍为15.0%，破线数为329对328，但相对短历史滚动规则的排名随时期改变。低频比较中，历史规则通常占优：扩展正则化后的周度面板回归仍输34/48格，同一FX记录的日频版本中F赢7/8格，保守选参也未消除大的周度损失。两批既有平稳模拟并未得到同一结论：包含截距极限的旧校准设计在短历史下接近持平，PR5较窄菜单的受控设计却已产生大幅损失。本轮拟合的平稳控制在W52相对F高116.2%，参数切换过程高121.4%；不稳定性不是这些校准模拟出现损失的必要条件，真实低频损失的机制仍未识别。

#### 三条共同发现

1. 小时级FX的匹配收益在两个时期重复，后期校准后仍保留，破线数接近；滚动参照的排名随时期改变。
2. 周度汇总头寸和同记录日频比较多由历史规则占优，扩大正则化与保守验证选参没有稳定守住基准。
3. 不同平稳设计给出不同短历史结果；WP3及新拟合平稳控制本身已有大幅损失，因此本轮未识别所提不稳定性机制。

#### 预登记判断与使用边界

- N1: `SUPPORTED`。原值见 `results/v9/nonstationarity/postrun/predictions.json`。
- N2: `UNASSESSABLE`。原值见 `results/v9/nonstationarity/postrun/predictions.json`。
- N3: `NOT_SUPPORTED`。原值见 `results/v9/nonstationarity/postrun/predictions.json`。
- N4: `UNASSESSABLE`。原值见 `results/v9/nonstationarity/postrun/predictions.json`。

N1为7/13原始拒绝、Holm13为2/13。N2因W260一条来源的必需重复失败而不可评估；不能用31次成功重复补中位数。N3不成立。两个FX诊断不可用于N4。实际数值、失败和资格条件均保留。

原任务“两次平稳模拟W52近持平且W≥260更优”的前提与PR5原表不符。`results/v9/nonstationarity/prior-stationary-reconciliation.json`保存逐行核对，两个v8的菜单、时钟、特征、拟合与汇总统计量也不同。不能将它们当成同一个实验，更不能据此主张样本短必然无害。

日频和扩展回溯来自已熟悉的FX记录，不能称第三次独立验证。C2只使用原评估前数据做诊断及拟合，再生成合成预测样本；研究问题仍由此前结果引发。目标定义、地板投影和经典界只作背景，不算贡献。

## Abstract (full)

Dealers set limits on the largest absolute position reached before a review horizon ends. We compare conditional quantile forecasts with historical rules using an hourly FX record, its daily aggregates and weekly dealer positions. Simple historical rules are hard to beat. Long-history FX regression lowers matched loss by 14.8% and 16.6% across periods. Delayed calibration retains the later gain (15.0%), with 329 versus 328 breaches. Rankings against a shorter rolling rule vary by period. Expanded regularization leaves regression behind in 34 of 48 weekly panel comparisons, and historical rules win most daily comparisons. Stationary controlled simulations already produce large short-history losses. In newly calibrated simulations at history 52, the full regression's median loss increase across series is 116.2% under constant parameters and 121.4% under parameter switching. The mechanism behind the observed low-frequency losses remains unidentified. Peak-limit validation should assess accuracy, breaches and reference stability together.

## First (full)

*First, matched FX gains recur across periods, and delayed calibration retains the later gain.* Regression lowers matched loss by 14.8% and 16.6% (Table 3). Calibration retains a 15.0% gain with 329 versus 328 breaches. The earlier ranking reverses against the shorter rolling reference. Before calibration, the matched gain accompanies 376 versus 360 breaches.

## Second (full)

*Second, historical rules usually prevail in the weekly and same-record daily comparisons.* Expanded regression still loses 34 of 48 weekly panel comparisons (Table 4). Historical headroom wins seven of eight daily comparisons. Wider penalties and conservative validation leave substantial weekly losses, including a worst-cell increase of 181.4%.

## Third (full)

*Third, stationary processes can produce large short-history regression losses.* The controlled stationary design already raises 33-predictor loss by 113.5--135.5% at history 52. The newly fitted constant control raises loss by 116.2%, compared with 121.4% under parameter switching. Section 7.4 compares the designs and the incomplete longer-history results. The proposed instability explanation remains unidentified.

## Conclusion (full)

Simple historical rules are hard to beat for peak net positions. Hourly FX regression lowers matched loss by 14.8% and 16.6% across periods. Delayed calibration retains the later gain with 329 versus 328 breaches. Rankings against the shorter rolling reference change by period.

Weekly regression still loses 34 of 48 expanded-panel comparisons, and historical headroom wins most same-record daily comparisons. Conservative validation leaves substantial losses. Stationary controlled and fitted constant-parameter processes also produce large short-history losses. At history 52, the newly fitted constant control yields a median increase of 116.2%, compared with 121.4% under switching. The low-frequency mechanism remains unidentified. Peak-limit validation should compare accuracy, error amounts, breaches and reference stability together.
