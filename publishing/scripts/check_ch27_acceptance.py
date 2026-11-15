#!/usr/bin/env python3
"""Chapter 27 acceptance: artifacts, local fencing and honest E5 limitation."""
from pathlib import Path
import re,sys,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2]
chapter=(R/'manuscript/part-04-implementation/ch27-build-5-optional-coordination-and-production-hardening/index.md').read_text()
root=R/'examples/refund-reference-system/build5'
files={name:(root/name).read_text() for name in ('README.md','coordinator.py','runner.py','demo.py','test_coordination.py')}
checks={
 'Substantive chapter, 2k–3.5k word source':2000<=len(re.findall(r"\b[\w'-]+\b",chapter))<=3500,
 'Complete case and CAB continuity':all(x in chapter for x in ('CASE-204','RF-1042','$500','Design A','Design B','Design C','C02','C04','C05','E2','E5','E7','E8','E9')),
 'Explicit non-guarantee E5 does not consume epoch':'does not transmit an E2 epoch' in chapter and 'does not presently consume/verify the E2 epoch' in files['README.md'],
 'Durable lease epoch transactional claim':all(x in files['coordinator.py'] for x in ('BEGIN IMMEDIATE','epoch+1','StaleOwner','EXECUTE_IN_FLIGHT','db.close()')),
 'One E5 execute request and read-only reconciliation':all(x in files['runner.py'] for x in ('mark_execute_intent','reconcile','RunnerUnavailable')),
 'Confirmation requires matching trusted operation identity':all(x in files['runner.py'] for x in ("proof != {'case_id':CASE,'operation_id':OPERATION}", "status='UNKNOWN'")),
 'Actual Build 4 E5 subprocess':"HERE.parent/'build4'/'service.py'" in files['demo.py'],
 'Negative concurrency/recovery and actual E5 test':all(x in files['test_coordination.py'] for x in ('test_concurrent_acquire_has_one_winner','test_crash_after_intent_before_e5_call_does_not_retry','test_stale_owner_cannot_override_new_owner_reconcile','test_direct_run_demonstrations_with_real_e5_subprocess')),
 'Embedded actual source architecture':'(architecture.svg)' in files['README.md'],
 'Book status and navigation updated':(('chapters: 36' in (R/'book.yaml').read_text() and 'All 36 chapters developed' in (R/'book.yaml').read_text())) and 'Build 5' in (R/'metadata/topic-traceability.md').read_text(),
 'Source register coverage':'Chapter 27 source-to-claim' in (R/'references/source-register.md').read_text(),
}
try:ET.parse(root/'architecture.svg');checks['Source diagram valid SVG']=True
except (OSError,ET.ParseError):checks['Source diagram valid SVG']=False
for idx in (1,2,3):
 k=f'F27-{idx:02d}'; s=R/f'assets/shared-figures/sources/{k}.svg';r=R/f'assets/shared-figures/rendered/{k}.svg';p=R/f'assets/shared-figures/rendered/{k}.png'
 try:ET.parse(s);good=s.read_bytes()==r.read_bytes() and p.stat().st_size>20_000 and k+'.png' in chapter
 except (OSError,ET.ParseError):good=False
 checks[k+' source/render/placement']=good
for name,value in checks.items():print(('PASS: ' if value else 'FAIL: ')+name)
sys.exit(not all(checks.values()))
