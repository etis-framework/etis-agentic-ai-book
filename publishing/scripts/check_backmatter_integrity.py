#!/usr/bin/env python3
"""Dynamic developed-chapter back-matter preflight (not a semantic/source/page-proof certification)."""
import json,re,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2]; errors=[]
def need(ok,why):
 if not ok:errors.append(why)
def read(path):return (R/path).read_text()
chapters={int(re.search(r'ch(\d+)-',str(p)).group(1)) for p in (R/'manuscript').glob('part-*/ch*/index.md') if 'STATUS: PLANNED / NOT DRAFTED' not in p.read_text()}
app=read('manuscript/backmatter/appendices.md');gloss=read('manuscript/backmatter/glossary.md');idx=read('manuscript/backmatter/index.md');bib=read('manuscript/backmatter/bibliography.md');ch8=next((R/'manuscript/part-02-architecture').glob('ch08-*/index.md')).read_text();src=read('references/source-register.md')
need(chapters and min(chapters)==1 and sorted(chapters)==list(range(1,max(chapters)+1)),'Developed chapter sequence is not contiguous')
need('Selected research, standards and professional sources' in bib and not re.search(r'curated bibliography for the developed Chapters 1[–-]\d+',bib),'Bibliography needs evergreen reader-facing introduction')
for n in range(1,10): need(len(re.findall(r'^\| C0'+str(n)+r'\b',app,re.M))==1,f'C0{n} appendix row count');need(f'**C0{n}' in ch8 or f'| **C0{n}' in ch8,f'C0{n} Chapter 8 catalog')
need('↔' not in app and '↔' not in ch8,'Bidirectional glyph may render as emoji in contract tables')
for n in range(0,6):
 if 22+n in chapters: need(f'Build {n} —' in app and f'**Build {n} ' in idx,f'Build {n} missing appendix/index locator')
need('E2 coordinates work while E7 persists' in app and 'E5 does *not* independently enforce' in app,'E2/E7/E5 distinction missing')
need(all(f'## Appendix {letter} —' in app for letter in 'ABC'),'Appendix A/B/C structure missing')
need('still planned' not in app.lower(),'Development status must not appear in published appendix')
terms=[m.group(1) for m in re.finditer(r'^\*\*(.+?)\.\*\*',gloss,re.M)]
need(len(terms)>=35,'Glossary lacks developed-chapter scope')
need(terms==sorted(terms,key=str.casefold),'Glossary terms are not alphabetized')
need('Additional terms will' not in gloss,'Reader-facing glossary contains editing placeholder')
data=json.loads(read('metadata/index-term-register.json'));entries=data['entries'];names=[e['term'] for e in entries]
need(names==sorted(names,key=str.casefold),'Index register is not alphabetical')
need(any(e['aliases'] for e in entries),'Index aliases register must be maintained')
need(len(names)>=25 and len(names)==len(set(names)),'Index register is incomplete or duplicate')
need(len(re.findall(r'^\- \*\*',idx,re.M))==len(entries),'Index markdown/register count drift')
for e in entries:need(f'**{e["term"]}**:' in idx,f'Index entry missing: {e["term"]}')
need('print-page numbers' in idx and 'Development edition' in idx,'Provisional index not identified')
for n in range(22,min(max(chapters),27)+1):need(f'Chapter {n}' in src,f'Developed Chapter {n} source queue absent')
need('metadata/backmatter-maintenance-standard.md' in read('Makefile') or 'check_backmatter_integrity.py' in read('Makefile'),'Back matter gate absent from make check')
print('Back-matter dynamic coverage:',len(chapters),'developed chapters;',len(terms),'glossary terms;',len(entries),'index entries; failures:',len(errors))
for e in errors:print('FAIL:',e)
sys.exit(bool(errors))
