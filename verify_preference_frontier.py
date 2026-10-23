"""Independent exact-affine readback; no production imports or financial fits.

For each method, intersect every inequality J_method(alpha)<=J_other(alpha)
with [0,1]. These feasible intervals independently identify all open winners
and boundary ties. Exactness concerns the frozen CSV decimal tokens only.
"""
import argparse
import csv
from fractions import Fraction
import hashlib
import io
import itertools
import json
from pathlib import Path
import re
import sys
import time


ROOT=Path(__file__).resolve().parent
FREEZE='protocol/revision-20261022/preference-robustness-freeze.json'
PREFIX='results/revision-20261022/'
INPUTS={
    PREFIX+'evaluation-summary.csv':('full','core'),
    PREFIX+'ar1-replay/ar1-summary.csv':('full','ar'),
    PREFIX+'rank-ablation/summary.csv':('full','rank'),
    PREFIX+'evaluation-nonoverlap.csv':('sparse','core'),
    PREFIX+'ar1-replay/ar1-nonoverlap.csv':('sparse','ar'),
    PREFIX+'rank-ablation/nonoverlap.csv':('sparse','rank')}
CORE={'QR','KNN','SCALED_KNN','frozen_F','frozen_S','frozen_K'}
METHODS=CORE|{'AR1_REPLAY','I'}
SOURCES={'fx_hourly':('USD',(720,2880),6625,24),
         'nyfed_weekly':('USD millions',(52,260),277,13)}
DECIMAL=re.compile(r'(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\Z')


def require(condition,message):
    if not condition:raise ValueError(message)


def decimal_value(token):
    require(isinstance(token,str) and len(token)<=128 and DECIMAL.fullmatch(token),
            'invalid nonnegative decimal token')
    if 'e' in token.lower():
        require(abs(int(token.lower().split('e')[1]))<=308,'decimal exponent bound')
    value=Fraction(token)
    require(value>=0,'negative coefficient')
    return value


def rational(token):
    require(isinstance(token,str) and re.fullmatch(r'[0-9]+/[1-9][0-9]*',token),
            'invalid rational boundary')
    value=Fraction(token)
    require(0<=value<=1 and token==fraction_token(value),'noncanonical boundary')
    return value


def fraction_token(value):return f'{value.numerator}/{value.denominator}'


def _unique_object(pairs):
    result={}
    for key,value in pairs:
        require(key not in result,'duplicate JSON key')
        result[key]=value
    return result


def read_json_bytes(raw):
    return json.loads(raw.decode('utf-8'),object_pairs_hook=_unique_object,
                      parse_constant=lambda _:(_ for _ in ()).throw(ValueError('nonfinite JSON')))


def coefficients(methods):
    require(isinstance(methods,dict) and methods,'empty method family')
    require(all(isinstance(name,str) and name for name in methods),'invalid method label')
    return {name:(decimal_value(row['u_token']),decimal_value(row['v_token']))
            for name,row in methods.items()}


def feasible_intervals(methods):
    """Solve a finite system of scalar affine inequalities for each method."""
    values=coefficients(methods);answer={}
    for name,(u,v) in values.items():
        lo,hi=Fraction(0),Fraction(1);possible=True
        for other,(U,V) in values.items():
            # (u-v-U+V)*alpha <= V-v, solved without pair-grid sampling.
            slope=u-v-U+V;rhs=V-v
            if slope>0:hi=min(hi,rhs/slope)
            elif slope<0:lo=max(lo,rhs/slope)
            elif rhs<0:possible=False;break
        answer[name]=(lo,hi) if possible and lo<=hi else None
    return answer


def pair_relation(left,right):
    u,v=map(decimal_value,left);U,V=map(decimal_value,right)
    if (u,v)==(U,V):return 'identical',None
    relation=('left_dominates' if u<=U and v<=V else
              'right_dominates' if u>=U and v>=V else 'crosses')
    slope=u-v-U+V
    cross=(V-v)/slope if slope else None
    equality=fraction_token(cross) if cross is not None and 0<=cross<=1 else None
    return relation,equality


def _names(value):
    require(isinstance(value,list) and all(isinstance(v,str) for v in value),'invalid name list')
    require(len(set(value))==len(value),'duplicate method name')
    return tuple(sorted(value))


