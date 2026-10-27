"""Read back public aggregate scalars only; no financial arrays or model imports."""
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PUBLIC=ROOT/'results/revision-20261023/v6'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close(left,right):
    assert math.isclose(left,right,rel_tol=1e-12,abs_tol=1e-8),(left,right)


def verify_holm(rows,family_n,declared_na):
    assert len(rows)==family_n
    assert len({r['slot_id'] for r in rows})==family_n
    na=sum(r['raw_p'] is None for r in rows)
    assert na==declared_na
    working=[]
    for row in rows:
        p=row['raw_p']
        assert p is None or 0<=p<=1
        expected=1. if p is None else p
        assert row['bookkeeping_p']==expected
        working.append(expected)
    running=0.
    for rank,index in enumerate(sorted(range(family_n),key=lambda j:(working[j],j))):
        running=max(running,(family_n-rank)*working[index])
        assert math.isclose(rows[index]['holm_p'],min(1.,running),rel_tol=1e-12,abs_tol=1e-15)
    return {'family_n':family_n,'raw_na_count':na,
            'raw_p_below_05':sum(r['raw_p'] is not None and r['raw_p']<.05 for r in rows),
            'holm_p_below_05':sum(r['raw_p'] is not None and r['holm_p']<.05 for r in rows),
            'status':'ALL_SCALAR_BOOKKEEPING_IDENTITIES_PASS'}


def cell(row):
    return row['source'],row['horizon'],row['window']


