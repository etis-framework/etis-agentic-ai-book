#!/usr/bin/env python3
"""Mechanical Chapter 9 checks. Visual, technical, and native Word sign-off remain human gates."""
from pathlib import Path
import hashlib, json, re, sys, zipfile, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2]
CH=ROOT/'manuscript/part-02-architecture/ch09-admission-identity-and-scoped-work-e1/index.md'
PART=ROOT/'manuscript/part-02-architecture/_part.md'
CH8=ROOT/'manuscript/part-02-architecture/ch08-from-requirements-to-a-reference-architecture/index.md'
LEDGER=ROOT/'publishing/SINGLE_VOLUME_FINISHED_PAGE_LEDGER_V12.json'
DOC=ROOT/'dist/etis-agentic-ai-book.docx'
issues=[]
def check(value,message):
    if not value:issues.append(message)
text=CH.read_text(encoding='utf-8');part=PART.read_text(encoding='utf-8');ch8=CH8.read_text(encoding='utf-8')
word_count=len(re.findall(r"\b[\w'-]+\b",text))
ledger=json.loads(LEDGER.read_text())
check(word_count <= 3000,f'Chapter 9 source word cap exceeded: {word_count}/3000')
check(int(ledger['chapter_pages']['9'])==13,'V12 Chapter 9 page allocation drifted from 13')
check(ledger['target_finished_pages']==550 and ledger['chapter_total_pages']==485 and ledger['front_back_reserve_pages']==65,'V12 whole-book allocation drift')
check('STATUS: PLANNED' not in text,'Chapter 9 still contains placeholder')
for needle in ('CASE-204','$500','RF-1042','Design A','Design B','Design C','DATA-01','AUTH-01','POL-02','PAY-03','OPS-01','E1','E2','E3','E4','E5','E6','E7'):
    check(needle in text,f'Missing Chapter 9 continuity/control identifier: {needle}')
for needle in ('case binding','workload identity','revocation','reconciliation','denial','read-only','trusted issuer','Chapter 10'):
    check(needle.lower() in text.lower(),f'Missing Chapter 9 technical treatment: {needle}')
check('Design B' in ch8 and 'Chapter 9' in ch8 and 'CASE-204' in part,'Chapter 8 or Part II narrative bridge missing')
# Terminology gate: domain codes are navigation aids, not prose substitutes.
for required in ('coordination and ownership responsibility (E2)', 'context and retrieval (E4)', 'agent reasoning (E3)', 'trusted execution (E5)', 'enterprise integration (E6)', 'durable operational state (E7)'):
    check(required in text, f'Chapter 9 fails named-domain readability: {required}')
for orphan in ('E4 retrieves', 'E3 returns', 'E5/E6/E7', 'E5/E6', 'Hand the admitted assignment to E2', 'E5 still determine', 'E1 reset'):
    check(orphan not in text, f'Unexplained bare domain reference: {orphan}')
check(ch8.count('**Architecture review verdict for the continuing case.**')==1,'Chapter 8 repeated architecture verdict')
check(text.count('![Figure 9.')==2,'Expected exactly two authored Figure 9 captions')
media_hashes=set()
if DOC.is_file():
    with zipfile.ZipFile(DOC) as z:
        media_hashes={hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/')}
else:issues.append('Integrated DOCX absent: run make book-docx')
for fid in ('F09-01','F09-02'):
    master=ROOT/f'assets/shared-figures/sources/{fid}.svg'
    rendered=ROOT/f'assets/shared-figures/rendered/{fid}.svg'
    png=ROOT/f'assets/shared-figures/rendered/{fid}.png'
    check(all(p.is_file() for p in (master,rendered,png)),f'{fid} missing source, SVG or PNG')
    if not all(p.is_file() for p in (master,rendered,png)):continue
    raw=master.read_bytes()
    try: xml=ET.fromstring(raw)
    except ET.ParseError as e: issues.append(f'{fid} invalid SVG: {e}');continue
    check(raw==rendered.read_bytes(),f'{fid} source and rendered SVG differ')
    check(xml.attrib.get('width')=='5.75in',f'{fid} not fixed to 5.75-inch print width')
    check(xml.attrib.get('viewBox','').startswith('0 0 1140 '),f'{fid} viewBox changed')
    check(len(xml.findall('{http://www.w3.org/2000/svg}rect'))>=5,f'{fid} lacking composed boxes')
    check(len(xml.findall('{http://www.w3.org/2000/svg}polyline'))>=3,f'{fid} lacking visible directional paths')
    for el in xml.findall('{http://www.w3.org/2000/svg}text'):
        fs=float(el.attrib.get('font-size','0'))
        check(fs>=18,f'{fid} small text: {el.text} at {fs} SVG units')
        check(el.attrib.get('font-family','').startswith('Arial'),f'{fid} inconsistent font')
    check(not (master.with_suffix('.dot')).exists(),f'{fid} obsolete DOT source conflicts with V9 SVG master')
    check(hashlib.sha256(png.read_bytes()).hexdigest() in media_hashes,f'{fid} current PNG not in built DOCX')
    check(png.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'),f'{fid} invalid PNG')
print(f'Chapter 9: {word_count}/3000 words; V12 allocation 13 finished pages')
if issues:
    print('CHAPTER 9 AUTOMATED QA FAILED:');print('\n'.join(f' - {x}' for x in issues));sys.exit(1)
print('PASS: narrative identifiers, V12, SVG master fidelity, composed figure structure, PNG/Word fingerprints')
print('MANDATORY MANUAL GATES: inspect printed figures and captions in native Word; technical six-lens review; actual rendered page count')
