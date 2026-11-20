"""Chapter 31 bounded evidence collector for selected existing ETIS unittest fixtures.

Educational evidence only: executes explicitly registered *local* test methods,
records source digests and safe result metadata. It neither signs/attests a host nor
provides an audit authority, provider connection, payment command or security gate.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
VERSION = 'ch31-fixture-evidence-v1'
CASE = 'CASE-204'
OPERATION = 'RF-1042'


@dataclass(frozen=True)
class FixtureCase:
    claim_id: str
    directory: str
    test_id: str
    source_files: tuple[str, ...]
    expected: str
    excluded: str


# Declared, fixed registry. No arbitrary shell commands or user-controlled test paths.
CASES: tuple[FixtureCase, ...] = (
    FixtureCase('AUTH_DENIAL', 'security', 'test_adversarial_cases.HijackedInvestigatorAgainstRealE5.test_valid_identity_without_finance_grant_denied_without_effect', ('security/test_adversarial_cases.py', 'build3/service.py'), 'Local E5 denial and no fixture E7/E8 effect', 'No production credential isolation'),
    FixtureCase('WRONG_PROOF', 'reliability', 'test_recovery_cases.RecoveryTests.test_wrong_operation_proof_escalates', ('reliability/recovery_cases.py', 'reliability/test_recovery_cases.py'), 'Wrong operation evidence cannot confirm RF-1042', 'No real provider settlement proof'),
    FixtureCase('NOT_FOUND', 'reliability', 'test_recovery_cases.RecoveryTests.test_not_found_never_declares_failure', ('reliability/recovery_cases.py', 'reliability/test_recovery_cases.py'), 'Missing provider observation does not prove payment failure', 'No real-world provider consistency'),
    FixtureCase('NO_REPLAY', 'build4', 'test_provider.Build4Test.test_replayed_execute_does_not_call_provider_twice', ('build4/test_provider.py', 'build4/ledger.py', 'build4/adapter.py'), 'Repeated local call makes no second mock effect', 'No global exactly-once guarantee'),
    FixtureCase('STALE_OWNER', 'build5', 'test_coordination.CoordinatorTests.test_stale_owner_cannot_override_new_owner_reconcile', ('build5/coordinator.py', 'build5/test_coordination.py'), 'Old worker rejected at local E2 state', 'E5 does not enforce current E2 epoch'),
    FixtureCase('READ_ONLY', 'operations', 'test_incident.IncidentTests.test_lost_ack_unknown_with_confirmed_synthetic_e8_still_requires_review', ('operations/incident.py', 'operations/test_incident.py'), 'Observer does not create another local effect', 'No protected operational audit'),
    FixtureCase('TELEMETRY_GAP', 'operations', 'test_incident.IncidentTests.test_missing_telemetry_never_closes_case', ('operations/incident.py', 'operations/test_incident.py'), 'Missing signal remains observable and unresolved', 'No guaranteed collector delivery'),
)

# Static declaration is a teaching aid, never automatically turned into implemented evidence.
PRODUCTION_GAPS = (
    {'id': 'E5_EPOCH', 'status': 'NOT_IMPLEMENTED', 'meaning': 'E5 does not independently check E2 current-owner epoch'},
    {'id': 'CREDENTIAL_CUSTODY', 'status': 'EXTERNAL_EVIDENCE_REQUIRED', 'meaning': 'Separate protected credential issuer and OS principal'},
    {'id': 'PROVIDER_SETTLEMENT', 'status': 'EXTERNAL_EVIDENCE_REQUIRED', 'meaning': 'Provider idempotency retention, query consistency and settlement'},
    {'id': 'PROTECTED_AUDIT', 'status': 'NOT_IMPLEMENTED', 'meaning': 'Independent tamper-evident E9 audit custody'},
    {'id': 'AGENT_EVALUATION', 'status': 'SPECIFIED_ONLY', 'meaning': 'Representative AI agent behavior and drift measurement'},
)

ID_PATTERN = re.compile(r'^[A-Z][A-Z0-9_]{2,40}$')
TEST_PATTERN = re.compile(r'^[A-Za-z_]\w*(?:\.[A-Za-z_]\w*){2}$')
SAFE_PATH = re.compile(r'^[a-zA-Z0-9_./-]+$')


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_registry(root: Path, registry: tuple[FixtureCase, ...] = CASES) -> None:
    """Fail closed before running any test on missing or unsafe declared inputs."""
    if not registry or len({c.claim_id for c in registry}) != len(registry):
        raise ValueError('Missing or duplicated claim identity')
    for case in registry:
        if not ID_PATTERN.fullmatch(case.claim_id) or not TEST_PATTERN.fullmatch(case.test_id):
            raise ValueError('Invalid case identifier or exact unittest method')
        if case.directory not in {'build4', 'build5', 'security', 'reliability', 'operations'}:
            raise ValueError('Undeclared fixture directory')
        if not case.source_files or not case.expected or not case.excluded:
            raise ValueError('Incomplete evidence contract')
        for relative in (f'{case.directory}/{case.test_id.split(".")[0]}.py', *case.source_files):
            if not SAFE_PATH.fullmatch(relative) or '..' in Path(relative).parts:
                raise ValueError('Unsafe source pathname')
            target = (root / relative).resolve()
            if not target.is_relative_to(root.resolve()) or not target.is_file():
                raise ValueError('Missing evidence source: ' + relative)


# A green exit without exactly one named test could be a false positive
# (e.g. discovery executed zero tests). The claim is bound to one method.
def result_status(returncode: int | None, completed: bool, test_count: int) -> str:
    """A test is green only after clean exit and exactly one executed test."""
    return 'EXECUTED_PASS' if completed and returncode == 0 and test_count == 1 else 'EXECUTED_FAIL'


def run_case(case: FixtureCase, root: Path, timeout: int = 40,
             runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run) -> dict:
    """Execute exact registered unittest method; do not persist subprocess stdout/stderr.

    stdout/stderr may carry secrets if a future test regresses. The report stores
    only an output digest and a bounded reason code, never raw output.
    """
    command = [sys.executable, '-m', 'unittest', '-q', case.test_id]
    state = 'COMPLETED'
    exit_code: int | None = None
    count = 0
    output = b''
    try:
        result = runner(command, cwd=root / case.directory, capture_output=True,
                        text=True, timeout=timeout, check=False)
        exit_code = result.returncode
        output = (result.stdout + '\n' + result.stderr).encode('utf-8', 'replace')
        matches = re.findall(r'\bRan (\d+) tests? in\b', result.stderr)
        count = int(matches[-1]) if matches else 0
    except subprocess.TimeoutExpired as exc:
        state = 'TIMEOUT'
        # Discard potentially sensitive process streams even on timeout.
    except (OSError, ValueError):
        state = 'UNAVAILABLE'
    status = result_status(exit_code, state == 'COMPLETED', count)
    # A digest helps compare outputs without publishing their contents. It is
    # neither a digital signature nor evidence of independent audit custody.
    digest = hashlib.sha256(output).hexdigest() if state == 'COMPLETED' else None
    return {
        'claim_id': case.claim_id,
        'test_id': case.test_id,
        'status': status,
        'execution': state,
        'exit_code': exit_code,
        'tests_run': count,
        'output_sha256': digest,
        'expected_narrow_claim': case.expected,
        'not_established': case.excluded,
        'source_sha256': {p: sha256(root / p) for p in case.source_files},
    }


def collect(root: Path = ROOT, timeout: int = 40) -> dict:
    validate_registry(root)
    entries = [run_case(c, root, timeout=timeout) for c in CASES]
    return {
        'schema': VERSION,
        'generated_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'case': CASE,
        'operation': OPERATION,
        'runtime': {'python': sys.version.split()[0], 'implementation': sys.implementation.name},
        'evidence': entries,
        'production_gaps': list(PRODUCTION_GAPS),
        'overall_fixture_status': 'EXECUTED_PASS' if all(x['status'] == 'EXECUTED_PASS' for x in entries) else 'EXECUTED_FAIL',
        'production_certified': False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='Local JSON evidence output; do not commit environment-specific results')
    parser.add_argument('--timeout', type=int, default=40)
    args = parser.parse_args()
    if args.timeout < 1 or args.timeout > 120:
        parser.error('timeout must be 1–120 seconds')
    if args.output.exists():
        parser.error('refusing to overwrite existing evidence output')
    try:
        report = collect(timeout=args.timeout)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    except (OSError, ValueError) as exc:
        # Expected invalid source/registry cases fail without writing a green report.
        print(f'ERROR: evidence collection unavailable ({type(exc).__name__})', file=sys.stderr)
        return 2
    print(f"{report['overall_fixture_status']}: {len(report['evidence'])} registered local cases; production_certified=false")
    return 0 if report['overall_fixture_status'] == 'EXECUTED_PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
