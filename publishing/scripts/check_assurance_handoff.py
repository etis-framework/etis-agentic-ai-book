#!/usr/bin/env python3
"""Verify Chapters 28–31 handoff anchors against executable unittest definitions.

Static consistency check only. Passing it does not mean the tests have run,
that the diagrams are accurate, or that planned Chapter 29–31 are completed.
"""
import ast
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'examples/refund-reference-system'
DOC = BASE / 'ASSURANCE_HANDOFF_CH28_CH31.md'
errors = []
body = DOC.read_text(encoding='utf-8')
anchors = re.findall(r'`((?:build[0-5]|reliability)/test_[a-z_]+\.py)::(test_[a-z0-9_]+)`', body)
if len(anchors) < 15:
    errors.append(f'expected at least 15 named unittest anchors; found {len(anchors)}')
for rel, method in anchors:
    path = BASE / rel
    if not path.is_file():
        errors.append(f'missing test file: {rel}')
        continue
    tree = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    methods = {node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    if method not in methods:
        errors.append(f'missing unittest method: {rel}::{method}')
for path in (BASE/'README.md', BASE/'TESTING.md', BASE/'IMPLEMENTATION_EVIDENCE_MAP.md'):
    if 'ASSURANCE_HANDOFF_CH28_CH31.md' not in path.read_text(encoding='utf-8'):
        errors.append(f'missing assurance link in {path.relative_to(ROOT)}')
for clause in ('Build 4 E5 **does not consume the E2 epoch**', 'Chapters 28–31', 'CASE-204', 'RF-1042', 'not a new Build 6', 'real provider', 'status-only'):
    if clause not in body:
        errors.append(f'missing claim limitation: {clause}')
for n in range(6):
    guide = BASE/f'build{n}'/'README.md'
    if not guide.is_file() or '(architecture.svg)' not in guide.read_text(encoding='utf-8'):
        errors.append(f'Build {n}: README does not embed source architecture')
print(f"Assurance handoff anchors: {len(anchors)} checked; {'PASS' if not errors else 'FAIL'}")
for error in errors: print('FAIL:', error)
sys.exit(bool(errors))
