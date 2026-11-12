#!/usr/bin/env python3
"""Chapter 13 deterministic acceptance checks; native Word and technical signoff remain manual."""
from pathlib import Path
import hashlib,json,re,sys,zipfile,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[2]
p=root/'manuscript/part-02-architecture/ch13-trusted-execution-and-authority-e5/index.md'
s=p.read_text();errors=[]
def check(ok,msg):
 if not ok:errors.append(msg)
words=len(re.findall(r"\b[\w'-]+\b",s))
ledger=json.loads((root/'publishing/SINGLE_VOLUME_FINISHED_PAGE_LEDGER_V12.json').read_text())
check(words<=3000,f'Chapter 13 exceeds 3000-word cap: {words}')
check(ledger['chapter_pages']['13']==15,'V12 Chapter 13 allocation changed')
check((ledger['chapter_total_pages'],ledger['front_back_reserve_pages'],ledger['target_finished_pages'])==(485,65,550),'V12 totals drift')
check('STATUS: PLANNED' not in s,'Chapter 13 still stub')
required=['CASE-204','$500','RF-1042','Design A','Design B','Design C','read-only investigation',
 'trusted execution','independent','authorization','approval','policy enforcement point','policy decision point',
 'idempotency key','time-of-check to time-of-use (TOCTOU)','durable intent','UNKNOWN','reconciliation',
 'lease','ownership epoch','fencing','transactional outbox','Chapter 14','E1','E2','E3','E4','E5','E6','E8','E9']
for t in required:check(t.lower() in s.lower(),f'Missing essential concept: {t}')
for bad in ['model authorizes the refund','RF-1043','Design C executes','timeout means failed','E3 approves payment']:
 check(bad.lower() not in s.lower(),f'Potential unsafe wording: {bad}')
# Credential custody and bypass controls are first-class Chapter 13 acceptance requirements.
for concept in ['**credential**','**access token**','**secret**','**private key**','**capability**','**policy enforcement point**',
                'direct network routes','wrong-audience','revoked credential','provider-credential exposure',
                'rotation','reconcile','protected credential']:
 check(concept.lower() in s.lower(),f'Missing credential/bypass control: {concept}')
check(s.index('### Credentials, capabilities, and protected doors') < s.index('## 13.3'), 'Credential introduction too late')
check(s.count('![Figure 13.')==3,'Expected exactly three Chapter 13 figures')
for t in ['**effect**','**consequential operation**','**Authentication**','**Authorization**','**Approval**','**Time-of-check to time-of-use (TOCTOU)**','**idempotency key**','**durable intent**','**Reconciliation**']:
 check(t.lower() in s.lower(),f'Missing first-use definition {t}')
doc=root/'dist/etis-agentic-ai-book.docx';media=set()
if doc.is_file():
 with zipfile.ZipFile(doc) as z: media={hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/')}
else:errors.append('DOCX missing; run make book-docx')
ns='{http://www.w3.org/2000/svg}'
for i in range(1,4):
 fid=f'F13-{i:02d}';src=root/f'assets/shared-figures/sources/{fid}.svg';svg=root/f'assets/shared-figures/rendered/{fid}.svg';png=root/f'assets/shared-figures/rendered/{fid}.png'
 if not all(x.is_file() for x in (src,svg,png)):
  errors.append(f'Missing figure files {fid}');continue
 check(src.read_bytes()==svg.read_bytes(),f'{fid} rendered SVG differs from master')
 if fid=='F13-01':
  for label in ['PROTECTED CREDENTIAL USE','DIRECT BYPASS','BLOCKED','PROVIDER VIA E6 ADAPTER']:
   check(label in src.read_text(),f'{fid} omits security boundary label: {label}')
 try: el=ET.fromstring(src.read_bytes())
 except ET.ParseError as ex:errors.append(f'{fid} invalid SVG {ex}');continue
 check(el.attrib.get('width')=='5.75in',f'{fid} wrong print width')
 check(el.attrib.get('viewBox','').startswith('0 0 1140 '),f'{fid} wrong viewBox')
 texts=[t for t in el.iter() if t.tag==ns+'text']
 check(all(float(t.attrib.get('font-size',0))>=19 for t in texts),f'{fid} labels <19px')
 check(all(t.attrib.get('font-family','').startswith('Arial') for t in texts),f'{fid} nonstandard label font')
 check(len([e for e in el.iter() if e.tag==ns+'rect'])>=4,f'{fid} weak diagram geometry')
 check(len([e for e in el.iter() if e.tag in (ns+'polyline',ns+'line')])>=2,f'{fid} missing connectors')
 check(hashlib.sha256(png.read_bytes()).hexdigest() in media,f'{fid} PNG not embedded in DOCX')
print(f'Chapter 13: {words}/3000 words; allocation 15 finished pages')
if errors:
 print('FAIL:\n'+'\n'.join('- '+x for x in errors));sys.exit(1)
print('PASS: case, semantics, V12, V9 source/render, embedded DOCX image fingerprints')
print('REMAINING: native Word Mac inspection and actual whole-book final pagination')
