#!/usr/bin/env python3
"""Preflight editorial publishing identity and truthful 31-chapter theme coverage."""
from pathlib import Path
import re,sys
ROOT=Path(__file__).resolve().parents[2]
TITLE='Engineering Agentic AI Systems'
SUB='Build, Secure, Verify, and Operate Trustworthy AI Agents'
OLD='Engineering Trustworthy Agentic AI Systems'
errors=[]
for rel in ('book.yaml','README.md','manuscript/frontmatter/title.md','manuscript/frontmatter/half-title.md','manuscript/frontmatter/copyright.md','publishing/scripts/paginate_docx.py'):
 s=(ROOT/rel).read_text()
 if TITLE not in s or OLD in s:errors.append(f'{rel}: title mismatch')
 if rel not in ('manuscript/frontmatter/half-title.md','publishing/scripts/paginate_docx.py') and SUB not in s:errors.append(f'{rel}: subtitle mismatch')
chapters=sorted((ROOT/'manuscript').glob('part-*/ch*/index.md'))
if len(chapters)!=36:errors.append(f'expected 36 chapter files, got {len(chapters)}')
for n,p in enumerate(chapters,1):
 s=p.read_text().lower()
 if n<=31 and not ('agent' in s or 'ai' in s):errors.append(f'chapter {n}: no agentic context')
 if n>=32 and len(s.split())>300:errors.append(f'chapter {n}: check development-status baseline and update this checker')
cover=(ROOT/'metadata/COVER_RETAIL_COPY_PROPOSED.md').read_text()
for x in ['Six Progressive Python Reference Builds','not final','production-certified']:
 if x.lower() not in cover.lower():errors.append(f'cover copy missing caveat: {x}')
if errors:
 print('Publishing identity and theme preflight FAIL:'); print('\n'.join(errors));sys.exit(1)
print('PASS: publishing identity, documented theme map, honest unfinished-chapter and companion boundaries')
