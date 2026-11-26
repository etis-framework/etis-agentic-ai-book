#!/usr/bin/env python3
"""Chapter 24 content, code and figure integration guard (not publication proof)."""
from pathlib import Path
import re
import sys
root = Path(__file__).resolve().parents[2]
ch = (root / 'manuscript/part-04-implementation/ch24-build-2-scoped-context-and-identity/index.md').read_text()
code = root / 'examples/refund-reference-system/build2'
checks = {
    'Chapter 24 developed; below 3500-word cap': 'STATUS: PLANNED' not in ch and 2000 <= len(ch.split()) <= 3500,
    'source implementation and tests': all((code / name).is_file() for name in ('README.md','identity.py','context.py','pipeline.py','demo.py','test_scope.py')),
    'three architecture/behavior/decision figures': all((root/f'assets/shared-figures/sources/F24-{n:02}.svg').is_file() and (root/f'assets/shared-figures/rendered/F24-{n:02}.png').is_file() and f'F24-{n:02}.png' in ch for n in (1,2,3)),
    'source-to-contract and financial boundaries': all(term in ch for term in ('CASE-204','RF-1042','E1','E3','E4','E5','E6','E7','E8','C01','C03','C04','UNKNOWN','Design B','Design C')),
    'executable Build 2, Build 1, Build 0 examples': all(re.search(r'unittest discover\s+\\\s*-s examples/refund-reference-system/build'+str(n),ch) for n in (0,1,2)),
    'scope, source, and limitations documented': all(term in (code/'README.md').read_text() for term in ('HMAC','cross-tenant','outage','Chapter 25','untrusted','RF-1042')),
    'source register and navigation updated': '## Historical source-review record — Chapter 24' in (root/'references/source-register.md').read_text() and 'Chapter 24 / Build 2' in (root/'metadata/topic-traceability.md').read_text(),
}
for label, ok in checks.items():
    print(('PASS' if ok else 'FAIL')+': '+label)
sys.exit(not all(checks.values()))
