#!/usr/bin/env python3
"""First-edition, standard-library-only companion test runner.

Full verification is POSIX-only (Build 3 uses Unix-domain sockets).
Use --portable for Builds 0-2 on native Windows. Does not modify manuscript.
"""
from pathlib import Path
import argparse
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
COMPANION = ROOT / 'examples' / 'refund-reference-system'
SUITES = ('build0','build1','build2','build3','build4','build5',
          'reliability','security','operations','assurance')


def main() -> int:
    parser = argparse.ArgumentParser(description='ETIS first-edition fixture verification')
    parser.add_argument('--portable', action='store_true',
                        help='run only Builds 0-2 (portable subset; not full certification)')
    args = parser.parse_args()
    if os.name == 'nt' and not args.portable:
        print('Full verification requires macOS/Linux: E5 uses Unix-domain sockets.\n'
              'On Windows, run with --portable for Builds 0-2 only.', file=sys.stderr)
        return 2
    suites = SUITES[:3] if args.portable else SUITES
    print('ETIS first-edition companion verification (local fixtures only)', flush=True)
    print('Scope: portable Builds 0-2 (NOT full certification)' if args.portable
          else 'Scope: full ten-suite fixture verification', flush=True)
    print(f'Python: {sys.version.split()[0]} | Source: {ROOT}', flush=True)
    for suite in suites:
        cmd = [sys.executable, '-m', 'unittest', 'discover', '-s',
               str(COMPANION / suite), '-p', 'test_*.py', '-v']
        print(f'\n=== {suite}: executing tests ===', flush=True)
        try:
            result = subprocess.run(cmd, cwd=ROOT, check=False)
        except OSError as exc:
            print(f'FAIL {suite}: {exc}', file=sys.stderr)
            return 1
        if result.returncode != 0:
            print(f'FAIL {suite}: exit {result.returncode}', file=sys.stderr)
            return 1
    print('\n=== architecture / documentation source checks ===', flush=True)
    cmd = [sys.executable, str(ROOT / 'publishing/scripts/check_companion_architecture_docs.py')]
    result = subprocess.run(cmd, cwd=ROOT, check=False)
    if result.returncode != 0:
        print(f'FAIL architecture/documentation: exit {result.returncode}', file=sys.stderr)
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
