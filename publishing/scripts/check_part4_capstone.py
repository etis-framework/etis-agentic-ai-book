#!/usr/bin/env python3
"""Guard Part IV educational composition claims and print controls."""
from pathlib import Path
import json,re,sys
from docx import Document
R=Path(__file__).resolve().parents[2];errors=[]
def chk(c,msg):
 if not c:errors.append(msg)
ch=next((R/'manuscript/part-04-implementation').glob('ch27-*/index.md')).read_text()
root=(R/'examples/refund-reference-system')
mp=(root/'IMPLEMENTATION_EVIDENCE_MAP.md').read_text()
chk('27.9 Part IV capstone' in ch and 'does not call Build 1' in ch,'Chapter capstone lacks composition truth')
chk(ch.index('## 27.9 Part IV capstone') < ch.index('## Chapter synthesis and transition to Part V'), 'Part IV capstone must precede final synthesis')
chk(ch.count('## Chapter synthesis')==1, 'Chapter 27 must have exactly one closing synthesis')
appendix=(R/'manuscript/backmatter/appendices.md').read_text()
chk('Proposed `operation_id` in C04' in appendix and 'advisory correlation reference' in appendix and 'two-way notation' in appendix, 'Consolidated C04 appendix explanation missing')
chk('**Contract direction.**' not in appendix and '**C04 field semantics.**' not in appendix, 'Repeated C04 appendix explanation remains')

chk(all(f'Build {i}' in mp for i in range(6)),'Missing build in map')
chk(all('E'+str(i) in mp for i in range(1,10)),'Missing domain in map')
chk(all('C0'+str(i) in mp for i in range(1,10)),'Missing contract in map')
chk(all(t in mp for t in ('Executed','fixture','specified only','not implemented','Compromised investigator','Lost provider','E5-side E2 epoch fencing')),'Missing assurance distinction')
chk('not** call Build 1' in (root/'build5/README.md').read_text(),'Build5 README composition claim omitted')
chk(all(f'build{i}/architecture.svg' in (root/'ARCHITECTURE.md').read_text() for i in range(6)),'Architecture diagram navigation incomplete')
for i in range(6):chk((root/f'build{i}/architecture.svg').exists(),f'Missing Build {i} SVG')
source=(R/'publishing/scripts/paginate_docx.py').read_text()
chk("'Index'" in source and 'page_break_before=True' in source,'Index heading page-break rule missing')
for label in ('Appendices','Glossary','References and bibliography','Index'):
 chk(label in source,f'Back-matter opening not governed: {label}')
# Check built artifact when it exists. The docx build is generated separately.
build_source=(R/'publishing/scripts/build.py').read_text()
chk("['Demonstration','Executed evidence','Not established']" in build_source and "w:tblHeader" in build_source and "w:cantSplit" in build_source, 'Capstone table pagination and header controls missing from builder')
doc=R/'dist/etis-agentic-ai-book.docx'
if doc.exists():
 d=Document(doc);matches=[p for p in d.paragraphs if p.text.strip()=='Index']
 chk(len(matches)==1,'Index heading count in built DOCX')
 if matches:chk(matches[0].paragraph_format.page_break_before is True,'Index not marked page-break-before in DOCX')
 tables=[t for t in d.tables if t.rows and [c.text.strip() for c in t.rows[0].cells]==['Demonstration','Executed evidence','Not established']]
 chk(len(tables)==1,'Expected exactly one capstone evidence table in DOCX')
 if len(tables)==1:
  from docx.oxml.ns import qn
  for i,row in enumerate(tables[0].rows):
   trPr=row._tr.get_or_add_trPr()
   chk(trPr.find(qn('w:cantSplit')) is not None,f'Capstone row {i} can split across pages')
   if i==0:chk(trPr.find(qn('w:tblHeader')) is not None,'Capstone header not repeated on continued pages')

print('Part IV capstone and print gate:', 'PASS' if not errors else 'FAIL')
for e in errors:print('FAIL:',e)
sys.exit(bool(errors))
