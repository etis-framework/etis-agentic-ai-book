#!/usr/bin/env python3
"""Preflight chapter-entry readability; lexical checks do not replace human reading.

Checks the objective paragraph, rather than all prose before the next heading,
so adjacent section-orientation notes are not misclassified as objectives.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT = ROOT / "manuscript"
IDENTIFIER = re.compile(r"(?<![A-Za-z0-9])(?:E[1-9]|C0[1-9]|CASE-204|RF-1042)(?![A-Za-z0-9])")
EXPLANATION = {
    22: ("recurring $500 refund case", "RF-1042"),
    23: ("advisory action-proposal contract (C04)", "stable refund-operation identity RF-1042"),
    24: ("context-query contract (C03)", "admission-and-identity (E1)"),
    25: ("advisory action-proposal contract (C04)", "stable consequential-operation identifier RF-1042"),
    26: ("advisory action-proposal contract (C04)", "refund-operation identity, **RF-1042**"),
    27: ("Coordination and durable ownership (E2)", "RF-1042"),
    28: ("CASE-204", "RF-1042"),
    29: ("CASE-204", "RF-1042"),
}
errors = []
checked = 0
for path in sorted(MANUSCRIPT.glob("part-*/ch*/index.md")):
    number = int(path.parent.name[2:4])
    text = path.read_text(encoding="utf-8")
    if number > 29 or "STATUS: PLANNED / NOT DRAFTED" in text:
        continue
    checked += 1
    match = re.search(r"^## Learning objectives\s*\n\s*([^\n]+)", text, flags=re.M)
    if not match:
        errors.append(f"Chapter {number}: missing objective paragraph")
        continue
    objective = match.group(1)
    # Expand only identifiers with nearby descriptive names; bare IDs fail.
    normalized = objective
    for pattern in [r"(?:independent trusted execution and authority|trusted execution and authority|coordination and ownership|enterprise integration|durable operational state|authoritative business systems|authoritative business truth|agent reasoning|context retrieval and provenance|admission and identity|governance and assurance) \(E[1-9]\)", r"(?:advisory action-proposal contract|authorization-decision contract|context contract|operational-state contract|provider-dispatch contract|reconciliation contract|telemetry and evidence contract|work-assignment contract|admission contract) \(C0[1-9]\)"]:
        normalized = re.sub(pattern, "explained responsibility", normalized)
    tokens = IDENTIFIER.findall(normalized)
    if tokens:
        errors.append(f"Chapter {number}: unexplained identifier(s) in learning objectives: {tokens}")
    for required in EXPLANATION.get(number, ()):
        if required not in text[:6000]:
            errors.append(f"Chapter {number}: missing early reader orientation {required!r}")
print(f"Chapter first-reference preflight: {checked} developed chapters; {len(errors)} issue(s)")
for item in errors:
    print("FAIL:", item)
print("Manual chapter-entry semantic review remains mandatory; placeholders not assessed")
sys.exit(bool(errors))
