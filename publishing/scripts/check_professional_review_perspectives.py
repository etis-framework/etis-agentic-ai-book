#!/usr/bin/env python3
"""Reader-facing multi-perspective review preflight; human semantics review still required."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT = ROOT / 'manuscript'
STANDARD = ROOT / 'metadata/professional-review-perspectives-standard.md'
ERRORS = []

def check(ok: bool, message: str) -> None:
    if not ok:
        ERRORS.append(message)

check(STANDARD.is_file(), 'Missing professional review perspectives editorial standard')
for n in range(1, 35):
    matches = list(MANUSCRIPT.glob(f'part-*/ch{n:02d}-*/index.md'))
    check(len(matches) == 1, f'Chapter {n} missing or ambiguous')
    if len(matches) != 1:
        continue
    text = matches[0].read_text(encoding='utf-8')
    # Public-facing student exercises remain appropriate; student-as-approval-role does not.
    check(n>=30 or not re.search(r'\badvanced student\s*(?:asks|must|should|:)', text, re.I),
          f'Chapter {n} presents advanced student as an enterprise architecture reviewer')
    if 22 <= n <= 29:
        headings = re.findall(r'^## (.+)$', text, re.M)
        check(('multi-perspective architecture review' in text.lower() or 'professional review' in text.lower()), f'Chapter {n} lacks a multi-perspective architecture review')
        for term in ('implementing engineer', 'enterprise architect', 'security', 'business owner'):
            check(term.lower() in text.lower(), f'Chapter {n} review lacks {term}')
        # The role may be written out for readers instead of abbreviated as SRE.
        # Accept either; do not require an acronym in otherwise clear textbook prose.
        check(bool(re.search(r'\bSRE\b|\bsite[- ]reliability\b|\bsite reliability and operations\b', text, re.I)),
              f'Chapter {n} review lacks SRE/site-reliability perspective')
        check('six-lens' not in text.lower(), f'Chapter {n} exposes internal six-lens QA label')
        check(not re.search(r'^## [^\n]*war.game', text, re.M|re.I),
              f'Chapter {n} exposes internal war-game as reader-facing section heading')
for n in (30, 31):
    p = next(MANUSCRIPT.glob(f'part-*/ch{n:02d}-*/index.md'))
    t = p.read_text(encoding='utf-8').lower()
    for term in ('implementing engineer', 'enterprise architect', 'security', 'business owner', 'site-reliability'):
        check(term in t, f'Chapter {n} lacks professional perspective {term}')
p = next(MANUSCRIPT.glob('part-*/ch33-*/index.md'))
t = p.read_text(encoding='utf-8').lower()
for term in ('implementing engineer', 'enterprise architect', 'security', 'business owner', 'site reliability engineering'):
    check(term in t, f'Chapter 33 lacks professional perspective {term}')
p = next(MANUSCRIPT.glob('part-*/ch34-*/index.md'))
t = p.read_text(encoding='utf-8').lower()
for term in ('implementing engineer', 'enterprise architect', 'security', 'business owner', 'site reliability engineering'):
    check(term in t, f'Chapter 34 lacks professional responsibility {term}')
check(not re.search(r'advanced student|six-lens|reviewer-lens',t), 'Chapter 34 contains internal reviewer taxonomy')
for n in (7, 8, 16, 21):
    p = next(MANUSCRIPT.glob(f'part-*/ch{n:02d}-*/index.md'))
    t = p.read_text(encoding='utf-8').lower()
    check('perspective' in t or 'professional review' in t, f'Chapter {n} lacks targeted review connection')

front = (MANUSCRIPT / 'frontmatter/how-to-use-this-book.md').read_text()
check('Professional review perspectives' in front, 'Missing reader navigation')
check('multi-perspective architecture review' in
      (MANUSCRIPT / 'part-04-implementation/_part.md').read_text().lower(),
      'Missing Part IV bridge')

if ERRORS:
    for issue in ERRORS:
        print('FAIL:', issue)
    raise SystemExit(1)
print('PASS: reader-facing professional review perspectives, Chapters 1–34; '
      'Part IV professional roles separated from internal student QA')
