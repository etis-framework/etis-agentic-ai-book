#!/usr/bin/env python3
"""Chapter 21 structural, semantic, printable figure and integrated Word-identity gate."""
from pathlib import Path
import re, json, hashlib, zipfile, sys, xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2]
s=(R/'manuscript/part-03-patterns/ch21-architecture-decisions-and-governance-as-code/index.md').read_text()
errors=[]
def require(ok,message):
 if not ok: errors.append(message)
w=len(re.findall(r"\b[\w'-]+\b",s));require(w<=3000,f'Chapter 21 words {w}/3000')
ledger=json.loads((R/'publishing/SINGLE_VOLUME_FINISHED_PAGE_LEDGER_V12.json').read_text())
require(ledger['chapter_pages']['21']==12,'V12 Chapter 21 allocation modified')
require((ledger['chapter_total_pages'],ledger['front_back_reserve_pages'],ledger['target_finished_pages'])==(485,65,550),'V12 totals changed')
required=['ADR-021','POL-021','G21-01','G21-07','CASE-204','$500','Design A','Design B','Design C','conditional initial production candidate','read-only','RF-1042','UNKNOWN','E1','E2','E3','E4','E5','E6','E7','E8','E9','C01–C09','C04','C05','C06','C07','C08','C09','policy digest','Chapter 13','Chapter 19','Chapter 20','Chapter 31','Figure 21.1','Figure 21.2','Kleppmann','NIST AI RMF']
for term in required:require(term.lower() in s.lower(),f'Missing {term}')
# Reader comprehension regression: on first substantive use Chapter 21 must name
# the approved E responsibilities and every C contract, including C02.
imported_domains = [
 'E1 admission and identity', 'E2 coordination and ownership',
 'E3 agent reasoning', 'E4 context and retrieval', 'E5 trusted execution',
 'E6 enterprise integration', 'E7 durable operational state',
 'E8 business truth', 'E9 assurance and operations']
imported_contracts = [
 'C01 Admission', 'C02 Work order', 'C03 Context query',
 'C04 Action proposal', 'C05 Decision', 'C06 Durable intent',
 'C07 Provider dispatch', 'C08 Reconciliation', 'C09 Telemetry']
for entry in imported_domains + imported_contracts:
 require(entry.lower() in s.lower(), f'Unexplained architecture identifier: {entry}')
require(s.index('E1 admission and identity') < s.index('## 21.2'),
        'E-domain names must appear in the opening section')
require(s.index('C01 Admission') > s.index('## 21.4'),
        'Contract map must be introduced at first operational use in section 21.4')
for bad in ['model authorizes refund','memory authorizes refund','timeout means failed','policy engine alone authorizes']:
 require(bad not in s.lower(),f'Misleading: {bad}')
base=R/'assets/shared-figures'
for stem in ['F21-01','F21-02']:
 src=base/'sources'/f'{stem}.svg';svg=base/'rendered'/f'{stem}.svg';png=base/'rendered'/f'{stem}.png'
 require(all(p.is_file() for p in [src,svg,png]),f'{stem} missing source/render')
 if not all(p.is_file() for p in [src,svg,png]):continue
 require(src.read_bytes()==svg.read_bytes(),f'{stem} stale SVG')
 try:
  root=ET.parse(src).getroot(); t=[n for n in root.iter() if n.tag.endswith('text')]
  require(root.get('width')=='5.75in' and root.get('viewBox')=='0 0 1140 840',f'{stem} wrong print geometry')
  require(len(t)>=15 and all(float(n.get('font-size',0))>=21 for n in t),f'{stem} label sizing')
  require(all(n.get('font-family','').startswith('Arial') for n in t),f'{stem} nonstandard font')
 except Exception as e:errors.append(f'{stem} svg parse: {e}')
 require(png.stat().st_size>15000,f'{stem} render unexpectedly small')
book=R/'dist/etis-agentic-ai-book.docx'
require(book.is_file(),'Full-book DOCX missing')
if book.is_file():
 with zipfile.ZipFile(book) as z:
  media={hashlib.sha256(z.read(p)).hexdigest() for p in z.namelist() if p.startswith('word/media/')}
 for stem in ['F21-01','F21-02']:
  p=base/'rendered'/f'{stem}.png'
  if p.is_file():require(hashlib.sha256(p.read_bytes()).hexdigest() in media,f'{stem} not current in Word')
require('Selected research, standards and professional sources' in (R/'manuscript/backmatter/bibliography.md').read_text(),'Bibliography coverage old')
require('## Chapter 21 — architecture decisions' in (R/'references/source-register.md').read_text(),'Chapter 21 source map absent')
require('## Chapter 21 verified continuity extension' in (R/'metadata/topic-traceability.md').read_text(),'Chapter 21 trace absent')
print(f'Chapter 21: {w}/3000 words; allocation 12 pages; {len(errors)} issue(s)')
for e in errors:print('FAIL:',e)
if errors:sys.exit(1)
print('PASS: chapter, ref-arch continuity, figure source/render, current Word figure identity, sources and V12')
print('OPEN: Mac Word 7x10 page measurement, printed visual acceptance, exact source-page audit, independent editorial certification')
