"""Final editorial pass, concrete picture prompts, and exact learning target fixes."""
import json
from pathlib import Path
p=Path('dist/data.json');d=json.loads(p.read_text());u=json.loads(Path('dist/learning.json').read_text());ed=json.loads(Path('instant_editorial.json').read_text())
notes=json.loads(Path('picture_notes.json').read_text())
pictures={'giblets':'giblets','grease':'grease','mason jar':'mason_jar','dumpster':'dumpster','mayo':'mayo','shiitake mushrooms':'shiitake','pain au lait':'pain_au_lait'}
for l in d['lessons']:
 if l['type']!='instant':continue
 if l['id'] in ed:
  l['suggestion']=ed[l['id']];l['cn']=l['suggestion'];l['short']=l['suggestion'][:26]
  if isinstance(l.get('prompt'),dict):l['prompt']={'expressionZh':l['suggestion']}
 if l['id']=='extra-instant-002':
  a=l['casual'].index("that's not what I meant");l['learningHighlights']={'casual':[[a,a+len("that's not what I meant")]]}
 if l['id']=='extra-instant-031':
  l['casual']='Sorry, was that for me?';l['pro']='Sorry, was that for me?';l['learningHighlights']={'casual':[[7,22]]}
 if l['id']=='extra-instant-033':
  l['casual']="It's working on my end—I can't reproduce the issue. Could you send me the steps you followed?"
  start=l['casual'].index('reproduce');l['learningHighlights']={'casual':[[start,start+len('reproduce the issue')]]}
 if l['id']=='instant-f04807e0400b46e0bc1505283a2f1be2':
  l['casual']="Something's up with the service. The connection keeps dropping—it's intermittent."
  start=l['casual'].index('intermittent');l['learningHighlights']={'casual':[[start,start+12]]}
 if l['id']=='instant-0e464b597f9842c3b8e00ceece9d9735':
  l['casual']="We're on a roll. Let's keep up the momentum and get the rest of the tests done."
  start=l['casual'].index('keep up the momentum');l['learningHighlights']={'casual':[[start,start+20]]}
 term=u[l['id']]['term']
 if term in pictures:
  l['picture']={'src':'assets/'+pictures[term]+'.png','alt':'看图回想这个物品的英文名称'}
  note=notes[term];l['explain']=note['why'];l['variant']=note['variation'];l['fix']=note['fix']
  l['contextNotes']={'why':l['explain'],'variation':l['variant'],'literalImprovement':l['fix']}
  u[l['id']]['example']=note['example'];u[l['id']]['exampleCn']=note['exampleCn']
 l['answer']={'chinese':l['suggestion'],'english':l['casual']}
 if l.get('picture'):
  l['prompt']={'image':l['picture']['src'],'questionZh':'这个用英文怎么说？'}
  l['answer']={'english':term}
 if l['id']=='instant-f04807e0400b46e0bc1505283a2f1be2':
  l['sub']='技术协作';l['tags']['topic']=['技术协作'];l['tags']['scene']=['技术沟通']
Path('dist/learning.json').write_text(json.dumps(u,ensure_ascii=False,separators=(',',':')))
p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')))
print('Polished',len(ed),'instant prompts; picture prompts:',len(pictures))
