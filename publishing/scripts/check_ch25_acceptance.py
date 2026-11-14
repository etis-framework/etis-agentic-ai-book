#!/usr/bin/env python3
"""Executable Chapter 25 acceptance: contracts, illustration, sources, and build QA.

Automated guards cannot certify a real E5 deployment or native print pagination.
"""
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2]
chapter=ROOT/'manuscript/part-04-implementation/ch25-build-3-trusted-consequential-execution/index.md'
text=chapter.read_text()
code=ROOT/'examples/refund-reference-system/build3'
checks={
 'Chapter 25 developed within working source cap': 'STATUS: PLANNED' not in text and 2000<=len(text.split())<=3500,
 'Mandatory case, contracts and authority language':all(x in text for x in ('CASE-204','RF-1042','50,000','E1','E2','E3','E4','E5','E6','E7','E8','E9','C01','C03','C04','C05','C06','C07','C08','UNKNOWN','Design B','Design C')),
 'Actual signed valid-token denial': all(x in (code/'test_gate.py').read_text() for x in ('LocalAssertionAuthority','test_valid_agent_token_is_not_payment_approval','assert_no_effect')),
 'Separate executable E5 process and controlled server-only adapter': 'Popen' in (code/'test_gate.py').read_text() and 'import refund' in (code/'service.py').read_text() and 'import refund' not in (code/'client.py').read_text(),
 'Source contracts, doc and test present': all((code/x).is_file() for x in ('README.md','architecture.svg','client.py','service.py','contracts.py','demo.py','test_gate.py')),
 'Legacy Builds 0–2 source diagrams included':all((ROOT/f'examples/refund-reference-system/build{i}/architecture.svg').is_file() for i in (0,1,2)),
 'Negative, approved and UNKNOWN exercises': all(x in text for x in ('--scenario compromised','--scenario approved','--scenario outage','--scenario tampered')),
 'Source and navigation updates': 'Chapter 25 source-to-claim' in (ROOT/'references/source-register.md').read_text() and 'Chapter 25 / Build 3' in (ROOT/'metadata/topic-traceability.md').read_text(),
 'Future security/deployment exclusions explicit':'same OS user' in text and 'Chapter 26' in text and 'Chapter 29' in text and 'Chapter 31' in text,
}
for i in (1,2,3):
 key=f'F25-{i:02}'
 master=ROOT/f'assets/shared-figures/sources/{key}.svg'
 embedded=ROOT/f'assets/shared-figures/rendered/{key}.svg'
 png=ROOT/f'assets/shared-figures/rendered/{key}.png'
 try:
  ET.parse(master)
  good=master.read_bytes()==embedded.read_bytes() and png.stat().st_size>10_000
 except (OSError,ET.ParseError):good=False
 checks[f'{key} source/render figure gate']=good and (key+'.png' in text)
for n in range(4):
 svg=ROOT/f'examples/refund-reference-system/build{n}/architecture.svg'
 readme=ROOT/f'examples/refund-reference-system/build{n}/README.md'
 try:
  ET.parse(svg)
  okay='(architecture.svg)' in readme.read_text()
 except (OSError,ET.ParseError):okay=False
 checks[f'Build {n} embedded source architecture']=okay
for name,result in checks.items():print(('PASS' if result else 'FAIL')+': '+name)
sys.exit(not all(checks.values()))
