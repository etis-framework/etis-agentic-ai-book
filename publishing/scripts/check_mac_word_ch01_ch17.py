#!/usr/bin/env python3
"""Validate the author-reported Word chapter-boundary arithmetic; not a Word renderer."""
from pathlib import Path
import json,sys
r=Path(__file__).resolve().parents[2]
d=json.loads((r/'publishing/evidence/ACTUAL_PAGINATION_MAC_WORD_CH01_CH17_2026-11-12.json').read_text())
a=json.loads((r/'publishing/SINGLE_VOLUME_FINISHED_PAGE_LEDGER_V12.json').read_text())
errors=[]
def check(ok,message):
 if not ok:errors.append(message)
starts=d['chapter_start_word_pages'];part=d['part_start_word_pages'];counts=d['chapters']
check(d.get('trim')=='7x10','Trim mismatch')
check('Word for Mac' in d.get('source',''),'Missing Word measurement provenance')
check(set(counts)=={str(i) for i in range(1,18)},'Chapter set wrong')
check(all(type(v)==int and v>0 for v in counts.values()),'Invalid page counts')
check(all(starts[str(i)]<starts[str(i+1)] for i in range(1,18)),'Nonincreasing chapter starts')
for i in range(1,18):
 n=str(i);end=part['II'] if i==7 else part['III'] if i==16 else starts[str(i+1)]
 check(counts[n]==end-starts[n],f'Chapter {i} boundary mismatch')
check(part['II']<starts['8'] and part['III']<starts['17'],'Part intro boundaries missing')
check(sum(counts.values())==208,'Developed chapter total not 208')
check(sum(a['chapter_pages'][str(i)] for i in range(1,18))==230,'V12 developed allocation changed')
check(sum(a['chapter_pages'].values())==485 and a['front_back_reserve_pages']==65,'V12 baseline changed')
check({n:counts[n]-a['chapter_pages'][n] for n in ('2','3','4')}=={'2':2,'3':3,'4':2},'Chapter exceptions changed')
ch=(r/'manuscript/part-03-patterns/ch17-choosing-deterministic-agentic-and-hybrid-designs/index.md').read_text()
check(ch.count('A logical responsibility does not require an AI model')==1,'Missing deterministic E3 explanation')
check('In Design A, deterministic logic can decide' not in ch,'Redundant Chapter 17 sentence remains')
for e in errors:print('FAIL:',e)
if errors:sys.exit(1)
print('PASS: author-reported Mac Word chapter arithmetic: 208/230; exceptions Ch2 +2, Ch3 +3, Ch4 +2; conditional V12 forecast 528')
print('NOTE: native Word page positions were provided by the author, not independently replicated here')
