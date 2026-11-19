"""Separate contextual cloze practice from immediate translation drills."""
import json
from pathlib import Path
p=Path('dist/data.json');d=json.loads(p.read_text())
for l in d['lessons']:
    if l['kind']=='curated' and l.get('exerciseType')=='context-recall':
        l['mode']='C';l['tag']='精确表达 · '+l['sub']
d['conversion']['trainingCounts']={m:sum(l['kind']=='curated' and l['mode']==m for l in d['lessons']) for m in ['A','B','C']}
p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')))
print(d['conversion']['trainingCounts'])
