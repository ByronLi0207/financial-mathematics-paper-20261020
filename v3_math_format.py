"""Mathematical display normalization; no data/model/result transformations.

ReportLab receives Unicode operators with genuine script markup. Complete
inline formula bindings let TeX use one math span rather than character pieces.
"""
import copy,re

GREEK={'alpha':'α','beta':'β','gamma':'γ','mu':'μ','nu':'ν','phi':'φ','theta':'θ','epsilon':'ε','lambda':'λ','tau':'τ','rho':'ρ'}
CATALOG={
 'k=⌈(n+1)τ⌉≤n':r'k=\lceil(n+1)\tau\rceil\le n',
 '⌈(3+1)·3/4⌉=3':r'\lceil(3+1)\cdot3/4\rceil=3',
 '⌈(k+1).95⌉=51':r'\lceil(k+1)\,0.95\rceil=51',
 'L=max{H,⌊4(n/100)<super>2/9</super>⌋}':r'L=\max\{H,\lfloor4(n/100)^{2/9}\rfloor\}',
 'N<sub>s+1</sub>=c+φN<sub>s</sub>+ε<sub>s</sub>':r'N_{s+1}=c+\phi N_s+\epsilon_s',
 'i₀=κ−H−W+1':r'i_0=\kappa-H-W+1',
 'i₀+1,…,κ':r'i_0+1,\ldots,\kappa',
 'φ<sub>κ</sub>=1':r'\phi_\kappa=1',
 'h=0':r'h=0',
 'max{B<sub>t</sub>,α<sub>κ</sub>+z<sub>t,κ</sub><super>T</super>θ<sub>κ</sub>}':r'\max\{B_t,\alpha_\kappa+z_{t,\kappa}^{\mathsf T}\theta_\kappa\}',
 'τ−1≤ν≤τ':r'\tau-1\le\nu\le\tau',
 'ρ=1/W':r'\rho=1/W',
 '1−τ':r'1-\tau',
 'α=1/20':r'\alpha=1/20',
 '[α,1]':r'[\alpha,1]',
 'u/α':r'u/\alpha',
 '(1−u)/(1−α)':r'(1-u)/(1-\alpha)',
 '0≤a≤1':r'0\le a\le1',
 '0&lt;a&lt;1':r'0<a<1',
 'τ=.95':r'\tau=0.95',
 'τ=.90':r'\tau=0.90',
 'τ=0.95':r'\tau=0.95',
 'U<sub>A</sub>−U<sub>B</sub>':r'U_A-U_B',
 'V<sub>A</sub>−V<sub>B</sub>':r'V_A-V_B',
 'G<sub>(j),κ,H</sub>':r'G_{(j),\kappa,H}',
 'J<sub>λ</sub>':r'\mathcal J_\lambda',
 'D<sub>λ</sub>':r'\mathcal D_\lambda',
 'ω=a/(1−a)':r'\omega=a/(1-a)',
 '|Nₜ|':r'|N_t|',
 'Pₜ,ₕ−Bₜ':r'P_{t,H}-B_t',
 'I=1{P&gt;C}':r'I=\mathbf1\{P>C\}',
}
# Each key is one complete mathematical expression. Bind longest first so
# inner symbols cannot split a larger formula across text/math modes.
CATALOG.update({
 'V<sub>i,t</sub>=max{x+u<sub>i</sub>,−x−l<sub>i</sub>}':r'V_{i,t}=\max\{x+u_i,-x-l_i\}',
 'max(1,|J<sub>λ</sub>|,|D<sub>λ</sub>|)':r'\max(1,|\mathcal J_\lambda|,|\mathcal D_\lambda|)',
 '10⁶':r'10^6',
 'ω >= 0':r'\omega\ge0',
 '0≤s≤721':r'0\le s\le721',
 '0≤s≤t':r'0\le s\le t',
 '0≤φ≤1':r'0\le\phi\le1',
 '1−φ<super>H</super>':r'1-\phi^H',
 'd<sub>abs</sub>=max<sub>i∈J</sub>∣B−|N<sub>i</sub>|∣':r'd_{\rm abs}=\max_{i\in J}\bigl|B-|N_i|\bigr|',
 'd<sub>signed</sub>=max<sub>i∈J</sub>|x−N<sub>i</sub>|':r'd_{\rm signed}=\max_{i\in J}|x-N_i|',
 '|F−K|≤d<sub>abs</sub>':r'|F-K|\le d_{\rm abs}',
 '|S−K|≤d<sub>signed</sub>':r'|S-K|\le d_{\rm signed}',
 '|F−S|≤d<sub>abs</sub>+d<sub>signed</sub>':r'|F-S|\le d_{\rm abs}+d_{\rm signed}',
 'd<sub>abs</sub>=0':r'd_{\rm abs}=0',
 'd<sub>signed</sub>=2c':r'd_{\rm signed}=2c',
 '1≤k≤|J|':r'1\le k\le|J|',
 'x=N<sub>t</sub>':r'x=N_t',
 'B=|x|':r'B=|x|',
 'B<sub>i</sub>=|N<sub>i</sub>|':r'B_i=|N_i|',
 'd<sub>i,h</sub>=N<sub>i+h</sub>−N<sub>i</sub>':r'd_{i,h}=N_{i+h}-N_i',
 'd<sub>i,0</sub>=0':r'd_{i,0}=0',
 'F<sub>J</sub>=Q<sub>k</sub>(A)':r'F_J=Q_k(A)',
 'S<sub>J</sub>=Q<sub>k</sub>(T)':r'S_J=Q_k(T)',
 'K<sub>J</sub>=Q<sub>k</sub>(C<sub>B</sub>(P))':r'K_J=Q_k(C_B(P))',
 'C<sub>B</sub>(A<sub>i</sub>)=A<sub>i</sub>':r'C_B(A_i)=A_i',
 '|T<sub>i</sub>−P<sub>i</sub>|≤|x−N<sub>i</sub>|':r'|T_i-P_i|\le|x-N_i|',
 'T<sub>i</sub>≥B':r'T_i\ge B',
 '|u<sub>i</sub>−v<sub>i</sub>|≤r':r'|u_i-v_i|\le r',
 'u<sub>i</sub>≤v<sub>i</sub>+r':r'u_i\le v_i+r',
 '|Q<sub>k</sub>(u)−Q<sub>k</sub>(v)|≤r':r'|Q_k(u)-Q_k(v)|\le r',
 '∣|N<sub>i</sub>|−|x|∣≤|N<sub>i</sub>−x|':r'\bigl||N_i|-|x|\bigr|\le|N_i-x|',
 '|x−N<sub>i</sub>|':r'|x-N_i|',
 'max(τ,1−τ)':r'\max(\tau,1-\tau)',
 'u<sub>i</sub>=b<sub>i</sub>≥0':r'u_i=b_i\ge0',
 'v<sub>i</sub>=−a<sub>i</sub>≥0':r'v_i=-a_i\ge0',
 'g<sub>i</sub>(N<sub>i</sub>)':r'g_i(N_i)',
 'g<sub>i</sub>(x)':r'g_i(x)',
 '[min(u<sub>i</sub>,v<sub>i</sub>),max(u<sub>i</sub>,v<sub>i</sub>)]':r'[\min(u_i,v_i),\max(u_i,v_i)]',
 'u<sub>i</sub>=v<sub>i</sub>':r'u_i=v_i',
 'F<sub>J</sub>=S<sub>J</sub>':r'F_J=S_J',
 'u<sub>i</sub>≥v<sub>i</sub>':r'u_i\ge v_i',
 'v<sub>i</sub>≥u<sub>i</sub>':r'v_i\ge u_i',
 'F<sub>J</sub>,S<sub>J</sub>≤R<sub>J</sub>':r'F_J,S_J\le R_J',
 'R<sub>J</sub>=B+Q<sub>k</sub>{max(u<sub>i</sub>,v<sub>i</sub>):i in J}':r'R_J=B+Q_k\{\max(u_i,v_i):i\in J\}',
 'B<sub>i</sub>≤B':r'B_i\le B',
 'A<sub>i</sub>≥C<sub>B</sub>(P<sub>i</sub>)':r'A_i\ge C_B(P_i)',
 'F<sub>J</sub>≥K<sub>J</sub>':r'F_J\ge K_J',
 'B<sub>i</sub>≥B':r'B_i\ge B',
 'C<sub>B</sub>(P<sub>i</sub>)=P<sub>i</sub>≥A<sub>i</sub>':r'C_B(P_i)=P_i\ge A_i',
 'F<sub>J</sub>≤K<sub>J</sub>':r'F_J\le K_J',
 'N<sub>s</sub>=(−1)<super>s+1</super>c':r'N_s=(-1)^{s+1}c',
 'N<sub>t</sub>=c':r'N_t=c',
 '|S−K|=2c':r'|S-K|=2c',
 'N<sub>s</sub>=d(t−s)':r'N_s=d(t-s)',
 'G<sub>i</sub>=0':r'G_i=0',
 'N<sub>t</sub>=0':r'N_t=0',
 'λ in {0.001,0.01,0.1}':r'\lambda\in\{0.001,0.01,0.1\}',
 'P(H6)≤P(H24)':r'P(H6)\le P(H24)',
 '10<super>−6</super>(1+|J<sub>λ</sub>|)':r'10^{-6}(1+|\mathcal J_\lambda|)',
 '10<super>−6</super>':r'10^{-6}',
 '10<super>−5</super>':r'10^{-5}',
 '2<super>−40</super>':r'2^{-40}',
 'y=G/a':r'y=G/a',
 'B≤P':r'B\le P',
 'a(U<sub>A</sub>−U<sub>B</sub>)+(1−a)(V<sub>A</sub>−V<sub>B</sub>)':r'a(U_A-U_B)+(1-a)(V_A-V_B)',
})

