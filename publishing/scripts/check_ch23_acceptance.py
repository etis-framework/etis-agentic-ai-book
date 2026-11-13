#!/usr/bin/env python3
"""Ch23 Build 1 source acceptance; not a substitute for runtime tests or print QA."""
from pathlib import Path
import re,sys
r=Path(__file__).resolve().parents[2]
ch=(r/'manuscript/part-04-implementation/ch23-build-1-bounded-advisory-reasoning/index.md').read_text()
b=r/'examples/refund-reference-system/build1'
checks={
 "Chapter 23 no placeholder": "STATUS: PLANNED" not in ch and len(ch.split())>=2000,
 "source interface": all((b/f).is_file() for f in ('contracts.py','advisory.py','model_interface.py','demo.py','README.md','test_advisory.py')),
 "three separated figures": all(f'F23-{i:02}.png' in ch and (r/f'assets/shared-figures/sources/F23-{i:02}.svg').is_file() for i in (1,2,3)),
 "canonical C04 explanation": all(x in ch for x in ('CASE-204','RF-1042','C04','E5','E6','E7','E8','UNKNOWN','Design B','Design C')),
 "build test references": re.search(r'unittest discover\s+\\\s*-s examples/refund-reference-system/build1', ch) is not None,
 "independent old tests": re.search(r'unittest discover\s+\\\s*-s examples/refund-reference-system/build0', ch) is not None,
 "edition lock warning": 'immutable' in ch,
 "new QA documented": 'Build 1' in (r/'examples/refund-reference-system/TESTING.md').read_text(),
}
for key,ok in checks.items():print(('PASS' if ok else 'FAIL'),key)
sys.exit(not all(checks.values()))
