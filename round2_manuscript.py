"""Generate round2 scientific additions from immutable archived/replayed outputs."""
import json
from v3_revision import ROOT,RESULT,para,sub,table

def augment_round2(c):
    # Keep the existing C2 table identifier and scientific numbers, while placing
    # it before the newly added Tables9--11 in reading order.
    discussion=c['sections'][8]['blocks']
    for block in list(discussion):
        if block.get('type')=='table' and block['caption'].startswith('Table 8.'):
            discussion.remove(block);c['sections'][7]['blocks'].append(block)
    paths=sorted((RESULT/'round2/shrinkage').glob('nyfed-h*-w*.json'))
    if len(paths)!=4:return
    data=[json.loads(p.read_text()) for p in paths];data.sort(key=lambda r:(r['horizon'],r['window']))
    f=lambda x:'NA' if x is None else format(float(x),'.4g')
    rows=[];comparisons=[]
    for r in data:
        norms=[a['slope_l2_norm'] for a in r['refits']]
        rows.append([r['horizon'],r['window'],f(r['selected_penalty']),str(len(norms)),f(min(norms))+'–'+f(max(norms)),f(r['aggregate_projected_native_slope_contribution']['mean_absolute']),f(r['comparison_I']['percent_pinball_difference']),f(r['comparison_F']['percent_pinball_difference'])])
        for method in ('I','F'):
            a=r['comparison_'+method];comparisons.append([r['horizon'],r['window'],method,f(a['capacity_difference']['maximum_absolute']),f(a['capacity_correlation']),f(a['headroom_correlation']),f(a['breach_jaccard']),str(a['left_breaches'])+'/'+str(a['right_breaches']),a['breach_xor']])
    norm_min=min(z['slope_l2_norm'] for r in data for z in r['refits']);norm_max=max(z['slope_l2_norm'] for r in data for z in r['refits'])
    abs_min=min(r['aggregate_projected_native_slope_contribution']['mean_absolute'] for r in data);abs_max=max(r['aggregate_projected_native_slope_contribution']['mean_absolute'] for r in data)
    gains=[-r['comparison_I']['percent_pinball_difference'] for r in data]
    c['sections'][8]['blocks'].append(para('A post-result / exploratory selected-fit readback examines the Treasury C2 menu boundary directly (Appendix I). At λ='+f(data[0]['selected_penalty'])+', standardized response-normalized slope norms range from '+f(norm_min)+' to '+f(norm_max)+'. Removing slopes while keeping each fitted intercept changes capacity by a mean absolute '+f(abs_min)+'–'+f(abs_max)+' source USD millions across the four cells. Relative to the lower empirical headroom-quantile report I, observed loss is '+f(min(gains))+'–'+f(max(gains))+'% lower; this descriptive difference has no dedicated selection-adjusted test. The fits have small normalized slopes and high headroom correlation with I, but are not identical to I or F. A boundary penalty and high capacity correlation do not by themselves demonstrate zero feature value. Three of the four C2 cells still have higher loss than F.'))
    c['sections'].append(dict(title='Appendix I. Post-result / exploratory selected-fit shrinkage diagnostics',blocks=[
      para('The diagnostic replays only the four already selected Treasury C2 fits, without validation retuning. Every C2 capacity and every frozen-F capacity exactly matches the retained origin-level traces. All per-refit coefficient vectors, standardized training transforms, response scales, norm and native contribution summaries are retained in results/revision-20261023/round2/shrinkage/. The contribution uses evaluation queries, not centered training rows; aggregate means weight the actual number of queries in each block. The intercept-only counterfactual holds the fitted intercept fixed and removes slopes, whereas I refits an intercept by the lower empirical quantile. These are distinct comparisons.'),
      table('Table I1. Treasury selected C2 coefficients and effects. Norms are in standardized/response-normalized coordinates. Mean absolute projected slope effect is in source USD millions. Loss changes are descriptive and all adverse F comparisons are retained.', ['H','W','λ','Refits','‖β‖₂ range','Mean |effect|','Δ I %','Δ F %'],[[str(x) for x in row] for row in rows]),
      table('Table I2. Pointwise C2 comparisons with I and F. Max |Δ| is capacity difference in source USD millions; ρC includes the shared issue floor, ρG removes it. J is strict-breach-set Jaccard. Hits show C2/reference and XOR counts discordant breach occasions.', ['H','W','Ref','Max |Δ|','ρC','ρG','J','Hits','XOR'],[[str(x) for x in row] for row in comparisons]),
      para('I uses rank ⌈19W/20⌉ and F uses ⌈19(W+1)/20⌉ from the same frozen mature pool. At W=260 these distinct ranks are adjacent endpoints of the empirical pinball minimizer interval; I is not a unique minimizer. All four selected penalties remain at the menu upper endpoint. The diagnostic quantifies the executed fits; it does not identify a causal feature effect or establish statistical equivalence to a historical quantile.')]))

    from round2_levy_manuscript import augment_levy
    augment_levy(c)

    from round2_panel_manuscript import augment_panel
    augment_panel(c)

    from round2_baselines_manuscript import augment_baselines
    augment_baselines(c)