CATALOG.update({
 'k=W':r'k=W',
 '(P−C)<sub>+</sub>':r'(P-C)_+',
 '(C−P)<sub>+</sub>':r'(C-P)_+',
 'P&gt;C':r'P>C',
 'a<sub>i</sub>=min<sub>h</sub>d<sub>i,h</sub>':r'a_i=\min_h d_{i,h}',
 'b<sub>i</sub>=max<sub>h</sub>d<sub>i,h</sub>':r'b_i=\max_h d_{i,h}',
 'a<sub>i</sub>≤0≤b<sub>i</sub>':r'a_i\le0\le b_i',
 'u<sub>i</sub>=b<sub>i</sub>':r'u_i=b_i',
 'v<sub>i</sub>=−a<sub>i</sub>':r'v_i=-a_i',
 '0&lt;τ&lt;1':r'0<\tau<1',
 't=H+n−1':r't=H+n-1',
 'J={0,...,n−1}':r'J=\{0,\ldots,n-1\}',
 'J={1,...,720}':r'J=\{1,\ldots,720\}',
 'J={0,1,2}':r'J=\{0,1,2\}',
 'S=Hd':r'S=Hd',
 'x=B=2':r'x=B=2',
 'P(H6)=P(H24)=1':r'P(H6)=P(H24)=1',
 'C(H6)=10':r'C(H6)=10',
 'C(H24)=1':r'C(H24)=1',
 '√2':r'\sqrt2',
 '1/√2':r'1/\sqrt2',
 '1/5':r'1/5',
 '‖β‖₂':r'\|\beta\|_2',
 'δ':r'\delta',
 'c&gt;0':r'c>0',
 'd&gt;0':r'd>0',
 'N(t−24)':r'N_{t-24}',
 'N(t)':r'N_t',
})

