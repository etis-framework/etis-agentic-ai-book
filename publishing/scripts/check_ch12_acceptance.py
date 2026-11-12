#!/usr/bin/env python3
"""Chapter 12 acceptance checks; publication-level technical/Word QA remains manual."""
from pathlib import Path
import hashlib,json,re,sys,zipfile,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[2]
p=root/'manuscript/part-02-architecture/ch12-context-retrieval-and-memory-e4/index.md'
s=p.read_text();errors=[]
def check(test,msg):
 if not test:errors.append(msg)
words=len(re.findall(r"\b[\w'-]+\b",s))
ledger=json.loads((root/'publishing/SINGLE_VOLUME_FINISHED_PAGE_LEDGER_V12.json').read_text())
check(words<=3000,f'Chapter 12 exceeds source cap: {words}>3000')
check(ledger['chapter_pages']['12']==14,'V12 Chapter 12 allocation drift')
check(ledger['chapter_total_pages']==485 and ledger['front_back_reserve_pages']==65 and ledger['target_finished_pages']==550,'V12 totals drift')
check('STATUS: PLANNED' not in s,'Chapter 12 remains a stub')
for term in ['CASE-204','$500','RF-1042','Design A','Design B','Design C','admission and identity','coordination and ownership','agent reasoning and proposals','context and retrieval','trusted execution','provenance','lineage','freshness','purpose limitation','data minimization','retrieval-augmented generation (RAG)','Embeddings','time-to-live (TTL)','prompt injection','memory','epoch','source of record','UNKNOWN','Chapter 13']:
 check(term.lower() in s.lower(),f'Missing architectural term or case invariant: {term}')
for prohibited in ['E4 authorizes','E4 issues refund','E4 completes payment','RF-1043','Design C autonomously pays']:
 check(prohibited.lower() not in s.lower(),f'Unsafe claim: {prohibited}')
check(s.count('![Figure 12.')==3,'Expected 3 Chapter 12 figures')
# Verify first substantive occurrence of important terms is explained, not merely named
for regex in [r'\*\*Provenance\*\* describes',r'\*\*Lineage\*\* is',r'\*\*Freshness\*\* is',r'\*\*Prompt injection\*\* is',r'\*\*Model working context\*\* is',r'\*\*ownership epoch\*\*.*increasing generation']:
 check(bool(re.search(regex,s,re.I)),f'Missing first-use explanation: {regex}')
doc=root/'dist/etis-agentic-ai-book.docx';media=set()
if not doc.is_file(): errors.append('No DOCX built: run make book-docx')
else:
 with zipfile.ZipFile(doc) as z:
  media={hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/')}
ns='{http://www.w3.org/2000/svg}'
for i in range(1,4):
 fid=f'F12-{i:02d}';src=root/f'assets/shared-figures/sources/{fid}.svg';svg=root/f'assets/shared-figures/rendered/{fid}.svg';png=root/f'assets/shared-figures/rendered/{fid}.png'
 if not all(f.is_file() for f in (src,svg,png)):
  errors.append(f'Missing figure master or render: {fid}');continue
 check(src.read_bytes()==svg.read_bytes(),f'{fid} rendered SVG not source-identical')
 try: el=ET.fromstring(src.read_bytes())
 except ET.ParseError as e: errors.append(f'{fid} malformed SVG: {e}');continue
 check(el.attrib.get('width')=='5.75in',f'{fid} not 5.75in')
 check(el.attrib.get('viewBox','').startswith('0 0 1140 '),f'{fid} V9 viewBox wrong')
 texts=[t for t in el.iter() if t.tag==ns+'text']
 check(all(float(t.attrib.get('font-size','0'))>=19 for t in texts),f'{fid} under 19px figure labels')
 check(all(t.attrib.get('font-family','').startswith('Arial') for t in texts),f'{fid} nonstandard font')
 check(len([e for e in el.iter() if e.tag==ns+'rect'])>=5,f'{fid} insufficient technical diagram objects')
 check(len([e for e in el.iter() if e.tag==ns+'polyline'])>=4,f'{fid} missing connector geometry')
 check(hashlib.sha256(png.read_bytes()).hexdigest() in media,f'{fid} current PNG not embedded in DOCX')
 check(not (src.parent/f'{fid}.dot').exists(),f'{fid} obsolete DOT figure')
print(f'Chapter 12: {words}/3000 words; V12 budget 14 pages')
if errors:
 print('FAIL:\n'+'\n'.join('- '+x for x in errors));sys.exit(1)
print('PASS: terminology, running case, V12 allocation, V9 figure masters, DOCX image fingerprint')
print('REMAINING: Microsoft Word print-size review and full-book final pagination evidence')
