#!/usr/bin/env python3
"""Create a print navigation layer with Word PAGEREF fields (not invented page numbers).

Fields are recalculated by Word/LibreOffice after pagination. The exact final
edition still needs native Word-for-Mac field refresh and visual inspection.
"""
from pathlib import Path
import json,re,sys
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

path=Path(sys.argv[1]);root=Path(__file__).resolve().parents[2]
doc=Document(path)

def mark(para,name,idx):
    begin=OxmlElement('w:bookmarkStart');begin.set(qn('w:id'),str(idx));begin.set(qn('w:name'),name)
    end=OxmlElement('w:bookmarkEnd');end.set(qn('w:id'),str(idx))
    para._p.insert(1,begin);para._p.append(end)

def ref(para,name):
    r=para.add_run();x=OxmlElement('w:fldChar');x.set(qn('w:fldCharType'),'begin');r._r.append(x)
    r=para.add_run();x=OxmlElement('w:instrText');x.set(qn('xml:space'),'preserve');x.text=' PAGEREF '+name+' \\h ';r._r.append(x)
    r=para.add_run();x=OxmlElement('w:fldChar');x.set(qn('w:fldCharType'),'separate');r._r.append(x)
    para.add_run('—')   # visible uncalculated page, never an invented locator
    r=para.add_run();x=OxmlElement('w:fldChar');x.set(qn('w:fldCharType'),'end');r._r.append(x)

names={};positions={};seq=1
for p in doc.paragraphs:
    if p.style.name not in {'Heading 1','Heading 2','Heading 3'}:continue
    t=p.text.strip()
    key=None
    cm=re.match(r'^Chapter\s+(\d+)\s*[—–-]',t)
    pm=re.match(r'^Part\s+([IVX]+)\s*[—–-]',t)
    sm=re.match(r'^(\d{1,2}\.\d{1,2}(?:\.\d+)?)(?:\s|\.|$)',t)
    if cm:key='c'+cm.group(1)
    elif pm:key='part'+pm.group(1)
    elif sm:key='s'+sm.group(1).replace('.','_')
    elif t in {'Preface','Introduction','How to use this book','Appendices','Glossary','References and bibliography','Index','Working subject index','About the Author','About the author'}:
        key='bm_index' if t=='Working subject index' else 'bm_'+re.sub('[^a-z]','_',t.lower())
    if key and key not in names:
        names[key]=p;positions[key]=seq;mark(p,key,seq);seq+=1

# Contents: reuse the deliberately reserved paragraphs while preserving the
# trailing section-break paragraph. No static page numbers are committed.
paras=list(doc.paragraphs)
start=next((i for i,p in enumerate(paras) if p.text.strip()=='Contents' and p.style.name=='Heading 1'),None)
end=next((i for i,p in enumerate(paras[start+1:],start+1) if p.text.strip()=='Preface' and p.style.name=='Heading 1'),None) if start is not None else None
if start is None or end is None:raise SystemExit('Cannot locate reserved Contents block')
reserved=paras[start+1:end]
if not reserved:raise SystemExit('Contents has no reserved rows')
items=[]
for p in doc.paragraphs:
    t=p.text.strip();key=None;level=0
    if p.style.name!='Heading 1':continue
    if re.match(r'^Part\s+[IVX]+\s*[—–-]',t):key='part'+re.match(r'^Part\s+([IVX]+)',t).group(1)
    elif re.match(r'^Chapter\s+\d+\s*[—–-]',t):key='c'+re.match(r'^Chapter\s+(\d+)',t).group(1);level=1
    elif t in {'Preface','Introduction','How to use this book','Appendices','Glossary','References and bibliography','Index','About the author','About the Author'}:key='bm_index' if t=='Working subject index' else 'bm_'+re.sub('[^a-z]','_',t.lower())
    if key and key in names:items.append((t,key,level))
# Expand the pre-existing list into all front/back matter, parts, and chapters.
while len(reserved)<len(items):
    reserved.insert(-1,reserved[-1].insert_paragraph_before('',style='Normal'))
while len(reserved)>len(items):
    extra=reserved.pop(0)
    # Keep a section-break paragraph intact.
    if not extra._p.xpath('./w:pPr/w:sectPr'):extra._element.getparent().remove(extra._element)
    else:raise SystemExit('Unexpected section break in Contents list')