CATALOG['E[Z<sub>t</sub>(I<sub>t</sub>−.05)]=0']=r'\mathbb E[Z_t(I_t-0.05)]=0'

CATALOG.update({
 'P>C':r'P>C',
 'p&gt;n':r'p>n',
 'p>n':r'p>n',
 'A<sub>i</sub>':r'A_i',
 'T<sub>i</sub>':r'T_i',
 'C<sub>B</sub>':r'C_B',
 'g<sub>i</sub>':r'g_i',
 'R<sub>J</sub>':r'R_J',
 '−dh':r'-dh',
 'τHd':r'\tau Hd',
 'Hd':r'Hd',
 'T−B':r'T-B',
 'P−C':r'P-C',
 'W+H−1':r'W+H-1',
 'W+H':r'W+H',
 'H+1':r'H+1',
 'H+4':r'H+4',
 'C(H6)>C(H24)':r'C(H6)>C(H24)',
 'C(H6)&gt;C(H24)':r'C(H6)>C(H24)',
 '1.311×10<super>8</super>':r'1.311\times10^8',
})

CATALOG.update({'N(t+h)':r'N_{t+h}','1≤h≤H':r'1\le h\le H','(1−τ)Hd':r'(1-\tau)Hd'})

NOTATION={
 'Nₜ; Bₜ':('N<sub>t</sub>; B<sub>t</sub>',r'N_t;\ B_t'),
 'Pₜ,ₕ; Gₜ,ₕ':('P<sub>t,H</sub>; G<sub>t,H</sub>',r'P_{t,H};\ G_{t,H}'),
 'Cₜᵐ; Floor':('C<sub>t</sub><super>m</super>; Floor',r'C_t^m;\ \mathrm{Floor}'),
 'aκ; zᵢ,κ':('a<sub>κ</sub>; z<sub>i,κ</sub>',r'a_\kappa;\ z_{i,\kappa}'),
 'Jλ; Dλ':('J<sub>λ</sub>; D<sub>λ</sub>',r'\mathcal J_\lambda;\ \mathcal D_\lambda'),
 'd(abs); d(signed)':('d<sub>abs</sub>; d<sub>signed</sub>',r'd_{\rm abs};\ d_{\rm signed}'),
 'Ñᵗʳᵢ,ₕ; Mᵢ,ₕ':('Ñ<sub>i,h</sub><super>tr</super>; M<sub>i,h</sub>',r'\widetilde N_{i,h}^{\rm tr};\ M_{i,h}'),
 'κ(t); W; d':('κ(t); W; d',r'\kappa(t);\ W;\ d'),
 'a; ω=a/(1−a)':('a; ω=a/(1−a)',r'a;\ \omega=a/(1-a)'),
}