def expected_frontier(methods):
    intervals=feasible_intervals(methods)
    boundaries={Fraction(0),Fraction(1)}
    for bounds in intervals.values():
        if bounds is not None:boundaries.update(bounds)
    boundaries=sorted(boundaries)
    def active(alpha):
        return tuple(sorted(name for name,bounds in intervals.items()
                            if bounds is not None and bounds[0]<=alpha<=bounds[1]))
    points={alpha:active(alpha) for alpha in boundaries}
    regions={}
    for lo,hi in zip(boundaries,boundaries[1:]):
        winners=active((lo+hi)/2)
        require(winners,'infeasible finite lower envelope')
        regions[lo,hi]=winners
    return regions,points,intervals


def verify_group(group):
    """Validate all mathematical outputs, including omitted and isolated winners."""
    methods=group['methods'];values=coefficients(methods)
    regions,points,intervals=expected_frontier(methods)
    actual_regions={}
    for row in group['frontier']['regions']:
        key=rational(row['left']),rational(row['right'])
        require(key[0]<key[1] and key not in actual_regions,'duplicate/empty frontier region')
        actual_regions[key]=_names(row['methods'])
    actual_points={}
    for row in group['frontier']['points']:
        alpha=rational(row['alpha'])
        require(alpha not in actual_points,'duplicate frontier point')
        actual_points[alpha]=_names(row['methods'])
    require(actual_regions==regions,'open frontier regions disagree with inequalities')
    require(actual_points==points,'boundary frontier winners disagree with inequalities')
    expected_pairs={};dominated=set()
    for left,right in itertools.combinations(sorted(methods),2):
        relation,equality=pair_relation(
            (methods[left]['u_token'],methods[left]['v_token']),
            (methods[right]['u_token'],methods[right]['v_token']))
        expected_pairs[left,right]=(relation,equality)
        if relation=='left_dominates':dominated.add(right)
        if relation=='right_dominates':dominated.add(left)
    actual_pairs={}
    for row in group['pairs']:
        left,right=row['left'],row['right']
        require(left in methods and right in methods and left!=right,'invalid pair labels')
        relation,equality=row['relation'],row['equality_alpha']
        if equality is not None:rational(equality)
        if left>right:
            left,right=right,left
            relation={'left_dominates':'right_dominates','right_dominates':'left_dominates'}.get(relation,relation)
        require((left,right) not in actual_pairs,'duplicate pair')
        actual_pairs[left,right]=relation,equality
    require(actual_pairs==expected_pairs,'pair inventory/relation/crossing mismatch')
    require(_names(group['dominated_methods'])==tuple(sorted(dominated)),'domination mismatch')
    alpha=Fraction(19,20)
    winners=tuple(sorted(name for name,bounds in intervals.items()
                         if bounds is not None and bounds[0]<=alpha<=bounds[1]))
    require(_names(group['winners_at_095'])==winners,'.95 winner mismatch')
    return dict(methods=len(values),pairs=len(expected_pairs),regions=len(regions),points=len(points))


def _identity(raw):return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def _read_bound(root,item):
    relative=item['path'];path=Path(relative)
    require(not path.is_absolute() and '..' not in path.parts,'unsafe frozen path')
    raw=(root/path).read_bytes();identity=_identity(raw)
    require(identity=={k:item[k] for k in ('bytes','sha256')},'frozen file identity mismatch: '+relative)
    return raw


