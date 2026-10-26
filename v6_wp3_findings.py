"""Descriptive reporting of the complete fixed combination inventory."""

def build(report):
    counts={}
    for method in ('MEAN_F_QR','MEDIAN_F_QR_KNN'):
        rows=[r for r in report['method_rows'] if r['method']==method]
        available=[r for r in rows if r['status']=='COMPLETE']
        counts[method]=dict(total=len(rows),complete=len(available),na=len(rows)-len(available),
            lower_than_both=sum(r['percent_vs_F']<0 and r['percent_vs_QR']<0 for r in available),
            lower_than_F=sum(r['percent_vs_F']<0 for r in available),lower_than_QR=sum(r['percent_vs_QR']<0 for r in available),
            exactly_F=sum(r['identity']=='EXACTLY_F' for r in available))
    primaries=[r for r in report['method_rows'] if r['original'] and r['horizon']==6 and ((r['source']=='fx_hourly' and r['window']==2880) or (r['source']=='nyfed_weekly' and r['window']==260))]
    return dict(status='COMPLETE',analysis_status='post-result / exploratory',counts=counts,primary_context_rows=primaries,
        murphy_rankings=[{k:r[k] for k in ('slot_id','ranking','breakpoint_count','positive_breakpoints','negative_breakpoints','integral_minus_pinball')} for r in report['murphy']],
        note='Counts describe dependent inspected cells, not independent replications; original FX rolling-F primary is not a matched combination control.')

def main():
    import json
    from v6_worker import PUBLIC,read_json,write_json_new,sha
    z=build(read_json(PUBLIC/'wp3-combinations.json'));z['source_sha256']=sha(PUBLIC/'wp3-combinations.json')
    write_json_new(PUBLIC/'wp3-findings.json',z);print(json.dumps(z,indent=2))
if __name__=='__main__':main()
