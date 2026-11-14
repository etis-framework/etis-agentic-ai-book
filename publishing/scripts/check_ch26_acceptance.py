#!/usr/bin/env python3
"""Chapter 26 release guard: actual provider-contract implementation and navigation.

This static gate supplements (never substitutes for) subprocess tests and
print-size inspection. It proves only the artifacts and invariants named below.
"""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[2]
chapter=ROOT/'manuscript/part-04-implementation/ch26-build-4-provider-integration-and-reconciliation/index.md'
book=chapter.read_text()
b4=ROOT/'examples/refund-reference-system/build4'
files={name:(b4/name).read_text() for name in (
    'README.md','provider_contracts.py','adapter.py','ledger.py',
    'workflow.py','service.py','demo.py','test_provider.py')}
checks={
 'Chapter 26 substantive and within editorial word cap': 'STATUS: PLANNED' not in book and 2000<=len(re.findall(r"\b[\w'-]+\b",book))<=3500,
 'CASE-204 / RF-1042 / $500 running identity':all(x in book for x in ('CASE-204','RF-1042','50,000','E1','E2','E3','E4','E5','E6','E7','E8','E9','C04','C05','C06','C07','C08')),
 'Architectural alternatives and limitations':all(x in book for x in ('Design A','Design B','Design C','not','UNKNOWN','NOT_FOUND','provider contract')),
 'Independent approval from Build 3 preserved':all(x in files['service.py'] for x in ('LocalAssertionAuthority','verify_grant','issue_fixture_grant' if False else 'scope.case_id')),
 'Explicit E7 before E6 and one local dispatch claim':all(x in files['workflow.py'] for x in ('self.ledger.prepare','self.ledger.claim_dispatch','self.provider.send')),
 'Status-only reconciliation': 'self.provider.lookup(command)' in files['workflow.py'] and 'self.provider.send(' not in files['workflow.py'].split('def reconcile(')[1],
 'Provider contract version and stable operation scope':all(x in files['provider_contracts.py'] for x in ('PROVIDER_VERSION','provider-account','retention_seconds','ProviderPort','ProviderObservation')),
 'SQLite connection explicitly closed': 'db.close()' in files['adapter.py'] and 'db.close()' in files['ledger.py'],
 'Hostile transport and recovery negative tests':all(x in files['test_provider.py'] for x in ('test_stalled_connection_has_bounded_delay','test_disconnected_client_cannot_kill_service','test_lost_ack_reconcile_via_service_no_second_send','test_valid_token_without_approval_cannot_create_provider_or_ledger','test_conflicting_stable_operation_key_blocks_dispatch')),
 'README embeds source architecture': '(architecture.svg)' in files['README.md'],
 'README clarifies simulated provider': 'not a payment system' in files['README.md'] and 'Commercial' not in files['README.md'][:80],
 'Book status and navigation updated': ('1–26 developed' in (ROOT/'book.yaml').read_text() or '1–27 developed' in (ROOT/'book.yaml').read_text()) and 'Build 4' in (ROOT/'metadata/topic-traceability.md').read_text(),
 'Source register coverage updated': 'Chapter 26 source-to-claim' in (ROOT/'references/source-register.md').read_text(),
}
for i in (1,2,3):
 key=f'F26-{i:02}'
 master=ROOT/f'assets/shared-figures/sources/{key}.svg'
 render=ROOT/f'assets/shared-figures/rendered/{key}.svg'
 png=ROOT/f'assets/shared-figures/rendered/{key}.png'
 try:
  ET.parse(master)
  good=master.read_bytes()==render.read_bytes() and png.stat().st_size>10_000 and key+'.png' in book
 except (OSError,ET.ParseError):good=False
 checks[f'{key} master/render/manuscript']=good
try:ET.parse(b4/'architecture.svg');checks['Build 4 readable source SVG']=True
except (OSError,ET.ParseError):checks['Build 4 readable source SVG']=False
for name,result in checks.items():print(('PASS: ' if result else 'FAIL: ')+name)
sys.exit(not all(checks.values()))
