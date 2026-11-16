#!/usr/bin/env python3
"""Pass 5 glossary/typesetting and production-language structural gate.

Does not certify final native-Word pagination or visual printing.
"""
from pathlib import Path
from docx import Document
import re,sys
R=Path(__file__).resolve().parents[2]
source=(R/'manuscript/backmatter/glossary.md').read_text()
terms=re.findall(r'(?m)^\*\*([^\n]+?)\.\*\*\s',source)
errors=[]
def need(condition,message):
 if not condition:errors.append(message)
need(len(terms)>=60,'source glossary unexpectedly short')
need(len(re.findall(r'(?m)^\*\*[^\n]+?\.\*\*\s',source))==len(re.findall(r'(?m)^\n\*\*[^\n]+?\.\*\*\s',source)), 'glossary terms lack independent Markdown paragraphs')
need(terms==sorted(terms,key=str.casefold),'glossary source not alphabetical')
for rel in ['manuscript/frontmatter/introduction.md','manuscript/part-01-foundations/ch01-enterprise-agentic-ai/index.md','manuscript/part-01-foundations/ch02-historical-foundations/index.md']:
 t=(R/rel).read_text().lower()
 for bad in ['consult the pinned edition before publication','references still requiring editorial verification','will be publicly accessible with publication']:
  need(bad not in t,f'production-status language in {rel}: {bad}')
p=R/'dist/etis-agentic-ai-book.docx'
if not p.exists():errors.append('DOCX absent; run make book-docx')
else:
 d=Document(p);inside=False;entries=[]
 for para in d.paragraphs:
  if para.text.strip()=='Glossary' and para.style.name=='Heading 1':inside=True;continue
  if inside and para.style.name=='Heading 1':break
  if inside and para.runs and para.runs[0].bold:entries.append(para)
 need(len(entries)==len(terms),f'Word glossary entries {len(entries)} differ from Markdown {len(terms)}')
 need(max((len(p.text) for p in entries),default=0)<700,'glossary contains collapsed long paragraph')
 need(all(p.paragraph_format.keep_together for p in entries),'glossary entries not kept together')
print('PASS 5 glossary typesetting:', 'PASS' if not errors else 'FAIL',f'{len(terms)} source entries',len(errors),'findings')
for e in errors:print('FAIL:',e)
sys.exit(bool(errors))
