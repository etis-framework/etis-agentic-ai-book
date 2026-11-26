#!/usr/bin/env python3
"""Check local inline Markdown link targets in active reader documentation.

No network access; does not validate external URLs, Markdown anchor semantics,
reference-style links, or historical manuscript and authoring records.
"""
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
COMPANION = ROOT / 'examples/refund-reference-system'
LINK = re.compile(r'\[[^]\n]+\]\(([^)\n]+)\)')


def main() -> int:
    paths = sorted(set(ROOT.glob('*.md')) | set((ROOT / 'docs').rglob('*.md'))
                   | set(COMPANION.rglob('*.md')))
    checked = 0
    errors = []
    for path in paths:
        for target in LINK.findall(path.read_text(encoding='utf-8')):
            parts = urlsplit(target)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            rel = unquote(parts.path)
            destination = ((ROOT / rel.lstrip('/')) if rel.startswith('/')
                           else (path.parent / rel)).resolve()
            checked += 1
            if not destination.is_relative_to(ROOT) or not destination.exists():
                errors.append(f'{path.relative_to(ROOT)}: unresolved local target {target}')
    for error in errors:
        print('FAIL:', error)
    print(f'Active reader links: {"FAIL" if errors else "PASS"}; '
          f'{len(paths)} documents, {checked} local targets, {len(errors)} findings')
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
