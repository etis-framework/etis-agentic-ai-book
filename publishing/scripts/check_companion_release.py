#!/usr/bin/env python3
"""First-edition, standard-library-only companion test runner.

Full verification is POSIX-only (Build 3 uses Unix-domain sockets).
Use --portable for Builds 0-2 on native Windows. Does not modify manuscript.
"""
from pathlib import Path
import argparse
import json
import os
import signal
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
COMPANION = ROOT / 'examples' / 'refund-reference-system'
SUITES = ('build0', 'build1', 'build2', 'build3', 'build4', 'build5',
          'reliability', 'security', 'operations', 'assurance')
# Frozen v1.0.1 fixture counts are lower bounds, not a proof of coverage.
MINIMUM = dict(zip(SUITES, (16, 16, 14, 21, 32, 23, 12, 6, 15, 16)))
TIMEOUT_SECONDS = 120


def execute_suite(directory: Path, minimum: int) -> int:
    """Use unittest's actual result, never a subprocess's textual OK alone."""
    suite = unittest.defaultTestLoader.discover(str(directory), pattern='test_*.py')
    discovered = suite.countTestCases()
    if discovered < minimum:
        raise ValueError(f'discovered {discovered}; expected at least {minimum}')
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if (result.testsRun != discovered or not result.wasSuccessful()
            or result.skipped or result.expectedFailures or result.unexpectedSuccesses):
        raise ValueError('incomplete or nonordinary unittest result: '
                         f'discovered={discovered}, executed={result.testsRun}, '
                         f'failures={len(result.failures)}, errors={len(result.errors)}, '
                         f'skipped={len(result.skipped)}, '
                         f'expected_failures={len(result.expectedFailures)}, '
                         f'unexpected_successes={len(result.unexpectedSuccesses)}')
    return result.testsRun


def suite_worker(name: str, record: Path) -> int:
    try:
        count = execute_suite(COMPANION / name, MINIMUM[name])
        # Fresh result path. An early exit or exception cannot leave a green record.
        with record.open('x', encoding='utf-8') as stream:
            json.dump({'suite': name, 'passed': count}, stream)
    except (ValueError, OSError, ImportError) as exc:
        print(f'FAIL {name}: {exc}', file=sys.stderr, flush=True)
        return 1
    return 0


def read_result(record: Path, name: str, minimum: int) -> int:
    """Require the successful worker's fresh, suite-specific completion record."""
    with record.open(encoding='utf-8') as stream:
        result = json.load(stream)
    if (not isinstance(result, dict) or set(result) != {'suite', 'passed'}
            or result['suite'] != name or type(result['passed']) is not int
            or result['passed'] < minimum):
        raise ValueError('missing or invalid suite completion evidence')
    return result['passed']


def run_child(cmd: list[str]) -> int:
    """Bound runtime. On POSIX, also stop fixture subprocesses on timeout."""
    with subprocess.Popen(cmd, cwd=ROOT, start_new_session=os.name == 'posix') as process:
        try:
            return process.wait(timeout=TIMEOUT_SECONDS)
        except (subprocess.TimeoutExpired, KeyboardInterrupt):
            if os.name == 'posix':
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            else:
                process.kill()
            process.wait()
            raise


def main() -> int:
    parser = argparse.ArgumentParser(description='ETIS first-edition fixture verification')
    parser.add_argument('--portable', action='store_true',
                        help='run only Builds 0-2 (portable subset; not full certification)')
    # Internal worker mode preserves fresh interpreter isolation between suites.
    parser.add_argument('--_suite', choices=SUITES, help=argparse.SUPPRESS)
    parser.add_argument('--_record', type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args._suite is not None or args._record is not None:
        if args._suite is None or args._record is None or args.portable:
            parser.error('invalid internal suite-worker arguments')
        return suite_worker(args._suite, args._record)
    if os.name == 'nt' and not args.portable:
        print('Full verification requires macOS/Linux: E5 uses Unix-domain sockets.\n'
              'On Windows, run with --portable for Builds 0-2 only.', file=sys.stderr)
        return 2
    suites = SUITES[:3] if args.portable else SUITES
    print('ETIS first-edition companion verification (local fixtures only)', flush=True)
    print('Scope: portable Builds 0-2 (NOT full certification)' if args.portable
          else 'Scope: full ten-suite fixture verification', flush=True)
    print(f'Python: {sys.version.split()[0]} | Source: {ROOT}', flush=True)
    total = 0
    # Each invocation gets a fresh directory: no reuse of earlier green evidence.
    with tempfile.TemporaryDirectory(prefix='etis-verification-') as temporary:
        for name in suites:
            record = Path(temporary) / f'{name}.json'
            cmd = [sys.executable, str(Path(__file__).resolve()),
                   '--_suite', name, '--_record', str(record)]
            print(f'\n=== {name}: executing tests ===', flush=True)
            try:
                status = run_child(cmd)
                if status != 0:
                    print(f'FAIL {name}: exit {status}', file=sys.stderr)
                    return 1
                count = read_result(record, name, MINIMUM[name])
            except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
                print(f'FAIL {name}: {exc}', file=sys.stderr)
                return 1
            total += count
            print(f'Verified {name}: {count} ordinary passing tests.', flush=True)
    print(f'Executed {total} ordinary passing tests across {len(suites)} suites.', flush=True)
    print('\n=== architecture / documentation source checks ===', flush=True)
    cmd = [sys.executable, str(ROOT / 'publishing/scripts/check_companion_architecture_docs.py')]
    try:
        status = run_child(cmd)
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f'FAIL architecture/documentation: {exc}', file=sys.stderr)
        return 1
    if status != 0:
        print(f'FAIL architecture/documentation: exit {status}', file=sys.stderr)
        return 1
    if args.portable:
        print('\nPASS: portable Builds 0-2 and architecture/documentation check.', flush=True)
        print('NOT RUN: Builds 3-5 and Chapters 28-31; not a full release certification.')
    else:
        print('\nPASS: all 10 local fixture suites and architecture/documentation check.', flush=True)
    print('Not tested: live payment providers, protected credentials, OS isolation,')
    print('E5-side owner fencing, independent audit custody or production certification.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
