#!/usr/bin/env python3
"""Chapter 32 acceptance: source/figure/reader semantic preflight, NOT a production certification."""
from pathlib import Path
import re,sys,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2]
CH=(R/'manuscript/part-06-governance-operations/ch32-human-oversight-and-accountable-governance/index.md').read_text()
PART=(R/'manuscript/part-06-governance-operations/_part.md').read_text()
A=(R/'manuscript/backmatter/appendices.md').read_text()
checks={}
def check(name,ok):checks[name]=ok
words=len(re.findall(r"\b[\w'-]+\b",CH))
check('V12 13-page allocation and <=3000 words',len(CH.split())>2300 and words<=3000 and '\"32\": 13' in (R/'publishing/SINGLE_VOLUME_FINISHED_PAGE_LEDGER_V12.json').read_text())
check('Chapter 32 developed / future truthful', 'STATUS: PLANNED' not in CH and 'Chapter 33' in PART and 'Chapter 34' in PART and 'remains planned' not in PART and 'Chapters 1–32 developed' in (R/'book.yaml').read_text())
check('Agentic identity and first-use definitions',all(x in CH[:5200] for x in ('Design A','Design B','Design C','CASE-204','RF-1042','$500','admission and identity (E1)','trusted execution (E5)','C04','C05','E9')))
check('No internal authoring baseline identifiers', 'CAB-001' not in CH and 'BP-001' not in CH)
check('Authority, intervention and revocation distinctions',all(x.lower() in CH.lower() for x in ('separation of duties','transaction-specific','policy version','revocation','quarantine','incident commander','release authority','human','grant issuer','read-only')))
check('Policy, no-redrive and reviewer scenarios',all(x in CH for x in ('UNKNOWN','NOT_FOUND','RF-1042','Runbook 32-A','Table 32.1','Table 32.2','Table 32.3','Table 32.4')))
check('No manufactured new Build 6', 'no additional build is provided' in CH and 'not implemented' in CH.lower() and 'E5' in CH)
for n in range(1,4):
 key=f'F32-{n:02d}';src=R/f'assets/shared-figures/sources/{key}.svg';rend=R/f'assets/shared-figures/rendered/{key}.svg';png=R/f'assets/shared-figures/rendered/{key}.png'
 try:root=ET.parse(src).getroot();ok=root.attrib.get('width')=='1000' and root.attrib.get('height')=='600' and src.read_bytes()==rend.read_bytes() and png.stat().st_size>30000 and f'{key}.png' in CH
 except (OSError,ET.ParseError):ok=False
 check(f'{key} master, raster, and manuscript',ok)
check('Governance fields grounded in fixture and explicit omissions', all(x in CH for x in ('issue_fixture_grant()', 'build3/contracts.py', 'approval_id', 'approver', 'does **not** implement', 'revocation_ref', 'audit_ref')))
check('Runbook identifier explained', 'first runbook in Chapter 32' in CH and 'Runbook 30-A' in CH)
check('No authoring reviewer lenses in developed narrative', not any(re.search(r'\badvanced student\b|\bsix lenses\b', (R / 'manuscript' / a).read_text(),re.I) for a in ['part-05-reliability-security/ch28-distributed-failure-and-recoverable-effects/index.md','part-05-reliability-security/ch29-security-and-adversarial-agent-behavior/index.md','part-05-reliability-security/ch30-reliability-observability-and-incident-response/index.md','part-05-reliability-security/ch31-verification-evaluation-and-evidence/index.md','part-06-governance-operations/ch32-human-oversight-and-accountable-governance/index.md']))
check('Part VI no future chapter drafting status', not re.search(r'remains planned|not yet written|not drafted', PART,re.I))
check('Companion 7 named sources exist',all((R/'examples/refund-reference-system'/s).is_file() and s in CH for s in ['security/test_adversarial_cases.py','reliability/test_recovery_cases.py','operations/test_incident.py','assurance/test_collect.py','build3/test_gate.py','build4/test_provider.py','build5/test_coordination.py']))
check('Back matter and source continuity',all('Chapter 32' in (R/f).read_text() for f in ['manuscript/backmatter/appendices.md','references/source-register.md','metadata/topic-traceability.md']) and 'Governance and approval' in A)
for k,v in checks.items():print(('PASS' if v else 'FAIL')+': '+k)
print(f'Chapter 32 words: {words}; V12 allocation 13 finished pages; native Word-for-Mac and production evidence remain separate gates')
sys.exit(not all(checks.values()))
