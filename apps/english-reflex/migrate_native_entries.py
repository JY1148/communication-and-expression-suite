"""Build native entries, typed exercises and three cross-type tag dimensions."""
import json,re,html,copy,collections
from pathlib import Path
root=Path(__file__).parent
D=json.loads((root/'dist/data.json').read_text());units=json.loads((root/'dist/learning.json').read_text());rows=json.loads((root/'notion-snapshot.json').read_text())
def pid(s):return s.split('/')[-1].split('?')[0].replace('-','')
def clean(s):return html.unescape(re.sub('<[^>]+>','',s or '')).strip()
def options(s):
    if isinstance(s,list):return s
    try:return json.loads(s or '[]')
    except:return []
def norm(s):return re.sub('[^a-z0-9]','',clean(s).lower().replace('someone','').replace('something','').replace('one’s',''))
extra_bodies=json.loads((root/'new-native-bodies.json').read_text()) if (root/'new-native-bodies.json').exists() else {}
source_by_id={pid(r['url']):r for r in rows};source_cards={pid(l.get('source','')):l for l in D['lessons'] if l['kind']=='source'}
natives={}
for r in rows:
    ident='native-'+pid(r['url']);card=source_cards.get(pid(r['url']),{})
    natives[ident]=dict(id=ident,title=clean(r['Name']),origin='notion',sourceUrl=r['url'],raw=dict(name=r['Name'],chinese=r.get('Expressions') or '',equivalent=r.get('Equivalent') or '',range=options(r.get('Range')),tags=options(r.get('Tags')),extension=options(r.get('Extension')),pronunciation=r.get('Pronounce') or '',body=extra_bodies.get(pid(r['url']),card.get('body',''))),entryIds=[],types=[])
lookup={norm(r['Name']):'native-'+pid(r['url']) for r in rows}
for old in D['lessons']:
    if old['id'].startswith('practice-') and old['id'] in units:lookup[norm(units[old['id']]['term'])]='native-'+old['id'][9:]
contexts={line.split('|')[0]:line.split('|')[1:] for line in (root/'advanced_workplace.tsv').read_text().splitlines()}
lessons=[]
for old in D['lessons']:
    if old['kind']!='curated':continue
    l=copy.deepcopy(old);raw=source_by_id.get(pid(l.get('source','')))
    native_id='native-'+pid(l['source']) if raw else lookup.get(norm(units[l['id']]['term']))
    if not native_id or native_id not in natives:
        native_id='native-authored-'+l['id'];natives[native_id]=dict(id=native_id,title=units[l['id']]['term'],origin='authored',sourceUrl='',raw=dict(name=units[l['id']]['term'],chinese=l['suggestion'],equivalent='',range=[],tags=[],extension=[],pronunciation='',body=''),entryIds=[],types=[])
    l['nativeId']=native_id
    l['type']={'A':'workplace','B':'instant','C':'precision'}[l['mode']]
    if l['id'].startswith('practice-') and raw and clean(raw.get('Equivalent')) and '专业版' not in raw.get('Equivalent',''):
        l['type']='advanced';l['mode']='D';parts=contexts[pid(raw['url'])];l['context']=parts[0]
        if len(parts)>1:
            l['pro']=l['casual']=parts[1];l['suggestion']=parts[2]
            units[l['id']]['example']=parts[1];units[l['id']]['exampleCn']=parts[2]
        l['cn']='你会怎样用英文表达？'
        l['originalEquivalent']=clean(raw['Equivalent'])
        l['explain']=l['explain'].replace('本句用','这里用')+' 原始 Equivalent 仅作为学习线索；是否能替换要看当前含义和语境。'
        if pid(raw['url'])=='6b41b0f3261745deb83668f4021f5b72':
            l['explain']='up-and-coming 表示崭露头角、有发展前景，并非只表示刚加入。'
            l['variant']='new 只说明新；up-and-coming 还带有潜力和上升趋势。a new designer 也可能只是刚入职，不一定已有成绩。'
            units[l['id']]['alternatives']='promising 强调有潜力；emerging 强调开始受到关注；new 只表示新，不能完整替代 up-and-coming。'
    lessons.append(l)
