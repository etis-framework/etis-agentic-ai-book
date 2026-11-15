#!/usr/bin/env python3
"""Certification-pass-01 structural checks (not final author/publisher proof)."""
import json,re,sys
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
R=Path(__file__).resolve().parents[2]
errors=[]
def expect(ok,why):
 if not ok:errors.append(why)
front=R/'manuscript/frontmatter'
back=R/'manuscript/backmatter'
text=(back/'about-the-author.md').read_text()
for name in ('William T. O’Connell','IBM Distinguished Engineer','Loyola University Chicago','Princeton University','University of Toronto','11 U.S. patents','ETIS'):
 expect(name in text,'Author biography missing '+name)
for f in ('half-title.md','series.md','title.md'):
 expect((front/f).exists(),'Missing opening '+f)
expect('etis professional computing series' in (front/'series.md').read_text().lower(),'Series identity missing')
expect('Build, Secure, Verify, and Operate Trustworthy AI Agents' in (front/'title.md').read_text(),'Subtitle mismatch')
reg=json.loads((R/'metadata/index-term-register.json').read_text())['entries']
expect(len(reg)>=100,'Index under 100 targeted entries')
expect([e['term'] for e in reg]==sorted([e['term'] for e in reg],key=str.casefold),'Unsorted index register')
expect(not any('perspective' in e['term'].lower() for e in reg),'Internal review lens leaked into index')
expect(all(f'Chapter {n}' not in (front/'title.md').read_text() for n in [35,36]),'Internal status leaked into title')
p=R/'dist/etis-agentic-ai-book.docx'
if p.exists():
 doc=Document(p)
 sz=doc.sections[0];expect(abs(sz.page_width.inches-7)<.02 and abs(sz.page_height.inches-10)<.02,'Not 7x10 trim')
 paras=[p.text.strip() for p in doc.paragraphs]
 expect(any(x.replace('\n',' ')=='ENGINEERING AGENTIC AI SYSTEMS' for x in paras),'Half title absent')
 expect('ETIS PROFESSIONAL COMPUTING SERIES' in paras,'Series page absent')
 expect('William T. O’Connell, Ph.D.' in paras,'Title byline absent')
 expect('About the Author' in paras,'About the Author heading absent')
 bookmarks={e.get(qn('w:name')) for e in doc.element.body.findall('.//'+qn('w:bookmarkStart'))}
 fields=[e.text or '' for e in doc.element.body.findall('.//'+qn('w:instrText'))]
 refs=[m.group(1) for f in fields for m in re.finditer(r'PAGEREF\s+(\S+)',f)]
 expect(len(refs)>=150,'Missing live contents/index fields')
 for target in refs:expect(target in bookmarks,'Broken print page reference: '+target)
 expect('bm_index' in bookmarks,'Index page bookmark missing')
 expect(not any('[[BOOK_TOC]]' in x for x in paras),'Unresolved contents token')
 chapters=[p.text.strip() for p in doc.paragraphs if p.style.name=='Heading 1' and re.match(r'^Chapter\s+\d+\s*[—–-]',p.text.strip())]
 expect(len(chapters)==36,'DOCX has '+str(len(chapters))+' chapter headings')
else:errors.append('Whole-volume DOCX missing: run make book-docx')
print('Publication certification pass 01:', 'PASS' if not errors else 'FAIL',f'({len(errors)} findings; {len(reg)} index terms)')
for e in errors:print('FAIL:',e)
sys.exit(bool(errors))
