"""Create authored practice from every source record, retaining source identity and notes."""
import json,re,html
from pathlib import Path
P=Path(__file__).parent
source=json.loads((P/'corpus.json').read_text())
data=json.loads((P/'dist/data.json').read_text())
learning=json.loads((P/'dist/learning.json').read_text())
examples=[line.split('|') for line in (P/'full_examples.tsv').read_text().splitlines()]
meanings=(P/'target_meanings.txt').read_text().splitlines()
alts=[x.strip() for x in (P/'target_alternatives.txt').read_text().splitlines()]
chinese=(P/'full_chinese.txt').read_text().splitlines()
assert len(source)==len(examples)==len(meanings)==len(alts)==len(chinese)==420
original_cards={x['source']:x for x in data['lessons'] if x['kind']=='source'}
def clean(s):
 s=html.unescape(s or '');s=re.sub(r'\[([^\]]+)\]\([^)]*\)',r'\1',s);return re.sub('<[^>]+>','',s).strip()
# Corrections explain why an original note cannot be reused literally.
notes={0:'原页面含多组表达，另有逐项拆分训练；本题练其中的 nail down。',2:'原 brushup 应按动词短语 brush up on 使用；不是简单的“更新”。',11:'immune to 表示不受影响；不能只释为 would not be。',12:'beat a deadline 是提前完成；按时完成用 meet a deadline。',13:'修正原拼写 collabrate 为 collaborate。',19:'circle the wagons 带有防御外界批评、保护自己人的意味，不是中性的“团结一致”。',25:'strategic intent 是战略意图，不等同于所有意义的 strategy。',27:'runaway success 表示巨大、压倒性成功，不必然是意想不到。',33:'giblets 通常指禽类内脏，不泛指牛杂。',35:'fixate on 常带过度执着的意味，比 focus on 更强。',39:'dying breed 是逐渐消失的一类人或事，不只是数量少。',41:'修正原 second-gues 为 second-guess。',42:'原 a healthy of 缺少名词；本句补为 a healthy amount of。',45:'henchman 常为贬义，指恶人的手下，不作中性助手使用。',49:'firm up 表示使计划更确定，不能泛译为“盖棺定论”。',50:'shipshape 常形容整洁有序，不只是“就绪”。',57:'pandemonium 在此是混乱喧闹；不把文学地名含义放入日常默认答案。',71:'这个习语在指责别人也有同样缺点时使用，不等同于所有“差不多”的情况。',79:'raise the stakes 改变利害或风险程度，不只是投入金额。',80:'修正原释义：cilantro 是香菜叶；celery 才是芹菜。',82:'pain au lait 是法语借词；英语场合 milk bread roll 更容易被理解。',86:'penultimate 为倒数第二；原 Equivalent 的 last but two 不准确。',87:'noob 是非正式网络用语，可能显得轻蔑；默认用 beginner。',88:'choppy 指不连贯、断断续续；lagging 则偏延迟。',97:'原短语字面是摧毁沿途一切；本题保留自然字面用法，不套入普通职场。',107:'fire drill 字面为消防演习；此处比喻临时紧急忙乱，不等于一般“煎熬”。',108:'将原残缺的 legibility throughout... 改写为完整、可说的句子。',119:'原词条的中文已经是完整练习；本题使用更简短的自然版本。',120:'milestones 是项目里程碑，而不是笼统的关键时期。',122:'grit 是毅力、韧性；guts 是胆量。本句用 determination 突出坚持。',126:'w.r.t. 多用于技术笔记；口语通常直接说 about 或 regarding。',134:'at capacity 表示工作容量已满，不只是空间装满。',137:'tight turnaround 指交付周转时间很紧，不是“难转弯”。',153:'此处采用更常见的 align with。',164:'用 comfortable using 完整表达技能；修正原 Knowledge in 的搭配。',167:'采用 knowledge of 描述知识，而不是原 Knowledge in。',170:'原记录缺少中文；补成具体的 AWS 使用经验表达，不把 Kafka 说成一项独立 AWS 服务。',178:'原 rich beliefs 搭配不自然；改为 a strong belief in。',181:'采用 give someone the warm fuzzies，而不是 make someone feel the fuzzies。',184:'proprietary 指专有的，不一定是已取得专利的。',186:'修正 fully function 为 fully functional。',191:'需求会变化，表述为 address new and evolving business needs 更清楚。',196:'resilient 在系统语境强调故障后的韧性与恢复能力。',199:'technology-enabled 作为复合修饰语；把抽象宣传用语落实为具体业务需求。',216:'补全 would otherwise spend 的主语与动词结构。',220:'将宣传性的 limitless value 改为较克制的 significant value。',228:'discretion 是酌情决定权，不只是做事的能力。',229:'softie 指容易心软的人，不一定是一般意义的软弱。',230:'on top of it 表示掌握进展且积极处理，不保证事情已经解决。',235:'原 multi-threaded performance services 表意含混，改为明确列出服务、API 和 Web 应用。',242:'intractable 指特别难处理，不是完全无法解决。',251:'aptitude 偏天赋、潜能，不等同于任何已掌握的技能。',253:'deeply invested in 表示重视并投入，不必然指从事时间长。',255:'单个概念验证用 a proof of concept；复数可说 proofs of concept。',263:'将 be hungry to 改为 eager to，较中性自然。',265:'兼顾多项任务不等于能同时做好所有事。',270:'原记录缺少中文；补齐 cloud computing 和 cloud services 的用法。',273:'test harness 指支持自动测试的程序或框架，不是字面的电气“线束”。',280:'empowered to 强调获授权或有自主权，不只是有能力。',281:'原记录缺中文，补成实际的 AWS 项目经验表达。',293:'强调获授权提出方案，不只是能够贡献。',295:'将宽泛的 lead millions... 改成产品帮助用户建立联系，不虚构主导用户的角色。',314:'transpilers 是转译器，linters 是静态代码检查器；原中文不准确。',318:'scale 在此为适配、扩展，不能逐字说“有良好的规模”。',327:'merchant-facing 是面向商户，不等于已经商业化。',337:'side projects 常是个人业余项目，不一定能赚钱的副业。',344:'continuously 是持续，不是快速。',350:'own projects 是负责；scaling in production 为上线后的生产扩容，不是扩大开发规模。',355:'cross-functional 指跨职能，不是个人拥有多种技能。',363:'if not billions 表示甚至可能达数十亿；不是排除十亿。',373:'extend 偏扩充功能；scale 偏承载更大规模，原中文不能都译作扩展。',381:'把不自然的 multitudes of 换成 many。',393:'修正 deliever 为 deliver。',394:'描述资深人员时用 an experienced / seasoned engineer；be seasoned with 更常见于调味。',413:'runtime 这里指运行耗时，目标是 reducing runtime；不能笼统把 increasing runtime 当性能改善。',418:'thrilled / excited 是兴奋、期待，不表示“胜任”。'}
forms={
'nail down':'nail down + 细节/安排；nail it down 中代词放在两个词之间。',
'pop out':'pop out for + 短暂去做的事；pop out to + 地点。通常暗示很快回来。',
'brush up on':'brush up on + 知识/技能；过去式 brushed up on；on 后不能直接接不带 -ing 的动词。',
'intermittent':'intermittent + 名词，如 intermittent failures；副词为 intermittently。',
'fine-tuning':'a little fine-tuning；fine-tune 是动词，fine-tuning 可作名词。',
'cropped up':'crop up → cropped up；an issue crops up；常以问题或意外事项为主语。',
'collaborate closely with':'collaborate with + 人/团队；collaborate on + 项目。',
'steer clear of':'steer clear of + 名词/动名词；不直接接动词原形。',
'fixate on':'fixate on + 对象；be fixated on 是“过分执着于”。',
'second-guess':'second-guess a decision；second-guess yourself；过去式 second-guessed。',
'firm up':'firm up the plan；firm it up；过去式 firmed up。',
'pull it off':'pull off + 有难度的事情；代词放中间：pull it off。',
'workaround':'a workaround / workarounds；find a workaround for the issue。work around the issue 是分开写的动词结构。',
'cilantro':'without cilantro；cilantro leaves。美式指香菜叶，英式常用 coriander。',
'penultimate':'the penultimate + 名词，如 the penultimate week；倒数第一为 last。',
'keep me in the loop':'keep + 人 + in the loop；loop + 人 + in；be looped in on + 事项。',
'at capacity':'be at capacity；have capacity for + 任务；并非固定要求加 with。',
'a tight turnaround':'a tight / quick turnaround；tight 强调时间不足，quick 强调速度快。',
'paired with':'be paired with + 人/物；pair A with B；配对并不意味着二者完全相同。',
'committed to creating':'be committed to + 名词/动名词；此处 to 是介词，不能写 committed to create。',
'deeply invested in':'be invested in + 名词/动名词；投资金钱和投入精力两种意义要靠语境区分。',
'empowered to':'be empowered to + 动词原形；empower someone to do something。',
'a firm grasp of':'have a firm / solid grasp of + 知识；不能说 a grasp in。',
'an aptitude for':'an aptitude for + 名词/动名词；不直接接动词原形。',
'a knack for':'have a knack for + 名词/动名词；表示做某事很有办法或天赋。',
'from scratch':'build / start / learn from scratch；表示没有现成基础地从头开始。',
'with ease':'with ease 为副词短语，对应 easily；easy 为形容词。',
'with minimal supervision':'work with minimal supervision；independently 也能表达独立性，监督程度要如实。',
'low staff turnover':'low / high staff turnover；此处 turnover 是人员流动，不是营业额。',
'proficient in':'be proficient in + 技能/语言；proficiency in 为名词结构。',
'in bulk':'process / buy / send in bulk；bulk 作前置修饰语时，如 bulk processing。'}
# Register notes protect against oversimplified synonym claims.
register={14:'curry favor 带贬义；win approval 不必然带讨好意味。',17:'throw someone a bone 暗含所给很有限；不适合把正式补偿说成施舍。',19:'circle the wagons / close ranks 都可能暗示防御与排外，不作赞美团结的默认话。',32:'smdh 属网络文字用语；不建议在正式职场消息中使用。',35:'obsess over 与 fixate on 都比 focus on 更强，常含负面判断。',45:'henchmen 带恶人爪牙色彩；accomplices 偏共同犯罪者，并非所有场景可替换。',64:'gut-wrenching 与 heartbreaking 都表示强烈痛苦，不用于轻微失望。',71:'习语带指责意味；对话中先考虑关系与冲突升级的可能。',82:'法语店铺可用 pain au lait；不熟悉该词的英语听众更容易理解 milk bread roll。',87:'noob 可能冒犯；描述自己可自嘲，对别人用 beginner 更稳妥。',97:'本句是破坏性的字面描写，不要把 level everything 用作普通排障表达。',104:'murderous look 形容非常凶狠；look full of fury 侧重愤怒，不必然有杀意。',107:'职场 fire drill 是比喻临时急活；真实消防演习也叫 fire drill，需靠语境区分。',110:'workaround 与 temporary solution 常接近；fix 通常指修复，不能暗示根因已解决。',124:'state-of-the-art / cutting-edge 都偏先进；不要在普通更新里无依据夸大。',139:'apologize profusely 表示反复或强烈道歉，语气重于 simply apologize。',151:'top-notch 更口语、带赞许；excellent 适用范围较广。',181:'the warm fuzzies 很口语且略俏皮，正式文档可说 a warm feeling。',242:'intractable 比 difficult 更强，含棘手、顽固难解的意味。',254:'leverage 常见于职场，但日常说 use / make use of 更直接。',263:'eager to 比 hungry to 更中性；hungry to 带强烈进取的宣传语气。',280:'trusted to 强调信任，empowered to 还涉及授予权限或自主空间。',295:'帮助建立联系并不等于领导数百万人，本题避免过度宣称影响。'}
# Every record gets a concrete recall prompt and its own complete reference sentence.
converted=[]
for i,(r,(sentence,target),meaning,alt,cn) in enumerate(zip(source,examples,meanings,alts,chinese)):
 assert target in sentence
 raw=original_cards[r['url']];sub=raw['sub'];key='practice-'+r['url'].rsplit('/',1)[-1]
 masked=sentence.replace(target,'____',1)
 # The semantic prompt is independent of the hidden answer. No learner input is required.
 context=f'补全这个语境中的表达（想表达“{meaning}”）：\n{masked}'
 explanation=notes.get(i) or f'本句用 {target} 表达“{meaning}”。结合完整句子记忆搭配，而不只背孤立的中文标签。'
 replacement=sentence.replace(target,alt,1)
 # Neutral technical sentences need not be artificially made informal.
 casual=sentence.replace('I am ',"I'm ").replace('We are ',"We're ").replace('We will ',"We'll ").replace('I will ',"I'll ")
 if i in [0,1,2,5,6,7,8,9,10,13,15,16,21,22,24,26,27,28,29,30,31,34,36,37,38,39,40,41,42,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,65,66,67,68,69,70,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112]:
  # A paraphrase is a second valid wording, not always a more casual one.
  casual=sentence
 if i==1:casual="I'm just stepping out for a coffee—back in ten."
 if i==2:casual='I need to brush up on my SQL before that interview.'
 if i==6:casual='Something new came up in testing.'
 if i==24:casual='Can you jump in and help sort this out?'
 if i==49:casual="Let's pin down the timeline before we announce it."
 if i==76:casual="Hang on—I'll check the reservation."
 if i==80:casual='No cilantro, please.'
 if i==88:casual="You're breaking up. Could you say that again?"
 if i==110:casual="There's a way around it for now, but we'll have to restart it manually."
 if i==119:casual="Quick check before we start: are we on the same page?"
 if i==134:casual="I'm pretty booked up right now."
 if i==135:casual='Keep me posted if the plan changes.'
 if i==137:casual="That's not much time for a full review."
 if i==230:casual="I'm on it. I'll let you know if anything changes."
 if i==243:casual="I'll script it so we can process the files in bulk."
 if i==264:casual='I plan ahead so I can get things done on time.'
 converted.append(dict(id=key,mode='B',kind='curated',exerciseType='context-recall',sub=sub,tag='即时表达 · '+sub,short=meaning,context=context,cn='空缺处你会怎么说？',suggestion=cn,reason=f'先确定要表达的是“{meaning}”，再看空缺前后的句法位置。这里可以使用一个词或搭配，不必逐字翻译整条旧笔记。',pro=sentence,casual=casual,explain=explanation,variant=register.get(i) or f'另一个表达方向是 {alt}。示例：{replacement}。替换后仍要核对主语、时态和语气，不能当作所有场景的等号。',fix=notes.get(i) or f'不要把“{meaning}”按中文字序拼接。本题参考搭配为 {target}；完整语境是 {sentence}',source=r['url'],sourceRecordIndex=i,origin='由 Notion 原记录改编 · 语境回忆',body=raw.get('body',''),bodyStatus=raw.get('bodyStatus','')))
 pattern=forms.get(target) or f'句型位置：{masked}\n本句填入：{target}。换主语、时间或对象时，其他部分也需相应调整。'
 learning[key]=dict(term=target,meaning=meaning,example=sentence,exampleCn=cn,forms=pattern,alternatives=f'{alt}\n{register.get(i) or "这是一个近义改写方向；用法和强调点未必完全相同。"}\n例：{replacement}')
# Keep original source cards for provenance, never count them as converted exercises.
base=[x for x in data['lessons'] if not x['id'].startswith('practice-')]
data['lessons']=base+converted
data['conversion']={'sourceRecords':420,'convertedRecords':420,'unconvertedRecords':0,'format':'context-recall','version':1}
(P/'dist/data.json').write_text(json.dumps(data,ensure_ascii=False))
(P/'dist/learning.json').write_text(json.dumps(learning,ensure_ascii=False))
(P/'conversion-audit.json').write_text(json.dumps({'coverage':[{'source':r['url'],'practice':l['id'],'target':examples[i][1]} for i,(r,l) in enumerate(zip(source,converted))]},ensure_ascii=False))
print(f'Converted {len(converted)} / {len(source)} unique records')
