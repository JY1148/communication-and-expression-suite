import json
from pathlib import Path
P=Path(__file__).parent
# Context-sensitive paraphrases: no blind word substitution where grammar changes.
changes={11:'completely protected against',21:'less-than and greater-than signs',39:'disappearing types of business',40:'rapidly growing',136:'be included in',137:'a very short delivery window',151:'first-rate',162:'world-leading',190:'complete configuration',196:'robust application that can grow, recover, and run across multiple machines',203:'people-centered',209:'enable a new era',228:'the freedom to',242:'challenging problems',246:'close the gap',260:'without much oversight',297:'emerging',314:'source-to-source compilers, static code checkers, and build tools',336:'coordinated software releases',345:'a work environment with a quick pace',355:'one that involves several functions',390:'Unix or Linux environments'}
custom={221:('people who share my values',"I'm looking forward to working with people who share my values."),361:('put coursework into practice','I put my computer science coursework into practice on real-world problems.'),373:('add features and increase capacity','As requirements evolve, we update functionality and increase the system’s capacity.')}
a=(P/'target_alternatives.txt').read_text().splitlines()
for i,v in changes.items():a[i]=v
for i,(v,_) in custom.items():a[i]=v
(P/'target_alternatives.txt').write_text('\n'.join(a)+'\n')
d=json.loads((P/'dist/data.json').read_text());u=json.loads((P/'dist/learning.json').read_text())
refs=[x.split('|') for x in (P/'full_examples.tsv').read_text().splitlines()]
for l in d['lessons']:
 if not l['id'].startswith('practice-'):continue
 i=l['sourceRecordIndex']
 if i not in changes and i not in custom:continue
 sent,target=refs[i];alt=a[i];replacement=custom[i][1] if i in custom else sent.replace(target,alt,1)
 description=f'近义表达方向：{alt}。改写例句：{replacement}\n这是一种语境中的改写，不代表两个词在所有场合完全等价。'
 l['variant']=description;u[l['id']]['alternatives']=description
# Some subjects and terms are neutral in register; avoid pretending the same sentence is a stylistic transformation.
for l in d['lessons']:
 if l['kind']=='curated' and l['pro']==l['casual']:
  l['explain']+=' 这句本身是中性表达，可用于专业和一般对话；两版相同时无需刻意改写。'
(P/'dist/data.json').write_text(json.dumps(d,ensure_ascii=False));(P/'dist/learning.json').write_text(json.dumps(u,ensure_ascii=False))