def read_sources(root,freeze):
    entries=freeze['input_files']
    require(len(entries)==len(INPUTS) and {r['path'] for r in entries}==set(INPUTS),'input inventory mismatch')
    selected={};all_rows={};identities=[]
    for entry in entries:
        raw=_read_bound(root,entry);sample,kind=INPUTS[entry['path']]
        reader=csv.DictReader(io.StringIO(raw.decode('utf-8'),newline=''))
        require(reader.fieldnames and len(set(reader.fieldnames))==len(reader.fieldnames),'duplicate CSV header')
        seen=set()
        for row in reader:
            require(None not in row and all(value is not None for value in row.values()),'ragged CSV row')
            s=row['source'];h=int(row['horizon']);w=int(row['window']);method=row['method']
            key=s,h,w,method
            require(key not in seen,'duplicate source row');seen.add(key)
            if kind=='core':all_rows[sample,s,h,w,method]=row
            keep=method in CORE if kind=='core' else method==('AR1_REPLAY' if kind=='ar' else 'I')
            if not keep:continue
            require(s in SOURCES and h in (6,24) and w in SOURCES[s][1],'unexpected source cell')
            unit,_,full_count,step=SOURCES[s]
            count=full_count if sample=='full' else (full_count-1)//(h+1)+1
            require(row['native_unit']==unit and int(row['origin_count'])==count and int(row['refit_step'])==step,
                    'source unit/count/refit mismatch')
            if kind=='ar':require(row['status']=='COMPLETE','incomplete AR source row')
            output_key=sample,s,h,w,method
            require(output_key not in selected,'duplicate selected input')
            for field in ('mean_positive_overrun','mean_unused_allowance','mean_pinball'):decimal_value(row[field])
            require(0<=int(row['strict_breach_count'])<=count,'invalid source breach count')
            selected[output_key]=row
        identities.append(dict(path=entry['path'],**_identity(raw)))
    expected={(sample,s,h,w,m) for sample in ('full','sparse') for s in SOURCES
              for h in (6,24) for w in SOURCES[s][1] for m in METHODS}
    require(set(selected)==expected,'selected input cell inventory mismatch')
    return selected,all_rows,identities


HEADLINES={
    'fx_h6_primary':(('fx_hourly',6,2880,'QR'),('fx_hourly',6,720,'rolling_F')),
    'fx_h6_matched':(('fx_hourly',6,2880,'QR'),('fx_hourly',6,2880,'frozen_F')),
    'fx_h24_legacy':(('fx_hourly',24,2880,'QR'),('fx_hourly',24,720,'rolling_S')),
    'treasury_h6_primary':(('nyfed_weekly',6,260,'QR'),('nyfed_weekly',6,260,'frozen_F'))}


def verify_result(result,selected,all_rows):
    require(type(result['schema_version']) is int and result['schema_version']==1,'unsupported result schema')
    groups=result['groups'];seen=set();counts=dict(groups=0,methods=0,pairs=0,regions=0,points=0)
    for group in groups:
        key=group['sample'],group['source'],group['horizon'],group['window']
        require(type(group['horizon']) is int and type(group['window']) is int,'invalid result cell indices')
        require(key not in seen,'duplicate result group');seen.add(key)
        require(set(group['methods'])==METHODS,'result method inventory mismatch')
        for method,row in group['methods'].items():
            require(key+(method,) in selected,'unexpected result group')
            source=selected[key+(method,)]
            require(row['u_token']==source['mean_positive_overrun'] and row['v_token']==source['mean_unused_allowance']
                    and row['mean_pinball']==source['mean_pinball'],'source decimal token mismatch')
            require(type(row['strict_breach_count']) is int and row['strict_breach_count']==int(source['strict_breach_count']),
                    'source strict breach mismatch')
            require(group['native_unit']==source['native_unit'] and type(group['origin_count']) is int
                    and group['origin_count']==int(source['origin_count']),'result group metadata mismatch')
            # Stored means use separately rounded floating summaries. This is
            # a consistency tolerance, not exact equality of financial means.
            score=Fraction(19,20)*decimal_value(row['u_token'])+Fraction(1,20)*decimal_value(row['v_token'])
            recorded=decimal_value(row['mean_pinball'])
            require(abs(score-recorded)<=Fraction(1,10**10)*max(Fraction(1),recorded),'.95 score reconstruction mismatch')
        checked=verify_group(group);counts['groups']+=1
        for name,value in checked.items():counts[name]+=value
    require(seen=={key[:4] for key in selected},'result group inventory mismatch')
    headlines=result['headline_comparisons'];seen_headlines=set()
    require(isinstance(headlines,list),'invalid headline list')
    headline_fields={'id','source','horizon','left_method','right_method',
                     'left_window','right_window','left','right','relation','equality_alpha'}
    statistic_fields={'u_token','v_token','mean_pinball','strict_breach_count'}
    for row in headlines:
        require(isinstance(row,dict) and headline_fields<=row.keys(),'incomplete headline record')
        name=row['id']
        require(isinstance(name,str) and name in HEADLINES and name not in seen_headlines,
                'headline inventory mismatch')
        seen_headlines.add(name)
        left_key,right_key=HEADLINES[name]
        require(all(isinstance(row[field],str) for field in ('source','left_method','right_method'))
                and all(type(row[field]) is int for field in ('horizon','left_window','right_window')),
                'headline identity type mismatch')
        require(row['source']==left_key[0]==right_key[0]
                and row['horizon']==left_key[1]==right_key[1]
                and row['left_window']==left_key[2] and row['right_window']==right_key[2]
                and row['left_method']==left_key[3] and row['right_method']==right_key[3],
                'headline identity mismatch')
        for side,key in zip(('left','right'),HEADLINES[name]):
            source=all_rows[('full',)+key]
            saved=row[side]
            require(isinstance(saved,dict) and statistic_fields<=saved.keys(),'incomplete headline side record')
            require(all(isinstance(saved[field],str) for field in ('u_token','v_token','mean_pinball'))
                    and type(saved['strict_breach_count']) is int,'headline statistic type mismatch')
            require(saved['u_token']==source['mean_positive_overrun']
                    and saved['v_token']==source['mean_unused_allowance']
                    and saved['mean_pinball']==source['mean_pinball'],'headline source token mismatch')
            require(saved['strict_breach_count']==int(source['strict_breach_count']),
                    'headline source strict breach mismatch')
        relation,equality=pair_relation((row['left']['u_token'],row['left']['v_token']),
                                        (row['right']['u_token'],row['right']['v_token']))
        require(row['relation']==relation and row['equality_alpha']==equality,'headline relation mismatch')
    require(seen_headlines==set(HEADLINES),'missing headline comparison')
    return dict(**counts,headline_comparisons=len(headlines))


