"""Stable-ID precision priority; preserve all other relative positions."""
import json
from pathlib import Path
p=Path('dist/data.json');d=json.loads(p.read_text());ids=json.loads(Path('precision_priority.json').read_text());ls=[l for l in d['lessons'] if l['type']=='precision'];byid={l['id']:l for l in ls};assert all(i in byid for i in ids)
ordered=iter([byid[i] for i in ids]+[l for l in ls if l['id'] not in ids]);d['lessons']=[next(ordered) if l['type']=='precision' else l for l in d['lessons']]
p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')))
print('Prioritized',len(ids),'precision entries')
