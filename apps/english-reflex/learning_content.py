import json
from pathlib import Path
P=Path(__file__).parent
# Each item teaches a phrase from an existing reference sentence, with a new example.
entries=[
('starter-0','slip someone’s mind','某件事一时被某人忘记；常在突然意识到遗漏时使用。','The meeting completely slipped my mind.','我完全忘了那个会议。','slip my mind → slipped my mind；主语通常是被忘记的事情。','I forgot about it 更直接；I can’t remember 表示现在想不起来，侧重点不同。'),
('starter-1','double-check','再核实一次，尤其是避免给出错误信息。','Let me double-check the address.','让我再核实一下地址。','double-check + 名词；double-check that + 从句。','check 是普通检查；verify 更偏核实准确性，通常更正式。'),
('starter-2','on the tip of my tongue','明明知道，却一时说不出来。','Her name is on the tip of my tongue.','她的名字就在嘴边，却想不起来。','It’s on the tip of my tongue；物主可变为 your / his / her。','I’m drawing a blank 更强调脑子一片空白，未必是差一点想起来。'),
('starter-3','commit to','承诺投入或确定承担某事。','We can’t commit to a date yet.','我们还不能承诺具体日期。','commit to + 名词 / 动名词；commit to delivering by Friday。','confirm a date 是确认日期；commit to a date 强调承担承诺。'),
('starter-4','I’d love to, but…','先表达意愿，再说明限制，适合礼貌婉拒。','I’d love to help, but I’m tied up today.','我很想帮忙，但今天抽不开身。','I’d love to + 动词；省略动作时直接 I’d love to。','I wish I could 更强调遗憾；I’m afraid I can’t 更明确但略正式。'),
('starter-5','One more thing','补充最后一点，适合临近结束时加入事项。','One more thing—who’s sending the notes?','还有一点：谁来发会议记录？','One other thing；Just one more thing 语气更轻。','By the way 常是顺带转题；One more thing 更像补充当前讨论。'),
('starter-6','clarify whether','澄清两种或多种可能中究竟是哪一种。','Could you clarify whether this applies to all users?','能确认一下这是否适用于所有用户吗？','clarify whether + 陈述语序；clarify what / how / which 也常见。','confirm 强调核实已有理解；clarify 强调把含糊处说清楚。'),
('starter-7','a heads-up','提前提醒，让对方有准备。','Just a heads-up: the schedule may change.','提前说一声：时间安排可能会变。','give someone a heads-up about something；带连字符。','an update 是进展更新；a warning 通常更强，可能涉及危险或严重后果。'),
('starter-8','prioritize','把某件事排在更高优先级。','We need to prioritize the customer-facing issue.','我们需要优先处理影响客户的问题。','prioritize A over B；priority 是名词。','focus on 强调注意力；prioritize 明确涉及事情的先后或重要性。'),
('adapt-a-0','refocus on','把注意力重新拉回某个重点。','Let’s refocus on the decision we need today.','我们回到今天要做的决定上。','refocus the discussion on + 议题。','bring this back to 更口语；get back to 表示回到先前话题。'),
('adapt-a-1','nail down','把原本未确定的细节最终明确下来。','Let’s nail down the timeline first.','我们先把时间线定下来。','nail down the details；nail it down（代词在中间）。','clarify 是说清楚；finalize 更偏完成最终定稿。'),
('adapt-a-2','make sure','确保某件事发生，或核实它是否成立。','I’ll make sure everyone gets the update.','我会确保所有人收到更新。','make sure that + 从句；make sure to + 动词。','ensure 较正式；check that 常侧重核查，而非负责使它发生。'),
('adapt-a-3','walk someone through','一步步带某人理解流程、例子或操作。','Could you walk me through the steps?','能带我一步步过一下这些步骤吗？','walk me through it；walk the team through the proposal。','explain 是一般解释；show me 更强调展示，未必逐步讲解。'),
('adapt-a-4','at capacity','已经达到可承担工作的上限。','Our team is at capacity this month.','我们团队这个月已经满负荷。','be at capacity；have capacity for + 名词。','booked up 更口语、偏时间排满；overloaded 表示已经超负荷。'),
('adapt-a-5','workaround','名词：绕开当前问题的变通办法，通常暂时缓解问题，并不代表根因已经修复。','Restarting the app is a workaround, not a permanent fix.','重启应用只是临时应对办法，不是永久修复。','a workaround / workarounds；find a workaround；a workaround for the issue。work around the issue 是动词结构，分开写。','temporary solution：强调临时性；stopgap measure：权宜措施，偏正式；a way around the problem：更口语。fix 通常指修复，不能在根因未解决时直接替换。'),
('adapt-a-6','I’m concerned…','提出担忧，把讨论落到可能影响上。','I’m concerned this change could affect existing users.','我担心这次改动可能影响现有用户。','concerned that + 从句；concerned about + 名词。','I’m worried 更口语；I have reservations about 表示有保留意见，不一定是担心后果。'),
('adapt-a-7','short of','没有达到某个目标、数量或标准。','We’re still short of the target.','我们仍未达到目标。','fall short of expectations；be short of staff 表示人手不足。','below target 更直白；fall short of 更强调未达预期。'),
('adapt-a-8','make a contribution','作出贡献；可进一步说明贡献在哪里。','She made a significant contribution to the launch.','她为这次发布作出了重要贡献。','contribute to + 名词 / 动名词；contributions 为复数。','help with 更日常；play a key role in 强调发挥关键作用，程度更强。'),
('adapt-a-9','break something down','把复杂任务拆成更小部分。','Let’s break the project down into milestones.','我们把项目拆成几个里程碑。','break it down into smaller tasks；代词放 break 与 down 之间。','split into 是普通拆分；break down 常用于帮助理解或执行复杂事项。'),
('adapt-a-10','I missed the last part','承认自己漏听了一部分，请对方补充。','Sorry, I missed the last part of your question.','抱歉，你问题的最后一部分我没听到。','missed that / missed the last bit；past tense 描述刚才漏听。','I didn’t catch that 很自然；I don’t understand 是不理解，不一定是没听到。'),
('adapt-a-11','a tight turnaround','完成或交付的时间窗口很短。','That’s a tight turnaround for a full review.','完整审查只给这么点时间，确实很紧。','a quick turnaround 强调速度快；tight turnaround 强调时间受限。','a tight deadline 是截止时间紧；turnaround 强调从接到任务到完成的周转。'),
('adapt-b-0','crop up','问题或事情突然、意外出现。','A few questions cropped up during testing.','测试中冒出了几个问题。','crop up → cropped up；常以 issues / problems / questions 为主语。','come up 更泛；arise 更正式；pop up 更随意，强调突然出现。'),
('adapt-b-1','break up','这里指通话音频断断续续，而不是关系结束。','Your audio keeps breaking up.','你的声音一直断断续续。','You’re breaking up；The audio broke up。','choppy audio 是不流畅的声音；lagging 是延迟，含义不完全一样。'),
('adapt-b-2','firm up','让安排、计划或数字变得更确定。','We’ll firm up the details tomorrow.','我们明天把细节定下来。','firm up the plan；firm it up。','pin down 强调确定难以确定的事；confirm 更偏确认已提出的安排。'),
('adapt-b-3','a mouthful','这里形容名字、词语很长或难以念出来。','That’s quite a mouthful of a name.','这个名字可真拗口。','quite a mouthful；也可字面指一口食物。','hard to pronounce 直接指发音难；a mouthful 还可能是因为名称很长。'),
('adapt-b-4','have a soft spot for','对某人或某物格外喜爱、心软。','I have a soft spot for old bookstores.','我对老书店情有独钟。','have always had a soft spot for；for 后接名词。','be fond of 较一般的喜欢；be obsessed with 强得多，不能随便替换。'),
('adapt-b-5','sit tight','暂时留在原地或等候下一步消息。','Sit tight—I’ll call you when it’s ready.','先等一下，准备好我就打给你。','常作简短祈使句；也可以 We’re sitting tight for now。','hold on 更常指等一下；please wait here 对陌生人更明确礼貌。'),
('adapt-b-6','wrap up','结束并收尾某项活动。','Let’s wrap up the meeting in five minutes.','我们五分钟后结束会议。','wrap it up；wrap-up 作名词或修饰语时通常带连字符。','wind down 是逐渐结束；call it a day 表示今天就做到这里。'),
('adapt-b-7','brush up on','温习已有知识或技能，恢复熟练。','I’m brushing up on my presentation skills.','我正在温习演讲技巧。','brush up on + 技能或知识；不是 brushup。','review 较中性；learn from scratch 是从零学习，含义不同。'),
('adapt-b-9','follow up on','继续跟进先前事项，确认进展或推动后续。','I’ll follow up on the request tomorrow.','我明天会继续跟进这个请求。','follow up with someone；follow up on something；a follow-up 是名词。','check on 更偏查看状态；chase up 催问意味更强，英式英语中更常见。'),
('adapt-b-10','one-off','一次性的事件或安排，不打算常态化。','This meeting is a one-off.','这个会议只开这一次。','a one-off；a one-off request；one-off 作形容词常放名词前。','one-time 更直白；single-use 通常指物品只能用一次，不等同。'),
('adapt-b-11','without cilantro','不放香菜；点餐中可直接表达偏好。','Could I have the soup without cilantro?','这份汤可以不放香菜吗？','without + 配料；cilantro 指香菜叶；celery 是芹菜。','No cilantro, please 更简短；on the side 是另外装，不是完全不放。')]
learning={}
for key,term,meaning,example,cn,forms,alternatives in entries:
 learning[key]={'term':term,'meaning':meaning,'example':example,'exampleCn':cn,'forms':forms,'alternatives':alternatives}
learning['adapt-b-8']=learning['adapt-a-5']
(P/'dist/learning.json').write_text(json.dumps(learning,ensure_ascii=False))
assert len(learning)==33
print('33 complete learning modules generated')
