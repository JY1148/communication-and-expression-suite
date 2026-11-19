"""Audit learning vocabulary against each visible answer; allow inflection and slots."""
import json,re
from pathlib import Path
D=json.loads(Path('dist/data.json').read_text());L=json.loads(Path('dist/learning.json').read_text())
ignore=set('a an the to on in at for with of and or but my your our their his her its it this that these those someone something one ones s i you we they me us he she have has been is are was m d ll ve t'.split())
irregular={'going':'go','made':'make','had':'have','fell':'fall','fallen':'fall','spoken':'speak','got':'get','running':'run','committing':'commit','cropped':'crop','slipped':'slip','digressing':'digress','committed':'commit','left':'leave','came':'come','said':'say','found':'find','took':'take','taken':'take','meant':'mean','was':'be','were':'be'}
def stem(w):
    if w in irregular:return stem(irregular[w])
    if w.endswith('ing') and len(w)>5:return w[:-3].rstrip('e')
    if w.endswith('ied') and len(w)>5:return w[:-3]+'y'
    if w.endswith('ed') and len(w)>4:return w[:-2].rstrip('e')
    if w.endswith('s') and len(w)>4 and not w.endswith(('ss','is')):return w[:-1]
    return w.rstrip('e')
def tokens(s):return [stem(w) for w in re.findall('[a-z]+',s.lower().replace('’', chr(39)).replace("n't",' not')) if w not in ignore]
report=[]
for l in D['lessons']:
    if l['kind']!='curated':continue
    term=L[l['id']]['term'];required=tokens(term)
    for version in (['pro','casual'] if l['mode']=='A' else ['casual']):
        actual=tokens(l[version]);missing=[w for w in required if w not in actual]
        report.append(dict(id=l['id'],version=version,term=term,matched=not missing,missing=missing))
Path('answer-alignment-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
failed=[r for r in report if not r['matched']]
for r in failed:print(r)
print(len(report),'answers checked;',len(failed),'unmatched')
assert not failed