for p,(label,key,level) in zip(reserved,items):
    p.text=''
    p.style='Normal';p.paragraph_format.left_indent=Inches(.16 if level else 0)
    p.paragraph_format.space_after=Pt(1 if level else 3)
    p.paragraph_format.tab_stops.add_tab_stop(Inches(5.1),WD_TAB_ALIGNMENT.RIGHT,WD_TAB_LEADER.DOTS)
    run=p.add_run(label);run.bold=(level==0);run.font.size=Pt(9.0 if level else 10.0)
    p.add_run('\t');ref(p,key)

# Index terms: each selected chapter/section page is a live PAGEREF bookmark,
# not a guessed or frozen number. Preserve headings and proper See also entries.
register=json.loads((root/'metadata/index-term-register.json').read_text())
terms=register['entries']
ix=next((p for p in doc.paragraphs if p.style.name=='Heading 1' and p.text.strip() in {'Index','Working subject index'}),None)
about=next((p for p in doc.paragraphs if p.style.name=='Heading 1' and p.text.strip().lower()=='about the author'),None)
if not ix or not about:raise SystemExit('Index/author headings missing')
if ix.text.strip()!='Index':ix.text='Index'
prev=[];node=ix._p.getnext()
while node is not None and node is not about._p:
    nxt=node.getnext()
    if node.tag==qn('w:p'):
        from docx.text.paragraph import Paragraph
        prev.append(Paragraph(node,ix._parent))
    node=nxt
# Preserve the last paragraph, which may carry the next section break.
if not prev:raise SystemExit('Index has no text rows')
# Build one row for each term, ordered case-insensitively.
while len(prev)<len(terms):prev.insert(-1,prev[-1].insert_paragraph_before(''))
while len(prev)>len(terms):
    p=prev.pop(0)
    if p._p.xpath('./w:pPr/w:sectPr'):raise SystemExit('Unexpected section break in Index')
    p._element.getparent().remove(p._element)
for p,e in zip(prev,sorted(terms,key=lambda e:e['term'].casefold())):
    p.text='';p.style='Normal'
    ppr=p._p.get_or_add_pPr();num=ppr.find(qn('w:numPr'))
    if num is not None:ppr.remove(num)
    p.paragraph_format.left_indent=Inches(.14)
    p.paragraph_format.first_line_indent=Inches(-.14)
    p.paragraph_format.space_after=Pt(2)
    run=p.add_run(e['term']);run.bold=True;run.font.size=Pt(9.0)
    locator=e.get('locator','')
    # Specific section references have priority over chapter-level fallbacks.
    sections=[]
    for m in re.finditer(r'\b(\d{1,2}\.\d{1,2})(?:[–-](\d{1,2}\.\d{1,2}))?',locator):
        for s in [m.group(1),m.group(2)]:
            if s and 's'+s.replace('.','_') in names and s not in sections:sections.append(s)
    anchors=['s'+s.replace('.','_') for s in sections[:4]]
    if not anchors:
        chapters=[]
        for m in re.finditer(r'\bChapter(?:s)?\s+(\d{1,2})(?:[–-](\d{1,2}))?',locator):
            start_n=int(m.group(1));end_n=int(m.group(2)) if m.group(2) else start_n
            for n in ([start_n,end_n] if end_n-start_n>5 else range(start_n,end_n+1)):
                if n not in chapters:chapters.append(n)
        anchors=['c'+str(n) for n in chapters[:5] if 'c'+str(n) in names]
    if anchors:
        anchors=sorted(set(anchors),key=lambda k:positions[k])
        p.add_run('  ')
        for i,k in enumerate(anchors):
            if i:p.add_run(', ')
            ref(p,k)
    else:p.add_run('  [reference requires review]')
    also=e.get('see_also',[])
    if also:p.add_run('; see also '+', '.join(also[:2]))

# Instruct MS Word to update live references when opened.
settings=doc.settings.element
for old in settings.findall(qn('w:updateFields')):settings.remove(old)
update=OxmlElement('w:updateFields');update.set(qn('w:val'),'true');settings.append(update)
doc.save(path)
print(f'Final navigation: {len(items)} Contents entries, {len(terms)} index entries, {len(names)} page bookmarks; live PAGEREF fields')
