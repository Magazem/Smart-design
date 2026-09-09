import re, json
SENT = chr(1)
SCHEMA='research/09-library-schema.md'
lines=open(SCHEMA,encoding='utf-8').read().split('\n')
sec=re.compile(r'^##\s+T(\d+)\.\s+`([a-z\-]+)\.csv`')
anyh=re.compile(r'^##\s')
starts=[(i,int(m.group(1)),m.group(2)) for i,l in enumerate(lines) if (m:=sec.match(l))]
def endof(s):
    for j in range(s+1,len(lines)):
        if anyh.match(lines[j]): return j
    return len(lines)
EXPAND={('doc-styles','Rule Weights'):['Rule Hair pt','Rule Strong pt','Rule Brand pt'],
        ('page-formats','Margin Top/Bottom/Inside/Outside mm'):
            ['Margin Top mm','Margin Bottom mm','Margin Inside mm','Margin Outside mm']}
def cellsplit(l):
    # markdown escapes an in-cell pipe as \| ; protect those before splitting
    prot = l.strip().replace('\|', SENT)
    return [c.replace(SENT,'\|').strip() for c in prot.strip('|').split('|')]
out={}
for s,tn,tbl in starts:
    e=endof(s); cols={}; order=[]; intbl=False
    for l in lines[s:e]:
        if not l.startswith('|'): intbl=False; continue
        cells=cellsplit(l); low=[c.lower() for c in cells]
        if len(cells)>=2 and low[0]=='column' and low[1]=='type': intbl=True; continue
        if set(''.join(cells))<=set('-: '): continue
        if not intbl: continue
        names=re.findall(r'`([^`]+)`',cells[0])
        if not names or re.sub(r'`[^`]+`','',cells[0]).strip(' /')!='': continue
        expanded=[]
        for n in names: expanded += EXPAND.get((tbl,n),[n])
        for col in expanded:
            if col in cols: continue
            cols[col]={'type':cells[1],'svr':cells[-1],
                       'nullable':'nullable' in cells[1].lower(),
                       'shared_row':cells[0] if len(expanded)>1 else None}
            order.append(col)
    out[tbl]={'T':tn,'columns':cols,'order':order}
json.dump(out,open('research/tmp-sweep/schema-types.json','w',encoding='utf-8'),indent=1,ensure_ascii=False)
print('declared columns',sum(len(d['order']) for d in out.values()),
      '| nullable',sum(1 for d in out.values() for v in d['columns'].values() if v['nullable']))
