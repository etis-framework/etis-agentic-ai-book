#!/usr/bin/env python3
"""Check Chapter 18 V2 reviewer comments, source records, and cross-chapter coverage."""
from pathlib import Path
import re,sys
R=Path(__file__).resolve().parents[2]
paths={
'10':'manuscript/part-02-architecture/ch10-coordination-registry-and-ownership-e2/index.md',
'17':'manuscript/part-03-patterns/ch17-choosing-deterministic-agentic-and-hybrid-designs/index.md',
'18':'manuscript/part-03-patterns/ch18-coordination-and-delegation-patterns/index.md',
'front':'manuscript/frontmatter/how-to-use-this-book.md',
'part':'manuscript/part-03-patterns/_part.md',
'glossary':'metadata/terminology.md',
'map':'metadata/topic-traceability.md',
'bib':'manuscript/backmatter/bibliography.md',
'bibtex':'references/bibliography.bib',
'sources':'references/source-register.md'}
s={k:(R/v).read_text() for k,v in paths.items()}
checks={
'Chapter 10 bridge':('10',['Chapter 18','generalist/specialist','registration is not authorization']),
'Chapter 17 bridge':('17',['Chapter 18','independent axes','hub/peer']),
'Chapter 18 agency and lifecycle':('18',['generalist agent','specialist agent','Warm capacity'.lower(),'version compatibility','cost per acceptable completed workflow']),
'Chapter 18 independent topology':('18',['hub-and-spoke','Direct peer advisory','Communication topology never transfers E2 ownership']),
'Chapter 18 registry staging':('18',['Registration','discovery','eligibility','delegation','independent enforcement','Figure 10.1']),
'Chapter 18 failure tests':('18',['worker version incompatible','pool exhausted','Peer message delayed']),
'Architecture limits':('18',['CASE-204','RF-1042','UNKNOWN','E5/E6','Chapter 8']),
'Front matter':('front',['topic through the book','Architectural contract reader reference']),
'Part III':('part',['Independent design axes','registry discovery is not authorization']),
'Terminology':('glossary',['Generalist agent','Specialist agent','Communication topology','Capability registry']),
'Traceability':('map',['Ch8 §§8.3–8.4','Ch10 §§10.4–10.5','Ch18 §18.3','planned obligations','unverified']),
'Bibliography':('bib',['Fowler, Martin','Microservice Trade-Offs','FinOps Foundation','Kleppmann']),
'BibTeX':('bibtex',['fowler_microservice_tradeoffs_2015','finops_unit_economics','kleppmann_2017']),
'Source register':('sources',['Chapter 18 V2','fowler_microservice_tradeoffs_2015','finops_unit_economics','hohpe_woolf_2003','source-page']),
}
fail=[]
for name,(file,terms) in checks.items():
 for term in terms:
  if term.lower() not in s[file].lower():fail.append(f'{name}: missing {term}')
count=len(re.findall(r"\b[\w'-]+\b",s['18']))
if count>3000:fail.append(f'Chapter 18 word cap {count}>3000')
for term in ['Fowler (2015)','FinOps Foundation (2025)','Hohpe and Woolf (2003)','Kleppmann (2017)','Bass, Clements, and Kazman (2021)']:
 if term not in s['18']:fail.append('local citation missing: '+term)
for f in fail:print('FAIL:',f)
print('Chapter 18 V2 source words:',count,'/ 3000; findings:',len(fail))
if fail:sys.exit(1)
print('PASS: comment responses, topical trace, local citations, bibliography and case constraints')
print('OPEN: exact edition/page source audit, Mac Word pagination and print-size figure inspection')
