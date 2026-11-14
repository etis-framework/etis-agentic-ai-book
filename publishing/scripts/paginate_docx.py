#!/usr/bin/env python3
"""ETIS print-layout postprocessor: no extra section-break paragraphs.

The section break is attached to the preceding paragraph. This avoids the
empty page sometimes inserted between a chapter heading and its opening text.
Word for Mac remains the final authority for odd-page parity.
"""
from pathlib import Path
import sys,re
from docx import Document
from docx.shared import Inches,Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

path=Path(sys.argv[1]); doc=Document(path)
for name in ['Heading 1','Heading 2','Heading 3']:
 if name in doc.styles:
  fmt=doc.styles[name].paragraph_format
  fmt.page_break_before=False;fmt.keep_with_next=True

headings=[]
for para in doc.paragraphs:
 if para.style.name!='Heading 1':continue
 t=para.text.strip()
 if re.match(r'^(Chapter \d+|Part [IVX]+)\s*[—–-]',t):typ='main'
 elif t=='Contents':typ='contents'
 elif t in {'Half title','Title page','Copyright','Preface','Introduction','How to use this book','Appendices','Glossary','References and bibliography','Index','Working subject index','About the author'}:typ='other'
 else:continue
 headings.append((para,typ,t))
 para.paragraph_format.keep_with_next=True
 para.paragraph_format.page_break_before=False

# Publication back matter starts on deliberately controlled fresh pages.
# Do not rely on accidental paragraph flow. A nextPage section break below
# also preserves the section-specific header/footer and numbering design.
BACK_OPENINGS={'Appendices','Glossary','References and bibliography','Working subject index','Index','About the author'}
for para in doc.paragraphs:
 if para.style.name=='Heading 1' and para.text.strip() in BACK_OPENINGS:
  para.paragraph_format.page_break_before=True
  para.paragraph_format.keep_with_next=True

# Add a section break at the END of the preceding paragraph, not as a new paragraph.
# The break belongs to the preceding section; the new heading begins the next.
section_meta=[]
for para,typ,title in headings:
 if title=='Half title':continue
 prev=para._p.getprevious()
 while prev is not None and prev.tag!=qn('w:p'):prev=prev.getprevious()
 if prev is None:continue
 ppr=prev.find(qn('w:pPr'))
 if ppr is None:ppr=OxmlElement('w:pPr');prev.insert(0,ppr)
 old=ppr.find(qn('w:sectPr'))
 if old is not None:ppr.remove(old)
 sect=OxmlElement('w:sectPr')
 bt=OxmlElement('w:type');bt.set(qn('w:val'),'oddPage' if title.startswith('Chapter ') else 'nextPage');sect.append(bt)
 ppr.append(sect)
 section_meta.append((typ,title))

# Reparse so python-docx discovers the newly inserted sections.
doc.save(path);doc=Document(path)
for sec in doc.sections:
 sec.page_width=Inches(7);sec.page_height=Inches(10)
 sec.top_margin=Inches(.78);sec.bottom_margin=Inches(.78)
 sec.left_margin=Inches(.85);sec.right_margin=Inches(.7)
 sec.header_distance=Inches(.36);sec.footer_distance=Inches(.4)

# The initial half-title/title/copyright section has no visible folio.
# Start Roman numbering at Contents and Arabic numbering at Chapter 1.
def set_numbering(sec,fmt=None,start=None):
 sp=sec._sectPr
 pg=sp.find(qn('w:pgNumType'))
 if pg is None:pg=OxmlElement('w:pgNumType');sp.append(pg)
 if fmt:pg.set(qn('w:fmt'),fmt)
 if start is not None:pg.set(qn('w:start'),str(start))

def field(paragraph,instruction):
 r=paragraph.add_run(); b=OxmlElement('w:fldChar');b.set(qn('w:fldCharType'),'begin');r._r.append(b)
 r=paragraph.add_run(); x=OxmlElement('w:instrText');x.set(qn('xml:space'),'preserve');x.text=' '+instruction+' ';r._r.append(x)
 r=paragraph.add_run(); b=OxmlElement('w:fldChar');b.set(qn('w:fldCharType'),'separate');r._r.append(b)
 r=paragraph.add_run('1')
 r=paragraph.add_run(); b=OxmlElement('w:fldChar');b.set(qn('w:fldCharType'),'end');r._r.append(b)

def folio(sec):
 foot=sec.footer;foot.is_linked_to_previous=False
 p=foot.paragraphs[0];p.text='';p.alignment=2
 field(p,'PAGE')
 for r in p.runs:r.font.size=Pt(9)

# Section 0 is preliminaries before Contents; each section i+1 starts at the
# heading named by section_meta[i].
main_started=False
for i,sec in enumerate(doc.sections):
 if i==0:
  sec.footer.is_linked_to_previous=False;sec.footer.paragraphs[0].text=''
  continue
 if i-1>=len(section_meta):break
 typ,title=section_meta[i-1]
 if title=='Contents':set_numbering(sec,'lowerRoman',1)
 elif title.startswith('Chapter 1 '):set_numbering(sec,'decimal',1);main_started=True
 elif main_started:set_numbering(sec,'decimal')
 elif title!='Contents':set_numbering(sec,'lowerRoman')
 if title in {'Title page','Copyright'}:sec.footer.is_linked_to_previous=False;sec.footer.paragraphs[0].text=''
 else:folio(sec)
 # Set simple running heads; no header on chapter or part opening pages.
 sec.header.is_linked_to_previous=False
 h=sec.header.paragraphs[0];h.text=''
 if typ=='main':
  sec.different_first_page_header_footer=True
  h.text='ETIS  •  Engineering Trustworthy Agentic AI Systems'
  h.style='Normal'
  # First-page footer must carry the chapter-opening page number.
  fp=sec.first_page_footer;fp.is_linked_to_previous=False
  p=fp.paragraphs[0];p.text='';p.alignment=2;field(p,'PAGE')
 elif title not in {'Contents','Preface','Introduction','How to use this book'}:
  h.text='ETIS  •  Engineering Trustworthy Agentic AI Systems'

# Visible draft contents: unlike an unpopulated Word field, entries always show.
# Entries are inserted BEFORE the paragraph carrying the next-section break.
for p in doc.paragraphs:
 if '[[BOOK_TOC]]' not in p.text:continue
 entries=[('Preface',0),('Introduction',0),('How to use this book',0)]
 for heading in list(doc.paragraphs):
  if heading.style.name!='Heading 1':continue
  label=heading.text.strip()
  if label.startswith('Part ') or label.startswith('Chapter '):entries.append((label,0 if label.startswith('Part ') else 1))
 for label,level in entries[:-1]:
  q=p.insert_paragraph_before(label,style='Normal')
  q.paragraph_format.left_indent=Inches(.17 if level else 0)
  q.paragraph_format.space_after=Pt(1)
  for r in q.runs:
   r.font.size=Pt(8.4 if level else 9.5);r.bold=not bool(level)
 p.text=entries[-1][0]
 p.paragraph_format.left_indent=Inches(.17)
 p.paragraph_format.space_after=Pt(1)
 for r in p.runs:r.font.size=Pt(8.4)
 break
settings=doc.settings.element
for e in settings.findall(qn('w:updateFields')):settings.remove(e)
doc.save(path)
print(f'ETIS pagination: {len(doc.sections)} sections; Roman front matter; Arabic Chapter 1; draft Contents listing')
