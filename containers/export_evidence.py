"""Export the original bounded Chapter 31 report on stdout only after success."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from verify import ROOT, runtime_findings

CLAIMS = {'AUTH_DENIAL', 'WRONG_PROOF', 'NOT_FOUND', 'NO_REPLAY',
          'STALE_OWNER', 'READ_ONLY', 'TELEMETRY_GAP'}


def validate_report(report: object) -> None:
    if (not isinstance(report, dict)
            or report.get('schema') != 'ch31-fixture-evidence-v1'
            or report.get('case') != 'CASE-204' or report.get('operation') != 'RF-1042'
            or report.get('production_certified') is not False
            or report.get('overall_fixture_status') != 'EXECUTED_PASS'):
        raise ValueError('invalid or unsuccessful fixture report')
    entries = report.get('evidence')
    if not isinstance(entries, list) or len(entries) != len(CLAIMS):
        raise ValueError('incomplete evidence set')
    seen = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError('invalid evidence entry')
        claim = entry.get('claim_id')
        if (not isinstance(claim, str) or claim not in CLAIMS or claim in seen
                or entry.get('status') != 'EXECUTED_PASS'
                or type(entry.get('tests_run')) is not int or entry['tests_run'] != 1):
            raise ValueError('invalid or unsuccessful evidence entry')
        seen.add(claim)


def main() -> int:
    try:
        findings = runtime_findings()
        if findings:
            raise ValueError('; '.join(findings))
        with tempfile.TemporaryDirectory(prefix='etis-evidence-') as tmp:
            path = Path(tmp) / 'report.json'
            result = subprocess.run([sys.executable, str(ROOT / 'examples/refund-reference-system/assurance/collect.py'),
                                     '--output', str(path)], cwd=ROOT, capture_output=True,
                                    text=True, check=False, timeout=360)
            # Keep the JSON stream distinct from human-readable diagnostics.
            if result.returncode:
                raise ValueError(f'collector failed (exit {result.returncode})')
            report = json.loads(path.read_text(encoding='utf-8'))
            validate_report(report)
            print(json.dumps(report, indent=2, sort_keys=True))
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f'FAIL: evidence export: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
