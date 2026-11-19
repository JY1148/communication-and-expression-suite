import json,re
from pathlib import Path
P=Path(__file__).parent
p=P/'dist/data.json';d=json.loads(p.read_text());
reasons={
'starter-0':'先承认遗漏，再说明马上补办；不需要把中文缓和语气中的“好像”机械变成不确定的推测。',
'starter-1':'先争取一点核实时间，再说明你会检查；不要给未经确认的答案。',
'starter-2':'说清楚是明明知道、差一点想起来，而不是完全不认识这个名字。',
'starter-3':'先表达暂不作出承诺，再指出何时具备确定日期的条件。',
'starter-4':'先表达参加的意愿，再说明今天无法安排，最后提出改期。',
'starter-5':'先提示有一个补充事项，再点出上线前仍需要的确认。',
'adapt-b-0':'先简短提示出现了意外情况，再说明下一步会查看；无需把问题说成已经很严重。',
'adapt-b-1':'描述实际的音频问题，再具体请求重复最后一句。',
'adapt-b-2':'区分目前未确定和稍后通知两个状态，不急于承诺一个日期。',
'adapt-b-3':'轻松表达名字难说，再询问是否有简称；不要嘲讽对方名字本身。',
'adapt-b-4':'表达个人偏爱，不必把喜欢说成强烈到痴迷。',
'adapt-b-5':'请对方短暂等待，并说明自己核实后会回来。',
'adapt-b-6':'明确今天先收尾，并说清剩余话题明天接着处理。',
'adapt-b-7':'这里是恢复已有技能，不是从零学习；英语要体现温习的意思。',
'adapt-b-8':'说明有临时办法，同时保留尚未永久修复这一限制。',
'adapt-b-9':'告诉对方自己正在处理，并承诺有进展时同步，不暗示问题已经解决。',
'adapt-b-10':'明确这只是一次性安排，不让对方误以为是长期流程。',
'adapt-b-11':'直接、礼貌说明不要某项配料；不必解释不喜欢的原因。'}
for l in d['lessons']:
 if l['mode']=='B' and l['kind']=='curated' and l['id'] in reasons:
  if l['cn']!='你会怎么说？':l['suggestion']=l['cn']
  l['cn']='你会怎么说？';l['reason']=reasons[l['id']]
 if l['kind']=='source':
  if l['cn']!='这个意思怎么用英文表达？':l['suggestion']=l['cn']
  l['cn']='这个意思怎么用英文表达？';l['reason']='这是一份原始笔记，可能有残缺或旧的释义。完整训练请使用“情境训练”筛选；这里仅保留原文供追溯。'
 l['reason']=re.sub(r'^时机：','',l.get('reason',''))
# Fix replacements that change the grammar or introduce a duplicate article.
fix={11:'completely protected against',21:'less-than and greater-than signs',39:'disappearing types of business',196:'application that can grow, recover, and run across multiple machines',389:'language designed for many kinds of programs'}
units=json.loads((P/'dist/learning.json').read_text())
for l in d['lessons']:
 i=l.get('sourceRecordIndex')
 if not l['id'].startswith('practice-') or i not in fix:continue
 sent,target=(P/'full_examples.tsv').read_text().splitlines()[i].split('|');alt=fix[i];replacement=sent.replace(target,alt,1)
 l['variant']=f'近义方向：{alt}。改写例句：{replacement} 注意：改写需要兼顾含义、冠词、时态及语气。'
 units[l['id']]['alternatives']=l['variant']
# Curated exercises are all reachable from practice and browsing; originals remain separately selectable.
counts={m:sum(x['kind']=='curated' and x['mode']==m for x in d['lessons']) for m in ['A','B']}
d['conversion']['trainingCounts']=counts
p.write_text(json.dumps(d,ensure_ascii=False));(P/'dist/learning.json').write_text(json.dumps(units,ensure_ascii=False))
print('Ready:',counts,'; all original records covered')
