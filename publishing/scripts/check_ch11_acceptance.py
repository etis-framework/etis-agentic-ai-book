#!/usr/bin/env python3
"""Chapter 11 mechanical acceptance. Human print and technical review remain mandatory."""
from pathlib import Path
import hashlib,json,re,sys,zipfile,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[2]
c10=root/'manuscript/part-02-architecture/ch10-coordination-registry-and-ownership-e2/index.md'
p=root/'manuscript/part-02-architecture/ch11-agent-reasoning-and-proposal-contracts-e3/index.md'
ledger=json.loads((root/'publishing/SINGLE_VOLUME_FINISHED_PAGE_LEDGER_V12.json').read_text())
s=p.read_text();issues=[]
def check(ok,msg):
 if not ok:issues.append(msg)
words=len(re.findall(r"\b[\w'-]+\b",s))
check(words<=3000,f'Word cap exceeded ({words}>3000)')
check(ledger['chapter_pages']['11']==14,'V12 Chapter 11 allocation drift')
check(ledger['chapter_total_pages']==485 and ledger['front_back_reserve_pages']==65 and ledger['target_finished_pages']==550,'V12 overall drift')
check('STATUS: PLANNED' not in s,'Chapter 11 remains a stub')
check('An **epoch** is an increasing ownership-generation number' in c10.read_text(),'Deferred Chapter 10 epoch definition missing')
for item in ['CASE-204','$500','RF-1042','Design A','Design B','Design C','coordination and ownership (E2)','reasoning and proposals (E3)','context and retrieval (E4)','trusted execution (E5)','Chapter 12','evidence_refs','scope_ref','NEEDS_REVIEW','UNKNOWN','fabricated','revoked']:
 check(item.lower() in s.lower(),f'Missing invariant: {item}')
check(s.count('![Figure 11.')==3,'Expected three substantive figures')
for bad in ['E3 authorizes','E3 issues payment','RF-1043','E4 approves refund']:
 check(bad not in s,f'Unsafe implication: {bad}')
doc=root/'dist/etis-agentic-ai-book.docx'
if not doc.is_file():issues.append('Built DOCX missing; run make book-docx');media=set()
else:
 with zipfile.ZipFile(doc) as z: media={hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/')}
ns='{http://www.w3.org/2000/svg}'
for fid in ['F11-01','F11-02','F11-03']:
 src=root/f'assets/shared-figures/sources/{fid}.svg'
 svg=root/f'assets/shared-figures/rendered/{fid}.svg'
 png=root/f'assets/shared-figures/rendered/{fid}.png'
 if not all(p.is_file() for p in (src,svg,png)):
  issues.append(f'{fid} missing master/render');continue
 check(src.read_bytes()==svg.read_bytes(),f'{fid} rendered SVG differs from source')
 try:r=ET.fromstring(src.read_bytes())
 except ET.ParseError as e:issues.append(f'{fid} broken SVG {e}');continue
 check(r.attrib.get('width')=='5.75in',f'{fid} width not print standard')
 check(r.attrib.get('viewBox','').startswith('0 0 1140 '),f'{fid} invalid V9 viewBox')
 texts=[e for e in r.iter() if e.tag==ns+'text']
 check(all(float(e.attrib.get('font-size','0'))>=19 for e in texts),f'{fid} substandard tiny text')
 check(all(e.attrib.get('font-family','').startswith('Arial') for e in texts),f'{fid} nonstandard text face')
 check(len([e for e in r.iter() if e.tag==ns+'rect'])>=6,f'{fid} missing composed boxes')
 check(len([e for e in r.iter() if e.tag==ns+'polyline'])>=4,f'{fid} missing diagram flow')
 check(hashlib.sha256(png.read_bytes()).hexdigest() in media,f'{fid} not actually embedded in DOCX')
 check(not (src.parent/f'{fid}.dot').exists(),f'{fid} obsolete DOT master')
print(f'Chapter 11: {words}/3000 source words; V12 14 pages allocated')
if issues:
 print('FAIL:\n'+'\n'.join('- '+x for x in issues));sys.exit(1)
print('PASS: chapter scope, running case, epoch clarification, figure masters and DOCX fingerprints')
print('REMAINING: native Word print inspection and publication-level technical/editorial acceptance')
