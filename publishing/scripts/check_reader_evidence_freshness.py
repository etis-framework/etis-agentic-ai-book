#!/usr/bin/env python3
"""Prevent stale chapter-development text and dead manuscript file links.

Source-only editorial gate; does not replace native Word, source validation or
proof that externally linked release artifacts are published.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
COMPANION = ROOT / 'examples/refund-reference-system'
errors = []

for rel in ('README.md', 'TESTING.md', 'IMPLEMENTATION_EVIDENCE_MAP.md'):
    source = (COMPANION / rel).read_text(encoding='utf-8')
    for pattern in (r'109 passing test cases', r'work to be performed in Chapters 29[–-]31',
                    r'not an assertion that Chapters 29[–-]31',
                    r'Chapters \*\*28[–-]30\*\* use'):
        if re.search(pattern, source, re.I):
            errors.append(f'{rel}: stale completed-chapter wording: {pattern}')

readme = (COMPANION / 'README.md').read_text(encoding='utf-8')
for chapter, directory in ((28, 'reliability'), (29, 'security'),
                           (30, 'operations'), (31, 'assurance')):
    if f'| {chapter} —' not in readme or not (COMPANION / directory / 'README.md').is_file():
        errors.append(f'companion navigation for Chapter {chapter} absent')

for path in (ROOT / 'manuscript').rglob('*.md'):
    source = path.read_text(encoding='utf-8')
    for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)', source):
        raw = target.split('#', 1)[0].split(' ', 1)[0]
        if not raw or raw.startswith('/') or '://' in raw or raw.startswith('mailto:'):
            continue
        if not (path.parent / raw).exists():
            errors.append(f'{path.relative_to(ROOT)}: unresolved Markdown link {target}')

print('Reader evidence freshness and relative links:', 'PASS' if not errors else 'FAIL')
for problem in errors:
    print('FAIL:', problem)
sys.exit(bool(errors))
