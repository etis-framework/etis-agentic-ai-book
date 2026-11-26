#!/usr/bin/env python3
"""Reader-facing bibliography / Appendix A-B-C publication structure preflight.

This verifies placement, navigation, and simple terminology; it does not
certify sources, external systems, or the rendered Mac Word page count.
"""
from pathlib import Path
import re,sys
R=Path(__file__).resolve().parents[2]
A=(R/'manuscript/backmatter/appendices.md').read_text()
B=(R/'manuscript/backmatter/bibliography.md').read_text()
S=(R/'references/source-register.md').read_text()
M=(R/'metadata/backmatter-maintenance-standard.md').read_text()
errors=[]
def require(ok,why):
 if not ok:errors.append(why)
require(all(A.count('## Appendix '+ch+' —')==1 for ch in 'ABC'), 'Appendix A/B/C headings')
require(not re.search(r'\b(still planned|currently planned|development log|Chapter (?:3[2-6]) remains planned)\b',A,re.I),'Appendix contains development status')
require(not re.search(r'^\*\*Chapter \d+ (?:reading guide|.*supplement)\.',B,re.M), 'Bibliography contains chapter reading guides')
require(not re.search(r'^\*\*Chapter \d+ (?:reading guide|.*supplement)\.',A,re.M),'Appendix contains chapter-by-chapter supplement prose')
require(not re.search(r'(?m)^## Chapter (?:28|29|30|31)\b',B),'Bibliography contains chapter-specific headings')
require('Chapters 28–31 — reader-bibliography reconciliation' in S,'Source register must retain Ch28–31 mapping')
require('Appendix B as concise companion tables' in M,'Maintenance standard missing editorial discipline')
for n in range(1,10):require(len(re.findall(r'^\| E'+str(n)+r' —',A,re.M))==1,f'E{n} responsibility missing')
for n in range(1,10):require(len(re.findall(r'^\| C0'+str(n)+r' —',A,re.M))==1,f'C0{n} contract missing')
for n in range(6):
 rel=f'build{n}/README.md'
 require(rel in A and (R/'examples/refund-reference-system'/rel).is_file(),f'Build {n} link missing/broken')
for n,folder in [(28,'reliability'),(29,'security'),(30,'operations'),(31,'assurance')]:
 rel=f'{folder}/README.md'
 require(re.search(r'^\| '+str(n)+r' \S*.*`'+re.escape(rel)+r'`',A,re.M) is not None,f'Chapter {n} table locator missing')
 require((R/'examples/refund-reference-system'/rel).is_file(),f'Chapter {n} README absent')
require('examples/refund-reference-system/' in A and 'All paths in the following tables' in A,'Companion root/path convention missing')
require(not re.search(r'\]\(examples/refund-reference-system/',A),'Invalid manuscript-relative repository link')
for term in ['UNKNOWN','RF-1042','E5','E7','E8','not','production']:
 require(term in A,f'Assurance qualification missing {term}')
print('Back-matter publication structure:', 'PASS' if not errors else 'FAIL', '; findings:',len(errors))
for e in errors:print('FAIL:',e)
sys.exit(bool(errors))
