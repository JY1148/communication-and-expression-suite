"""Validate native coverage, taxonomy rules and type-specific learning data."""
import json
from pathlib import Path
D=json.loads(Path('dist/data.json').read_text());L=json.loads(Path('dist/learning.json').read_text());N={n['id']:n for n in D['nativeEntries']};E={e['id']:e for e in D['lessons']};valid={'instant','workplace','precision','advanced'}
assert len(E)==len(D['lessons'])
assert len([n for n in N.values() if n['origin']=='notion'])==421
for n in N.values():
    assert n['entryIds']
    assert set(n['types'])=={E[k]['type'] for k in n['entryIds']}
    assert all(E[k]['nativeId']==n['id'] for k in n['entryIds'])
    if '应用-生活表达' in n['raw']['range']:assert 'instant' in n['types']
for e in E.values():
    assert e['nativeId'] in N and e['type'] in valid
    assert set(e['tags'])=={'topic','scene','form'} and all(e['tags'].values())
    assert all(L[e['id']].get(k) for k in ['term','meaning','example','exampleCn','forms','alternatives'])
    assert all(e.get(k) for k in ['suggestion','pro','casual','explain','variant','fix'])
    if e['type']=='workplace':assert e['context'] and e['cn'] and e['reason']
    if e['type']=='advanced':
        assert e['context'] and '____' not in e['context'] and e['originalEquivalent']
        c=e['comparison'];a,b=c['highlight'];assert c['sentenceEn'][a:b]==c['equivalent']
        assert e['prompt']['baseSentenceEn']==c['sentenceEn']
        assert e['answer']['english']==e['casual'] and e['contextNotes']['why']==e['explain']
    if e['type']=='precision' and not e.get('picture'):
        assert e['context'] and '____' not in e['context'] and '补全' not in e['context']
        assert '____' in e['cloze']['sentenceEn'] and e['cloze']['hintZh']
        assert e['prompt']['scenarioZh']==e['context']
        assert e['prompt']['expressionZh']==e['suggestion']
        assert e['answer']['english']==e['casual']
    if e.get('picture'):
        assert e['prompt']['image']==e['picture']['src']
        assert Path('dist',e['picture']['src']).is_file()
    for version in (['pro','casual'] if e['type']=='workplace' else ['casual']):
        assert e['learningHighlights'][version]
        for a,b in e['learningHighlights'][version]:assert 0<=a<b<=len(e[version])
assert E['practice-c9bfe8071fa74291a8d577e1b6198c10']['type']=='precision'
assert L['practice-c9bfe8071fa74291a8d577e1b6198c10']['term']=='business-critical systems'
assert E['practice-6b41b0f3261745deb83668f4021f5b72']['type']=='advanced'
assert 'instant' in N['native-bd2feb6fe9e54693a422db176e84879d']['types']
assert all(old_id in E for old_id in ['starter-0','extra-instant-001','extra-judgment-024'])
print('Native coverage, multi-type mapping, tags, learning modules and stable IDs verified.')