def equation(html,latex):return dict(type='equation',html=html,latex=latex)
def paragraph(html):return dict(type='p',html=html)

def text_math(s):
    s=s.replace('At exact phi1','At exact φ<sub>κ</sub>=1').replace('At exact φ1','At exact φ<sub>κ</sub>=1')
    s=s.replace('ceil((n+1)τ)','⌈(n+1)τ⌉').replace('ceil((3+1)3/4)','⌈(3+1)·3/4⌉')
    s=s.replace('N(s+1)=c+phi N(s)+epsilon(s)','N<sub>s+1</sub>=c+φN<sub>s</sub>+ε<sub>s</sub>')
    s=s.replace('Set h0','Set h=0').replace('sqrt(2)','√2')
    s=re.sub(r'\bi in N<sub>', 'i∈N<sub>', s)
    s=s.replace('0&lt;=a&lt;=1','0≤a≤1').replace('(1-a)','(1−a)')
    for a,b in GREEK.items():s=re.sub(r'\b'+a+r'\b',b,s)
    s=s.replace('(P−C)₊','(P−C)<sub>+</sub>').replace('(C−P)₊','(C−P)<sub>+</sub>')
    s=re.sub(r'\bk=W(\d+)\b',r'k=W=\1',s)
    s=s.replace('Vᵢ,ₜ=max{x+uᵢ,−x−lᵢ}','V<sub>i,t</sub>=max{x+u<sub>i</sub>,−x−l<sub>i</sub>}').replace('x=Nₜ','x=N<sub>t</sub>')
    s=s.replace('k τ','kτ').replace('times τ','times τ')
    s=s.replace('Jλ','J<sub>λ</sub>').replace('Dλ','D<sub>λ</sub>')
    s=s.replace('G(j),κ,H','G<sub>(j),κ,H</sub>')
    s=s.replace('U_A-U_B','U<sub>A</sub>−U<sub>B</sub>').replace('V_A-V_B','V<sub>A</sub>−V<sub>B</sub>')
    s=s.replace('a(i)=min over h of d(i,h)','a<sub>i</sub>=min<sub>h</sub>d<sub>i,h</sub>').replace('b(i)=max over h of d(i,h)','b<sub>i</sub>=max<sub>h</sub>d<sub>i,h</sub>')
    s=s.replace('a(i)≤0≤b(i)','a<sub>i</sub>≤0≤b<sub>i</sub>').replace('u(i)=b(i)','u<sub>i</sub>=b<sub>i</sub>').replace('v(i)=−a(i)','v<sub>i</sub>=−a<sub>i</sub>')
    s=s.replace('d(abs)=max|B−|N(i)||','d<sub>abs</sub>=max<sub>i∈J</sub>∣B−|N<sub>i</sub>|∣').replace('d(signed)=max|x−N(i)|','d<sub>signed</sub>=max<sub>i∈J</sub>|x−N<sub>i</sub>|')
    s=s.replace('d(abs)','d<sub>abs</sub>').replace('d(signed)','d<sub>signed</sub>').replace('r<sub>abs</sub>','d<sub>abs</sub>').replace('r<sub>signed</sub>','d<sub>signed</sub>')
    s=s.replace('||N<sub>i</sub>|−|x||','∣|N<sub>i</sub>|−|x|∣')
    s=s.replace('max{B,α+z θ}','max{B<sub>t</sub>,α<sub>κ</sub>+z<sub>t,κ</sub><super>T</super>θ<sub>κ</sub>}')
    s=s.replace('i₀+1,...,κ','i₀+1,…,κ')
    return s

