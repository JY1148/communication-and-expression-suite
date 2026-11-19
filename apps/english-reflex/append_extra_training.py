"""Append 60 authored exercises, preserving original IDs and source records."""
import json
from pathlib import Path
root=Path(__file__).parent
dp=root/'dist/data.json';lp=root/'dist/learning.json'
d=json.loads(dp.read_text());learning=json.loads(lp.read_text())
d['lessons']=[l for l in d['lessons'] if not l['id'].startswith('extra-')]
for key in list(learning):
    if key.startswith('extra-'): del learning[key]
for mode,name in [('B','instant'),('A','judgment')]:
    rows=(root/f'extra_{name}.tsv').read_text().splitlines()
    for i,row in enumerate(rows,1):
        fields=row.split('|');ident=f'extra-{name}-{i:03d}'
        if mode=='B':
            sub,title,cn,casual,term,meaning,example,example_cn,forms,alternatives,explain,fix,variant=fields
            context='';question='';reason='';pro=casual
        else:
            sub,title,context,question,reason,cn,pro,casual,term,meaning,example,example_cn,forms,alternatives,explain,fix,variant=fields
        lesson=dict(id=ident,mode=mode,kind='curated',exerciseType='instant' if mode=='B' else 'scenario',sub=sub,tag=('即时表达' if mode=='B' else '沟通判断')+' · '+sub,short=title,context=context,cn=question,suggestion=cn,reason=reason,pro=pro,casual=casual,explain=explain,fix=fix,variant=variant,origin='新增原创情境训练',source='',body='',bodyStatus='原创训练，无对应 Notion 原始笔记。')
        assert all(lesson[k] for k in ['id','short','suggestion','pro','casual','explain','fix','variant'])
        if mode=='A': assert all(lesson[k] for k in ['context','cn','reason'])
        d['lessons'].append(lesson)
        learning[ident]=dict(term=term,meaning=meaning,example=example,exampleCn=example_cn,forms=forms,alternatives=alternatives)
d['conversion']['trainingCounts']={m:sum(l['kind']=='curated' and l['mode']==m for l in d['lessons']) for m in ['A','B','C']}
d['originalExpansion']={'date':'2026-10-22','instantAdded':36,'judgmentAdded':24,'notionRecordsModified':0}
assert len({l['id'] for l in d['lessons']})==len(d['lessons'])
dp.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')))
lp.write_text(json.dumps(learning,ensure_ascii=False,indent=2)+'\n')
print(d['conversion']['trainingCounts'])
