#!/usr/bin/env python3
"""Chapter 17 + Part III entry V12, running case, figure identity and DOCX mechanical acceptance."""
from pathlib import Path
import hashlib,json,re,sys,zipfile,xml.etree.ElementTree as ET
r=Path(__file__).resolve().parents[2]; errors=[]
ch=r/'manuscript/part-03-patterns/ch17-choosing-deterministic-agentic-and-hybrid-designs/index.md'
part=r/'manuscript/part-03-patterns/_part.md';c=ch.read_text();p=part.read_text()
ledger=json.loads((r/'publishing/SINGLE_VOLUME_FINISHED_PAGE_LEDGER_V12.json').read_text())
word_count=len(re.findall(r"\b[\w'-]+\b",c))
def need(condition,message):
 if not condition:errors.append(message)
need(word_count<=3000,f'Chapter 17 word cap exceeded: {word_count}/3000')
need(ledger['chapter_pages']['17']==12,'Chapter 17 V12 page allocation changed')
need((ledger['chapter_total_pages'],ledger['front_back_reserve_pages'],ledger['target_finished_pages'])==(485,65,550),'Locked whole-book page budget changed')
for term in ('CASE-204','$500','RF-1042','Design A','Design B','Design C','Figure 8.1','Chapter 16','Chapter 18','Part III','E1','E2','E3','E4','E5','E6','E7','E8','E9','UNKNOWN','independent','credential','idempotency key','not a security credential','reconciliation','cost per acceptable','conditional','negative','evidence','ADR'):
 need(term.lower() in c.lower(),f'Chapter 17 missing {term}')
for term in ('17 —','18 —','19 —','20 —','21 —','target-state','CASE-204','RF-1042','Design A','Design B','Design C','Figure 8.1'):
 need(term.lower() in p.lower(),f'Part III introduction missing {term}')
need('A/B/C are **case-level comparison alternatives**' in c,'Alternative-vs-pattern distinction missing')
need('These are **alternatives**, not a cumulative implementation sequence' in c,'A/B/C could be mistaken as stages')
need('not an automated classifier' in c,'Decision figure could be mistaken for deterministic classifier')
need(c.count('![Figure 17.')==3,'Expected three Chapter 17 figure references')
need(all(f'F17-0{i}.png' in c for i in range(1,4)),'Figures not linked')
need(all(s in c for s in ('Parasuraman, Sheridan, and Wickens, 2000','Bass, Clements, and Kazman, 2021','Yao et al., 2024','FinOps Foundation, 2025')),'Missing expected local citations')
need('Chapter 17' in (r/'references/source-register.md').read_text(),'Chapter 17 source mapping absent')
need('Selected research, standards and professional sources' in (r/'manuscript/backmatter/bibliography.md').read_text(),'Bibliography scope not updated')
for bad in ('timeout proves failure','agent can authorize itself','refund payment without approval','model holds payment credentials'):
 need(bad not in c.lower(),f'Unsafe statement: {bad}')
media=set();doc=r/'dist/etis-agentic-ai-book.docx';need(doc.exists(),'Integrated DOCX absent')
if doc.exists():
 try:
  with zipfile.ZipFile(doc) as z:media={hashlib.sha256(z.read(k)).hexdigest() for k in z.namelist() if k.startswith('word/media/')}
 except Exception as e:errors.append(f'Cannot inspect Word: {e}')
ns='{http://www.w3.org/2000/svg}'
for i in range(1,4):
 tag=f'F17-0{i}';master=r/f'assets/shared-figures/sources/{tag}.svg';rend=r/f'assets/shared-figures/rendered/{tag}.svg';png=r/f'assets/shared-figures/rendered/{tag}.png'
 if not all(f.exists() for f in (master,rend,png)):
  errors.append(f'{tag} missing figure member');continue
 need(master.read_bytes()==rend.read_bytes(),f'{tag}: master/render SVG differ')
 try: s=ET.fromstring(master.read_bytes())
 except Exception as e:errors.append(f'{tag}: SVG invalid {e}');continue
 need(s.attrib.get('width')=='5.75in',f'{tag}: wrong print width')
 need(s.attrib.get('viewBox','').startswith('0 0 1140 '),f'{tag}: wrong canvas')
 labels=list(s.iter(ns+'text'))
 need(len(labels)>=15 and all(float(x.get('font-size','0'))>=19 for x in labels),f'{tag}: source label size below 19px')
 need(all(x.get('font-family','').startswith('Arial') for x in labels),f'{tag}: incorrect font family')
 need(len(list(s.iter(ns+'rect')))>=5,f'{tag}: insufficient diagram content')
 need(hashlib.sha256(png.read_bytes()).hexdigest() in media,f'{tag}: current PNG not embedded in Word')
print(f'Chapter 17 acceptance: {word_count}/3000 source words; V12 allowance 12 rendered pages; {len(errors)} error(s)')
if errors:
 for e in errors: print('FAIL:',e)
 sys.exit(1)
print('PASS: Part III progression, case continuity, local citations, V12 plan, SVG masters, PNGs and Word fingerprints')
print('OPEN MANUAL GATES: Native Word on Mac print-size/actual pagination, full six-lens editorial sign-off, exact source-page citations')