def main():
    names=['wp2-summary.json','wp2-comparisons.json','wp3-combinations.json',
           'wp3-findings.json','wp4-states.json']
    loaded={name:json.loads((PUBLIC/name).read_text()) for name in names}
    wp2=loaded['wp2-summary.json'];cmp2=loaded['wp2-comparisons.json']
    wp3=loaded['wp3-combinations.json'];find3=loaded['wp3-findings.json'];wp4=loaded['wp4-states.json']
    paired_path=ROOT/'results/revision-20261022/paired-comparisons.csv'
    with paired_path.open(newline='') as handle:paired=list(csv.DictReader(handle))
    assert sha(paired_path)==wp4['paired_archive_sha256']
    assert sha(PUBLIC/'wp3-combinations.json')==find3['source_sha256']
    out={'scope':'Public aggregate scalars and immutable public paired aggregate CSV only; no raw source, private NPZ, model workers or new inferential analyses.',
         'input_sha256':{name:sha(PUBLIC/name) for name in names},
         'paired_aggregate_sha256':sha(paired_path)}
    out['families']={
        'WP2':verify_holm(cmp2['rows'],56,cmp2['raw_na_count']),
        'WP3':verify_holm(wp3['comparisons'],224,wp3['raw_na_count']),
        'WP4':verify_holm(wp4['ranking'],4,wp4['raw_na_count'])}
    out['wp4']=[]
    for row in wp4['rows']:
        groups=row['groups'];n=row['full_n']
        assert sum(g['n'] for g in groups)==n
        weighted=math.fsum(g['n']*g['mean_difference'] for g in groups)/n
        matches=[r for r in paired if r['contrast_id']==row['contrast_id']]
        assert len(matches)==1
        original=float(matches[0]['mean_pinball_difference'])
        close(weighted,row['unchanged_primary_mean_difference']);close(weighted,original)
        assert int(matches[0]['origin_count'])==n
        assert row['gw']['full_n']==n
        assert row['gw']['n']+row['gw']['burn_in']==n
        assert row['gw']['burn_in']==row['horizon']==6
        assert row['gw']['bandwidth']==row['group_bandwidth']
        assert row['gw']['instrument_rank']==row['gw']['covariance_rank']==3
        assert row['heterogeneity']['covariance_rank']==2
        assert row['gw']['covariance_condition']<=1e12
        assert row['heterogeneity']['covariance_condition']<=1e12
        ranks=[{k:r[k] for k in ('test','raw_p','bookkeeping_p','holm_p')} for r in wp4['ranking'] if r['source']==row['source']]
        out['wp4'].append({'source':row['source'],'unit':row['native_unit'],
            'contrast_id':row['contrast_id'],'group_n':[g['n'] for g in groups],
            'group_mean_difference':[g['mean_difference'] for g in groups],
            'group_hac_se':[g['hac_se'] for g in groups],
            'full_n':n,'weighted_group_mean':weighted,'public_primary_mean':row['unchanged_primary_mean_difference'],
            'archived_primary_mean':original,'weighted_minus_archived_primary':weighted-original,
            'gw_suffix_n':row['gw']['n'],'gw_burn_in':row['gw']['burn_in'],
            'all_groups_negative':all(g['mean_difference']<0 for g in groups),
            'all_groups_positive':all(g['mean_difference']>0 for g in groups),
            'ranking':ranks})
    assert len(wp2['method_rows'])==24 and len(wp2['control_rows'])==16
    lookup={(cell(r),r['method']):r for r in wp2['method_rows']+wp2['control_rows']}
    pairs=[]
    for pair in wp2['aci_pairs']:
        if pair['status']!='COMPLETE':
            pairs.append({k:pair[k] for k in ('source','horizon','window','status','reason')})
            continue
        key=cell(pair);q=lookup[(key,'ACI_QR')]['scores'];f=lookup[(key,'ACI_F')]['scores']
        uq=lookup[(key,'QR')]['scores'];uf=lookup[(key,'frozen_F')]['scores']
        for label,left,right in [('wrapped',q,f),('unwrapped',uq,uf)]:
            assert left['n']==right['n']
            close(pair[label+'_qr_minus_f_mean_loss'],left['mean_loss']-right['mean_loss'])
            close(pair[label+'_qr_minus_f_coverage_distance'],left['coverage_distance']-right['coverage_distance'])
            assert pair[label+'_qr_minus_f_full_hits']==left['full_hits']-right['full_hits']
        pairs.append({'source':pair['source'],'horizon':pair['horizon'],'window':pair['window'],
            'status':'COMPLETE','n':q['n'],'ACI_QR_mean_loss':q['mean_loss'],'ACI_F_mean_loss':f['mean_loss'],
            'ACI_QR_hits':q['full_hits'],'ACI_F_hits':f['full_hits'],
            'wrapped_qr_minus_f_mean_loss':pair['wrapped_qr_minus_f_mean_loss'],
            'wrapped_qr_minus_f_coverage_distance':pair['wrapped_qr_minus_f_coverage_distance']})
    out['wp2']={'complete_method_count':sum(r['status']=='COMPLETE' for r in wp2['method_rows']),
        'na_method_count':sum(r['status']!='COMPLETE' for r in wp2['method_rows']),
        'method_status_counts':{m:{'complete':sum(r['method']==m and r['status']=='COMPLETE' for r in wp2['method_rows']),
            'na':sum(r['method']==m and r['status']!='COMPLETE' for r in wp2['method_rows'])} for m in ('ACI_F','ACI_QR','SAV')},
        'aci_pairs':pairs}
    assert out['wp2']['complete_method_count']==wp2['complete_method_count']
    assert out['wp2']['na_method_count']==wp2['na_method_count']
    controls3={(r['cell_id'],r['method']):r['scores'] for r in wp3['control_rows']}
    counters={}
    identities=[]
    for method in ('MEAN_F_QR','MEDIAN_F_QR_KNN'):
        rows=[r for r in wp3['method_rows'] if r['method']==method]
        count={'total':len(rows),'complete':0,'na':0,'lower_than_both':0,'lower_than_F':0,'lower_than_QR':0,'exactly_F':0}
        for row in rows:
            if row['status']!='COMPLETE':count['na']+=1;continue
            count['complete']+=1
            score=row['scores'];f=controls3[(row['cell_id'],'F')];q=controls3[(row['cell_id'],'QR')]
            lowf=score['mean_loss']<f['mean_loss'];lowq=score['mean_loss']<q['mean_loss']
            count['lower_than_F']+=int(lowf);count['lower_than_QR']+=int(lowq)
            count['lower_than_both']+=int(lowf and lowq)
            close(row['percent_vs_F'],100*(score['mean_loss']-f['mean_loss'])/f['mean_loss'])
            close(row['percent_vs_QR'],100*(score['mean_loss']-q['mean_loss'])/q['mean_loss'])
            if row.get('identity')=='EXACTLY_F':
                count['exactly_F']+=1
                assert score['mean_loss']==f['mean_loss'] and score['full_hits']==f['full_hits']
                assert score['coverage_distance']==f['coverage_distance']
                identities.append({'cell_id':row['cell_id'],'method':method,'identity':'EXACTLY_F'})
        assert count==find3['counts'][method]
        counters[method]=count
    assert wp3['method_row_count']==112==len(wp3['method_rows'])
    murphy=[]
    for row in wp3['murphy']:
        assert row['positive_breakpoints']+row['negative_breakpoints']+row['zero_breakpoints']==row['breakpoint_count']
        assert row['ranking']=='CROSSING' and row['positive_breakpoints']>0 and row['negative_breakpoints']>0
        close(row['integral_difference']-row['pinball_difference'],row['integral_minus_pinball'])
        matches=[r for r in find3['murphy_rankings'] if r['slot_id']==row['slot_id']]
        assert len(matches)==1
        assert matches[0]['ranking']==row['ranking']
        murphy.append({'slot_id':row['slot_id'],'ranking':row['ranking'],
                       'integral_minus_pinball':row['integral_minus_pinball']})
    primary=[]
    for row in find3['primary_context_rows']:
        matching=[r for r in wp3['method_rows'] if r['cell_id']==row['cell_id'] and r['method']==row['method']]
        assert len(matching)==1 and matching[0]==row
        primary.append({'cell_id':row['cell_id'],'method':row['method'],
                        'mean_loss':row['scores']['mean_loss'],'hits':row['scores']['full_hits'],
                        'n':row['scores']['n'],'coverage_distance':row['scores']['coverage_distance'],
                        'percent_vs_F':row['percent_vs_F'],'percent_vs_QR':row['percent_vs_QR']})
    out['wp3']={'counts':counters,'algebraic_identity_rows':identities,
                'primary_contexts':primary,'murphy':murphy}
    out['status']='PASS_PUBLIC_SCALAR_READBACK'
    print(json.dumps(out,indent=2,allow_nan=False))


if __name__=='__main__':main()
