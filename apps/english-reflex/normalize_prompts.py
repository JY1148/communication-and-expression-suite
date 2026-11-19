"""Keep scenario facts and questions separate in all curated planning exercises."""
import json,re
from pathlib import Path
P=Path(__file__).parent
questions={
'starter-6':'开始实施前，你需要先确认什么？',
'starter-7':'现在应该同步哪些信息？',
'starter-8':'怎样让经理做出知情的优先级选择？',
'adapt-a-0':'你会怎样介入？',
'adapt-a-1':'你会提出哪些具体问题？',
'adapt-a-2':'你会如何补齐信息并避免再次遗漏？',
'adapt-a-3':'你会如何追问？',
'adapt-a-4':'你会怎样回应？',
'adapt-a-5':'你会如何给出建议？',
'adapt-a-6':'你会如何提出不同意见？',
'adapt-a-7':'在进展会上，你会怎样汇报？',
'adapt-a-8':'你会怎样回应这份表扬？',
'adapt-a-9':'你会怎样推动下一步？',
'adapt-a-10':'你会怎样回应？',
'adapt-a-11':'你会如何回应这个时间要求？'}
def normalize(data):
 for l in data:
  if l.get('mode')!='A':continue
  ctx=l['context']
  if l['id'].startswith('adapt-a-'):
   # Each adaptation ends in a question sentence; remove only that sentence.
   parts=re.split(r'(?<=。)',ctx)
   l['context']=''.join(p for p in parts if not p.endswith('？'))
  l['cn']=questions[l['id']]
  if l.get('reason'):
   l['reason']=re.sub(r'^时机：[\s\S]*?目的：','',l['reason'])
   l['reason']=re.sub(r'^目的：','',l['reason'])
 return data
p=P/'dist/data.json';d=json.loads(p.read_text());normalize(d['lessons']);p.write_text(json.dumps(d,ensure_ascii=False))
p=P/'curated.json';d=json.loads(p.read_text())
for i,l in enumerate(d):l.setdefault('id','starter-'+str(i))
normalize(d);p.write_text(json.dumps(d,ensure_ascii=False))
print('Normalized all 15 planning exercises; source notes preserved.')
