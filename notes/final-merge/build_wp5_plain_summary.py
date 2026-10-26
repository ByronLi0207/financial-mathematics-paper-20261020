"""Bind the executor's Chinese one-sentence readings to every scoped paragraph."""
from pathlib import Path
import argparse, hashlib, importlib.util, json, re

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('language',ROOT/'notes/final-merge/audit_wp5_language.py')
lang=importlib.util.module_from_spec(spec);spec.loader.exec_module(lang)
SUMMARIES={
'I':[
'限额要防的是两次检查之间的最高持仓，所以期末回落并不能说明期间没有超限。',
'复杂模型估计更多关系也会消耗有限历史，因此实务上应检验它能否胜过明确的历史基准。',
'研究比较一家外汇做市商和两套官方交易商汇总数据，各自保留单位与信息日期，不能把汇总类别当成独立交易商。',
'历史长度、惩罚候选集合和假设成本能整理这些结果，但历史规则仍很强，普适门槛和因果解释尚未识别。',
'新增期货检验只部分符合模拟与外汇的历史模式，尤其长期胜率和严格改善要求未通过。',
'扩大候选集合既可能减轻估计损失也可能直接选中历史分位数，因此应分开看候选表现、选择损失与额外预测变量的价值。',
'准备额度、超限次数和超限幅度的假设权重会改变成本排名，但尚未测得真实融资收益或交易干预效果。',
'匹配已完成标签的历史与重估时点使基准更明确，却没有统一所有特征和验证信息，因果与失败边界仍须保留。',
'文章先定义目标并报告预测比较，再把跨数据的历史证据与假设成本联系起来。',
],
'R':[
'较长历史下外汇回归在两个时期都胜过匹配基准，但换成较短滚动基准后早期排名反转。',
'短历史和较长预测期的外汇回归损失与超限次数都更差，说明长历史案例的优势只能作条件化解释。',
'延迟校准保留了相对外汇得分优势，却仍有略多超限，而且每个校准方法相对自己的未校准版本都付出了绝对得分成本。',
'状态、目标分位数和重叠回溯比较的完整结果仍保留在原补充材料的对应位置。',
'外汇回归在历史网格内先改善后回吐优势，完整曲线需要连同各自匹配基准一起看。',
'小时结果对基准敏感，所以还要比较其他记录频率与报告系统，同时保持各比较内部的历史和标签一致。',
'国库券周频比较在得分与超限上都偏向历史规则，较早短窗口的不利结果也因历史不同而单独保留。',
'更强正则化缩小了周频损失，却没有消除历史基准优势，保守选择的最差国库券案例仍然失败。',
'简化条件模型和固定组合仍有周频失败，完整损失与失败表支持继续保留历史基准。',
'改成日频后历史规则赢了大多数比较，唯一回归得分优势仍伴随更多超限。',
'原期货比较大体重复历史规则难以击败的模式，但其事后较优历史参考不能当作可执行选择规则。',
'联合方法比较通常把历史规则和多种替代方法一起留下，这表示尚未统计区分，而不是已经证明预测风险相同。',
'周频损失同时来自选择错误和有限候选集合内的表现差距，各分量中位数也不能直接相加。',
'事后挑选最好候选只能用于诊断，历史选项还可能让选择分量为负，因此部署表现和其他条件信息的价值仍未确定。',
'延长验证期后短训练历史的期货中位损失缩小，但仍按原来的目标、基准和预测日期比较。',
'较长训练历史也出现中位损失缩小，同时完整结果保留不同合约之间的差异。',
'延长验证期更常选中普通经验分位数，但这些跨合约中位数和选择次数既不证明典型配对改善也不识别因果效应。',
'极端分位数检验仍有数值失败，期货门槛和外汇综合判据都保持无法判定，不能用成功子集替代完整分组。',
'平均预测损失与是否超限衡量不同错误，所以得分改善时仍须同时报告超限。',
'误差权重改变会使特定长预测期的外汇比较反转，而较短预测期的两种误差都下降，不能把反转推广到全部比较。',
'平均损失检验、超限事件检验和状态分组诊断回答不同问题，完整解释必须保持这种区分。',
],
'H':[
'模拟选中的历史与预测期比值只是整理固定网格的描述坐标。',
'该比值没有模型参数数目，按方法分别估门槛还使常数缩放等价，因此它不能识别复杂度归一化或有效样本量。',
'首次交点及宽区间只反映给定坐标与网格内的不确定性，多次交叉和坐标选择的不确定性排除了永久充分历史的解释。',
'模拟的短长期损失方向判据通过，但保留的六个反例使全称简化命题失败。',
'部分外汇交点落入宽范围，另一条左删失曲线仍未定位首次交点，而且混合模拟交点不能等同于固定金融预测期交点。',
'较长预测期在最大历史又失去优势，这些重用的外汇记录只支持同一记录内比较，尚不构成独立交易商或全新留出样本。',
'新增期货计算先固定门槛且只扩展长历史，标签按时成熟的正确性与历史首次公开信息仍是两回事。',
'完整和稀疏回归在短历史区域的失利比例都达到预写门槛，支持这一限定范围内的短历史模式。',
'稀疏回归在长历史的胜率没有达到预写要求，因此主判定只能是部分支持。',
'只有部分稀疏回归曲线每一步都严格改善，次要严格改善判据失败且不能改变主判定。',
'七个长期不利市场、全部失败和不利曲线都保留，而较短期货结果事先已知也限制了独立确认与因果解释。',
],
'C':[
'期货成本比较同时考虑准备额度、超限事件和幅度，幅度系数固定而其余偏好变化，且网格仍有局部反转。',
'在已声明成本网格的中心，回归只在较少匹配比较中更便宜。',
'当直接超限事件收费为零且更重视准备额度时，回归在大多数匹配比较中更便宜。',
'相反地更重视超限事件时，回归很少更便宜，完整网格仍保留中间结果和例外。',
'这些排名反映假设偏好而不是实际运营开支，完整归一化和方法结果仍可追溯。',
]}

