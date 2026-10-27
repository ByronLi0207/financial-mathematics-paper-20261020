"""Final visual-review corrections: whitespace only, no numerical edits."""
from pathlib import Path
import json,hashlib
p=Path('submission-v10/manuscript.tex');s=p.read_text().replace(r'\theproposition (',r'\theproposition{} (');s=s.replace(' Their original short-history losses motivate the paired menu comparison below.','');p.write_text(s)
p=Path('submission-v10/title-page.tex');s=p.read_text().replace(r'\usepackage{hyperref}',r'\usepackage[hidelinks]{hyperref}').replace(r'\section*{Hard to Beat:',r'\section*{\raggedright\hyphenpenalty=10000 Hard to Beat:');p.write_text(s)
p=Path('submission-v10/generated/v10-mcs-main.tex');s=p.read_text();assert r'\tabcolsep}{2pt}'in s;s=s.replace(r'\tabcolsep}{2pt}',r'\tabcolsep}{4pt}');p.write_text(s)
p=Path('notes/v10b/style_saved_displays.py');s=p.read_text();a=s.index('def mcs_table():');b=s.index('def supplementary_table_fixes',a);s=s[:a]+s[a:b].replace(r'\tabcolsep}{2pt}',r'\tabcolsep}{4pt}')+s[b:];p.write_text(s)
p=Path('notes/v10b/visual-style-report.json');d=json.loads(p.read_text());d['root_final_spacing_refinement']={'changes':['main proposition number word-space','MCS tabcolsep 2pt to4pt','title raggedright/no hyphenation/hidelinks','remove duplicate menu-transition sentence'],'no_numeric_change':True,'new_mcs_display_sha256':hashlib.sha256(Path('submission-v10/generated/v10-mcs-main.tex').read_bytes()).hexdigest()};p.write_text(json.dumps(d,indent=2)+'\n')
p=Path('notes/v10b/visual-style-report.md');p.write_text(p.read_text()+'\nRoot逐页复核后的最终间距修正：MCS主表列距2pt→4pt，命题编号后补词间空格，标题页禁标题断词并隐藏链接彩框，删除menu重复过渡句。均不改数据，final-native-r2会重新编译；未变页面按渲染SHA复用逐页检查，变化页重新打开。\n')
