#!/usr/bin/env python3
"""Chapter 10 mechanical acceptance. Printed Word inspection remains a separate gate."""
from pathlib import Path
import re,sys,json,hashlib,zipfile,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[2]
p=root/'manuscript/part-02-architecture/ch10-coordination-registry-and-ownership-e2/index.md'
c9=root/'manuscript/part-02-architecture/ch09-admission-identity-and-scoped-work-e1/index.md'
c8=root/'manuscript/part-02-architecture/ch08-from-requirements-to-a-reference-architecture/index.md'
ledger=json.loads((root/'publishing/SINGLE_VOLUME_FINISHED_PAGE_LEDGER_V12.json').read_text())
text=p.read_text(); t9=c9.read_text();t8=c8.read_text();issues=[]
def chk(condition,desc):
 if not condition:issues.append(desc)
words=len(re.findall(r"\b[\w'-]+\b",text))
chk(words<=3000,f'Chapter 10 exceeds 3,000 words ({words})')
chk(int(ledger['chapter_pages']['10'])==14,'Chapter 10 V12 allocation must be 14')
chk(ledger['target_finished_pages']==550 and ledger['chapter_total_pages']==485 and ledger['front_back_reserve_pages']==65,'V12 totals changed')
chk('STATUS: PLANNED' not in text,'Chapter 10 placeholder remains')
chk('Admission and identity (E1) is therefore the start of an enforcement chain' in t9,'Chapter 9 §9.3 deferred edit missing')
chk('The admission and identity responsibility does not need to solve all of those mechanisms' in t9,'Chapter 9 §9.6 deferred edit missing')
chk(t8.count('**Architecture review verdict for the continuing case.**')==1,'Chapter 8 review verdict repeated')
for token in ('CASE-204','$500','RF-1042','Design A','Design B','Design C','epoch','lease','fencing','registry','revocation','reconciliation','Chapter 11'):
 chk(token.lower() in text.lower(),f'Missing narrative invariant {token}')
for responsibility in ('admission and identity (E1)','coordination and ownership (E2)','agent reasoning (E3)','context and retrieval (E4)','trusted execution (E5)','enterprise integration (E6)','durable operational state (E7)'):
 chk(responsibility.lower() in text.lower(),f'No named responsibility {responsibility}')
for anti in ('E4 retrieves','E5/E6/E7 reconcile','E3 returns','E2 grants payment','create `RF-1043` as a retry'):
 chk(anti not in text,f'Unexplained/shadow authority phrase: {anti}')
chk(text.count('![Figure 10.')==3,'Expected 3 teaching diagrams')
doc=root/'dist/etis-agentic-ai-book.docx'; media=set()
if doc.is_file():
 with zipfile.ZipFile(doc) as z:media={hashlib.sha256(z.read(name)).hexdigest() for name in z.namelist() if name.startswith('word/media/')}
else:issues.append('Built DOCX absent; run make book-docx')
for fid in ('F10-01','F10-02','F10-03'):
 a=root/f'assets/shared-figures/sources/{fid}.svg';b=root/f'assets/shared-figures/rendered/{fid}.svg';c=root/f'assets/shared-figures/rendered/{fid}.png'
 chk(all(x.is_file() for x in (a,b,c)),f'{fid}: missing SVG master/rendered SVG/PNG')
 if not all(x.is_file() for x in (a,b,c)):continue
 raw=a.read_bytes()
 try:svg=ET.fromstring(raw)
 except ET.ParseError as e:issues.append(f'{fid} invalid SVG {e}');continue
 chk(raw==b.read_bytes(),f'{fid} source SVG drift')
 chk(svg.attrib.get('width')=='5.75in',f'{fid} wrong print width')
 chk(svg.attrib.get('viewBox','').startswith('0 0 1140 '),f'{fid} wrong viewBox')
 elems=list(svg.iter())
 ns='{http://www.w3.org/2000/svg}'
 chk(len([el for el in elems if el.tag==ns+'rect'])>=6,f'{fid} insufficient composed boxes')
 chk(len([el for el in elems if el.tag==ns+'polyline'])>=4,f'{fid} insufficient visible transitions')
 for el in elems:
  if el.tag==ns+'text':
   fs=float(el.attrib.get('font-size','0'));chk(fs>=20,f'{fid} small figure text {el.text!r}: {fs}')
   chk(el.attrib.get('font-family','').startswith('Arial'),f'{fid} inconsistent figure font')
 chk(hashlib.sha256(c.read_bytes()).hexdigest() in media,f'{fid} PNG not embedded in book DOCX')
 chk(not (root/f'assets/shared-figures/sources/{fid}.dot').exists(),f'{fid} obsolete DOT master')
print(f'Chapter 10: {words}/3000 words; V12 allocated maximum 14 rendered chapter pages')
if issues:
 print('FAILED:');print('\n'.join('- '+x for x in issues));sys.exit(1)
print('PASS: domain prose, CASE-204 continuity, deferred Chapter 9 updates, V9 SVG/PNG/Word fingerprints, V12 controls')
print('MANDATORY MANUAL: actual print pages, figures/captions, technical six-lens review, native Word on Mac')
