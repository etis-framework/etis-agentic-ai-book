#!/usr/bin/env python3
"""Check source figure references; use --built to validate the current DOCX."""
from pathlib import Path
import re,sys,zipfile,hashlib
root=Path(__file__).resolve().parents[2];errors=[];count=0
for chapter in (root/'manuscript').glob('part-*/ch*/index.md'):
 for rel in re.findall(r'!\[[^]]*\]\(([^)]+)\)',chapter.read_text()):
  count+=1
  if not (root/rel).is_file():errors.append(f'Missing {rel} in {chapter}')
for prefix,n in [('F01',3),('F02',4)]:
 for i in range(1,n+1):
  for ext in ('svg','png'):
   if not (root/f'assets/shared-figures/rendered/{prefix}-{i:02}.{ext}').is_file():errors.append(f'Missing {prefix}-{i:02}.{ext}')
if '--built' in sys.argv:
 p=root/'dist/etis-agentic-ai-book.docx'
 if not p.exists():errors.append(f'Build missing: {p}')
 else:
  try:
   with zipfile.ZipFile(p) as z:
    n=len([x for x in z.namelist() if x.startswith('word/media/')]);
    if n<7:errors.append(f'Only {n} embedded images; expected >=7')
    # Fail if the DOCX retains an older figure even when generated PNGs are current.
    media_hashes={hashlib.sha256(z.read(x)).hexdigest() for x in z.namelist() if x.startswith('word/media/')}
    for i in range(1,4):
     fig=root/f'assets/shared-figures/rendered/F04-{i:02}.png'
     if fig.is_file() and hashlib.sha256(fig.read_bytes()).hexdigest() not in media_hashes:
      errors.append(f'F04-{i:02} current PNG is NOT embedded in built DOCX (stale asset/build)')
  except zipfile.BadZipFile:errors.append(f'Invalid DOCX: {p}')
print(f'Chapter image references checked: {count}')
if errors:print('\n'.join(errors));sys.exit(1)
print('Figure checks passed')