def collect(text):
    rows=[]
    for label,code in [('sec:intro','I'),('sec:results','R'),('sec:history-mechanism','H'),('sec:cost','C')]:
        mark='\\label{'+label+'}';start=text.index(mark)+len(mark);end=text.find('\\section{',start)
        raw=text[start:end if end>=0 else len(text)]
        raw=re.sub(r'\\begin\{(figure|table)\}.*?\\end\{\1\}','\n\n',raw,flags=re.S)
        raw=re.sub(r'\\\[.*?\\\]',' ',raw,flags=re.S)
        raw=re.sub(r'\\(?:subsection|subsubsection)\{[^}]*\}(?:\\label\{[^}]*\})?','\n\n',raw)
        raw=re.sub(r'(?<!\\)%[^\n]*','',raw)
        raw=re.sub(r'\\(?:FloatBarrier|input\{[^}]*\})','',raw)
        blocks=[b.strip() for b in re.split(r'\n\s*\n',raw) if re.search(r'[A-Za-z]{3}',' '.join(lang.clean(b).split()))]
        if len(blocks)!=len(SUMMARIES[code]):raise ValueError((label,len(blocks),len(SUMMARIES[code])))
        for n,(block,chinese) in enumerate(zip(blocks,SUMMARIES[code]),1):
            if chinese.count('。')!=1:raise ValueError('one Chinese sentence required')
            rows.append(dict(id=f'{code}{n:02}',section=label,source_tex=block,source_sha256=hashlib.sha256(block.encode()).hexdigest(),readable_text=' '.join(lang.clean(block).split()),chinese_summary=chinese))
    return rows

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--receipt',type=Path,default=ROOT/'notes/final-merge/wp5-plain-summary-bindings.json');args=parser.parse_args()
    source=ROOT/'submission-final/manuscript.tex';rows=collect(source.read_text());out=ROOT/'notes/final-merge'
    receipt=dict(status='PASS',source=str(source.relative_to(ROOT)),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),scope='Every narrative paragraph in Introduction, Results, history-mechanism section and cost section. Tables, captions and displayed identities are separate source/display checks.',paragraph_count=len(rows),missing_summaries=0,rows=rows)
    args.receipt.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n')
    md=['# 引言与结果的逐段外行概括','', '由同一执行者逐段阅读并写成；不是新增审稿人或跨模型复核。', '', '范围包含引言、结果、历史机制与成本四节的全部叙述段；表格、图注和公式另作数字与图形检查。每条绑定实际段落 SHA-256，覆盖情况由脚本核对。','']
    for r in rows:md += ['## '+r['id']+' — '+r['section'],'',r['chinese_summary'],'','Source paragraph SHA-256: `'+r['source_sha256']+'`.','', '> '+r['readable_text'],'']
    (out/'plain-summary.md').write_text('\n'.join(md)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k!='rows'},ensure_ascii=False))
