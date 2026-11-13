#!/usr/bin/env python3
"""Book-wide print-width and executable shell-fence regression check."""
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[2]
errors = []
checked = 0
for path in sorted((root / "manuscript").rglob("*.md")):
    text = path.read_text(encoding="utf-8")
    for match in re.finditer(r"^```([^\n]*)\n(.*?)^```[ \t]*$", text, re.M | re.S):
        language = match.group(1).strip().lower()
        lines = match.group(2).splitlines()
        checked += 1
        # 8.2pt Consolas on a 7x10 page with the shared indents: conservative.
        # Configuration may have additional punctuation but still fits this limit.
        for number, line in enumerate(lines, 1):
            if len(line.expandtabs(4)) > 68:
                errors.append(f"{path.relative_to(root)} fence {checked}, line {number}: {len(line)} columns")
        if language in {"sh", "bash", "shell"}:
            for number, line in enumerate(lines[:-1], 1):
                if line.rstrip().endswith("\\") and not lines[number].strip():
                    errors.append(f"{path.relative_to(root)} line {number}: blank continuation target")
            if lines and lines[-1].rstrip().endswith("\\"):
                errors.append(f"{path.relative_to(root)}: unterminated shell continuation")

build = (root / "publishing/scripts/build.py").read_text()
for token in ("para.style.name != 'Source Code'", "para.paragraph_format.left_indent", "w:shd", "w:left"):
    if token not in build:
        errors.append(f"DOCX source-code styling missing: {token}")
for item in errors:
    print("FAIL", item)
print(f"{'FAIL' if errors else 'PASS'}: {checked} fenced manuscript blocks checked for 7x10 printing")
sys.exit(bool(errors))
