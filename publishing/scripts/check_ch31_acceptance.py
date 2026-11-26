#!/usr/bin/env python3
"""Chapter 31 deterministic release/evidence acceptance preflight; not production certification."""
from pathlib import Path
import ast
import json
import re
import sys
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2]
CH=(R/'manuscript/part-05-reliability-security/ch31-verification-evaluation-and-evidence/index.md').read_text()
A=R/'examples/refund-reference-system/assurance'
SRC=(A/'collect.py').read_text(); TEST=(A/'test_collect.py').read_text();README=(A/'README.md').read_text()
words=len(re.findall(r"\b[\w'-]+\b",CH))
checks={
 'Substantive 2,300–3,500 source words and three figures': 2300<=words<=3500 and all(f'F31-{n:02d}.png' in CH for n in range(1,4)),
 'Reader orientation and agentic distinction':all(x in CH[:5000] for x in ('CASE-204','RF-1042','$500','Design A','Design B','Design C','agent','E1','E2','E3','E4','E5','E6','E7','E8','E9')),
 'No internal baseline label in published chapter':'CAB-001' not in CH,
 'Contracts and trust boundaries': all(f'C{n:02d}' in CH for n in range(1,10)) and 'E5 current-owner enforcement remains absent' in CH,
 'Evidence and falsifier structure':all(x in CH for x in ('Table 31.1','Table 31.2','falsifier','EXECUTED_FAIL','NOT_IMPLEMENTED','EXTERNAL_EVIDENCE_REQUIRED','source digests')),
 'Agent evaluation / production assurance not conflated':all(x in CH.lower() for x in ('model evaluation','protected','provider','release','drift','not established')),
 'Source and test links':all(x in CH for x in ('assurance/collect.py','assurance/README.md','assurance/test_collect.py','security/test_adversarial_cases.py','reliability/test_recovery_cases.py','operations/test_incident.py','build5/test_coordination.py')),
 'Collector is allowlisted and non-effectful':all(x in SRC for x in ('CASES: tuple[FixtureCase','validate_registry','result_status','run_case','output_sha256','source_sha256',"'production_certified': False")) and not any(s in SRC for s in ('from adapter import','from client import','provider.send(', 'issue_fixture_grant(')),
 'Collector has 7 exact methods and 12 negative/structural tests':SRC.count('FixtureCase(')>=7 and len(re.findall(r'^    def test_',TEST,re.M))>=12,
 'Embedded actual module diagram in README':'![Chapter 31 assurance collector source/module architecture, test invocation and evidence flow](architecture.svg)' in README and 'not Build 6' in README and 'production' in README,
 'Book, appendix and evidence metadata updated':'First-edition manuscript frozen; companion source aligned with edition' in (R/'book.yaml').read_text() and all('Chapter 31' in (R/p).read_text() for p in ('manuscript/backmatter/appendices.md','references/source-register.md','metadata/topic-traceability.md','examples/refund-reference-system/ASSURANCE_HANDOFF_CH28_CH31.md','examples/refund-reference-system/IMPLEMENTATION_EVIDENCE_MAP.md')),
 'E5 gaps remain visible':all(x in README for x in ('E5','PROVIDER_SETTLEMENT','PROTECTED_AUDIT','AGENT_EVALUATION')),
}
for n in range(1,4):
 name=f'F31-{n:02d}';a=R/f'assets/shared-figures/sources/{name}.svg';b=R/f'assets/shared-figures/rendered/{name}.svg';p=R/f'assets/shared-figures/rendered/{name}.png'
 try:
  parsed=ET.parse(a).getroot();checks[f'{name} SVG/PNG fidelity']=a.read_bytes()==b.read_bytes() and p.stat().st_size>30_000 and parsed.attrib.get('width')=='1000' and parsed.attrib.get('height')=='600' and len(list(parsed.iter()))>20
 except (OSError,ET.ParseError):checks[f'{name} SVG/PNG fidelity']=False
try:ET.parse(A/'architecture.svg');checks['Assurance architecture SVG parses']=True
except (OSError,ET.ParseError):checks['Assurance architecture SVG parses']=False
for label,ok in checks.items():print(('PASS' if ok else 'FAIL')+': '+label)
print(f'Chapter 31 source words: {words}; V12 allocated 15 finished pages; native Word layout and source-passage signoff open')
sys.exit(not all(checks.values()))
