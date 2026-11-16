#!/usr/bin/env python3
"""Validate format-specific ISBN-13 registration data and book identity.

An ISBN-13 checksum verifies transcription, not ownership, registration, format
eligibility, or external Bowker metadata. Those require publisher approval.
"""
from pathlib import Path
import re, sys
ROOT = Path(__file__).resolve().parents[2]
PAPER = '979-8-9966760-6-4'
HARD = '979-8-9966760-7-1'
errors = []

def valid(isbn):
    digits = re.sub(r'[^0-9]', '', isbn)
    if len(digits) != 13 or not digits.startswith(('978', '979')):
        return False
    check = (10 - sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(digits[:12])) % 10) % 10
    return check == int(digits[12])

if not all(map(valid, (PAPER, HARD))) or PAPER == HARD:
    errors.append('Invalid or duplicate format ISBNs')
copy = (ROOT / 'manuscript/frontmatter/copyright.md').read_text(encoding='utf-8')
config = (ROOT / 'book.yaml').read_text(encoding='utf-8')
identity = (ROOT / 'metadata/PUBLISHING_IDENTITY.md').read_text(encoding='utf-8')
for label, isbn, config_key in [('Paperback', PAPER, 'paperback_isbn'), ('Hardcover', HARD, 'hardcover_isbn')]:
    if f'{label} ISBN: {isbn}' not in copy:
        errors.append(f'Copyright page missing correct {label} ISBN')
    if not re.search(r'^' + config_key + r':\s*' + re.escape(isbn) + r'\s*$', config, re.M):
        errors.append(f'book.yaml missing correct {label} ISBN')
    if isbn not in identity:
        errors.append(f'Publishing identity missing {label} ISBN')
if re.search(r'ISBN:\s*To be assigned', copy, re.I):
    errors.append('Unassigned ISBN placeholder remains in reader-facing copyright')
if errors:
    print('FAIL: print ISBN identity:', '; '.join(errors))
    sys.exit(1)
print('PASS: 2 distinct valid ISBN-13 check digits and synchronized paperback/hardcover front-matter metadata')
