#!/usr/bin/python3
from pathlib import Path
import json, subprocess
R=Path(__file__).resolve().parents[2]
N=Path(__file__).resolve().parent
e=json.loads((N/'R0-author-guidelines-observation.json').read_text())
text=(R/'submission-package/ASMBI/journal-checklist.md').read_text()
assert e['abstract_limit_words']==250 and e['keywords_max']==5
assert e['running_title_max_characters']==70 and e['font_points']==12
assert e['initial_free_format'] and e['references_ama'] and e['references_superscript']
assert e['separate_supporting_information'] and e['self_contained_si_references']
assert '未明确' in text and '未核实' in text and 'AMA' in text
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
remote=subprocess.check_output(['git','rev-parse','FETCH_HEAD'],cwd=R,text=True).strip()
assert head==remote=='3dba6d906fc181be116c0b630ea97fd1a79fee7c'
result={'step':'R0','status':'PASS','live_official_guide_observed_utc':e['observed_utc'],'abstract_limit':e['abstract_limit_words'],'keywords_limit':e['keywords_max'],'reference_style':'AMA, consecutive superscript numbers; consistent style allowed at first submission','template_route':'Free Format accepted; NJD recommended','supporting_information':'separate and self-contained','blind_review':'UNVERIFIED; author guide only specifies two independent referees','remote_local_head_equal':True}
(N/'R0-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
