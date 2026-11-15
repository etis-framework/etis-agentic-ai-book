#!/usr/bin/env python3
"""Editorial regression preflight, not a replacement for chapter-by-chapter human reading."""
from pathlib import Path
import re, sys
R=Path(__file__).resolve().parents[2]
P=R/'manuscript'
errors=[]
chapters={int(p.parent.name[2:4]):p.read_text() for p in P.glob('part-*/ch*/index.md') if int(p.parent.name[2:4])<=30}
if sorted(chapters)!=list(range(1,31)):errors.append('Not all 30 developed chapters found')
for n,s in sorted(chapters.items()):
 if 'CAB-001' in s:errors.append(f'Ch{n:02}: internal CAB identifier in published prose')
 if 'Design ' in s and any(re.search(r'\bDesign '+letter+r'\b',s) for letter in 'ABC'):
  # A local definition may appear in the original section (before or after the heading)
  definitions=('deterministic','advisory','bounded AI advice','bounded investigation','investigator')
  if not any(x.lower() in s[:3500].lower() for x in definitions):errors.append(f'Ch{n:02}: opening design context not found')
 if n==30:
  for item in ('operations/incident.py','operations/test_incident.py','build4/ledger.py','build5/coordinator.py','UNKNOWN','Chapter 31'):
   if item not in s:errors.append(f'Ch30 missing reader navigation/assurance: {item}')
for rel in ('manuscript/frontmatter/how-to-use-this-book.md','manuscript/backmatter/appendices.md','manuscript/backmatter/glossary.md','manuscript/backmatter/index.md','references/source-register.md','examples/refund-reference-system/README.md','examples/refund-reference-system/operations/README.md'):
 if not (R/rel).exists():errors.append(f'Missing: {rel}')
for rel in ('assets/shared-figures/sources/F28-01.svg','assets/shared-figures/rendered/F28-01.svg'):
 if 'CAB-001' in (R/rel).read_text():errors.append(f'Internal name in reader figure: {rel}')
for rel in ('examples/refund-reference-system/operations/incident.py','examples/refund-reference-system/operations/test_incident.py','examples/refund-reference-system/build4/adapter.py','examples/refund-reference-system/build4/ledger.py','examples/refund-reference-system/build5/coordinator.py'):
 if not (R/rel).is_file():errors.append(f'Referenced code missing: {rel}')
print('Reader editorial audit: 30 chapters; errors:',len(errors))
for error in errors:print('FAIL:',error)
sys.exit(bool(errors))