def verify_files(result_path,output_path,*,root=ROOT):
    """Write an exclusive success receipt after same-snapshot verification."""
    started=time.monotonic();root=Path(root).resolve();output_path=Path(output_path)
    require(not output_path.exists(),'verification output already exists')
    freeze_raw=(root/FREEZE).read_bytes();freeze=read_json_bytes(freeze_raw)
    require(freeze['schema_version']==1,'unsupported freeze schema')
    closure=freeze['implementation_files']+[freeze['design_file']]
    require(len({r['path'] for r in freeze['implementation_files']})==len(freeze['implementation_files']),
            'duplicate implementation freeze entry')
    require('verify_preference_frontier.py' in {r['path'] for r in closure},'verifier missing from freeze')
    for entry in closure:_read_bound(root,entry)
    selected,all_rows,identities=read_sources(root,freeze)
    result_raw=Path(result_path).read_bytes();result=read_json_bytes(result_raw)
    counts=verify_result(result,selected,all_rows)
    require((root/FREEZE).read_bytes()==freeze_raw,'freeze changed during verification')
    for entry in closure+freeze['input_files']:_read_bound(root,entry)
    require(Path(result_path).read_bytes()==result_raw,'result changed during verification')
    receipt=dict(schema_version=1,status='VERIFIED',
        scope='Independent affine-inequality validation of fixed decimal-summary preference frontiers; no raw-loss refit or new observations',
        freeze_identity=_identity(freeze_raw),result_identity=_identity(result_raw),
        verifier_identity=_identity(Path(__file__).read_bytes()),inputs=identities,counts=counts,
        elapsed_seconds=time.monotonic()-started)
    with output_path.open('x',encoding='utf-8') as stream:json.dump(receipt,stream,indent=2);stream.write('\n')
    return receipt


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--result');parser.add_argument('--output')
    args=parser.parse_args(argv)
    if args.result is None and args.output is None:parser.print_help();return 0
    parser.error('--result and --output must be supplied together') if not (args.result and args.output) else None
    try:receipt=verify_files(args.result,args.output)
    except (ValueError,KeyError,TypeError,OSError,csv.Error) as exc:
        print(json.dumps(dict(status='FAILED',reason=str(exc))),file=sys.stderr);return 1
    print(json.dumps(dict(status=receipt['status'],counts=receipt['counts'])));return 0


if __name__=='__main__':raise SystemExit(main())
