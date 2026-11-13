#!/usr/bin/env python3
"""Static companion-code entrypoint and reader-guide consistency gate."""
from pathlib import Path
import sys
r=Path(__file__).resolve().parents[2]
c=r/'examples/refund-reference-system'
required=['README.md','ARCHITECTURE.md','CONTRIBUTING.md','TESTING.md','build0/README.md','build0/refund.py','build0/test_refund.py']
errors=[]
for rel in required:
    if not (c/rel).is_file():errors.append(f'missing {rel}')
for rel in ['README.md','ARCHITECTURE.md','CONTRIBUTING.md','TESTING.md','build0/README.md']:
    content=(c/rel).read_text() if (c/rel).exists() else ''
    for term in ['CASE-204','E7','E8'] if rel in ('README.md','TESTING.md','build0/README.md') else []:
        if term not in content:errors.append(f'{rel} missing {term}')
if (c/'README.md').exists() and 'TESTING.md' not in (c/'README.md').read_text():errors.append('reader README missing TESTING.md')
if (c/'build0/README.md').exists() and 'unittest discover' not in (c/'build0/README.md').read_text():errors.append('no runnable test command')
front=(r/'manuscript/frontmatter/preface.md').read_text()
if 'source-controlled Python reference implementation' not in front:errors.append('Preface missing explicit runnable-code value proposition')
part1=(r/'manuscript/part-01-foundations/_part.md').read_text()
if 'development draft' in part1:errors.append('Part I exposes manuscript-production status')
print('Companion documentation and reader-value QA:', 'PASS' if not errors else 'FAIL')
for item in errors:print('FAIL:',item)
sys.exit(bool(errors))
