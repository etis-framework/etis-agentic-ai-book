#!/usr/bin/env python3
"""Validate binding chapter and part budgets; rendered pagination still needs editorial signoff."""
from pathlib import Path
import json,sys,re
r=Path(__file__).resolve().parents[2]
x=json.loads((r/'publishing/SINGLE_VOLUME_FINISHED_PAGE_LEDGER_V11.json').read_text())
w=json.loads((r/'publishing/SINGLE_VOLUME_BUDGET_V10.json').read_text())
parts=[(1,7,'I'),(8,16,'II'),(17,21,'III'),(22,27,'IV'),(28,31,'V'),(32,34,'VI'),(35,36,'VII')]
errors=[]
if set(x['chapter_pages'])!={str(i) for i in range(1,37)}:errors.append('Ledger does not cover exactly 36 chapters')
if set(x['part_pages'])!={z for _,_,z in parts}:errors.append('Ledger must contain all seven parts')
for lo,hi,name in parts:
 if sum(x['chapter_pages'].get(str(i),0) for i in range(lo,hi+1))!=x['part_pages'].get(name):errors.append(f'Part {name} does not reconcile')
total=sum(x['part_pages'].values())+x['front_back_reserve_pages']
if total!=x['target_finished_pages'] or total!=550:errors.append(f'Ledger total {total} differs from target 550')
if not (total<=x['policy']['preferred_max']<=x['policy']['planning_limit']<=x['policy']['absolute_max']):errors.append('Page thresholds invalid')
for chapter in (r/'manuscript').glob('part-*/ch*/index.md'):
 n=int(re.search(r'ch(\d+)-',str(chapter)).group(1)); count=len(re.findall(r"\b[\w'-]+\b",chapter.read_text()))
 if count>w['chapter_word_caps'][str(n)]:errors.append(f'Chapter {n} exceeds word cap')
print(f'Finished-page ledger: {total} allocated (50 front/back, 500 chapters), 36 chapters, 7 parts')
if errors:print('FAIL: '+'; '.join(errors));sys.exit(1)
print('PASS: budget allocations and source caps reconcile; final printed pagination requires separate measurement')
