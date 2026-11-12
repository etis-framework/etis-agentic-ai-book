#!/usr/bin/env python3
"""ETIS V12 planning ledger and evidence-qualified 7x10 pagination forecast.

Optional measured page evidence: --actual-pages PATH. JSON shape:
 {"trim":"7x10", "source":"LibreOffice/Word build identifier", "verified":true,
  "chapters":{"1":13,"2":18,...}, "supporting_pages_actual":null}
Only use `verified:true` for inspected rendered chapter extents; source must be nonblank.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARTS = [(1,7,'I'),(8,16,'II'),(17,21,'III'),(22,27,'IV'),(28,31,'V'),(32,34,'VI'),(35,36,'VII')]
P = argparse.ArgumentParser()
P.add_argument('--actual-pages', type=Path, help='Inspected 7x10 page counts with provenance')
args = P.parse_args()
errors = []
x = json.loads((ROOT/'publishing/SINGLE_VOLUME_FINISHED_PAGE_LEDGER_V12.json').read_text())
w = json.loads((ROOT/'publishing/SINGLE_VOLUME_BUDGET_V10.json').read_text())
chapters = x['chapter_pages']
if set(chapters) != {str(i) for i in range(1,37)}:
    errors.append('V12 ledger does not cover precisely chapters 1-36')
if set(x['part_pages']) != {z for _,_,z in PARTS}:
    errors.append('V12 must contain all seven parts')
for start, end, name in PARTS:
    if sum(chapters.get(str(i),0) for i in range(start,end+1)) != x['part_pages'].get(name):
        errors.append(f'Part {name} does not reconcile')
if sum(chapters.values()) != x['chapter_total_pages'] or x['chapter_total_pages'] != 485:
    errors.append('Chapter allocations must total 485')
if sum(x['supporting_pages'].values()) != x['front_back_reserve_pages'] or x['front_back_reserve_pages'] != 65:
    errors.append('Supporting material allocations must total 65')
total = sum(chapters.values()) + x['front_back_reserve_pages']
if total != x['target_finished_pages'] or total != 550:
    errors.append(f'V12 total {total} must equal 550')
policy = x['policy']
if (policy['preferred_max'],policy['planning_limit'],policy['absolute_max']) != (575,600,700):
    errors.append('Publishing thresholds must be 575 / 600 / 700')
if not policy.get('underruns_are_contingency') or not policy.get('overrun_requires_compensating_allocation'):
    errors.append('Non-spend and overrun controls not enabled')
for chapter in (ROOT/'manuscript').glob('part-*/ch*/index.md'):
    match = re.search(r'ch(\d+)-',str(chapter))
    if not match: continue
    n = int(match.group(1))
    count = len(re.findall(r"\b[\w'-]+\b",chapter.read_text()))
    if count > w['chapter_word_caps'][str(n)]:
        errors.append(f'Chapter {n} exceeds existing word cap: {count}')
print(f'V12 LOCKED PLAN: {sum(chapters.values())} chapter + {x["front_back_reserve_pages"]} supporting = {total} pages; preferred <=575; escalation >575; planning limit 600')
if args.actual_pages:
    data = json.loads(args.actual_pages.read_text())
    if data.get('trim') != '7x10' or data.get('verified') is not True or not str(data.get('source','')).strip():
        errors.append('Actual pagination evidence must declare trim=7x10, verified=true, and a nonempty inspected build source')
    actual = data.get('chapters',{})
    if not actual or any(k not in chapters or type(v) is not int or v <= 0 for k,v in actual.items()):
        errors.append('Actual chapter page counts must be positive integers for known chapters')
    if actual and sorted(map(int,actual)) != list(range(1,max(map(int,actual))+1)):
        errors.append('Actual chapter page counts must be contiguous from chapter 1')
    remaining = sum(v for k,v in chapters.items() if k not in actual)
    support_actual=data.get('supporting_pages_actual')
    if support_actual is not None and (type(support_actual) is not int or support_actual < 0):
        errors.append('supporting_pages_actual must be a nonnegative integer or null')
    supporting = x['front_back_reserve_pages'] if support_actual is None else support_actual
    forecast = sum(actual.values())+remaining+supporting
    print(f'RENDERED-BASED FORECAST: completed chapters={len(actual)} actual={sum(actual.values())}, remaining allocation={remaining}, supporting={supporting} ({"reserved" if support_actual is None else "measured"}), projected total={forecast}')
    for k,v in sorted(actual.items(),key=lambda t:int(t[0])):
        if v>chapters[k]: print(f'OVER ALLOCATION: Chapter {k}: {v} actual vs {chapters[k]} budget (+{v-chapters[k]})')
    if forecast>700: errors.append(f'ABSOLUTE CEILING BREACH: {forecast}>700')
    elif forecast>600: errors.append(f'PLANNING LIMIT BREACH: {forecast}>600')
    elif forecast>575: errors.append(f'PREFERRED MAX BREACH: {forecast}>575; reallocation required')
    elif forecast>550: print(f'NOTICE: forecast {forecast} exceeds 550 target by {forecast-550} pages; seek savings')
else:
    print('ACTUAL PAGINATION: NOT PROVIDED — this validates allocations and words, not the final print forecast')
if errors:
    for e in errors: print('FAIL:',e)
    sys.exit(1)
print('PASS: V12 allocation controls reconcile'+(' and provided rendered forecast is within thresholds' if args.actual_pages else ' (rendered measurement still required)'))
