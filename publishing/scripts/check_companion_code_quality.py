#!/usr/bin/env python3
"""Static companion-code entrypoint and reader-guide consistency gate."""
from pathlib import Path
import sys
r=Path(__file__).resolve().parents[2]
c=r/'examples/refund-reference-system'
required=['README.md','ARCHITECTURE.md','CONTRIBUTING.md','ENGINEERING_STANDARD.md','TESTING.md','build0/README.md','build0/refund.py','build0/test_refund.py','build1/README.md','build1/contracts.py','build1/advisory.py','build1/model_interface.py','build1/demo.py','build1/test_advisory.py','build2/README.md','build2/identity.py','build2/context.py','build2/pipeline.py','build2/demo.py','build2/test_scope.py']
errors=[]
for rel in required:
    if not (c/rel).is_file():errors.append(f'missing {rel}')
for rel in ['README.md','ARCHITECTURE.md','CONTRIBUTING.md','ENGINEERING_STANDARD.md','TESTING.md','build0/README.md']:
    content=(c/rel).read_text() if (c/rel).exists() else ''
    for term in ['CASE-204','E7','E8'] if rel in ('README.md','TESTING.md','build0/README.md') else []:
        if term not in content:errors.append(f'{rel} missing {term}')
if (c/'README.md').exists():
    for target in ['TESTING.md','ENGINEERING_STANDARD.md']:
        if target not in (c/'README.md').read_text():errors.append(f'reader README missing {target}')
standard=(c/'ENGINEERING_STANDARD.md').read_text() if (c/'ENGINEERING_STANDARD.md').exists() else ''
for term in ['Build 0','Build 1','Build 2','Build 3','Build 4','Build 5','C01–C09','UNKNOWN','RF-1042','fencing','token']:
    if term.lower() not in standard.lower():errors.append(f'engineering standard missing {term}')
code=(c/'build0/refund.py').read_text() if (c/'build0/refund.py').exists() else ''
for term in ['cursor.rowcount != 1','fail_before_provider_commit','db.close()','type(amount_cents) is not int']:
    if term not in code:errors.append(f'Build 0 hardening mechanism missing {term}')
if (c/'build0/README.md').exists() and 'unittest discover' not in (c/'build0/README.md').read_text():errors.append('no runnable test command')
front=(r/'manuscript/frontmatter/preface.md').read_text()
if 'source-controlled Python reference implementation' not in front:errors.append('Preface missing explicit runnable-code value proposition')
part1=(r/'manuscript/part-01-foundations/_part.md').read_text()
if 'development draft' in part1:errors.append('Part I exposes manuscript-production status')
print('Companion documentation and reader-value QA:', 'PASS' if not errors else 'FAIL')
for item in errors:print('FAIL:',item)
sys.exit(bool(errors))
