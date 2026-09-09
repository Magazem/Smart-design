import json,csv,os,sys
S=json.load(open('research/tmp-sweep/schema-types.json',encoding='utf-8'))
MF='skill/document-design-intelligence/data/schema-manifest.json'
M=json.load(open(MF,encoding='utf-8'))['tables']
BASE='skill/document-design-intelligence/data/base/'
SURR={'scale_row_key','chart_key','cv_region_key','heading_key','substitute_key'}
def enum_of(t,c): return (M[t].get('enums') or {}).get(c)
rows_blank=[]; rows_place=[]; unswept=[]; undecl=[]; dead_nullable=[]
tot_nn=0; tot_nn_swept=0; tot_null=0
for t,d in M.items():
    path=BASE+d['filename']; exists=os.path.exists(path)
    data=list(csv.DictReader(open(path,encoding='utf-8'))) if exists else []
    for c in d['columns']:
        decl=S[t]['columns'].get(c)
        if decl is None:
            undecl.append((t,c,'surrogate' if c in SURR else 'UNDECLARED'))
            if c not in SURR: continue
            nullable=False; svr='—'; typ='(none)'
        else:
            nullable=decl['nullable']; svr=decl['svr']; typ=decl['type']
        if nullable: tot_null+=1
        else: tot_nn+=1
        if not exists:
            if not nullable: unswept.append((t,c))
            continue
        if not nullable: tot_nn_swept+=1
        n=len(data)
        blanks=[i+2 for i,r in enumerate(data) if not (r.get(c) or '').strip()]
        e=enum_of(t,c)
        ph=[i+2 for i,r in enumerate(data)
            if (v:=(r.get(c) or '').strip()) and v.lower() in ('none','n/a','na','tbd','-','null')
            and not (e and v in e)]
        if not nullable and blanks: rows_blank.append((t,c,typ,svr,len(blanks),n,blanks))
        if ph: rows_place.append((t,c,typ,svr,len(ph),n,ph,nullable))
        if nullable and not blanks and not ph: dead_nullable.append((t,c,typ,svr,n))
print(f'non-nullable columns: {tot_nn} (of 174) | nullable: {tot_null} | swept: {tot_nn_swept} | unsweepable (file missing): {len(unswept)}')
print(f'undeclared: {sum(1 for x in undecl if x[2]=='UNDECLARED')} real + {sum(1 for x in undecl if x[2]=='surrogate')} surrogate')
print('\n=== CLASS 1: NON-NULLABLE COLUMNS WITH BLANK CELLS ===')
for t,c,typ,svr,k,n,ln in sorted(rows_blank,key=lambda r:(-r[4]/r[5],-r[4])):
    pct=100*k/n; dots='...' if len(ln)>8 else ''
    print(f'{t:<16}{c:<26}{typ[:22]:<23}[{svr:<3}] {k:>3}/{n:<3} {pct:5.1f}% rows {ln[:8]}{dots}')
print('\n=== CLASS 2: PLACEHOLDER VALUES NOT IN A DECLARED ENUM ===')
for t,c,typ,svr,k,n,ln,nul in rows_place:
    print(f'{t:<16}{c:<26}{typ[:22]:<23}[{svr:<3}] {k}/{n} rows {ln} nullable={nul}')
print('\n=== CLASS 3: UNSWEEPABLE (table file does not exist) ===')
import collections
for t,cs in collections.Counter(x[0] for x in unswept).items(): print(f'{t}: {cs} non-nullable columns unsweepable')
print('\n=== CLASS 4: UNDECLARED NULLABILITY (no type row) ===')
for t,c,k in undecl:
    if k=='UNDECLARED': print(f'{t:<16}{c}')
print('\n=== CLASS 5: NULLABLE BUT NEVER NULL IN LOADED DATA ===')
for t,c,typ,svr,n in dead_nullable: print(f'{t:<16}{c:<26}{typ[:26]:<27}[{svr}] 0 blanks in {n} rows')
