"""B5 writing-only responses to fifteen internal simulated concerns."""
import json
from pathlib import Path
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[2]


def replace_once(text,old,new):
    assert text.count(old)==1,old[:100]
    return text.replace(old,new,1)


if __name__=='__main__':
    p=ROOT/'submission-jof/manuscript.tex';text=p.read_text();changes=[]
    edits=[
      ('Two pre-specified comparisons anchor the analysis.','Two comparisons, pre-specified in the original execution protocol, anchor the analysis.','M3: define the protocol-relative meaning of pre-specified.'),
      ('The Treasury-bill series has 706 economic-date observations in USD millions.','The Treasury-bill series has 706 economic-date observations in USD millions. These are reported fair-value positions aggregated as long-minus-short totals.','F3: clarify measurement using existing FR2004 reference, checked SectionIII.A/p13.'),
      ('The horizons \\(H\\in\\{6,24\\}\\) count subsequent source records, and each peak includes the issue position.','The horizons \\(H\\in\\{6,24\\}\\) count subsequent source records, and each peak includes the issue position. Calendar gaps extend the elapsed span of an FX horizon, while weekly steps represent a different review interval.','F4: distinguish observation-count and calendar horizons.'),
      ('Accuracy uses mean pinball loss; breaches are strict peak exceedances.','Accuracy uses mean pinball loss; breaches are strict peak exceedances. Evaluation scores passive reports on the observed position paths.','F1: identify the evaluated report and fixed path, without claiming intervention benefits.'),
      ('The preceding validation segment selects parameters; the entire specified evaluation grid then receives forecasts.','The preceding validation segment selects parameters; the entire specified evaluation grid then receives forecasts. Validation labels overlap in time.','M4: identify overlapping validation labels.'),
      ('The wrapper comparison is a separate finite projected delayed ACI-style exercise.','The wrapper comparison is a separate finite projected delayed ACI-style exercise; both regression and historical headroom are calibrated in that row.','M1: explicit wrapped control.'),
      ('Original matched Holm uses 72 contrasts. The later regrouped family is separate and documented in the Supplement.','Original matched Holm uses 72 contrasts. Each adjusted p-value applies only to its named family; the later regrouped family is separate.','M2: identify multiplicity scope without changing any p-value.'),
      ('Stationary weekly simulations favor regression with longer histories, unlike the financial record.','The calibrated simulation does not reproduce the persistent weekly losses in the financial record.','M5/E3: state the unsuccessful mechanism result directly.'),
      ('Trading and funding gains are not measured, and scoring weights do not identify actual decision costs. The calibrated simulations leave the hourly mechanism unresolved and fail to reproduce persistent weekly losses. Their DGPs bundle frequency, validation length and volatility laws.',
       'Trading and funding gains are not measured, and scoring weights do not identify actual decision costs. Independent dealer data and prospective evaluation are needed for broader validation. Valuation, gross-exposure and decision-cost observations would connect forecasts to inventory actions.\n\nThe calibrated simulations leave the hourly mechanism unresolved and fail to reproduce persistent weekly losses. Their DGPs bundle frequency, validation length and volatility laws. Isolating these effects and studying failed hourly fits requires a separate experiment. Longer chronologically eligible validation histories also require future evaluation.',
       'M3-M5/F1-F5/E2-E3: explicit future-data and future-design needs in Limitations.')]
    for old,new,reason in edits:
        text=replace_once(text,old,new);changes.append(dict(old=old,new=new,reason=reason))
    old='Relative to the endpoint and path-risk precedents in Table~\\ref{tab:literature}, the contribution is three comparative findings. First, matched FX gains of 14.8\\% and 16.6\\% recur across periods; the later gain survives calibration, while the shorter rolling reference changes the earlier ranking (Table~\\ref{tab:fx}). Second, expanded regression still loses 34 of 48 weekly panel comparisons, while conservative validation leaves a 181.4\\% worst-cell excess (Table~\\ref{tab:weekly}). Third, the matched FX score gain accompanies 376 versus 360 breaches; the two original comparisons have crossing elementary-score curves (Table~\\ref{tab:diagnostics}; Figures~\\ref{fig:murphyfx}--\\ref{fig:murphybill}). The forecasting and scoring methods are standard.'
    new='Table~\\ref{tab:literature} distinguishes the peak response from earlier endpoint and path-risk tasks. First, matched FX gains of 14.8\\% and 16.6\\% recur; the later gain survives calibration, while reference rankings change (Table~\\ref{tab:fx}). Second, expanded weekly regression loses 34 of 48 comparisons, and conservative validation leaves a 181.4\\% worst excess (Table~\\ref{tab:weekly}). Third, matched FX gains accompany 376 versus 360 breaches; the original comparisons have crossing elementary-score curves (Table~\\ref{tab:diagnostics}; Figures~\\ref{fig:murphyfx}--\\ref{fig:murphybill}).'
    text=replace_once(text,old,new);changes.append(dict(old=old,new=new,reason='E4: shorten duplicated signposting while retaining the same three numbered empirical points.'))
    p.write_text(text)
    with (ROOT/'notes/v8/mock-writing-changes.json').open('x') as f:json.dump(changes,f,indent=2);f.write('\n')
    todo=ROOT/'submission-jof/AUTHOR-TODO.md';t=todo.read_text()
    t=t.replace('- Inspect and approve the new PR/compare view. Do not merge the main branch or PR #3 as part of this task.','- Inspect the revision-v8 compare view after publication. Creating or merging any PR is a later author decision; this task publishes revision-v8 only.')
    t=t.replace('This revision adds no model, financial sample, statistical test or prospective issuance.','The v8 experiment adds the prespecified calibrated simulation; it adds no financial forecast re-evaluation, new financial sample or prospective issuance.')
    t+='''
## v8 simulated-review follow-up decisions

- T1 (M3, F2, E2): obtain a compatible independent dealer record and a genuinely prospective protocol before expanding the within-record stability claim. Related weekly categories remain one reporting system.
- T2 (M4): assess longer chronologically eligible validation histories in a separate future design; retain the current short-validation and 181.4% adverse result. Do not retune the present exercise.
- T3 (M5, E3): decide whether to study hourly numerical feasibility and separate frequency, validation length and volatility mechanisms. Any later solver study or rerun needs a separate fixed design and must retain the seven v8 failed cells.
- T4 (F1, F3-F5): obtain valuation/gross-exposure, finer-frequency exposure and intervention/decision-cost data before studying inventory-policy, trading or funding benefits. Current results score passive reports only.
- T5 (E1): retain the chosen title unless the author selects a more narrowly descriptive alternative. The three contributions remain empirical; elementary target properties and standard forecasting/scoring tools are background.
- T6 (E5): complete personal author/ORCID/funding/conflict/AI fields, verify data permissions and live journal forms, and review the final v8 package. These fields remain placeholders throughout this task.
'''
    todo.write_text(t)
    records=[
      ('M1','比较基准与包装公平性','已改','Table 3表注明确双方均校准；摘要/贡献使用14.8%匹配对照，滚动对照分列。','无需新数据。'),
      ('M2','推断与多重比较','已改','Section 6保留探索性推断定位；Table 5表注明确调整p只属于所命名比较族，原值全部保留。','无需重算或新检验。'),
      ('M3','2015回顾性与复制含义','已改并限定','Introduction定义原执行协议固定的比较；Section 9明确已见历史与2015事后设计。','T1：独立交易商/前瞻观察。'),
      ('M4','短验证与重叠标签','已改并保留负面','Section 6明示验证标签重叠；Table 4保留每格52评估点及181.4%最差单元；Supplement给选择规则。','T2：更长验证设计，本轮不补跑。'),
      ('M5','模拟机制与数值失败','已改','Section 7.4首句直接说明未重现周度损失；Supplement S26.4区分数值不可用与预测准确性。','T3：解耦设计/数值可执行性。'),
      ('F1','预测报告与库存政策','已改','Section 6明确在观测路径上评分被动报告；Section 8建议仍为模型验证。','T4：干预及成本数据。'),
      ('F2','代表性与外推','已改并限定','Section 4保留不同测量单位；Section 9集中单FX、同报告体系与回顾性范围。','T1：扩大外推前取得独立证据。'),
      ('F3','周度测量口径','已改','Section 4补明fair-value与long-minus-short；FR2004 Section III.A公允价值规则已核对。','T4：估值/总敞口渠道需新数据。'),
      ('F4','记录数与经济期限','已改','Section 5在H定义旁说明FX缺口延长日历跨度、周度步长不同；Section 9保留采样遗漏。','T4：更高频实际敞口。'),
      ('F5','分数与经济价值','保留明确边界','Section 8联合报告损失、U/V和破线；Section 9明确未测量交易/资金收益与实际决策成本。','T4：货币效用另行设计。'),
      ('E1','贡献、标题与JoF定位','已改定位；标题保留','三条经验发现覆盖五处，初等理论降级；cover letter定位于比较预测评价。','T5：标题改选由作者决定。'),
      ('E2','经验广度','不扩大主张','Section 9与T1保留单记录/相关聚合限制；不把13类当13位独立交易商。','需要新数据，超出本轮。'),
      ('E3','模拟增加何种证据','已改','Section 7.4/图4/Table 6明示失败或未支持；第三条贡献采用分数与破线分歧。','T3：后续机制实验。'),
      ('E4','重复与摘要密度','已缩短Section 2','保留任务要求的三条同口径定位；摘要9个数字对应三组必要比较，仍低于10个上限。','不删必要对照或负面数字。'),
      ('E5','投稿包与可用性','B6顺序收尾','README、包清单、编译源和声明将在B6统一；作者占位符保持，T6记录个人核实。','B6完成后将本项更新为已核对。')]
    with (ROOT/'notes/v8/mock-responses.json').open('x') as f:json.dump(records,f,indent=2,ensure_ascii=False);f.write('\n')
    sections=['# v8内部模拟审稿与回应','', '三份意见由同一模型的独立角色生成；每份五条、少于300英文词，相当于一页以内的审稿文本。它们是内部压力测试，不代表外部审稿、期刊意见或录用预测。','']
    for filename in ['mock-methodology.md','mock-finance.md','mock-editor.md']:
        sections.append((ROOT/'notes/v8'/filename).read_text());sections.append('\n---\n')
    sections+=['## 逐条回应','', '|编号|质疑|处理|对应改动或证据|后续边界|','|---|---|---|---|---|']
    sections+=['|'+'|'.join(r)+'|' for r in records]
    sections+=['','新数据与新实验需求集中写入Section 9及AUTHOR-TODO的T1--T6。本轮没有启动这些扩展。']
    with (ROOT/'notes/v8/mock-referees.md').open('x') as f:f.write('\n'.join(sections)+'\n')
    print('Applied',len(changes),'writing clarifications;15 responses; no result changes')