# Add an immediate-expression exercise for each daily-life source without that type.
for r in rows:
    if '应用-生活表达' not in options(r.get('Range')):continue
    native_id='native-'+pid(r['url'])
    if any(l['nativeId']==native_id and l['type']=='instant' for l in lessons):continue
    base=next(l for l in lessons if l['id']=='practice-'+pid(r['url']))
    l=copy.deepcopy(base);l.update(id='instant-'+pid(r['url']),type='instant',mode='B',exerciseType='instant',context='',cn='',reason='',origin='由 Notion 生活标签生成 · 即时表达')
    l.pop('originalEquivalent',None)
    units[l['id']]=copy.deepcopy(units[base['id']])
    if pid(r['url'])=='bd2feb6fe9e54693a422db176e84879d':
        l.update(suggestion='别担心，系统会提示你重设密码。',pro="Don't worry. You'll be prompted to reset your password.",casual="Don't worry. You'll be prompted to reset your password.",explain='be prompted to do 表示系统给出提示，要求某人执行一个动作；这里不是别人给你一个含糊暗示。',variant='be prompted to reset 表示被提示去重设；be forced to reset 表示被强制重设，不能随意互换。',fix='避免 You will be hinted to reset；系统操作提示自然说 You will be prompted to reset。')
    lessons.append(l)
# Correct the focus of the requested precision example.
l=next(l for l in lessons if l['id']=='practice-c9bfe8071fa74291a8d577e1b6198c10')
l.update(short='关键业务系统',context='你在向同事介绍值班职责。\n补全“关键的业务系统”：\nI help keep ____ up and running.',suggestion='我帮助保障关键业务系统持续正常运行。',explain='business-critical systems 指对业务运转至关重要的系统；business-critical 作为复合形容词放在 systems 前。',variant='critical systems 强调重要性；business-critical systems 明确重要性与业务运行有关。',fix='避免把“关键业务”逐字拼成 key business system；根据含义使用 business-critical systems。')
units[l['id']]=dict(term='business-critical systems',meaning='对业务运行至关重要的系统。',example='We monitor business-critical systems around the clock.',exampleCn='我们全天候监控关键业务系统。',forms='business-critical + 名词；keep + 系统 + up and running。',alternatives='mission-critical systems 强调完成核心任务所必需；business-critical 明确强调业务层面的重要性。',pronunciation='美式 · critical /ˈkrɪtɪkəl/')
# The latest Notion training wasn't in the original snapshot.
r=source_by_id['4020fe1e5cef81558d14ddbb151163f3'];nid='native-'+pid(r['url']);ident='practice-'+pid(r['url'])
if not any(l['id']==ident for l in lessons):
    lessons.append(dict(id=ident,nativeId=nid,type='workplace',mode='A',kind='curated',exerciseType='scenario',sub='会议与决策',tag='职场沟通',short='没人回复是否代表同意',context='你把会影响另一团队的接口变更方案发到群里，两天没人回复。项目经理说：“没人反对，就按这个做吧。”但对方负责人还没有确认。',cn='此刻你会怎样回应？',reason='在把未回复当作实施依据前区分沉默与明确同意，找到负责人确认，避免返工；若已有明确约定的默认批准流程，应按流程判断。',suggestion='我不想把没有回复当作同意。我们能先请对方负责人明确确认，再开始做吗？',pro="I'd rather not take silence as approval. Could we get explicit confirmation from their lead before proceeding?",casual="I don't want to take silence as approval. Can we check with their lead before we start?",explain='take silence as approval 表示把沉默当作同意；take A as B 表示把 A 理解为 B。',variant="They haven't raised objections 只表示尚未提出异议；They've approved it 表示已经批准。",fix="避免 treat no reply as agree；agree 是动词，应使用名词 approval。",source=r['url'],origin='Notion 每日训练',body='',bodyStatus='原生词条已同步。'))
    units[ident]=dict(term='take silence as approval',meaning='把沉默或未回复当作同意。',example="Let's not take silence as approval until we hear from the owner.",exampleCn='在收到负责人的答复前，我们不要把沉默当作同意。',forms='take A as B；take something as approval。',alternatives='assume consent 也表示假定同意，语气更正式；no objections 只说明没有异议。',pronunciation='美式 · approval /əˈpruvəl/')
