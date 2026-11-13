#!/usr/bin/env python3
"""Structural preflight for manuscript conceptual continuity; not a human six-lens signoff."""
from pathlib import Path
import re,sys
R=Path(__file__).resolve().parents[2]
read=lambda p:(R/p).read_text()
files={
'front':read('manuscript/frontmatter/how-to-use-this-book.md'),
'8':read('manuscript/part-02-architecture/ch08-from-requirements-to-a-reference-architecture/index.md'),
'11':read('manuscript/part-02-architecture/ch11-agent-reasoning-and-proposal-contracts-e3/index.md'),
'13':read('manuscript/part-02-architecture/ch13-trusted-execution-and-authority-e5/index.md'),
'14':read('manuscript/part-02-architecture/ch14-enterprise-integration-and-business-truth-e6-e8/index.md'),
'15':read('manuscript/part-02-architecture/ch15-durable-operational-state-and-assurance-e7-e9/index.md'),
'17':read('manuscript/part-03-patterns/ch17-choosing-deterministic-agentic-and-hybrid-designs/index.md'),
'18':read('manuscript/part-03-patterns/ch18-coordination-and-delegation-patterns/index.md'),
'app':read('manuscript/backmatter/appendices.md'),
'map':read('metadata/topic-traceability.md')}
expect={
'front':['cross-domain contracts','Appendix','Chapter 35'],
'8':['Table 8.1','Table 8.2','Table 8.3','proposal','E7','E8'],
'11':['C04','RF-1042','E5/E7'],
'13':['C04','C05','C06','RF-1042'],
'14':['E7 operation journal','E8','UNKNOWN'],
'15':['State ownership reminder','E7','E8'],
'17':['not a progression from Design A through B to C'],
'18':['nine **logical responsibilities**','cross-domain contracts','**no additional deployed services**','RF-1042'],
'app':['C01','C02','C03','C04','C05','C06','C07','C08','C09','UNKNOWN','Chapters 22–27'],
'map':['CCR-01','CCR-09','six lenses']}
fail=[]
for name,terms in expect.items():
 for term in terms:
  if term.casefold() not in files[name].casefold():fail.append(f'{name}: missing {term}')
for n in range(1,10):
 if len(re.findall(r'\| C0'+str(n)+r'\b',files['app']))!=1:fail.append(f'Appendix C0{n} not exactly once')
if 'These are *logical contracts*, not mandatory services.' in files['18']:fail.append('old conflated terminology remains')
if len(re.findall(r"\b[\w'-]+\b",files['18']))>3000:fail.append('Chapter 18 word cap exceeded')
for x in fail:print('FAIL:',x)
print('Conceptual continuity structural preflight:', 'FAIL' if fail else 'PASS', f'({len(fail)} issue(s))')
print('OPEN: six-lens human reading, CAB-001 field-level audit, source-page audit, Mac Word figures and pagination')
sys.exit(bool(fail))
