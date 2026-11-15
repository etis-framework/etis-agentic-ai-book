#!/usr/bin/env python3
"""Pre-Part VII structural gate; does NOT certify printed or production behavior."""
from pathlib import Path
import re,sys
R=Path(__file__).resolve().parents[2]
errors=[]
chapter_paths=sorted((R/'manuscript').glob('part-*/ch*/index.md'))
chapters={int(re.search(r'/ch(\d+)-',str(p)).group(1)):p for p in chapter_paths}
if set(chapters)!=set(range(1,37)):errors.append('Chapter inventory must contain 1–36')
for n in range(1,35):
 p=chapters.get(n)
 if not p:continue
 t=p.read_text()
 if 'STATUS: PLANNED' in t:errors.append(f'Chapter {n} unexpectedly stubbed')
 if 'CAB-001' in t:errors.append(f'Chapter {n} exposes internal architecture identifier')
 if re.search(r'advanced student|\bsix[- ]lens\b|six perspectives',t,re.I):errors.append(f'Chapter {n} leaks internal QA perspective terminology')
for n in (35,36):
 p=chapters.get(n)
 if p and 'STATUS: PLANNED / NOT DRAFTED' not in p.read_text():
  print(f'NOTE: Chapter {n} has moved beyond placeholder; perform full chapter acceptance')
for i in range(6):
 d=R/f'examples/refund-reference-system/build{i}'
 for fn in ('README.md','architecture.svg'):
  if not (d/fn).exists():errors.append(f'Build {i}: missing {fn}')
 if (d/'README.md').exists() and 'architecture.svg' not in (d/'README.md').read_text():errors.append(f'Build {i} README does not embed diagram')
for f in (R/'manuscript').rglob('*.md'):
 for a in re.findall(r'!\[[^]]*\]\(([^)]+)\)',f.read_text()):
  if a.startswith(('http:','https:','data:')):continue
  if not ((R/a).is_file() or (f.parent/a).is_file()):errors.append(f'Broken image: {f.relative_to(R)} -> {a}')
for f in ('review/pre-part-vii-holistic-war-game.md','review/pre-part-vii-selective-reading-paths.md','review/pre-part-vii-architecture-code-audit.md','publishing/PRE_PART_VII_QA_REPORT.md'):
 if not (R/f).is_file():errors.append('Missing audit artifact: '+f)
print('Pre–Part VII structural audit:', 'PASS' if not errors else 'FAIL', f'({len(errors)} issue(s))')
for e in errors:print('ERROR:',e)
print('NOT COVERED: native Word pagination, live Git SHA, external source verification, deployed control certification')
sys.exit(bool(errors))
