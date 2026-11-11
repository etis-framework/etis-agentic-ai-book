#!/usr/bin/env python3
"""Assemble Markdown book; explicit publishing order, no Pandoc TOC preface."""
import argparse,pathlib,re,shutil,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[2]
CHAPTERS=list((ROOT/'manuscript').glob('part-*/ch*/index.md'))
def order(p):
 m=re.search(r'/ch(\d+)-',str(p));return int(m.group(1)) if m else 999
CHAPTERS.sort(key=order)
FRONT=['half-title','title','copyright','contents','preface','introduction','how-to-use-this-book']
BACK=['appendices','glossary','bibliography','index','about-the-author']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--chapter',type=int);ap.add_argument('--format',choices=['docx','pdf','html'],default='docx');args=ap.parse_args()
 if args.chapter:
  files=[p for p in CHAPTERS if order(p)==args.chapter]
  if not files:raise SystemExit('Unknown chapter')
 else:
  files=[ROOT/'manuscript/frontmatter'/f'{n}.md' for n in FRONT]
  for part in sorted((ROOT/'manuscript').glob('part-*')):
   files.append(part/'_part.md');files.extend(sorted(part.glob('ch*/index.md'),key=order))
  files +=[ROOT/'manuscript/backmatter'/f'{n}.md' for n in BACK]
 missing=[str(p) for p in files if not p.exists()]
 if missing:raise SystemExit('Missing book sources:\n'+'\n'.join(missing))
 out=ROOT/'dist';out.mkdir(exist_ok=True)
 name=f'chapter-{args.chapter:02d}' if args.chapter else 'etis-agentic-ai-book';dest=out/f'{name}.{args.format}'
 cmd=['pandoc',*map(str,files),'--standalone','--resource-path='+str(ROOT),'-o',str(dest)]
 if args.format=='pdf':
  engine=next((x for x in ['xelatex','lualatex','pdflatex'] if shutil.which(x)),None)
  if not engine:raise SystemExit('PDF requires LaTeX engine; use DOCX/HTML otherwise.')
  cmd+=['--pdf-engine='+engine]
 if args.format=='docx' and (ROOT/'publishing/templates/reference.docx').exists():cmd+=['--reference-doc='+str(ROOT/'publishing/templates/reference.docx')]
 subprocess.run(cmd,check=True,cwd=ROOT)
 if args.format=='docx' and not args.chapter:
  subprocess.run([sys.executable,str(ROOT/'publishing/scripts/paginate_docx.py'),str(dest)],check=True)
  # Keep the illustrative delegation contract legible and consistently monospaced.
  from docx import Document
  from docx.shared import Inches,Pt,RGBColor
  doc=Document(dest)
  for para in doc.paragraphs:
   if para.style.name=='Source Code' and 'case_id: CASE-204' in para.text:
    para.paragraph_format.left_indent=Inches(0.20)
    para.paragraph_format.right_indent=Inches(0.05)
    para.paragraph_format.space_before=Pt(6)
    para.paragraph_format.space_after=Pt(6)
    for run in para.runs:
     run.font.name='Consolas'
     run.font.size=Pt(8.5)
     run.font.color.rgb=RGBColor(32,60,77)
  doc.save(dest)
 print(dest)
if __name__=='__main__':main()
