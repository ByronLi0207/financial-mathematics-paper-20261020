"""Whole formula bindings for newly authorized classical-bound paragraphs."""
def bind_round2_math(content):
    mapping={
      'X<sub>1</sub>,…,X<sub>H</sub>':r'X_1,\ldots,X_H',
      'S<sub>0</sub>=0':r'S_0=0',
      'S<sub>h</sub>=∑<sub>j=1</sub><super>h</super>X<sub>j</sub>':r'S_h=\sum_{j=1}^{h}X_j',
      'q=inf{u:Pr(|S<sub>H</sub>|≤u)≥0.975}':r'q=\inf\{u:\Pr(|S_H|\le u)\ge0.975\}',
      '|N<sub>i+H</sub>−N<sub>i</sub>|':r'|N_{i+H}-N_i|',
      '⌈39(W+1)/40⌉':r'\lceil39(W+1)/40\rceil',
      'B<sub>t</sub>':r'B_t',
      'M=max<sub>1≤h≤H</sub>|S<sub>h</sub>|':r'M=\max_{1\le h\le H}|S_h|',
      '|S<sub>h</sub>|&gt;c':r'|S_h|>c',
      '{η=k}':r'\{\eta=k\}',
      'S<sub>k</sub>':r'S_k',
      'R<sub>k</sub>=S<sub>H</sub>−S<sub>k</sub>':r'R_k=S_H-S_k',
      'R<sub>k</sub>≥0':r'R_k\ge0',
      'R<sub>k</sub>≤0':r'R_k\le0',
      '|S<sub>H</sub>|&gt;c':r'|S_H|>c',
      'Pr(M&gt;c)≤2Pr(|S<sub>H</sub>|&gt;c)':r'\Pr(M>c)\le2\Pr(|S_H|>c)',
      'max<sub>0≤h≤H</sub>|x+S<sub>h</sub>|≤|x|+M':r'\max_{0\le h\le H}|x+S_h|\le|x|+M',
      'Pr(|S<sub>H</sub>|&gt;q)≤0.025':r'\Pr(|S_H|>q)\le0.025',
      'X<sub>1</sub>=Z':r'X_1=Z',
      'X<sub>2</sub>=−Z':r'X_2=-Z',
      'S<sub>2</sub>=0':r'S_2=0',
      '1−φ²':r'1-\phi^2',
      '⌈19(M+1)/20⌉':r'\lceil19(M+1)/20\rceil',
      '⌊0.1W⌋':r'\lfloor0.1W\rfloor',
      'H+2∑<sub>j=1</sub><super>H−1</super>(H−j)φ<super>j</super>':r'H+2\sum_{j=1}^{H-1}(H-j)\phi^j'}
    for section in content['sections']:
        for b in section['blocks']:
            if b['type']=='p' and ('Proposition 1' in b.get('html','') or section['title'].startswith(('Appendix J.','Appendix L.')) or 'operational report L' in b.get('html','')):
                merged={p['html']:p['latex'] for p in b.get('inline_math',[])}
                merged.update({k:v for k,v in mapping.items() if k in b['html']});b['inline_math']=[dict(html=k,latex=v) for k,v in merged.items()]
    return content
