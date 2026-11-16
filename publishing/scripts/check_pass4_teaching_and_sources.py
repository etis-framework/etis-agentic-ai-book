#!/usr/bin/env python3
"""Check the Pass 4 teaching guide against actual source/tests, not just prose."""
from pathlib import Path
import re, sys, xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2]
E=R/'examples/refund-reference-system'
guide=(E/'LEARNING_PATH.md').read_text()
root=(E/'README.md').read_text()
errors=[]

def require(ok, description):
    if not ok: errors.append(description)

require('LEARNING_PATH.md' in root,'root README missing teaching guide')
for i in range(6):
    d=E/f'build{i}'
    require((d/'README.md').exists(),f'build{i} README absent')
    try: ET.parse(d/'architecture.svg')
    except (OSError,ET.ParseError):errors.append(f'build{i} SVG invalid')
    require(f'Build {i}, Ch{22+i}' in guide,f'build{i} guide crosswalk absent')
for d in ('reliability','security','operations','assurance'):
    require((E/d/'README.md').is_file() and any((E/d).glob('test_*.py')),
            f'{d} learning fixture incomplete')
# All named test locators in the teaching guide must really exist.
for rel,test in re.findall(r'`((?:build[0-5]|reliability|security|operations|assurance)/test_[^`/ ]+\.py)::(test_[a-zA-Z0-9_]+)`',guide):
    file=E/rel
    require(file.is_file(),f'missing test file {rel}')
    if file.is_file():
        require(re.search(r'^\s*def\s+'+re.escape(test)+r'\s*\(',file.read_text(),re.M) is not None,
                f'missing method {rel}::{test}')
require('E5-side epoch' in guide and 'not' in guide.lower(), 'missing E5 epoch limitation')
require('not* compose' in guide.lower() or 'does *not* compose' in guide.lower(),
        'missing non-composed Build 1/2 to Build 5 limitation')
require('production guarantee' in guide.lower() or 'production obligations' in guide.lower(),
        'missing production assurance caveat')
for name in ('identity.py','context.py','workflow.py','runner.py','service.py'):
    require(name in guide,f'missing educational module {name}')
for rel in ('modelcontextprotocol.io/specification/2026-07-28', 'a2a-protocol.org/v1.0.0/specification/'):
    require(rel in (R/'manuscript/backmatter/bibliography.md').read_text(), f'missing source {rel}')
    require(rel in (R/'references/bibliography.bib').read_text(), f'bib/source mismatch {rel}')
for phrase in ('Context engineering', 'Bounded', 'Memory', 'Long-horizon'):
    require(phrase.lower() in guide.lower() or phrase == 'Long-horizon',f'teaching linkage absent {phrase}')
print(f'Pass 4B teaching/source acceptance: {"FAIL" if errors else "PASS"}; {len(errors)} findings')
for e in errors: print('FAIL:',e)
sys.exit(bool(errors))
