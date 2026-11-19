"""Structured cloze prompts with individual scenarios and stable instant ordering."""
import json,re
from pathlib import Path
p=Path('dist/data.json');d=json.loads(p.read_text());u=json.loads(Path('dist/learning.json').read_text());scenes=json.loads(Path('precision_scenes.json').read_text())
first=['instant-af2e4f1332484e799597cc383daa86b3','instant-0980136b2a31436db97782889887df5f','extra-instant-035','instant-f0002ec3881343669fda4388133ddf28','instant-544f6a9075274d209b390bd2d67800b0','instant-658f9b2e6f274da5af17a074521a052a','instant-480a9f24f7214c5f836c1e9e5fdc0d71','instant-4e7194f5e0d34cd7a2dd632aa197418f','instant-bf12b04e8cca4d438536ac7fd8437a18','instant-9b57f33a65f645be92d4dc42f00f2d2e']
byid={l['id']:l for l in d['lessons']};assert all(i in byid for i in first)
rest=iter([l for l in d['lessons'] if l['type']=='instant' and l['id'] not in first]);instant=iter([byid[i] for i in first]+list(rest))
d['lessons']=[next(instant) if l['type']=='instant' else l for l in d['lessons']]
for l in d['lessons']:
 if l['type']!='precision':continue
 old=l.get('cloze',{});context=l['context'];match=re.search('想表达“([^”]+)”',context) or re.search('补全“([^”]+)”',context)
 hint=old.get('hintZh') or (match.group(1) if match else l['short']);blank=old.get('sentenceEn') or context.splitlines()[-1]
 assert '____' in blank,(l['id'],blank)
 if l['id']=='practice-e1bbb9103162451194f79d75fbc81f56':
  l['suggestion']='我在代码层面排查了流量异常。';l['casual']=l['pro']='I troubleshot traffic anomalies at the code level.';blank='I ____ at the code level.'
  l['learningHighlights']={'casual':[[2,2+len('troubleshot traffic anomalies')]]}
  l['explain']='troubleshoot 表示系统地排查问题；这里回顾已发生的事件，过去式用 troubleshot。at the code level 说明你从代码层面着手。'
  l['variant']='描述日常职责用 I troubleshoot traffic anomalies；回顾刚才的处理用 I troubleshot traffic anomalies。'
  l['fix']='不要说 I checked the traffic abnormal；可以用 I troubleshot traffic anomalies at the code level。'
 if l['id']=='practice-9ede96cc4ff04ad7990b7edf4f55c2af':
  l['suggestion']='该加固代码、防范恶意活动了。';l['casual']=l['pro']="It's time to harden the code against malicious activity.";blank="It's time to ____ against malicious activity.";hint='加固代码'
  a=l['casual'].index('harden the code');l['learningHighlights']={'casual':[[a,a+15]]}
  l['explain']='harden the code 指提高代码的安全防护能力。It’s time to… 适合在发现风险后提出接下来该采取的行动。'
  l['variant']='harden 也可搭配 a server 或 a system。这里是练习中的假设安全事件，不是在报告 PHP 的实际漏洞。'
  l['fix']='不要逐字说 make the code hard；安全语境用 harden the code。也可解释为 make the code more secure。'
 a,b=l['learningHighlights']['casual'][0];blank=l['casual'][:a]+'____'+l['casual'][b:]
 l['context']=scenes[l['id']];l['cloze']={'sentenceEn':blank,'hintZh':hint};l['prompt']={'scenarioZh':l['context'],'expressionZh':l['suggestion'],'clozeEn':blank,'hintZh':hint}
 l['answer']={'chinese':l['suggestion'],'english':l['casual']};l['contextNotes']={'why':l['explain'],'variation':l['variant'],'literalImprovement':l['fix']}
p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')))
print('321 structured precision prompts; instant first 10 ordered')
