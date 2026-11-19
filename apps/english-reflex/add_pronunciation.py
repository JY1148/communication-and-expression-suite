"""Apply reviewed American IPA word annotations from pronunciation.json."""
import json,re
from pathlib import Path
p=Path('dist/learning.json'); units=json.loads(p.read_text()); pronunciations=json.loads(Path('pronunciation.json').read_text())
for unit in units.values():
    words=list(dict.fromkeys(w.lower() for w in re.findall(r'[A-Za-z]+',unit['term'])))
    entries=[f'{w} /{pronunciations[w]}/' for w in words if w in pronunciations]
    if entries: unit['pronunciation']='美式 · '+'；'.join(entries)
    else: unit.pop('pronunciation',None)
p.write_text(json.dumps(units,ensure_ascii=False,indent=2)+'\n')
print(f'Pronunciation: {sum(bool(u.get("pronunciation")) for u in units.values())} learning modules')
