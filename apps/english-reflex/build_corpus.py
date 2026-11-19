import json,re,html
from pathlib import Path
P=Path(__file__).parent
rows=json.loads((P/'corpus.json').read_text());base=json.loads((P/'curated.json').read_text())
def clean(x):
 x=html.unescape(str(x or ''));x=re.sub(r'\[([^\]]+)\]\([^)]*\)',r'\1',x);x=re.sub('<[^>]*>','',x);return x.strip()
def find(term):
 return next((r['url'] for r in rows if term.lower() in clean(r['Name']).lower()),rows[0]['url'])
for i,l in enumerate(base):
 l.update(id='starter-'+str(i),sub=('即时反应与修正' if l['mode']=='B' else '需求与范围'),kind='curated')
 if i==7:l['sub']='风险与进度'
 if i==8:l['sub']='优先级与边界'
A=[
('会议与意见','讨论没有结束','会议讨论越来越发散，只剩十分钟，还没确定谁做什么。你会怎样介入？','先肯定讨论的价值，再把话题拉回要做出的决定；结尾确认负责人和下一步。','我们先回到今天需要决定的事情上，最后留两分钟确认行动项和负责人。','Could we refocus on the decision we need to make today and leave two minutes to confirm the action items and owners?','Can we bring this back to today’s decision? Let’s save two minutes for next steps and who’s doing what.','streamline the meeting agenda'),
('需求与范围','方案还缺实施细节','团队要马上开发，但错误处理和验收标准尚未讨论。你会提出什么，而不仅是说“需要对齐”？','点出会影响实现的缺口，请大家先敲定；不要用“确认一下”掩盖具体问题。','动手前我们先敲定错误处理和验收标准，免得后面返工。','Could we nail down error handling and the acceptance criteria before implementation to avoid rework?','Before we build this, can we nail down how errors should work and what counts as done?','nail down'),
('协作与反馈','重要更新有人没收到','你发现设计同事不知道需求已经改变，继续按旧方案制作。你会如何纠正信息链？','先补齐变化和影响，再约定后续更新参与者；不把重点放在谁漏发了消息。','我把最新变更同步给你，后续相关讨论也会把你加上。','I’ll share the latest changes with you and make sure you’re included in future discussions.','Let me catch you up on the changes. I’ll keep you in the loop from here.','keep sb. in the loop'),
('协作与反馈','对方的建议不够具体','你拿到一句“这个页面用起来不顺”，但不知道具体在哪里卡住。你会如何追问？','先确认反馈，再索取能定位问题的例子或操作步骤；避免空泛地说“请详细说明”。','能举个你操作时卡住的例子吗？这样我更容易定位问题。','Could you walk me through a specific example of where the flow felt difficult? That would help me identify the issue.','Can you show me where you got stuck? That’ll help me figure out what to fix.','get one’s input'),
('优先级与边界','容量已经满了','同事请你帮忙做一个没有截止时间的新功能，但你的本周任务已排满。你会怎样回应？','说明当前容量，问清紧急程度，提供可行时点；不默默接下，也不只说“不归我管”。','我这周已经排满了。这个最晚什么时候需要？如果不急，我下周可以开始。','I’m at capacity this week. When is this needed? If it isn’t urgent, I can start next week.','I’m pretty booked this week. When do you need it? I could pick it up next week if that works.','be at capacity'),
('风险与进度','临时方案有代价','你找到能绕开当前缺陷的办法，但会增加手动操作。你会如何给出建议？','区分临时缓解与长期修复，说明代价和适用期限，避免把“能跑”当作最终解决。','有个临时方案可以先用，但需要手动操作。我们可以先恢复流程，再安排正式修复。','We have a workaround, but it requires manual steps. We could use it to restore the workflow while scheduling a permanent fix.','There’s a workaround, though it’s manual. We can use it for now and plan a proper fix.','workaround'),
('会议与意见','你不赞成当前提议','团队倾向于赶在今天上线，但你发现一个未解决的数据一致性问题。你如何提出不同意见？','把异议落到可验证的风险与建议上；既不人身判断，也不因措辞客气而隐藏严重程度。','我担心这个问题会造成数据不一致。建议先解决它，再决定是否上线。','I’m concerned this could cause inconsistent data. I recommend resolving it before we decide whether to release.','I’m worried this could leave the data out of sync. Can we fix that before we ship?','I dont agree'),
('复盘与成果','结果没有达到预期','你的改动上线后延迟只降低了5%，低于预期20%。在进展会上应该怎样汇报？','分清目标、实际结果和下一步；不只报“做完了”，也不把差距包装成成功。','目前延迟降低了5%，还没达到20%的目标。我会继续分析主要瓶颈。','Latency has improved by 5%, short of our 20% target. I’ll investigate the remaining bottlenecks.','We got a 5% improvement, but we’re not at the 20% target yet. I’ll dig into what’s still slowing us down.','fall short'),
('复盘与成果','表扬时如何分配功劳','经理表扬了你交付的功能，但设计和后端同事也有重要贡献。你会怎样回应？','接受肯定，再具体指出合作贡献；不否认自己的工作，也不把团队成果全揽下来。','谢谢！设计和后端团队也帮了很多，尤其是提前解决了接口问题。','Thank you. The design and backend teams made important contributions, particularly by resolving the API issues early.','Thanks! A big shout-out to design and backend—they helped sort out the API issues early on.','shoutout'),
('需求与范围','大任务让人无从开始','需求很大、估时差异也大，团队还不知道如何分工。你会怎样推动下一步？','先把工作拆成可讨论和估算的小块，再确定依赖与负责人。','我们先按阶段拆一下任务，再看每部分的依赖和负责人。','Let’s break the work down by stage, then identify the dependencies and owners for each part.','Let’s break this into smaller pieces and work out what depends on what and who owns each piece.','break down the work'),
('协作与反馈','你也没听明白','远程会议中，你走神漏听了问题，但并没有网络故障。你会怎样回应？','诚实请求重复，不捏造音频中断；可以先复述听到的部分再补问。','抱歉，我漏听了最后一部分。你能再说一下希望我确认什么吗？','Sorry, I missed the last part. Could you repeat what you’d like me to confirm?','Sorry, I missed that last bit. What did you need me to check?','商务英语'),
('风险与进度','截止时间非常紧','对方希望一天完成三天的工作。你还没有评估哪些范围可以缩减。你会如何回应？','先表达时限限制，再讨论范围与可行方案；不要只说“我尽量”而形成无条件承诺。','这个时间比较紧。我们能先确定必须包含哪些内容，再看今天能交付什么吗？','The turnaround is tight. Could we agree on the must-have scope before confirming what we can deliver today?','That’s a tight turnaround. Can we work out what absolutely needs to be in today’s version?','tight turnaround')]
for j,(sub,title,ctx,reason,cn,pro,cas,term) in enumerate(A):
 base.append(dict(id='adapt-a-'+str(j),mode='A',kind='curated',sub=sub,tag='沟通判断 · '+sub,short=title,context=ctx,cn='你会在此刻沟通什么？先写中文思路，再尝试英文。',suggestion=cn,reason=reason,pro=pro,casual=cas,explain='训练目标：先识别沟通时机、说清具体问题，再选择适合关系与场合的英文。',variant='参考表达是一种可行方式；请按实际事实、权限与时间调整，不必逐字背诵。',fix='避免只表达模糊态度。补齐当前事实、影响和明确的请求或下一步。',source=find(term),origin='根据已有笔记改编的模拟场景'))
