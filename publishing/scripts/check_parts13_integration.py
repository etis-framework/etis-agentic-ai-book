#!/usr/bin/env python3
"""Chapters 1–17 integration regression checks; not primary-source certification.

Check controlled figure terminology, CAB-001 contract traceability, running
case and V12 invariants, and robust handling of macOS AppleDouble sidecars.
"""
from pathlib import Path
import hashlib, json, re, sys, zipfile, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2]
errors=[]
def need(ok,msg):
    if not ok: errors.append(msg)
def read(p):return (ROOT/p).read_text()
ch03=read('manuscript/part-01-foundations/ch03-enterprise-processes-goals-and-bounded-autonomy/index.md')
ch04=read('manuscript/part-01-foundations/ch04-what-an-agent-is-and-is-not/index.md')
ch08=read('manuscript/part-02-architecture/ch08-from-requirements-to-a-reference-architecture/index.md')
ch17=read('manuscript/part-03-patterns/ch17-choosing-deterministic-agentic-and-hybrid-designs/index.md')
front=read('manuscript/frontmatter/how-to-use-this-book.md')
cat=read('metadata/architecture-catalog.md')
need('not CASE-204 Designs A/B/C' in ch04,'Chapter 4 must disambiguate general patterns from case alternatives')
need('A logical responsibility does not require an AI model' in ch17,'Chapter 17 deterministic E3 interpretation missing')
for num,term in enumerate(['Admission','Work order','Context query','Action proposal','Decision','Durable intent','Provider dispatch','Reconciliation','Telemetry'],1):
    key=f'C{num:02d} {term}'
    need(key in ch08, f'Chapter 8 contract catalog missing {key}')
    need(f'C{num:02d}' in cat, f'CAB catalog summary missing C{num:02d}')
need('C01–C09' in front and 'Chapter 8' in front,'Front matter contract introduction incorrect')
need('CAB-001' in ch08 and 'not separately deployed services' in ch08,'CAB origin/deployment distinction missing')
need('CASE-204' in ch17 and 'RF-1042' in ch17 and '$500' in ch17,'Chapter 17 case identifiers missing')
need('Design B' in ch03 and 'Design C' in ch17,'Case alternative continuity missing')
F=ROOT/'assets/shared-figures/sources'
for name in ('F03-03','F04-02'):
    svg=ET.parse(F/(name+'.svg')).getroot()
    text=' '.join((n.text or '') for n in svg.iter() if n.tag.endswith('text'))
    if name=='F03-03':
        need('TRUSTED EXECUTION' in text,'Figure 3.3 execution box must not be another PERMIT decision')
        need(text.count('PERMIT')==1,'Figure 3.3 must have precisely one branch PERMIT')
    else:
        need(all(x in text for x in ('FIXED WORKFLOW','BOUNDED AGENT','HYBRID WORKFLOW')),'Figure 4.2 component headings missing')
        need(not re.search(r'\b[ABC]\s{1,2}(?:FIXED|BOUNDED|HYBRID)',text),'Figure 4.2 wrongly reuses A/B/C')
    need((F/(name+'.svg')).read_bytes()==(ROOT/'assets/shared-figures/rendered'/(name+'.svg')).read_bytes(),name+' SVG master/render mismatch')
    png=ROOT/'assets/shared-figures/rendered'/(name+'.png')
    need(png.is_file() and png.stat().st_size>10000,name+' rendered PNG missing')
need("not p.name.startswith('._')" in read('publishing/scripts/figures.py'),'Figure generator does not exclude AppleDouble sidecars')
ledger=json.loads(read('publishing/SINGLE_VOLUME_FINISHED_PAGE_LEDGER_V12.json'))
need((ledger['chapter_total_pages'],ledger['front_back_reserve_pages'],ledger['target_finished_pages'])==(485,65,550),'V12 locked budget changed')
source=read('references/source-register.md')
for n in range(1,18):
    need(bool(re.search(rf'(?i)(?:\bChapter\s+{n}\b|\bCh{n}\b)',source)),f'No source-register section for chapter {n}')
for claim in ('exact-page','not an external normative standard'):
    need(claim in source or claim in cat,'External and original-authorial sourcing boundary missing: '+claim)
doc=ROOT/'dist/etis-agentic-ai-book.docx'
if doc.is_file():
    with zipfile.ZipFile(doc) as z:
        media={hashlib.sha256(z.read(k)).hexdigest() for k in z.namelist() if k.startswith('word/media/')}
    for name in ('F03-03','F04-02'):
        png=ROOT/'assets/shared-figures/rendered'/(name+'.png')
        if png.exists():need(hashlib.sha256(png.read_bytes()).hexdigest() in media,name+' new PNG not embedded in Word')
else:errors.append('Integrated Word manuscript absent; run make book-docx')
print('Parts I–III integration checks: '+ ('PASS' if not errors else 'FAIL'))
for e in errors:print('FAIL:',e)
print('Manual gates remain: all print-size figures, native Word pagination, and exact claim-to-source verification')
sys.exit(bool(errors))
