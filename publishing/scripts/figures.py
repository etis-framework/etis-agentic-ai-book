#!/usr/bin/env python3
"""Regenerate vector and compatibility renders from all DOT masters."""
from pathlib import Path
import shutil,subprocess,sys
try:
 import cairosvg
except ImportError:
 cairosvg=None
root=Path(__file__).resolve().parents[2]
if not shutil.which('dot'): sys.exit('Graphviz dot not found (brew install graphviz)')
src=root/'assets/shared-figures/sources'; dst=root/'assets/shared-figures/rendered';dst.mkdir(parents=True,exist_ok=True)
for p in sorted(p for p in src.glob('*.dot') if not p.name.startswith('._')):
 if (src/(p.stem+'.svg')).exists(): continue  # SVG master supersedes legacy DOT
 for ext,flags in [('svg',['-Tsvg']),('png',['-Tpng','-Gdpi=180'])]:
  subprocess.run(['dot',*flags,str(p),'-o',str(dst/(p.stem+'.'+ext))],check=True)
for p in sorted(p for p in src.glob('*.svg') if not p.name.startswith('._')):
 if p.name.startswith('F04-') and not cairosvg:
  sys.exit('Chapter 4 SVG master requires cairosvg for a fresh PNG render; never reuse an old PNG')
 shutil.copy2(p,dst/p.name)
 if cairosvg:
  cairosvg.svg2png(url=str(p),write_to=str(dst/(p.stem+'.png')),output_width=1800)
 elif not (dst/(p.stem+'.png')).exists():
  sys.exit(f'Missing PNG for {p.name}; install cairosvg to regenerate')
print('Rendered DOT and SVG master figures to SVG and PNG')