B=[
('即时反应与修正','刚冒出个问题','刚开始讨论时发现一个新问题。','刚冒出个问题，我先看一下。','An issue has just cropped up. Let me check it first.','Something just cropped up—let me take a look.','crop up','crop up 强调意外出现，常用于问题或事情。'),
('会议与远程沟通','声音断断续续','视频会议中对方声音不连续。','你的声音断断续续的，最后一句能再说一遍吗？','Your audio is breaking up. Could you repeat the last sentence?','You’re breaking up. Could you say that last bit again?','choppy','音频不连续可用 breaking up / choppy；确实有音频问题时才这样说。'),
('计划与跟进','定下来再告诉你','对方问你还没定下来的时间安排。','时间还没定，定下来我就告诉你。','The timing isn’t confirmed yet. I’ll let you know once we’ve firmed it up.','We haven’t pinned down a time yet. I’ll let you know when we do.','firm up','firm up 是让安排更确定，不是“盖棺定论”。'),
('即时反应与修正','这名字可真拗口','同事说出一个很长的产品名字。','这个名字可真拗口，有简称吗？','That name is quite a mouthful. Is there a shorter version?','That’s a mouthful! Is there a short name for it?','quite a mouthful','a mouthful 可描述名字又长又难说，不是指嘴里真的塞满东西。'),
('情绪与人际','我就特别喜欢这个','朋友问你为什么总买旧式文具。','我就是对老式文具有点情有独钟。','I have a soft spot for vintage stationery.','I’ve always had a soft spot for old-school stationery.','have a soft spot','have a soft spot for 表示特别喜爱，语气温柔，不需要直译“软的地方”。'),
('计划与跟进','先别动，等我消息','你去确认信息，请对方暂时留在原地。','你先在这里等一下，我问完就回来。','Please wait here for a moment. I’ll be back after I check.','Sit tight—I’ll check and be right back.','sit tight','sit tight 可表示先别行动、等消息；对陌生人用 please wait here 更稳妥。'),
('计划与跟进','今天先到这里','一次讨论已接近结束。','今天先到这里，剩下的我们明天接着聊。','Let’s wrap up for today and continue the remaining discussion tomorrow.','Let’s call it a day. We can pick this up tomorrow.','wind down','wind down 强调逐渐结束；wrap up 强调收尾，call it a day 表示今天到此为止。'),
('计划与跟进','抽空补一下知识','你发现自己某项技能生疏了。','我得找时间补一下 SQL。','I need to set aside some time to brush up on SQL.','I need to brush up on my SQL.','brushup','动词短语写作 brush up on，不是 brushup；表示温习恢复熟练。'),
('技术协作','先临时绕过去','暂时不能修复问题，但有替代操作。','有办法先绕过去，不过不是长久之计。','There’s a workaround, but it isn’t a long-term solution.','There’s a way around it for now, but it’s not a permanent fix.','workaround','workaround 是临时变通，不等于根因已经修复。'),
('情绪与人际','我来处理就行','对方担心一件你正在负责的事。','这件事我在跟进，有进展就告诉你。','I’m following up on this and will share any updates.','I’m on top of it. I’ll keep you posted.','be on top of it','on top of it 表示掌握、积极处理；不是对所有情况都保证“已经搞定”。'),
('计划与跟进','只做这一次','同事问这项手动操作是否要常态化。','这次只是临时做一次，之后不会每次都这样。','This is a one-off. We won’t need to do it this way every time.','It’s just a one-off—we won’t be doing this every time.','one-off','one-off 表示一次性的安排或事件，不是 single-use 那种物品用一次即丢。'),
('日常与饮食','不要香菜','点餐时说明不想加香菜。','这份可以不放香菜吗？','Could you make this without cilantro, please?','Could I get this without cilantro?','cilantro','cilantro 是香菜叶，不是芹菜；芹菜是 celery。')]
for j,(sub,title,ctx,cn,pro,cas,term,exp) in enumerate(B):
 base.append(dict(id='adapt-b-'+str(j),mode='B',kind='curated',sub=sub,tag='即时表达 · '+sub,short=title,context=ctx,cn=cn,pro=pro,casual=cas,explain=exp,variant='两版都可自然使用；专业版偏明确礼貌，口语版偏简短随意。',fix='先表达这个场景里的意图，再选英语常用搭配；不要按中文词序拼接。',source=find(term),origin='根据已有词条改编的模拟例句'))