def normalize_math(content):
    for section in content['sections']:
        output=[]
        for block in section['blocks']:
            s=block.get('html','')
            if block['type']=='p' and ('B(i)=mu(B)' in s or 'alpha=mu(B)' in s):
                output.extend([
                  paragraph('This is not generally ordinary zero-centered ridge on the peak. At a fixed refit κ, the standardized magnitude coordinate and transformed coefficients satisfy'),
                  equation('B<sub>i</sub>=μ<sub>κB</sub>+s<sub>κB</sub>z<sub>i,κ,B</sub>; &nbsp; α<sub>κ</sub>=μ<sub>κB</sub>+a<sub>κ</sub>β<sub>0,κ</sub>; &nbsp; θ<sub>κ</sub>=a<sub>κ</sub>β<sub>κ</sub>+s<sub>κB</sub>e<sub>B</sub>.',r'B_i=\mu_{\kappa B}+s_{\kappa B}z_{i,\kappa,B},\quad\alpha_\kappa=\mu_{\kappa B}+a_\kappa\beta_{0,\kappa},\quad\theta_\kappa=a_\kappa\beta_\kappa+s_{\kappa B}e_B.'),
                  paragraph('Multiplying the headroom objective by its positive response scale gives the equivalent unprojected peak objective with a shifted penalty:')]);continue
            if block['type']=='p' and ' and fit N(s)=' in s:
                prefix,rest=s.split(' and fit ',1);_,sep,tail=rest.partition(' on the unique transitions ')
                if not sep:raise ValueError('AR fit definition changed; inspect source')
                output.extend([paragraph(prefix+'.'),equation('N<sub>s</sub>=c<sub>κ</sub>+φ<sub>κ</sub>N<sub>s−1</sub>+ε<sub>s</sub>.',r'N_s=c_\kappa+\phi_\kappa N_{s-1}+\epsilon_s.'),paragraph('Fit on the unique transitions '+tail)]);continue
            if block['type']=='p' and ' gives M(i,h;x)=' in s:
                prefix,rest=s.split(' gives ',1);_,sep,tail=rest.partition('. Set h0')
                if not sep:raise ValueError('AR replay definition changed; inspect source')
                output.extend([paragraph(prefix+' gives the replay identity'),equation('M<sub>i,h</sub>(x)=N<sub>i+h</sub>+φ<sub>κ</sub><super>h</super>(x−N<sub>i</sub>).',r'M_{i,h}(x)=N_{i+h}+\phi_\kappa^h(x-N_i).'),paragraph(text_math('Set h=0'+tail))]);continue
            if 'html' in block:block['html']=text_math(s)
            if block['type']=='equation':
                if block.get('latex','').startswith('C^F_t='):
                    block['html']='C<sub>t</sub><super>F</super>=B<sub>t</sub>+Q{G<sub>i,H</sub>:i∈A}; &nbsp; C<sub>t</sub><super>S</super>=B<sub>t</sub>+Q{V<sub>i,t</sub>−B<sub>t</sub>:i∈A}; &nbsp; C<sub>t</sub><super>K</super>=max{B<sub>t</sub>,Q{P<sub>i,H</sub>:i∈A}}.'
                if block.get('latex','').startswith(r'\min_{\beta_0,\beta}'):
                    block['html']=block['html'].replace('‖β‖<super>2</super>','‖β‖<sub>2</sub><super>2</super>')
                if block.get('latex','').startswith('J_m(a)='):
                    block['html']=block['html'].replace('L<sub>m,.95</sub>','L̄<sub>m,.95</sub>')
                if block['html'].startswith('J<sub>λ</sub>=mean '):
                    block['html']='J<sub>λ</sub>=W<super>−1</super>∑<sub>i</sub>ρ<sub>τ</sub>(y<sub>i</sub>−X<sub>i</sub>b)+(λ/2)‖β‖<super>2</super>; &nbsp; D<sub>λ</sub>(ν)=ν<super>T</super>y/W−‖Z<super>T</super>ν/W‖<super>2</super>/(2λ).'
                block['html']=re.sub(r'\bsum\b','∑',block['html'])
                if '|M<sub>i,h</sub>(x)‖' in block['html']:
                    block['html']=block['html'].replace('|M<sub>i,h</sub>(x)‖','|M<sub>i,h</sub>(x)|∣')
                    if block['html'].startswith('|max'):block['html']='∣'+block['html'][1:]
                if 'P_{i,H}-\\alpha-' in block.get('latex',''):
                    block.update(html='W<super>−1</super>∑<sub>i∈T</sub>ρ<sub>τ</sub>(P<sub>i,H</sub>−α<sub>κ</sub>−z<sub>i,κ</sub><super>T</super>θ<sub>κ</sub>)+[λ/(2a<sub>κ</sub>)]‖θ<sub>κ</sub>−s<sub>κB</sub>e<sub>B</sub>‖<sub>2</sub><super>2</super>.',latex=r'\frac1W\sum_{i\in\mathcal T}\rho_\tau(P_{i,H}-\alpha_\kappa-z_{i,\kappa}^{\mathsf T}\theta_\kappa)+\frac{\lambda}{2a_\kappa}\|\theta_\kappa-s_{\kappa B}e_B\|_2^2.')
                block['latex']=block['latex'].replace('s_{rB}',r's_{\kappa B}')
            if block['type']=='table':
                block['caption']=block['caption'].replace('10^6','10⁶')
                cells=block.setdefault('cell_html',{})
                for row in block['rows']:
                    for cell in row:
                        if 'ω >= 0' in str(cell):cells[cell]=cell.replace('>=','≥')
                for key in ('headers','rows'):
                    if key=='headers':block[key]=[text_math(x) for x in block[key]]
                    # Financial table rows stay byte-for-byte unchanged.
                if block['caption'].startswith('Notation.'):
                    block['cell_html']={k:v[0] for k,v in NOTATION.items()}
                    block['math_cells']={k:v[1] for k,v in NOTATION.items()}
            output.append(block)
        section['blocks']=output
        # Add full inline math bindings after the semantic-preserving rewrites.
        for block in output:
            if 'html' in block:
                block['html']=text_math(block['html'])
                block['inline_math']=[dict(html=k,latex=v) for k,v in CATALOG.items() if k in block['html']]
    return content

