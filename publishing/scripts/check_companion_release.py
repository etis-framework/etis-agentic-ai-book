#!/usr/bin/env python3
"""Cross-platform, standard-library-only companion test runner.

Does not build or edit the manuscript, call a provider, or write evidence files.
"""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
COMPANION = ROOT / 'examples' / 'refund-reference-system'
SUITES = ('build0','build1','build2','build3','build4','build5',
          'reliability','security','operations','assurance')


def main() -> int:
    print('ETIS first-edition companion verification (local fixtures only)', flush=True)
    print(f'Python: {sys.version.split()[0]} | Source: {ROOT}', flush=True)
    for suite in SUITES:
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
    print('\nPASS: all 10 local fixture suites and architecture/documentation check.', flush=True)
    print('Not tested: live payment providers, protected credentials, OS isolation,')
    print('E5-side owner fencing, independent audit custody or production certification.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
