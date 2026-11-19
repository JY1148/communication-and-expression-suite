"""Resolve inflected learning expressions to concrete offsets in each answer."""
import json,re
from pathlib import Path
from audit_answer_alignment import stem,ignore,tokens
p=Path('dist/data.json');data=json.loads(p.read_text());units=json.loads(Path('dist/learning.json').read_text())
count=0
for lesson in data['lessons']:
    if lesson['kind']!='curated':continue
    term=units[lesson['id']]['term'];required=set(tokens(term));lesson['learningHighlights']={}
    for version in (['pro','casual'] if lesson['mode']=='A' else ['casual']):
        sentence=lesson[version]
        # Prefer literal patterns, including function-word-only expressions such as
        # 'was that for me?'. A stem set may otherwise be empty and match 'Sorry'.
        literal=term.rstrip('?.…').strip()
        literal_pattern="[’']".join(re.escape(part) for part in re.split("[’']",literal))
        exact=re.search(r'(?<![A-Za-z])'+literal_pattern+r'(?![A-Za-z])',sentence,re.I)
        if exact:
            lesson['learningHighlights'][version]=[[exact.start(),exact.end()]];count+=1;continue
        words=list(re.finditer('[A-Za-z]+',sentence))
        normalized=[stem(w.group().lower()) for w in words]
        negative_roots={'don':'do','doesn':'does','didn':'did','aren':'are','isn':'is','wasn':'was','weren':'were','haven':'have','hasn':'has','hadn':'had','can':'can','couldn':'could','wouldn':'would','shouldn':'should','won':'wo'}
        for j,w in enumerate(words):
            if w.group().lower()=='t' and j>0 and words[j-1].group().lower() in negative_roots:
                normalized[j]='not';normalized[j-1]=stem(negative_roots[words[j-1].group().lower()])
        candidates=[]
        for start in range(len(words)):
            found=set()
            for end in range(start,len(words)):
                found.add(normalized[end])
                if required<=found:
                    candidates.append((end-start,start,end));break
        assert candidates,(lesson['id'],version,term)
        _,start,end=min(candidates)
        # Include adjacent literal function words from the displayed pattern.
        pattern=re.findall('[a-z]+',term.lower())
        if pattern:
            for size in range(min(start,len(pattern)),0,-1):
                if [w.group().lower() for w in words[start-size:start]]==pattern[:size]:
                    start-=size;break
            for size in range(min(len(words)-end-1,len(pattern)),0,-1):
                if [w.group().lower() for w in words[end+1:end+1+size]]==pattern[-size:]:
                    end+=size;break
        if lesson['id']=='starter-4':
            match=re.search(r'I[’\x27]d love to.*?but',sentence,re.I)
            if match:lesson['learningHighlights'][version]=[[match.start(),match.end()]];count+=1;continue
        lesson['learningHighlights'][version]=[[words[start].start(),words[end].end()]]
        count+=1
p.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')))
print('Highlight offsets generated for',count,'answers')
