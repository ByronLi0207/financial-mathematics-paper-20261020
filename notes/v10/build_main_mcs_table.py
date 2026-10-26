"""Legible main MCS summary; full bounds/classes remain in Supplement."""
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parents[2];src=root/'results/v10/mcs/report-values.json';j=json.loads(src.read_text())
lines=[r'\begin{table}[t]\centering\small',r'\caption{Ninety-percent model confidence sets across all planned comparisons. Counts retain their own comparison or conditional-procedure denominators.}\label{tab:v10-mcs-main}',r'\begin{tabular}{lrrrrr}\toprule',r'Group & Complete & Matched $F/I$ & Sole literal $F/I$ & Conditional & Prior NA \\',r' & / planned & included & & excluded & methods \\\midrule']
for row in j['groups']:
 def val(k):
  x=row['metrics'][k];return f"{x['count_successful']}/{x['denominator_successful']} ({100*x['fraction_successful']:.1f}\\%)"
 c=row['conditional_exclusion'];cond=f"{c['excluded_slots']}/{c['successful_complete_slots']} ({100*c['fraction_successful']:.1f}\\%)"
 lines.append(' & '.join([row['group_label'],f"{row['successful_comparisons']}/{row['planned_comparisons']}",val('matched_FI_membership'),val('literal_sole_FI'),cond,str(row['unavailable_method_slots'])])+r' \\')
lines += [r'\bottomrule\end{tabular}',r'\par\smallskip\begin{minipage}{.98\linewidth}\footnotesize',r'All planned comparisons complete, so successful and planned denominators coincide. Matched F/I excludes rolling references and query-nearest state baselines. Conditional exclusions count complete procedure slots; prior NA methods are not statistical exclusions. A sole exact-loss class can retain several procedures: 4/98 sets have such a class containing F/I, versus 2/98 sole literal historical methods. Related tasks are not independent replications. The Supplement retains every set, p-value, loss class, secondary membership measure and availability record.',r'\end{minipage}\end{table}','']
out=root/'submission-v10/generated/v10-mcs-main.tex';out.write_text('\n'.join(lines))
(root/'notes/v10/main-mcs-display.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),source=str(src.relative_to(root)),output_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),groups=len(j['groups']),all_inference_unchanged=True),indent=2)+'\n')
