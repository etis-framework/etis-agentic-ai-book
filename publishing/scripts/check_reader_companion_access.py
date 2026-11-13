#!/usr/bin/env python3
"""Regression gate: edition reader can locate code; avoid manuscript-status leakage.

This is a source/text check, not live GitHub accessibility or publication QA.
"""
from pathlib import Path
import re, sys
r = Path(__file__).resolve().parents[2]
read = lambda x: (r / x).read_text(encoding='utf-8')
front = read('manuscript/frontmatter/how-to-use-this-book.md')
intro = read('manuscript/frontmatter/introduction.md')
part = read('manuscript/part-04-implementation/_part.md')
ch22 = read('manuscript/part-04-implementation/ch22-build-0-deterministic-refund-baseline/index.md')
app = read('manuscript/backmatter/appendices.md')
code = read('examples/refund-reference-system/README.md')
issues=[]
def need(value, desc):
 if not value: issues.append(desc)
root='https://github.com/etis-framework/etis-agentic-ai-book'
for title, body in [('front',front),('introduction',intro),('Part IV',part),('Ch22',ch22),('appendix',app),('code README',code)]:
 need(root in body, f'{title}: no official GitHub access path')
need('examples/refund-reference-system/' in front and 'README.md' in front, 'front: companion reader entry point missing')
need('edition' in front and 'tag' in front and 'private during manuscript development' in front,'reader access and release expectations unclear')
for n in range(6):need(f'| {n} |' in code, f'code README: Build {n} missing')
for title, body in [('front',front),('Part IV',part),('Ch22',ch22),('appendix',app)]:
 need(not re.search(r'(?:Chapters?\s+23[–-]36\s+remain planned|Only Build 0 is presently implemented|planned compromised-investigator|Remaining planned appendices|Chapter 35 is planned)', body, re.I), f'{title}: development status in reader narrative')
need('UNKNOWN' in ch22 and 'E7' in ch22 and 'E8' in ch22,'Ch22: simulation trust distinction missing')
need('Design C' in part and 'optional' in part, 'Part IV: optional design C forgotten')
print('Companion code reader access and full-book editorial gate:', 'FAIL' if issues else 'PASS')
for issue in issues:print('FAIL:',issue)
sys.exit(bool(issues))
