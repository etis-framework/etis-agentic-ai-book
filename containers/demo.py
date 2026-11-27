"""Run existing educational demonstrations without changing their authority paths."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
COMPANION = ROOT / 'examples/refund-reference-system'
SCENARIOS = {1: (), 2: (), 3: ('--scenario', 'approved'),
             4: ('--scenario', 'lost-ack'), 5: ('--scenario', 'lost-ack')}


def run_build(build: int) -> int:
    if build in SCENARIOS:
        return subprocess.run([sys.executable, str(COMPANION / f'build{build}' / 'demo.py'),
                               *SCENARIOS[build]], cwd=ROOT, check=False).returncode
    # Keep all four steps in the same invocation, with a fresh disposable directory.
    with tempfile.TemporaryDirectory(prefix='etis-build0-') as directory:
        for action, expected in (('prepare', 'AUTHORIZED'), ('dispatch-lost-ack', 'UNKNOWN'),
                                 ('status', 'UNKNOWN'), ('reconcile', 'CONFIRMED')):
            result = subprocess.run([sys.executable, str(COMPANION / 'build0/refund.py'),
                                     action, '--directory', directory], cwd=ROOT,
                                    capture_output=True, text=True, check=False)
            print(result.stdout, end='', flush=True)
            if result.returncode:
                print(result.stderr, end='', file=sys.stderr)
                return result.returncode
            observation = json.loads(result.stdout)
            # Use the actual durable status rather than conflating provider truth with E7.
            local = observation['local']
            status = local[0] if isinstance(local, list) and local else None
            if status != expected:
                print(f'FAIL: {action}: expected {expected}, observed {status}', file=sys.stderr)
                return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', type=int, choices=range(6), required=True)
    return run_build(parser.parse_args().build)


if __name__ == '__main__':
    raise SystemExit(main())
