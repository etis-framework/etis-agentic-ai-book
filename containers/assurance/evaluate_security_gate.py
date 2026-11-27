#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Strict evidence reconciliation. Assessment records cannot grant authority."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from applicability import validate_probe, review_hint

SEVERITIES = {"UNKNOWN", "LOW", "MEDIUM", "HIGH", "CRITICAL"}
ID = re.compile(r"sha256:[0-9a-f]{64}\Z")
FIELDS = ("role", "architecture", "cve", "package", "version")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON member: " + key)
        result[key] = value
    return result


def parse_json(raw):
    return json.loads(raw, object_pairs_hook=unique_object,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def read_json(path):
    return parse_json(path.read_bytes())


def load_register(path):
    data = read_json(path)
    require(data["schema_version"] == 1, "unsupported register schema")
    records = {}
    for row in data["assessments"]:
        key = tuple(row[k] for k in FIELDS)
        require(all(isinstance(x, str) and x for x in key), "invalid assessment key")
        require(key[0] in {"companion", "dev"} and key[1] in {"amd64", "arm64"}, "invalid scope")
        require(re.fullmatch(r"CVE-\d{4}-\d{4,}", key[2]), "invalid CVE")
        require(key not in records, "duplicate assessment")
        require(row["status"] == "under_investigation", "unapproved disposition in draft register")
        require(isinstance(row["rationale"], str) and row["rationale"].strip(), "missing rationale")
        records[key] = row
    return records


def evaluate(directory, role, architecture, expected_id, register, risks):
    require(role in {"companion", "dev"} and architecture in {"amd64", "arm64"}, "invalid requested scope")
    require(ID.fullmatch(expected_id), "invalid expected image ID")
    # No authority has been approved: even syntactically valid acceptance records are rejected.
    require(read_json(risks) == {"schema_version": 1, "acceptances": []}, "risk authority not enabled")
    records = load_register(register)
    paths = {suffix: directory / f"{role}-{suffix}" for suffix in
             ("image.txt", "packages.tsv", "sbom.json", "vulnerabilities.json", "hardening.txt", "applicability.json")}
    blobs = {key: path.read_bytes() for key, path in paths.items()}
    identity = blobs["image.txt"].decode().split()
    require(len(identity) == 3 and identity[:2] == [expected_id, "linux/" + architecture]
            and int(identity[2]) > 0, "inventory image identity mismatch")
    probe = validate_probe(parse_json(blobs["applicability.json"]), role, architecture, expected_id)
    report = parse_json(blobs["vulnerabilities.json"])
    meta = report["Metadata"]
    require(report["SchemaVersion"] == 2 and report["ArtifactType"] == "container_image", "invalid report schema")
    require(report["Trivy"]["Version"] == "0.76.2", "unreviewed scanner version")
    require(report["ArtifactName"] == meta["ImageID"] == expected_id, "report image identity mismatch")
    require(meta["ImageConfig"]["architecture"] == architecture and meta["ImageConfig"]["os"] == "linux", "report platform mismatch")
    require(meta["OS"]["Family"] == "debian", "unexpected distribution")
    sbom = parse_json(blobs["sbom.json"])
    require(sbom["bomFormat"] == "CycloneDX" and sbom["metadata"]["component"]["name"] == expected_id, "SBOM image identity mismatch")
    sbom_props = {x["name"]: x["value"] for x in sbom["metadata"]["component"]["properties"] if x["name"] == "aquasecurity:trivy:ImageID"}
    require(sbom_props.get("aquasecurity:trivy:ImageID") == expected_id, "SBOM image property mismatch")
    inventory = set()
    for line in blobs["packages.tsv"].decode().splitlines():
        parts = line.split("\t")
        require(len(parts) == 2 and all(parts), "malformed package inventory")
        name, version = parts
        item = (name.split(":")[0], version)
        require(item not in inventory, "duplicate inventory package")
        inventory.add(item)
    require(inventory, "empty package inventory")
    result = report["Results"]
    require(isinstance(result, list) and result, "missing scan results")
    os_results = [x for x in result if x["Class"] == "os-pkgs" and x["Type"] == "debian"]
    require(len(os_results) == 1, "missing or duplicate Debian result")
    packages = {(p["Name"], p["ID"].split("@", 1)[1]) for p in os_results[0]["Packages"]}
    sbom_packages = {(p["name"], p["version"]) for p in sbom["components"] if p.get("purl", "").startswith("pkg:deb/")}
    require(packages == sbom_packages == inventory, "scan/SBOM/installed inventory mismatch")
    findings = []
    seen = set()
    for group in result:
        # Trivy may omit Vulnerabilities on a clean result. Scanner success is enforced separately by the caller.
        for v in group.get("Vulnerabilities", []):
            severity = v["Severity"]
            require(severity in SEVERITIES, "unknown severity label")
            cve, package, version = (v[k] for k in ("VulnerabilityID", "PkgName", "InstalledVersion"))
            require(all(isinstance(x, str) and x for x in (cve, package, version)), "invalid finding identity")
            if group is os_results[0]:
                require((package, version) in inventory, "finding not in installed inventory")
            key = (role, architecture, cve, package, version)
            require(key not in seen, "duplicate finding identity")
            seen.add(key)
            blocked = severity in {"HIGH", "CRITICAL"}
            assessment = records.get(key)
            findings.append(dict(zip(FIELDS, key), severity=severity,
                                 fixed_version=v.get("FixedVersion") or "", scanner_status=v.get("Status"),
                                 assessment="under_investigation" if assessment else "unassessed",
                                 rationale=assessment["rationale"] if assessment else None,
                                 applicability_hint=review_hint(cve, package, role, probe) if assessment else "review_required",
                                 blocking=blocked))
    expected_hardening = f"PASS: {role} image privilege-bit and target-specific CLI checks"
    hardening = blobs["hardening.txt"].decode().strip() == expected_hardening
    blockers = sum(x["blocking"] for x in findings)
    return {"schema_version": 1, "role": role, "architecture": architecture,
            "image_id": expected_id, "evaluated_at": datetime.now(timezone.utc).isoformat(),
            "scan_created_at": report.get("CreatedAt"),
            "policy": "strict-no-exceptions", "production_certified": False,
            "evidence_sha256": {key: hashlib.sha256(value).hexdigest() for key, value in blobs.items()},
            "hardening_pass": hardening, "severity_counts": dict(Counter(x["severity"] for x in findings)),
            "blocking_findings": blockers, "status": "PASS" if not blockers and hardening else "BLOCKED",
            "findings": findings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("role", choices=("companion", "dev"))
    parser.add_argument("architecture", choices=("amd64", "arm64"))
    parser.add_argument("image_id")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    try:
        result = evaluate(args.directory, args.role, args.architecture, args.image_id,
                          here / "vulnerability-assessments.json", here / "risk-acceptances.json")
    except (ValueError, KeyError, TypeError, AttributeError, IndexError, OSError) as exc:
        result = {"schema_version": 1, "status": "ERROR", "role": args.role,
                  "image_id": args.image_id, "production_certified": False, "error": str(exc)}
    output = args.directory / f"{args.role}-disposition.json"
    with output.open("x") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(f"{args.role}: governance {result['status']}")
    return {"PASS": 0, "BLOCKED": 1, "ERROR": 2}[result["status"]]


if __name__ == "__main__":
    sys.exit(main())
