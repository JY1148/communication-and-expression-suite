import json,re
from pathlib import Path
P=Path(__file__).parent
d=json.loads((P/'dist/data.json').read_text());units=json.loads((P/'dist/learning.json').read_text());rows=json.loads((P/'corpus.json').read_text());source=rows[0]['url'];raw=next(x for x in d['lessons'] if x['kind']=='source' and x['source']==source)
A={
1:('需求与范围','团队准备马上实施，但错误处理和边界条件还没讨论清楚。','你会怎样推进？'),
2:('优先级与边界','完整功能按当前速度无法赶上截止时间，但其中一部分并非上线必需。','你会提出什么取舍？'),
3:('会议与意见','会议议程排了十项，只有半小时，其中只有两项需要当场决定。','你会怎样调整讨论？'),
4:('协作与反馈','同事问你某项配置是否已经生效，你手头没有可靠的信息。','你会怎样回应？'),
5:('协作与反馈','对方解释了一个新概念，你听到了每个词，但仍不明白具体含义。','你会怎样追问？'),
6:('会议与意见','大家倾向于采用当前方案，你觉得还没充分比较备选方案。','你会怎样表达保留意见？'),
10:('优先级与边界','待办任务持续增加，团队还沿用原来的优先级，已经有人无法按期交付。','你会怎样提出这个问题？'),
19:('协作与反馈','双方对同一决定的理解不同，后续讨论正在建立在这份误解上。','你会怎样处理？'),
25:('会议与意见','讨论已经离开原定议题，但主要问题还没有答案。','你会怎样拉回话题？'),
29:('需求与范围','双方口头谈妥了条款，但没有留下书面记录。','你会提出什么下一步？'),
39:('协作与反馈','你需要同事发送文档，但这个请求没有必须完成的日期。','你会怎样礼貌地提出请求？'),
44:('风险与进度','你打算要求跨时区团队在下班前发报告，但双方的工作日结束时间不同。','你需要怎样把截止时间说清楚？'),
50:('复盘与成果','你发现自己在已发出的文件中漏掉了一项信息，对方还在等你确认。','你会怎样回应并补救？')}
alt=['join in','resolve the details','reduce','simplify','reply after checking','not quite understanding','unsure','explain in more detail','catch up','omit','accumulate','dismiss','explain with an example','miss','diagnose and fix','gradually retire','stop by','deliver','figure out','resolve','discuss and agree on','assign','let’s get started','hand over','connect with','go off topic','move on to','cause controversy','brief and clear','written down','stranded','not directly comparable','be candid with','muted','repeated sound','fail to meet','special thanks to','a demanding initial learning period','exactly right','when you have a chance','realistic','fit into the schedule','draft','perform','before the end of the working day','become exhausted from prolonged stress','go through step by step','invent','sort out','remove','omission']
for i,line in enumerate((P/'long_note_examples.tsv').read_text().splitlines()):
 term,meaning,sentence,cn,why=line.split('|');key=f'long-note-{i}'
 m=re.search(re.escape(term),sentence,re.I)
 if not m:
  variants={14:'phasing out',36:'shout-out to',38:'spot on',41:'schedule it in',35:'fell short of',45:'burning out'}
  candidate=variants.get(i)
  if candidate is None:
   if term=='phase out':candidate='phasing out'
   elif term=='a shout-out to':candidate='shout-out to'
   elif term=='fall short of':candidate='fell short of'
   elif term=='burn out':candidate='burning out'
   elif term=='schedule in':candidate='schedule it in'
  assert candidate,(i,term,sentence)
  m=re.search(re.escape(candidate),sentence,re.I)
 assert m,(i,term,sentence)
 masked=sentence[:m.start()]+'____'+sentence[m.end():]
 mode='A' if i in A else 'B';sub=A[i][0] if i in A else '会议与远程沟通'
 context=A[i][1] if i in A else f'补全语境中的表达（想表达“{meaning}”）：\n{masked}'
 question=A[i][2] if i in A else '空缺处你会怎么说？'
 d['lessons'].append(dict(id=key,mode=mode,kind='curated',exerciseType='scenario' if mode=='A' else 'context-recall',sub=sub,tag=('沟通判断' if mode=='A' else '即时表达')+' · '+sub,short=meaning,context=context,cn=question,suggestion=cn,reason=why,pro=sentence,casual=sentence,explain=f'{term} 在这句话中表达“{meaning}”。'+why,variant=f'近义表达方向：{alt[i]}。实际替换时需要重新检查句法和语气。',fix=f'保留要表达的目的，用 {term} 组织英语；不要机械照搬原笔记的残缺句或过度正式说法。',source=source,origin='商务英语长笔记拆分训练',sourceRecordIndex=0,body=raw.get('body',''),bodyStatus=raw.get('bodyStatus','')))
 units[key]=dict(term=term,meaning=meaning,example=sentence,exampleCn=cn,forms=f'本句完整搭配：{sentence}\n复用时先确定说话对象，再替换任务、时间或话题，不改变原来的语法关系。',alternatives=f'{alt[i]}：可表达相近意图，不一定能逐字替换。'+why)
 # Deadline clarity requires an explicit timezone, rather than teaching EOD as enough.
 if i==44:
  l=d['lessons'][-1];l['pro']='Could you send the report by 5 p.m. Pacific Time on Friday?';l['casual']='Could you get me the report by Friday at 5 p.m. Pacific?';l['suggestion']='你能在周五太平洋时间下午五点前把报告发给我吗？';l['explain']='跨时区任务不要只写 EOD。写清日期、具体时间、时区，减少双方对“今天下班前”的不同理解。'
# Idempotent generation; all existing learners' ids remain stable.
seen=set();d['lessons']=[l for l in d['lessons'] if not(l['id'] in seen or seen.add(l['id']))]
d['conversion']['longNoteExercises']=51
(P/'dist/data.json').write_text(json.dumps(d,ensure_ascii=False));(P/'dist/learning.json').write_text(json.dumps(units,ensure_ascii=False));print('Added 51 long-note exercises')