def prepare_tex_math(content):
    c=copy.deepcopy(content);bindings={}
    def token(tex):
        key='VTHM'+str(len(bindings)).zfill(5)+'TOKEN';bindings[key]=tex;return key
    greek={v:'\\'+k for k,v in GREEK.items()}|{'κ':r'\kappa','ω':r'\omega','η':r'\eta'}
    simple=re.compile(r'(?<![A-Za-z0-9_])([A-Za-zα-ωΑ-Ω]{1,3})([=≤≥])([+−-]?(?:\d+(?:\.\d+)?|\.\d+)(?:[eE][+-]?\d+)?(?:/\d+)?)(?![A-Za-z0-9_])')
    def simple_tex(match):
        left,op,right=match.groups();left=''.join(greek.get(x,x) for x in left)
        op={'=':'=','≤':r'\le ','≥':r'\ge '}[op];right=right.replace('−','-')
        if 'e' in right.lower():
            mantissa,power=re.split('[eE]',right);right=mantissa+r'\times10^{'+str(int(power))+'}'
        return token(left+op+right)
    def bind(text,pairs):
        # Protect a complete chained equality before a shorter catalog term.
        chain=r'(?<!\w)([A-Za-zα-ω])=([A-Za-zα-ω])=(\d+)(?!\w)'
        text=re.sub(chain,lambda m:token(greek.get(m[1],m[1])+'='+greek.get(m[2],m[2])+'='+m[3]),text)
        for pair in sorted(pairs,key=lambda x:-len(x['html'])):
            key=pair['html']
            if key not in text:continue
            left=r'(?<!\w)' if key[0].isalnum() or key[0]=='_' else ''
            right=r'(?!\w)' if key[-1].isalnum() or key[-1]=='_' else ''
            text=re.sub(left+re.escape(key)+right,lambda m:token(pair['latex']),text)
        return simple.sub(simple_tex,text)
    for s in c['sections']:
        for b in s['blocks']:
            if b['type']=='p':
                b['html']=bind(b['html'],b.get('inline_math',[]))
            if b['type']=='table':
                b['caption']=bind(b['caption'],[dict(html=k,latex=v) for k,v in CATALOG.items()])
                mapping=b.get('math_cells',{})
                pairs=[dict(html=k,latex=v) for k,v in CATALOG.items()]
                convert=lambda x:token(mapping[x]) if x in mapping else bind(x,pairs)
                b['headers']=[convert(x) for x in b['headers']]
                b['rows']=[[convert(x) for x in row] for row in b['rows']]
    for figure in c.get('figures',[]):
        figure['caption']=bind(figure['caption'],[dict(html=k,latex=v) for k,v in CATALOG.items()])
    return c,bindings

def restore_tex_math(tex,bindings):
    for key,value in bindings.items():tex=tex.replace(key,r'\('+value+r'\)')
    if re.search(r'VTHM[0-9]+TOKEN',tex):raise ValueError('Unresolved inline math token')
    return tex
