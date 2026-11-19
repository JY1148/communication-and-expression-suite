"""User-requested advanced exclusions, picture reclassification and curated order."""
import json
from pathlib import Path
p=Path('dist/data.json');d=json.loads(p.read_text());u=json.loads(Path('dist/learning.json').read_text())
removed={'practice-'+i for i in ['99f1fa75d92047c7b05b016d652d91e6','9f69282426e6422d9766ed7584aa3242','d964808c57794c078f8246623c970df5','bd4b257340264aaba4c01d5e06640efe','302beaf8480f445884f44ce10061337e']}
d['lessons']=[l for l in d['lessons'] if l['id'] not in removed]
for i in removed:u.pop(i,None)
leotard='practice-4ed3550b67af415aa98b29e133f70e99'
l=next(l for l in d['lessons'] if l['id']==leotard)
l.update(type='precision',mode='C',exerciseType='picture-recall',tag='精准表达',short='看图识物：体操服',context='你在为体操课准备服装。',suggestion='连体体操服',pro='leotard',casual='leotard',sub='日常用品',picture={'src':'assets/leotard.png','alt':'看图回想这件衣物的英文名称'},tags={'topic':['日常用品'],'scene':['日常对话'],'form':['名词']},prompt={'image':'assets/leotard.png','questionZh':'这个用英文怎么说？'},answer={'english':'leotard'},learningHighlights={'casual':[[0,7]]},explain='leotard 指体操、舞蹈中常穿的连体紧身衣。它没有裤腿，不等于运动背心或整套运动服。',variant='a sleeveless leotard 是无袖款；a long-sleeved leotard 是长袖款。bodysuit 范围更广，不一定是用于体操或舞蹈的服装。',fix='不要把“体操服”逐字拼成 gymnastics clothes 来指这件具体衣物；看图中的连体紧身衣用 leotard。')
for k in ['comparison','cloze']:l.pop(k,None)
l['contextNotes']={'why':l['explain'],'variation':l['variant'],'literalImprovement':l['fix']}
u[leotard].update(term='leotard',pronunciation='/ˈliː.ə.tɑːrd/',meaning='体操、舞蹈常穿的连体紧身衣；通常没有裤腿。',example='Do I need a leotard for gymnastics class?',exampleCn='上体操课需要穿连体体操服吗？',forms='a leotard；wear a leotard；a sleeveless leotard（无袖款）；a long-sleeved leotard（长袖款）',alternatives='bodysuit 是更宽泛的“连体紧身衣”；gymnastics outfit 泛指体操服装，不一定是这一件式款式。')
first=['8fff7e3dcc944c899df3a342f186aaae','f50fc3d81fcd4cb09de988b59f601597','9ea61c506aa542148b015e7f79ae3548','c68279c6a8d24f0494176a264511764c','6f37e356fd524a02bf843becb24ccb86','a0320ff7c9b24015812572cd40359369','48f701872edc43b4a860f747db39a43c','0c73d4796f9a42d7be3f68541b77663d','ccf830312d664ea9be38efc4e193b00f','cef4d1e522db410f847d6547655e1d4d','17d939db286044faa99f1d1a2419c863','be8c8a96b4a6461085c261a97c7fffe6','12cfd42b7f214338aa77cd9f00fe14b8','cad426ae87cd4991a73d192a1fce9ed0']
first=['practice-'+i for i in first];byid={l['id']:l for l in d['lessons']};assert all(byid[i]['type']=='advanced' for i in first)
ordered=iter([byid[i] for i in first]+[l for l in d['lessons'] if l['type']=='advanced' and l['id'] not in first]);d['lessons']=[next(ordered) if l['type']=='advanced' else l for l in d['lessons']]
for n in d['nativeEntries']:
 entries=[l for l in d['lessons'] if l['nativeId']==n['id']];n['entryIds']=[l['id'] for l in entries];n['types']=list(dict.fromkeys(l['type'] for l in entries))
counts={t:sum(l['type']==t for l in d['lessons']) for t in ['instant','workplace','precision','advanced']};d['coverage'].update(entryCount=len(d['lessons']),typeCounts=counts);d['conversion']['trainingCounts']=counts
p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')));Path('dist/learning.json').write_text(json.dumps(u,ensure_ascii=False,separators=(',',':')))
print(counts)
