#!/usr/bin/env python3
"""Chapter 20 evidence gate: architecture, original figure print geometry, whole-book embedding, citations, V12."""
from pathlib import Path
import sys,re,json,hashlib,zipfile,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2]
s=(R/'manuscript/part-03-patterns/ch20-state-memory-and-knowledge-design/index.md').read_text()
errors=[]
def need(cond,why):
 if not cond: errors.append(why)
words=len(re.findall(r"\b[\w'-]+\b",s))
need(words<=3000, f'word budget {words}/3000 exceeded')
ledger=json.loads((R/'publishing/SINGLE_VOLUME_FINISHED_PAGE_LEDGER_V12.json').read_text())
need(ledger['chapter_pages']['20']==13,'Chapter 20 allocation must be 13')
need((ledger['chapter_total_pages'],ledger['front_back_reserve_pages'],ledger['target_finished_pages'])==(485,65,550),'V12 baseline modified')
for x in ['CASE-204','$500','Design A','Design B','Design C','conditional initial production candidate','read-only','RF-1042','RF-1043','UNKNOWN','C01–C09','E1','E2','E3','E4','E5','E6','E7','E8','E9','Chapter 12','Chapter 15','Chapter 19','Figure 20.1','Figure 20.2','tenant','provenance','invalidation','correction','revocation','reconciliation','negative tests','Lewis et al.','Kleppmann','NIST']:
 need(x.casefold() in s.casefold(),'Missing key marker: '+x)
for bad in ['memory authorizes','cache authorizes','agent issues refund']:
 need(bad not in s.casefold(), 'Forbidden misleading claim: '+bad)
need('original ETIS' in s and 'not a guarantee' in s, 'Original synthesis / source limitation missing')
for name in ['F20-01','F20-02']:
 base=R/'assets/shared-figures';src=base/'sources'/f'{name}.svg';svg=base/'rendered'/f'{name}.svg';png=base/'rendered'/f'{name}.png'
 need(all(p.is_file() for p in [src,svg,png]),f'{name} files absent')
 if not all(p.is_file() for p in [src,svg,png]):continue
 need(src.read_bytes()==svg.read_bytes(),f'{name} SVG source/render mismatch')
 try:
  root=ET.parse(src).getroot();texts=[n for n in root.iter() if n.tag.endswith('text')]
  need(root.get('width')=='5.75in' and root.get('viewBox','').startswith('0 0 1140 '),f'{name} print width geometry')
  need(len(texts)>=15 and min(float(n.get('font-size','0')) for n in texts)>=21,f'{name} label sizing')
  need(all(n.get('font-family','').startswith('Arial') for n in texts),f'{name} font standard')
 except Exception as e:errors.append(f'{name} invalid SVG: {e}')
 need(png.stat().st_size>15000,f'{name} PNG render too small')
book=R/'dist/etis-agentic-ai-book.docx'
need(book.is_file(), 'full book Word file absent')
if book.is_file():
 with zipfile.ZipFile(book) as z:
  media={hashlib.sha256(z.read(x)).hexdigest() for x in z.namelist() if x.startswith('word/media/')}
 for name in ['F20-01','F20-02']:
  png=R/'assets/shared-figures/rendered'/f'{name}.png'
  if png.is_file():need(hashlib.sha256(png.read_bytes()).hexdigest() in media,f'{name} current PNG not embedded in complete Word book')
register=(R/'references/source-register.md').read_text();bib=(R/'manuscript/backmatter/bibliography.md').read_text();trace=(R/'metadata/topic-traceability.md').read_text()
need('## Chapter 20 — state, memory' in register,'Chapter 20 source-register mapping missing')
need('Chapters 1–20' in bib,'Bibliography coverage stale')
need('Chapter 20 verified continuity extension' in trace,'Cumulative traceability missing')
need('Pinned credential compromise obligation' in trace,'Chapter 29/31 pinned future test lost')
print(f'Chapter 20: {words}/3000 source words, V12 allocation 13 finished pages, {len(errors)} errors')
for e in errors:print('FAIL:',e)
if errors:sys.exit(1)
print('PASS: structure, current full-book figure embeddings, claim/source registers, continuity and V12 allocation')
print('OPEN: native Word 7x10 page count, actual-size visual review, complete six-lens editorial acceptance, exact source-page audit')
