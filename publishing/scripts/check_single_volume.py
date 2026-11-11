#!/usr/bin/env python3
"""V10 mandatory single-volume, figure, and continuity gates."""
import json,re,sys,pathlib,subprocess
R=pathlib.Path(__file__).resolve().parents[2]
B=json.loads((R/'publishing/SINGLE_VOLUME_BUDGET_V10.json').read_text())
fail=[]; report=[]; total=0
for p in sorted((R/'manuscript').glob('part-*/ch*/index.md')):
 m=re.search(r'ch(\d+)-',str(p));
 if not m:continue
 n=int(m.group(1));txt=p.read_text();words=len(re.findall(r"\b[\w'-]+\b",txt));total+=words;cap=B['chapter_word_caps'][str(n)]
 status='PASS' if words<=cap else 'FAIL';report.append(f'Chapter {n:02d}: {words} / {cap} words — {status}')
 if words>cap:fail.append(f'Chapter {n} exceeds cap by {words-cap} words')
 if re.search(r'\bE[1-9]\s*[–-]\s*E[1-9]\b',txt):fail.append(f'Chapter {n}: opaque E-number range')
for name in ['F03-01','F03-02','F03-03','F03-04']:
 dot=R/f'assets/shared-figures/sources/{name}.dot';svg=R/f'assets/shared-figures/rendered/{name}.svg';png=R/f'assets/shared-figures/rendered/{name}.png'
 if not ((dot.exists() or (R/f'assets/shared-figures/sources/{name}.svg').exists()) and svg.exists() and png.exists()):fail.append(f'{name} missing asset');continue
 if not dot.exists():
  import xml.etree.ElementTree as ET
  master=R/f'assets/shared-figures/sources/{name}.svg'
  try: ET.parse(master)
  except Exception as e: fail.append(f'{name}: SVG invalid: {e}')
  continue
 src=dot.read_text();fs=[int(x) for x in re.findall(r'fontsize\s*=\s*(\d+)',src)]
 if not fs or min(fs)<22:fail.append(f'{name}: label font below 22pt in source')
 try:subprocess.run(['dot','-Tsvg',str(dot),'-o','/dev/null'],check=True,capture_output=True)
 except Exception as e:fail.append(f'{name}: DOT failed: {e}')
report.append(f'Current draft source words: {total}; finished pages not certified from source counts.')
report.append(f'Full-book planning allocation: {sum(B["chapter_word_caps"].values())} source words; working target {B["target_finished_pages"]} pages; HARD MAX {B["absolute_max_pages"]}.')
report.append('Rendered DOCX print-page, font effective-size and human technical figure checks remain separate required gates.')
print('\n'.join(report));print('\nFAILURES: '+ ('; '.join(fail) if fail else 'none'))
sys.exit(1 if fail else 0)
