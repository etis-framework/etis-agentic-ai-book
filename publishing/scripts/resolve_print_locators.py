#!/usr/bin/env python3
"""Populate PAGEREF cached displays from physically paginated PDF headings.

The Word fields stay live. This is a proof-stage operation, not a substitute
for a final native Word field-update and pagination inspection.
"""
import argparse,re,sys
from pathlib import Path
import fitz
from docx import Document
from docx.oxml.ns import qn

ap=argparse.ArgumentParser();ap.add_argument('docx');ap.add_argument('pdf');ap.add_argument('--strict',action='store_true');args=ap.parse_args()
doc=Document(args.docx); pdf=fitz.open(args.pdf)
parts=[]
for i,p in enumerate(pdf):
 txt=p.get_text('text',sort=False)
 lines=[x.strip() for x in txt.splitlines() if x.strip()]
 val=next((x for x in lines[:5] if re.fullmatch(r'[ivxlcdm]+|[0-9]{1,4}',x,re.I)),None)
 parts.append((txt,val,i))
first_main=next(i for i,(t,_,_) in enumerate(parts) if re.search(r'(?m)^Chapter 1\s*[—–-]',t) and i>8)

bookmarks={}
for p in doc.paragraphs:
 for b in p._p.xpath('.//w:bookmarkStart'):
  key=b.get(qn('w:name'))
  if key:bookmarks[key]=p.text.strip()

cache={};unresolved={}
def matcher(key,label):
 if key.startswith('s') and re.fullmatch(r's\d+_\d+(?:_\d+)?',key):
  number=key[1:].replace('_','.')
  return re.compile(r'(?m)^'+re.escape(number)+r'(?:\s+|\.\s+)(?!\d)')
 if re.fullmatch(r'c\d+',key):return re.compile(r'(?m)^Chapter '+key[1:]+r'\s*[—–-]')
 if key.startswith('part'):return re.compile(r'(?m)^Part '+key[4:]+r'\s*[—–-]')
 return re.compile(r'(?m)^'+re.escape(label)+r'\s*$')
for key,label in bookmarks.items():
 if key not in {'bm_contents','bm_preface','bm_introduction','bm_how_to_use_this_book','bm_appendices','bm_glossary','bm_references_and_bibliography','bm_index','bm_about_the_author'} and not (key.startswith('s') or re.fullmatch(r'c\d+',key) or key.startswith('part')):continue
 pattern=matcher(key,label)
 candidates=[(i,v) for i,(t,v,_) in enumerate(parts) if pattern.search(t) and (i>=first_main or key.startswith('bm_') or key.startswith('part'))]
 if candidates:
  # Part heads and chapter names can appear in text; select first actual heading.
  cache[key]=candidates[0][1]
 else:unresolved[key]=label[:80]

field_count=updated=0;miss=[]
for para in doc.paragraphs:
 for i,run in enumerate(para.runs):
  instruction=' '.join((x.text or '') for x in run._r.findall(qn('w:instrText')))
  m=re.search(r'\bPAGEREF\s+(\S+)',instruction)
  if not m:continue
  field_count+=1;key=m.group(1);value=cache.get(key)
  if not value:
   miss.append(key);continue
  for following in para.runs[i+1:]:
   if following.text=='—':
    following.text=str(value);updated+=1;break
   if following._r.findall(qn('w:fldChar')) and any(x.get(qn('w:fldCharType'))=='end' for x in following._r.findall(qn('w:fldChar'))):break
  else:miss.append(key)

if args.strict and miss:
 print('UNRESOLVED',len(set(miss)),sorted(set(miss))[:40]);sys.exit(1)
doc.save(args.docx)
print('LOCATOR CACHE:',updated,'of',field_count,'fields; mapped',len(cache),'bookmarks; missing',len(set(miss)), 'examples', sorted(set(miss))[:15])
