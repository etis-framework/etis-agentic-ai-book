#!/usr/bin/env python3
"""Pass-4 MCP/A2A teaching audit; checks source references, not protocol conformance."""
from pathlib import Path
import re,sys
R=Path(__file__).resolve().parents[2]
E=R/'examples/refund-reference-system'
errors=[]
def require(v,msg):
    if not v: errors.append(msg)
def get(path):
    p=R/path
    require(p.is_file(),f'missing {path}')
    return p.read_text() if p.is_file() else ''
ch=get('manuscript/part-03-patterns/ch19-tools-adapters-and-effect-isolation/index.md')
ch13=get('manuscript/part-02-architecture/ch13-trusted-execution-and-authority-e5/index.md')
study=get('examples/refund-reference-system/PROTOCOL_BOUNDARY_STUDY.md')
root=get('examples/refund-reference-system/README.md')
learn=get('examples/refund-reference-system/LEARNING_PATH.md')
for x in ('host application','MCP client','MCP server','tools/list','tools/call','listChanged','A2A','independent E5','centralized E5','credential'):
    require(x.lower() in ch.lower(),f'chapter 19 missing {x}')
for x in ('E5','protected credential','policy enforcement point','authorization'):
    require(x.lower() in ch13.lower(),f'chapter 13 missing {x}')
for x in ('PROTOCOL_BOUNDARY_STUDY.md','not','conformance'):
    require(x.lower() in root.lower() and x.lower() in (root+learn).lower(),f'companion entry missing {x}')
for x in ('tools/list','tools/call','E5','A2A','not runnable','five falsification','CASE-204'):
    require(x.lower() in study.lower(),f'study missing {x}')
for rel,method in [('build3/test_gate.py','test_valid_agent_token_is_not_payment_approval'),('build4/test_provider.py','test_lost_ack_requires_authoritative_reconciliation')]:
    p=E/rel
    require(p.is_file() and re.search(r'^\s*def '+method+r'\s*\(',p.read_text(),re.M) is not None,f'actual fixture not found {rel}::{method}')
print('Pass 4 protocol-boundary teaching audit:', 'PASS' if not errors else 'FAIL')
for x in errors:print('FAIL',x)
sys.exit(bool(errors))
