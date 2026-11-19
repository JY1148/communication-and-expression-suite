"""Keep the learned expression present in every answer the UI can display."""
import json
from pathlib import Path
p=Path('dist/data.json');d=json.loads(p.read_text());before={l['id']:{k:l.get(k) for k in ['pro','casual']} for l in d['lessons']}
patches={
 'extra-instant-033':{'pro':"I haven't been able to reproduce the issue on my end. Could you send me the steps you followed?",'casual':"I haven't been able to reproduce the issue on my end. Could you send me the steps you followed?"},
'starter-0':{'casual':"Oh, booking a table completely slipped my mind. I'll do it now."},
'starter-3':{'casual':"Let's not commit to a date just yet. We're still waiting on that dependency."},
'starter-5':{'casual':"Oh, one more thing—we still need them to sign off before we go live."},
'starter-6':{'casual':"Quick check before I dive in: can we clarify whether we're exporting this page or everything? And who should be able to use it?"},
'starter-8':{'casual':"I can prioritize this now, but the other task would have to wait until tomorrow. Which one comes first?"},
'adapt-a-0':{'casual':"Can we refocus on today's decision? Let's save two minutes for next steps and who's doing what."},
'adapt-a-2':{'casual':"Let me catch you up on the changes. I'll make sure you're kept in the loop from here."},
'adapt-a-3':{'casual':"Can you walk me through where you got stuck? That'll help me figure out what to fix."},
'adapt-a-4':{'casual':"I'm at capacity this week. When do you need it? I could pick it up next week if that works."},
'adapt-a-6':{'casual':"I'm concerned this could leave the data out of sync. Can we fix that before we ship?"},
'adapt-a-7':{'casual':"We got a 5% improvement, but we're still short of the 20% target. I'll dig into what's slowing us down."},
'adapt-a-8':{'casual':"Thanks! Design and backend made a big contribution—they helped sort out the API issues early on."},
'adapt-a-9':{'casual':"Let's break this down into smaller pieces and work out what depends on what and who owns each piece."},
'adapt-a-10':{'casual':"Sorry, I missed the last part. What did you need me to check?"},
'adapt-b-2':{'casual':"We haven't firmed up a time yet. I'll let you know when we do."},
'adapt-b-6':{'casual':"Let's wrap up for today. We can pick this up tomorrow."},
'adapt-b-8':{'casual':"There's a workaround for now, but it's not a permanent fix."},
'adapt-b-9':{'casual':"I'll follow up on it and keep you posted."},
'long-note-44':{'pro':"Could you send the report by EOD on Friday? For this request, that means 5 p.m. Pacific Time.",'casual':"Could you get me the report by EOD Friday? Let's use 5 p.m. Pacific as the cutoff."},
'extra-judgment-001':{'casual':"We're aiming for Friday, but I can't commit to it until we've checked the integration. We plan to finish that tomorrow afternoon, then I'll confirm the date."},
'extra-judgment-002':{'casual':"Quick clarification: two or three days was an initial estimate. Can we pin down the testing scope before promising a date externally?"},
'extra-judgment-003':{'casual':"The API update is ready in test. Docs and examples are here. Maya, can you validate it by tomorrow afternoon and flag anything missing?"},
'extra-judgment-004':{'pro':"This item appears to have fallen through the cracks because ownership wasn't clear. To protect tomorrow's release, I can update the configuration today if you can review it. Let's also add ownership to the release checklist."},
'extra-judgment-005':{'casual':"I'd like to flag a potential issue before we decide: I think test traffic is included here. I haven't checked how much that changes the result. Can we verify it first?"},
'extra-judgment-006':{'pro':"I should have spoken up earlier. I've since confirmed that option A would break our existing automation. Could we assess the remediation effort before implementation and confirm whether that cost is acceptable?"},
'extra-judgment-007':{'pro':"I can review this today, but I don't yet have enough information to sign off on it. Please share the change scope, test results, and rollback steps. Once those are available, I'll respond within two hours."},
'extra-judgment-008':{'casual':"We've now seen the same export failure for three customers. The cause is still under investigation. I'm checking what they have in common and will update you in fifteen minutes."},
'extra-judgment-009':{'casual':"Service has been restored for now, but we haven't found the cause yet. We'll keep watching it and follow up with a longer-term fix once we know more."},
'extra-judgment-010':{'casual':"Quick heads-up: test is slow on and off. It's not blocking our critical tests yet, but it could affect acceptance testing if it continues tomorrow. I'll check back tomorrow afternoon."},
'extra-judgment-011':{'casual':"I haven't agreed to take this on tonight, and I can't make time this evening. I can size it up tomorrow. If it has to happen tonight, we need someone else assigned."},
'extra-judgment-012':{'casual':"I jumped in on a temporary basis, but this is now taking time every week and pushing back my planned work. Can we work out who owns it going forward and when I can hand it over?"},
'extra-judgment-014':{'casual':"This interaction doesn't meet the keyboard requirements we agreed on. To avoid further rework, can we pause this bit and find an accessible option today?"},
'extra-judgment-015':{'casual':"I see the approach is decided. It touches my module, so I need the decision context and a chance to size the changes before I can confirm this week's delivery."},
'extra-judgment-016':{'pro':"Before we close, I've heard two different targets: an external launch next week, or an internal demo only. Which target are we committing to? I'll capture the action items based on that.",'casual':"Before we wrap up, which target are we committing to: launching next week or just doing an internal demo? I've heard both, and the work we need to do is different."},
'extra-judgment-017':{'casual':"Can we bring it back to the options? Let's pin down the response-time target and what users need to do, then compare both options against those criteria."},
'extra-judgment-018':{'casual':"We know it fails while opening the connection. We haven't proved why yet. We're testing a hypothesis about the connection pool and will update you within an hour, even if we're still investigating."},
'extra-judgment-019':{'casual':"Aggregate metrics can look fine while a small group is still affected. Let's check these accounts and app versions before we call it done."},
'extra-judgment-020':{'pro':"I made an unintended change to the shared configuration, which may affect dependent services. I'm following the rollback procedure and checking the impact. I'll update the recovery status and confirmed impact within ten minutes."},
'extra-judgment-021':{'casual':"Who's taking the first look at this? Can we agree on an owner and get initial findings or an update by the end of the day?"},
'extra-judgment-022':{'casual':"The latest version passed, but I haven't checked older clients yet, so I can't confirm compatibility. Let me test the older versions we support and get back to you tomorrow afternoon."},
'extra-judgment-023':{'casual':"Before we size it up, what problem would the animation solve, and how would we evaluate its benefit? Then we can decide if it goes into this release."},
'extra-judgment-024':{'casual':"I'm stuck on this error. I've ruled out config and permissions, but I can't tell where the request disappears. Could you help me trace it for twenty minutes? It could affect tomorrow's delivery if we don't sort it out today."}
}
for l in d['lessons']:
    if l['id'] in patches:l.update(patches[l['id']])
    # Cloze practice must reveal the sentence used to construct the blank,
    # rather than a paraphrase which may omit the target altogether.
    if l['kind']=='curated' and l['mode']=='C':l['casual']=l['pro']
changed=[{'id':l['id'],'fields':[k for k in ['pro','casual'] if before[l['id']][k]!=l[k]]} for l in d['lessons'] if any(before[l['id']][k]!=l[k] for k in ['pro','casual'])]
p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')))
Path('answer-alignment-changes.json').write_text(json.dumps(changed,ensure_ascii=False,indent=2)+'\n')
print('Aligned',len(changed),'exercise answers')
