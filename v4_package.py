"""Package the verified sources, figures and author-facing submission drafts."""
import hashlib,html,json,re,zipfile
from pathlib import Path
from v4_submission import ROOT,OUT,NOTE,TITLE,ALTERNATES,dump,plain
from v4_typeset import pdf_document,tconv

def main():
 metrics=json.loads((NOTE/'document-metrics.json').read_text())
 title={'title':TITLE,'subtitle':'Title page for Journal of Forecasting; author completion required','abstract':'','sections':[{'title':'Author details','blocks':[
 {'type':'p','html':'Authors and affiliations: [TO BE COMPLETED BY AUTHOR].'},
 {'type':'p','html':'Corresponding author and contact: [TO BE COMPLETED BY AUTHOR].'},
 {'type':'p','html':'ORCID: [TO BE COMPLETED BY AUTHOR].'},
 {'type':'p','html':'Running title: Forecasting Position Peaks'},
 {'type':'p','html':'Funding: [TO BE COMPLETED BY AUTHOR].'},
 {'type':'p','html':'Conflict of interest: [TO BE COMPLETED BY AUTHOR].'},
 {'type':'p','html':'AI-use disclosure: [TO BE COMPLETED BY AUTHOR].'},
 {'type':'p','html':"Study code and aggregate results: <a href='https://github.com/ByronLi0207/financial-mathematics-paper-20261020'>GitHub repository</a>."}]}], 'references':[],'figures':[]}
 # Standard article source; no claim about author identity, originality declarations or consent.
 tex='\\documentclass[11pt,a4paper]{article}\n\\usepackage[margin=25mm]{geometry}\n\\usepackage[T1]{fontenc}\n\\usepackage[utf8]{inputenc}\n\\usepackage{hyperref}\n\\begin{document}\n\\section*{'+tconv(TITLE)+'}\n'
 for b in title['sections'][0]['blocks']:tex+=tconv(b['html'])+'\\par\\medskip\n'
 tex+='\\end{document}\n';(OUT/'title-page.tex').write_text(tex)
 pdf_document(title,OUT/'title-page-preview.pdf')
 # A complete union bibliography; displayed per-document lists have already been pruned.
 audit=json.loads((NOTE/'reference-audit.json').read_text());parts=[]
 for r in audit['entries']:
  meta=r['verified_metadata'];title_meta=meta.get('title',r['suggested_html']);title_meta=title_meta[0] if isinstance(title_meta,list) else title_meta
  urls=re.findall(r"href=['\"]([^'\"]+)",r['suggested_html']);url=urls[0] if urls else ''
  year=meta.get('year') or (meta.get('published',{}).get('date-parts',[[None]])[0][0])
  # Retain exact verified citation in note; no invented missing field.
  fields={'title':str(title_meta),'note':plain(r['suggested_html'])}
  if year:fields['year']=str(year)
  if meta.get('DOI'):fields['doi']=meta['DOI']
  if url:fields['url']=url
  def brace(s):return s.replace('\\','\\textbackslash{}').replace('{','\\{').replace('}','\\}').replace('%','\\%').replace('&','\\&').replace('_','\\_')
  parts.append('@misc{'+r['id']+',\n'+',\n'.join('  '+k+' = {'+brace(v)+'}' for k,v in fields.items())+'\n}\n')
 (OUT/'references.bib').write_text('\n'.join(parts))
 (OUT/'main.tex').write_text('% Overleaf default target. Select supplement.tex or title-page.tex separately.\n\\input{manuscript.tex}\n')
 (OUT/'cover-letter.md').write_text('Dear Editors of the Journal of Forecasting,\n\nPlease consider “'+TITLE+'” as a research article. The study evaluates established historical and conditional quantile procedures for a sampled net-position maximum with an observed current-position floor and explicitly matured training outcomes. Its contribution is a financial forecasting application and model-validation benchmark, rather than a new forecasting algorithm.\n\nThe inspected FX short-horizon comparison improves the stipulated quantile score while producing more breach occasions. The separately fitted Treasury regression primary deteriorates. Related aggregate tasks, parsimonious regression and filtered-simulation, peak-tail and quantile-forest baselines give mixed and frequently adverse outcomes, with failed complete cells retained. Crossed elementary-score curves and finite-menu preference comparisons delimit claims of overall forecast improvement. These accuracy, calibration and transport questions fit the journal’s interest in forecasting methods and their evaluation.\n\nThe manuscript identifies the previously inspected FX record and later exploratory analyses. The Treasury exercise is a downloaded-vintage replay by economic date, not historical public-release validation. A compatible unseen dealer sample and execution of the prospective protocol remain outstanding.\n\nAcquisition routes, source fingerprints, code and archived aggregate results are available through the linked public study repository. FX inputs are available from the original Kaggle source without assuming redistribution rights; New York Fed data retain the required attribution and terms.\n\nAuthor identity, author approval, submission declarations, funding, conflicts and applicable AI-use disclosure: [TO BE COMPLETED BY AUTHOR]. No journal submission or declaration has been made through this preparation task.\n\nSincerely,\n[TO BE COMPLETED BY AUTHOR]\n')
 (OUT/'AUTHOR-TODO.md').write_text('# 投稿前由作者本人完成\n\n- 填写作者姓名、顺序、单位、通讯方式和 ORCID，确认所有作者认可稿件。\n- 亲自填写基金、利益冲突和适用 AI 使用披露；目前均为占位符，未代为声明或签署。Wiley 当前政策见 journal-requirements.md。\n- 确认标题；备选：\n'+''.join('  - '+x+'\n' for x in ALTERNATES)+'- 上传 overleaf-package.zip；主文件 main.tex，另选 supplement.tex 和 title-page.tex 分别编译并逐页检查正式输出。应用内置编译诊断通过不等于已导出正式PDF；随包PDF为ReportLab预览。\n- 复核两条来源的实际获取权限及 NYFed 归属/条款，按提交时状态更新数据声明。原始 FX 和私有逐期预测没有再分发。\n- 按审稿系统要求选择文章类型并检查最新要求；本次未注册账号、未投稿、未代签 originality/author approval 等表。\n- 参考文献仍有明确待核字段：MaxVaR页码冲突已暂省；van den Hoogen专业暂省；Christoffersen/Koenker结束页及Jr.本轮注册字段核实不完整，详见reference-audit.md。\n- 认识证据限制：缺兼容的第二交易商样本，前瞻协议未执行，强基线六个NA保留；本次不补造外部验证。\n- PR只供审阅；是否合并main由用户另行决定。\n')
 (OUT/'README.md').write_text('# Journal of Forecasting submission preparation\n\nThis is a preparation package, not a journal submission or acceptance claim. The official guideline check identifies single-blind review and Free Format initial submission. Personal author and disclosure fields remain placeholders.\n\n- manuscript.tex / manuscript-preview.pdf: main article; '+str(metrics['manuscript']['pages'])+' preview pages, '+str(metrics['manuscript']['prose_words_excluding_abstract_references_tables_captions'])+' prose words excluding abstract, references, tables and captions.\n- supplement.tex / supplement-preview.pdf: '+str(metrics['supplement']['pages'])+' pages, all original tables retained across the two documents.\n- title-page.tex / title-page-preview.pdf: author completion sheet.\n- references.bib: union of verified metadata dispositions; each document displays only its own cited references in consistent author–date format under Free Format.\n- figures/: grayscale vector assets; all curve-display values and original figure numbers are preserved.\n- overleaf-package.zip: select main.tex for the article; supplement.tex and title-page.tex are separate targets. Sources use standard article/packages and relative vector assets, with no local font path dependency.\n- cover-letter.md: draft for author completion; no signed declarations.\n- AUTHOR-TODO.md: remaining personal actions and evidential limitations.\n\nPreview PDFs are independently typeset with ReportLab. Saved TeX source compilation is checked using the desktop editor compiler, which returns diagnostics rather than an exported PDF. Formal TeX-generated PDFs must be obtained and inspected by the author before submission.\n\nNumerical checks, full selected-suite pytest output, source/figure bindings, preservation and visual receipts are in notes/revision-v4-jof/. No forecast model was refitted in this revision. Build the content and previews with v4_scientific_port.py, v4_submission.py, v4_figures.py and v4_typeset.py using existing dependencies; check with v4_numeric.py; package with v4_package.py.\n')
 included=[OUT/'main.tex',OUT/'manuscript.tex',OUT/'supplement.tex',OUT/'title-page.tex',OUT/'references.bib',OUT/'README.md',*sorted((OUT/'figures').glob('*.pdf'))]
 with zipfile.ZipFile(OUT/'overleaf-package.zip','w',zipfile.ZIP_DEFLATED) as z:
  for path in included:z.write(path,path.relative_to(OUT))
 files={str(p.relative_to(OUT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in included}
 dump(NOTE/'overleaf-manifest.json',{'files':files,'sha256':hashlib.sha256((OUT/'overleaf-package.zip').read_bytes()).hexdigest(),'targets':['main.tex','supplement.tex','title-page.tex'],'absolute_asset_paths':False})
 print('Author placeholders, cover letter, union bibliography, complete relative-asset ZIP and title preview created.')

if __name__=='__main__':main()
