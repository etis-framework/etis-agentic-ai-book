#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Reconcile exact scan evidence and enforce bounded maintainer decisions."""
import argparse
from collections import Counter
from datetime import datetime, timezone, timedelta
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


def utc(value):
    require(isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value), "invalid UTC timestamp")
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_acceptances(path, records, now):
    data = read_json(path)
    require(data.get("schema_version") == 1, "unsupported acceptance schema")
    if data == {"schema_version": 1, "acceptances": []}:
        return {}, None
    require(set(data) == {"schema_version", "approval", "acceptances"}, "invalid acceptance register")
    approval = data["approval"]
    require(set(approval) == {"authority", "issued_at", "expires_at", "reviewed_at", "basis_commit", "basis_run", "advisory_scope"}, "invalid approval metadata")
    require(approval["authority"] == "ETIS repository maintainer", "unauthorized acceptance authority")
    require(re.fullmatch(r"[0-9a-f]{40}", approval["basis_commit"]) and type(approval["basis_run"]) is int and approval["basis_run"] > 0, "invalid approval provenance")
    require(approval["advisory_scope"] == "Debian Trixie stable and security", "invalid remediation scope")
    issued, expires, reviewed = (utc(approval[k]) for k in ("issued_at", "expires_at", "reviewed_at"))
    require(reviewed <= issued <= now and issued < expires <= issued + timedelta(days=30), "invalid approval interval")
    require(issued - reviewed <= timedelta(days=1), "stale advisory review at approval")
    decisions = {}
    for row in data["acceptances"]:
        require(set(row) == set(FIELDS) | {"severity", "scanner_status", "fixed_version", "disposition", "applicability_hint", "advisory", "rationale"}, "invalid acceptance fields")
        key = tuple(row[k] for k in FIELDS)
        require(key in records and key not in decisions, "unregistered or duplicate acceptance")
        require(row["severity"] == "HIGH" and row["fixed_version"] == "", "only unfixed high findings eligible")
        require(row["scanner_status"] in {"affected", "fix_deferred"}, "invalid scanner status")
        require(row["advisory"] == "https://security-tracker.debian.org/tracker/" + row["cve"], "invalid advisory reference")
        require(isinstance(row["rationale"], str) and len(row["rationale"].strip()) >= 30, "missing decision rationale")
        require((row["disposition"] == "risk_accepted" and row["applicability_hint"] == "review_required") or
                (row["disposition"] == "limited_absence" and row["applicability_hint"] in {"candidate_service_absent", "candidate_module_absent_from_default_inc", "candidate_cli_absent_from_standard_location_and_path"}), "invalid disposition")
        decisions[key] = row
    require(decisions, "empty populated approval")
    return decisions, approval if now < expires else None


def evaluate(directory, role, architecture, expected_id, register, risks, *, now=None):
    require(role in {"companion", "dev"} and architecture in {"amd64", "arm64"}, "invalid requested scope")
    require(ID.fullmatch(expected_id), "invalid expected image ID")
    now = now or datetime.now(timezone.utc)
    records = load_register(register)
    decisions, approval = load_acceptances(risks, records, now)
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
    # A review of the supported runtime does not extend to privileged or custom configurations.
    require(not probe["fstab_entries"], "unexpected fstab entries")
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
            hint = review_hint(cve, package, role, probe) if assessment else "review_required"
            decision = decisions.get(key)
            disposition = "under_investigation" if assessment else "unassessed"
            rationale = assessment["rationale"] if assessment else None
            if (approval and decision and severity == "HIGH" and not v.get("FixedVersion")
                    and v.get("Status") == decision["scanner_status"] and hint == decision["applicability_hint"]
                    and group is os_results[0]):
                blocked = False
                disposition = decision["disposition"]
                rationale = decision["rationale"]
            findings.append(dict(zip(FIELDS, key), severity=severity,
                                 fixed_version=v.get("FixedVersion") or "", scanner_status=v.get("Status"),
                                 assessment=disposition,
                                 rationale=rationale,
                                 applicability_hint=hint,
                                 blocking=blocked))
    expected_hardening = f"PASS: {role} image privilege-bit and target-specific CLI checks"
    hardening = blobs["hardening.txt"].decode().strip() == expected_hardening
    blockers = sum(x["blocking"] for x in findings)
    return {"schema_version": 1, "role": role, "architecture": architecture,
            "image_id": expected_id, "evaluated_at": datetime.now(timezone.utc).isoformat(),
            "scan_created_at": report.get("CreatedAt"),
            "policy": "bounded-maintainer-acceptance", "production_certified": False,
            "approval": approval, "expired_approval": bool(decisions and not approval),
            "disposition_counts": dict(Counter(x["assessment"] for x in findings if x["severity"] in {"HIGH", "CRITICAL"})),
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
