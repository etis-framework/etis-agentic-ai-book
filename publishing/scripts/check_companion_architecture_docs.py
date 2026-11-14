#!/usr/bin/env python3
"""Companion reader-entry and architecture documentation guard (Builds 0–4).

This deterministic check catches missing diagrams, misleading security claims,
wrong tree entries and broken local Markdown file links. It does not establish
that diagrams are true to executable code; human six-lens review remains required.
"""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "examples/refund-reference-system"
errors = []
main = (DOCS / "README.md").read_text(encoding="utf-8")
architecture = (DOCS / "ARCHITECTURE.md").read_text(encoding="utf-8")
testing = (DOCS / "TESTING.md").read_text(encoding="utf-8")

for build in range(5):
    d = DOCS / f"build{build}"
    readme = d / "README.md"
    diagram = d / "architecture.svg"
    try:
        body = readme.read_text(encoding="utf-8")
        ET.parse(diagram)
        if "(architecture.svg)" not in body:
            errors.append(f"Build {build}: README does not embed architecture.svg")
        if "does **not** establish" not in body and build < 3:
            errors.append(f"Build {build}: source diagram lacks isolation caveat")
        if f"build{build}/" not in main:
            errors.append(f"root README tree omits Build {build}")
        if f"build{build}/architecture.svg" not in architecture:
            errors.append(f"architecture index omits Build {build} diagram")
    except (OSError, ET.ParseError) as exc:
        errors.append(f"Build {build}: {exc}")

for source in [DOCS / "README.md", DOCS / "ARCHITECTURE.md", DOCS / "TESTING.md"] + [DOCS / f"build{i}" / "README.md" for i in range(5)]:
    body = source.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", body):
        if target.startswith(("http:", "https:", "mailto:", "#")):
            continue
        rel = target.split("#")[0]
        if rel and not (source.parent / rel).exists():
            errors.append(f"broken Markdown link in {source.relative_to(ROOT)}: {target}")

for text, phrase, location in [
    (main, "durable operational state (E7)", "root README E7 first reference"),
    (main, "simulated authoritative payment-provider record (E8)", "root README E8 first reference"),
    (architecture, "logical enterprise responsibilities (E1–E9)", "architecture domain definition"),
    (testing, "trusted execution (E5)", "testing gate description"),
    ((DOCS / "build3" / "README.md").read_text(encoding="utf-8"), "same OS user", "Build 3 threat caveat"),
]:
    if phrase not in text:
        errors.append(f"missing: {location}")

if "*independently protected* E5" in (DOCS / "build2" / "README.md").read_text(encoding="utf-8"):
    errors.append("Build 2 falsely claims protected E5 boundary")
if "Independent E5 consequential execution gate" in (DOCS / "build3" / "README.md").read_text(encoding="utf-8"):
    errors.append("Build 3 header overstates process isolation")
for name in ["client.py", "contracts.py", "service.py", "demo.py", "test_gate.py"]:
    if name not in main:
        errors.append(f"root README missing Build 3 module {name}")

build3 = (DOCS / "build3" / "README.md").read_text(encoding="utf-8")
for phrase in ("absolute 0.75-second frame deadline", "aborted connections", "per-principal admission quotas", "refund.prepare()"):
    if phrase not in build3:
        errors.append(f"Build 3 missing transport/ordering explanation: {phrase}")
service = (DOCS / "build3" / "service.py").read_text(encoding="utf-8")
for phrase in ("FRAME_DEADLINE_SECONDS", "time.monotonic()", "serve_connection(", "ConnectionResetError"):
    if phrase not in service:
        errors.append(f"Build 3 transport hardening missing: {phrase}")
# Chapter 26 must introduce the provider's simulated guarantees explicitly,
# and name the modules and evidence a reader can inspect.
b4=(DOCS/'build4'/'README.md').read_text(encoding='utf-8')
for term in ('provider_contracts.py','adapter.py','ledger.py','workflow.py','service.py',
             'reconcile()', 'NOT_FOUND', 'UNKNOWN', 'same-UID', '86,400'):
    if term.lower() not in b4.lower():
        errors.append(f'Build 4 missing explanation: {term}')

for err in errors:
    print("FAIL:", err)
print(f"Companion architecture/documentation QA: {'FAIL' if errors else 'PASS'}; {len(errors)} issue(s)")
sys.exit(bool(errors))

