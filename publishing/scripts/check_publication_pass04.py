#!/usr/bin/env python3
"""Pass 4 guard: concrete manuscript/code/source crosswalk; NOT production certification."""
from pathlib import Path
import json,re,sys
R=Path(__file__).resolve().parents[2]
errors=[]
def need(ok,msg):
    if not ok:errors.append(msg)
def chapter(n):
    files=list((R/'manuscript').glob(f'part-*/ch{n:02d}-*/index.md'))
    need(len(files)==1,f'Chapter {n}: missing or ambiguous path')
    return files[0].read_text() if len(files)==1 else ''
ch={n:chapter(n) for n in range(1,37)}
for n,fragments in {
    12:['Context engineering across a workflow','Persistent-memory poisoning','Build 2'],
    19:['Model Context Protocol (MCP)','Agent2Agent (A2A) protocol','particular `CASE-204` refund','computer-use'],
    20:['Cross-task memory contamination review','cross-task persistent-memory'],
    31:['Long-horizon trajectories need separate evaluation','trajectory constraint compliance','statistical confidence'],
    33:['Changing agents are changing release artifacts','cannot expand its own tool grants, modify E5 policy, change its release cohort or replace evidence standards','must remain independently governed and verified'],
}.items():
    for x in fragments:need(x.casefold() in ch[n].casefold(),f'Chapter {n} missing {x}')
for path,needed in {
    'references/bibliography.bib':['a2a_protocol_2026','mcp_2026','nist_agent_standards_2026'],
    'manuscript/backmatter/bibliography.md':['Agent2Agent (A2A) Protocol Specification','AI Agent Standards Initiative'],
    'references/source-register.md':['Pass 4 — emerging agent engineering','cross-task poisoning','trajectory-level'],
    'manuscript/backmatter/glossary.md':['Agent2Agent (A2A) protocol','Context engineering','Memory poisoning','Long-horizon trajectory evaluation'],
    'metadata/topic-traceability.md':['Pass 4 modern-agent scope audit'],
    'review/pass4-state-of-the-art-six-lens.md':['Implementing engineer','Enterprise architect','Advanced student','Security','SRE','Business owner','State-of-the-art','eight selective'],
    'publishing/PUBLICATION_CERTIFICATION_PASS_04.md':['153','NOT CERTIFIED','V12'],
}.items():
    p=R/path;need(p.is_file(),f'Missing {path}')
    if p.is_file():
        s=p.read_text()
        for term in needed:need(term.casefold() in s.casefold(),f'{path}: missing {term}')
terms={x['term'] for x in json.loads((R/'metadata/index-term-register.json').read_text())['entries']}
for t in ['Agent2Agent (A2A) interoperability','Context engineering — assembly and budget','Long-horizon trajectory evaluation','Persistent memory poisoning']:
    need(t in terms,f'Index register missing {t}')
for build in range(6):
    d=R/f'examples/refund-reference-system/build{build}'
    need((d/'README.md').is_file(),f'Build {build} README missing')
    if (d/'README.md').exists():
        readme=(d/'README.md').read_text()
        need('.svg' in readme,f'Build {build} README missing source diagram')
    need(any(d.glob('test_*.py')),f'Build {build} tests missing')
for comp in ('security','reliability','operations','assurance'):
    d=R/f'examples/refund-reference-system/{comp}'
    need((d/'README.md').is_file() and any(d.glob('test_*.py')),f'{comp} fixture missing')
for t in ('REAL PAYMENT','PRODUCTION CERTIFICATION'):
    pass
print('Pass 4 static acceptance:', 'PASS' if not errors else 'FAIL',len(errors),'findings')
for x in errors:print('FAIL:',x)
sys.exit(bool(errors))
