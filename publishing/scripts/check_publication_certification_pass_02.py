#!/usr/bin/env python3
"""Print/editorial source checks for publication pass 02; not production certification."""
import json,re,sys
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
R=Path(__file__).resolve().parents[2];errors=[]
def req(ok,msg):
 if not ok:errors.append(msg)
front=R/'manuscript/frontmatter';back=R/'manuscript/backmatter'
a=(back/'about-the-author.md').read_text()
req(len(a.split())>=300,'Author narrative is shorter than 300 source words')
for term in ['IBM Distinguished Engineer','two Chief Technology Officer','Loyola University Chicago','Princeton University','University of Toronto','11 U.S. patents','AT&T Bell Laboratories','ETIS']:
 req(term in a,'Missing author credential: '+term)
copy=(front/'copyright.md').read_text()
req('Digital edition' not in copy and 'digital edition' not in copy and 'eBook ISBN' not in copy,'Digital edition wording remains')
req('ISBN: To be assigned' in copy,'Unassigned print ISBN must be explicit')
for name in ['half-title','series','title']:
 req((front/f'{name}.md').is_file(),f'Missing {name} source')
req('Build, Secure, Verify, and Operate Trustworthy AI Agents' in (front/'title.md').read_text(),'Subtitle drift')
reg=json.loads((R/'metadata/index-term-register.json').read_text())['entries']
req(len(reg)>=109,'Index register lost entries')
req([x['term'] for x in reg]==sorted((x['term'] for x in reg),key=str.casefold),'Index terms no longer sorted')
req('Chapters 1–36' in (R/'references/source-register.md').read_text()[:500],'Stale source register development status')
req((R/'publishing/scripts/resolve_print_locators.py').is_file(),'Missing print locator caching tool')
path=R/'dist/etis-agentic-ai-book.docx'
if path.exists():
 d=Document(path);paras=d.paragraphs
 req(len(d.sections)>=55,'Missing authored section boundaries')
 for i in range(3):req(abs(d.sections[i].page_width.inches-7)<.01 and abs(d.sections[i].page_height.inches-10)<.01,'Wrong 7x10 trim')
 req(any(p.text.strip()=='ENGINEERING AGENTIC\nAI SYSTEMS' for p in paras[:10]),'Two-line title absent')
 half=next((p for p in paras[:10] if p.text.strip()=='ENGINEERING AGENTIC\nAI SYSTEMS'),None)
 req(half is not None and any(r.font.size and r.font.size.pt>=24 for r in half.runs),'Half title under 24 pt')
 req(any(p.text=='ETIS PROFESSIONAL COMPUTING SERIES' for p in paras[:10]),'Series heading missing')
 req('ETIS FRAMEWORK' in d.sections[1].footer.paragraphs[0].text,'Series imprint missing from lower page')
 req('ETIS Framework' in d.sections[2].footer.paragraphs[0].text,'Title imprint missing from lower page')
 index=next((p for p in paras if p.text=='Index' and p.style.name=='Heading 1'),None)
 author=next((p for p in paras if p.text=='About the Author' and p.style.name=='Heading 1'),None)
 req(index is not None and author is not None,'Index or author heading missing')
 req(author is not None and author.paragraph_format.page_break_before,'About the Author must start on own page')
 refs=[x.text or '' for x in d.element.body.findall('.//'+qn('w:instrText'))]
 req(sum('PAGEREF ' in x for x in refs)>=250,'Contents/index live page reference loss')
else:errors.append('Build DOCX before checking')
print('Publication certification pass 02:', 'PASS' if not errors else 'FAIL',len(errors),'findings')
for e in errors:print('FAIL:',e)
sys.exit(bool(errors))