# Every record remains accessible with provenance; unfinished or doubtful records are review cards.
corrections={'cilantro':('香菜','cilantro 是香菜，不是芹菜。'),'second-gues':('质疑；事后指点','拼写应为 second-guess。'),'a healthy of':('可观数量的……','原搭配缺词；通常为 a healthy amount of / a healthy dose of。'),'p enultimate':('倒数第二','penultimate 是倒数第二，不是 last but two。'),'giblet':('禽类内脏','通常用复数 giblets；不泛指牛杂。'),'brushup':('温习；复习','动词短语为 brush up on。'),'consistently beat deadlines':('总能提前完成','beat a deadline 表示提前完成；按时完成更常用 meet deadlines。')}
raw=[]
for i,r in enumerate(rows):
 name=clean(r.get('Name'));cn=clean(r.get('Expressions'));eq=clean(r.get('Equivalent'));meta=' '.join([str(r.get('Range','')),str(r.get('Tags','')),name]).lower()
 sub='词汇与习语'
 if any(t in meta for t in ['food & drink','mayo','cilantro','shiitake','palate']):sub='日常与饮食'
 elif any(t in meta for t in ['编程','api','code','software','system','javascript','cloud','architecture','frontend','backend','distributed','technical','deploy','test','unix','aws']):sub='技术协作'
 elif any(t in meta for t in ['project','deadline','milestone','scope','capacity','turnaround','stakeholder','schedule','risk']):sub='计划与跟进'
 elif any(t in meta for t in ['teamwork','collaborat','team','feedback','loop','input']):sub='协作与反馈'
 elif any(t in meta for t in ['职场','ability','career','growth','experience','expertise','self-','proficien']):sub='求职与成长'
 elif '生活' in meta or 'daily things' in meta:sub='日常与人际'
 note='';review=not cn or cn=='中文翻译' or not re.search('[\u4e00-\u9fff]',cn)
 if name in corrections:cn,note=corrections[name];review=True
 if name=='penultimate':cn='倒数第二';note='原 Equivalent 的 last but two 不准确；应为 second to last。';review=True
 if name=='collabrate closely with a team of ..':note='collabrate 应为 collaborate。';review=True
 if name=='deliever quality solutions':note='deliever 应为 deliver。';review=True
 raw.append(dict(id='notion-'+r['url'].rsplit('/',1)[-1],mode='B',kind='source',sub=sub,tag='语料复习 · '+sub,short=name,context='复习你的已有笔记。先尝试英文，再查看原文；这里的旧笔记不是已校验的标准答案。',cn=cn if cn and cn!='中文翻译' else '这条笔记缺少可直接练习的中文释义，请先查看原文补充。',pro=name,casual=eq or '原记录没有填写替代表达。',explain=note or '原始词条按笔记保留。请结合语境使用；需要完整场景训练时选择“情境训练”。',variant='本卡展示原始英文与原 Equivalent，不强行把它们标成专业版、口语版。',fix=note or '如发现拼写、搭配或释义不完整，可通过来源链接回到 Notion 核对。',source=r['url'],review=review,original=r,origin='Notion 原始记录'))
