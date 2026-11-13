#!/usr/bin/env python3
"""Static regression preflight for Parts I–III reader navigation.

NOT a substitute for six-lens human reading, source-page audit, Mac Word print QA,
or a measured finished-page ledger.
"""
from pathlib import Path
import re,sys
ROOT=Path(__file__).resolve().parents[2]
errors=[]

def text(rel):
 p=ROOT/rel
 if not p.exists():
  errors.append(f'Missing: {rel}')
  return ''
 return p.read_text(encoding='utf-8')

def need(condition,why):
 if not condition: errors.append(why)

front=text('manuscript/frontmatter/how-to-use-this-book.md')
part=text('manuscript/part-03-patterns/_part.md')
ch18=text('manuscript/part-03-patterns/ch18-coordination-and-delegation-patterns/index.md')
ch19=text('manuscript/part-03-patterns/ch19-tools-adapters-and-effect-isolation/index.md')
ch20=text('manuscript/part-03-patterns/ch20-state-memory-and-knowledge-design/index.md')
ch21=text('manuscript/part-03-patterns/ch21-architecture-decisions-and-governance-as-code/index.md')
bib=text('references/bibliography.bib')
back=text('manuscript/backmatter/bibliography.md')
source=text('references/source-register.md')
qa=text('metadata/parts-01-03-six-lens-audit.md')
appendix=text('manuscript/backmatter/appendices.md')

need('Chapters 17–21' in front,'Front matter: Part III path must include Chapters 17–21')
need('no external architecture file is required' in front,'Front matter must not require private CAB for basic comprehension')
need('**E1** admits' in part and '**E2** coordinates' in part and '**E3** reasons' in part and '**E4** controls' in part,'Part III E-domain map incomplete')
for i,s in enumerate(['admission','bounded work order','context query','advisory proposal','authorization decision','durable intent','provider dispatch','reconciliation','telemetry/assurance'],1):
 need(f'**C{i:02d}** {s}' in part,f'Part III C{i:02} functional reference missing')
need('**admission (E1)**' in ch18 and '**coordination (E2)**' in ch18 and '**governance (E9)**' in ch18,'Ch18 compact E map absent')
need('**trusted execution (E5)**' in ch19 and '**enterprise integration (E6)**' in ch19,'Ch19 first-use boundary names absent')
need('**governed context and retrieval (E4)**' in ch20 and '**durable operational state (E7)**' in ch20,'Ch20 first-use names absent')
need('**C02 Work order**' in ch21 and '**C09 Telemetry**' in ch21,'Ch21 C catalog should include C02/C09')
need('NIST SP 800-162' in ch21 and '@techreport{nist_sp800_162_2019' in bib and 'NIST Special Publication 800-162' in back and '`nist_sp800_162_2019`' in source,'New NIST ABAC source not consistently mapped')
need('113 | 95 | +18' in qa and '122 | 123 | -1' in qa and '62 | 62 | 0' in qa,'Measured V12 exceptions absent from QA report')
need('NOT certified or frozen' in qa,'Publication-gate warning missing')
need('Chapters 17–21 compare' in appendix and 'Chapters 22–36 remain planned' in appendix,'Appendix must distinguish drafted Ch17–21 from planned Ch22–36')
need('Chapters 19–36 are *planned*' not in appendix,'Appendix stale developed-chapter status')
need('CASE-204' in ch21 and 'RF-1042' in ch21,'Running-case identity missing in Ch21')
need('**conditional initial production candidate**' in ch21 or '*conditional initial production candidate*' in ch21,'Design B status must stay conditional')
need(not re.search(r'\bE10\s+(?:owns|is the|is a)\b',part+ch18+ch19+ch20+ch21),'Unapproved E10 responsibility assigned')

print('Parts I–III reader navigation, source-link and page-exception preflight: '+('FAIL' if errors else 'PASS'))
for e in errors: print('FAIL:',e)
print('MANUAL GATES: semantic six-lens reading, source passage and edition validation, 7x10 native Mac Word print review, chapter-page exceptions')
sys.exit(bool(errors))