# Three independent facets, shared by all exercise types.
topic_overrides={'147b1cb4f2c84ae0be7c5c455738dc9a':'日常与人际','6b41b0f3261745deb83668f4021f5b72':'求职与成长'}
merged={'优先级与边界':'职责与优先级','优先级与职责':'职责与优先级','风险与故障':'风险与进度','会议与意见':'会议与决策'}
for l in lessons:
    n=natives[l['nativeId']];raw=n['raw'];l['sub']=topic_overrides.get(l['nativeId'].removeprefix('native-'),merged.get(l['sub'],l['sub']));scenes=[]
    if '应用-生活表达' in raw['range']:scenes.append('日常对话')
    if '应用-职场英语' in raw['range'] or l['type'] in ['workplace','advanced']:scenes.append('职场协作')
    if '应用-编程代码' in raw['range'] or l['sub']=='技术协作':scenes.append('技术沟通')
    if '应用-书信表达' in raw['range']:scenes.append('书面沟通')
    if l['sub']=='求职与成长':scenes.append('求职与成长')
    if not scenes:scenes=['日常对话' if l['type']=='instant' and any(x in l['sub'] for x in ['日常','情绪','即时']) else '职场协作']
    forms=raw['extension'][:]
    if not forms:
        term=units[l['id']]['term'];forms=['句式' if re.search(r"\b(I|we|you|that|it|could|let|when)\b",term,re.I) else '短语' if len(term.split())>1 else '词汇']
    l['tags']={'topic':[l['sub']],'scene':list(dict.fromkeys(scenes)),'form':forms}
    l['tag']={'instant':'即时表达','workplace':'职场沟通','precision':'精准表达','advanced':'进阶表达'}[l['type']]
    n['entryIds'].append(l['id'])
    if l['type'] not in n['types']:n['types'].append(l['type'])
    l['body']=n['raw']['body'];l['source']=n['sourceUrl']
    l['prompt']={'expressionZh':l['suggestion']} if l['type']=='instant' else {'scenarioZh':l['context'],'questionZh':l['cn']} if l['type']=='workplace' else {'scenarioZh':l['context']}
    l['answer']={'chinese':l['suggestion'],'english':{'professional':l['pro'],'casual':l['casual']} if l['type']=='workplace' else l['casual']}
    l['learningId']=l['id'];l['contextNotes']={'why':l['explain'],'variation':l['variant'],'literalImprovement':l['fix']}
D['conversion'].update(sourceRecords=len(rows),convertedRecords=len(rows),unconvertedRecords=0,format='native-entries',trainingCounts=dict(collections.Counter(l['type'] for l in lessons)))
D['schemaVersion']='3.0';D['nativeEntries']=list(natives.values());D['lessons']=lessons;D['sourceCount']=len(rows);D['snapshot']='2026-10-22';D['tagDimensions']=[{'id':'topic','label':'细分类别'},{'id':'scene','label':'使用场景'},{'id':'form','label':'语言形式'}]
D['types']=[{'id':k,'label':v} for k,v in [('instant','即时表达'),('workplace','职场沟通'),('precision','精准表达'),('advanced','进阶表达')]]
D['coverage']={'notionNativeCount':len(rows),'coveredNotionNativeCount':sum(n['origin']=='notion' and bool(n['entryIds']) for n in natives.values()),'nativeCount':len(natives),'entryCount':len(lessons),'typeCounts':dict(collections.Counter(l['type'] for l in lessons)),'dailyNativeCount':sum('应用-生活表达' in n['raw']['range'] for n in natives.values()),'dailyNativesWithInstant':sum('应用-生活表达' in n['raw']['range'] and 'instant' in n['types'] for n in natives.values())}
assert D['coverage']['notionNativeCount']==D['coverage']['coveredNotionNativeCount']
assert D['coverage']['dailyNativeCount']==D['coverage']['dailyNativesWithInstant']
assert all(len(l['tags'])==3 and all(l['tags'].values()) for l in lessons)
assert len({l['id'] for l in lessons})==len(lessons)
(root/'dist/data.json').write_text(json.dumps(D,ensure_ascii=False,separators=(',',':')))
(root/'dist/learning.json').write_text(json.dumps(units,ensure_ascii=False,indent=2)+'\n')
(root/'native-coverage-audit.json').write_text(json.dumps([{'nativeId':n['id'],'sourceUrl':n['sourceUrl'],'types':n['types'],'entryIds':n['entryIds']} for n in natives.values()],ensure_ascii=False,indent=2)+'\n')
print(D['coverage'])