data={'snapshot':'2026-10-22','sourceCount':len(rows),'lessons':base+raw}
(P/'dist/data.json').write_text(json.dumps(data,ensure_ascii=False))
print(json.dumps({'source':len(raw),'curated':len(base),'review':sum(x['review'] for x in raw)},ensure_ascii=False))
# Attach all fetched page bodies, using plain text rendering in the browser.
pages=json.loads((P/'corpus-pages-complete.json').read_text());bodies={}
for x in pages:
 r=x['result'];v=r.get('structuredContent')
 if not v:
  v=json.loads(next(y['text'] for y in r['content'] if y['type']=='text'))
 t=v.get('text','');m=re.search(r'<content>([\s\S]*?)</content>',t)
 bodies[x['url']]=(m[1].strip() if m else '',bool(v.get('truncated') or v.get('unknown_block_count')))
for l in data['lessons']:
 body,partial=bodies.get(l.get('source'),('',False));l['body']=body;l['bodyStatus']='正文已读取；原始 Markdown 按纯文本展示。'+(' 部分块无法完整读取，请查看 Notion 来源。' if partial else '')
(P/'dist/data.json').write_text(json.dumps(data,ensure_ascii=False))
assert len({x['url'] for x in rows})==420
assert len({x['id'] for x in data['lessons']})==len(data['lessons'])
print('Verified: 420 unique source records; 33 curated lessons; all page bodies fetched')
# Apply presentation rules on every rebuild, preserving original notes in their own field.
import runpy
runpy.run_path(str(P/'normalize_prompts.py'))
