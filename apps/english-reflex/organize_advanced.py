"""Curated sentence-level Equivalent → target comparisons for every advanced entry."""
import json
from pathlib import Path
p=Path('dist/data.json');d=json.loads(p.read_text());lessons=[l for l in d['lessons'] if l['type']=='advanced']
comparisons=json.loads(Path('advanced_comparisons.json').read_text())
assert len(comparisons)==len(lessons)==137
for l in lessons:
 c=comparisons[l['id']];i=c['index'];a,b=l['learningHighlights']['casual'][0];sentence=l['casual'];base=c['basePhrase']
 if i==1:
  sentence='For your information, a new issue cropped up during testing.';a=sentence.index('cropped up');b=a+len('cropped up');l['pro']=l['casual']=sentence
 if i==53:
  a=sentence.index('a brief glimpse');b=a+len('a brief glimpse of');base='a quick look at'
 if i==67:
  a=sentence.index('a complete beginner');b=a+len('a complete beginner at');base='someone with no experience in'
 if i==135:
  a=sentence.index('on a mission to');b=a+len('on a mission to make')
 baseline=sentence[:a]+base+sentence[b:];ba=a;bb=a+len(base)
 if i==12:
  baseline="Use the symbol ':' before the list of options.";ba=4;bb=4+len("the symbol ':'")
 if i==133:
  baseline="We're interviewing a promising new designer for the team.";ba=baseline.index('promising new');bb=ba+len('promising new')
 if i==53:l['variant']='glimpse 常接 of；look 作名词常接 at：a brief glimpse of the design / a quick look at the design。替换词语时，介词也要一起调整。'
 l['suggestion']=c['chinese'];l['explain']=c['why'];l['learningHighlights']['casual']=[[a,b]]
 l['comparison']={'sentenceEn':baseline,'highlight':[ba,bb],'equivalent':base,'target':sentence[a:b],'originalEquivalent':l['originalEquivalent']}
 l['prompt']={'scenarioZh':l['context'],'expressionZh':l['suggestion'],'baseSentenceEn':baseline,'equivalentRange':[ba,bb]}
 l['answer']={'chinese':l['suggestion'],'english':l['casual']}
 l['contextNotes']={'why':l['explain'],'variation':l['variant'],'literalImprovement':l['fix']}
 assert baseline[ba:bb]==base and l['casual'][a:b],l['id']
p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')))
print('137 advanced comparison prompts prepared')
