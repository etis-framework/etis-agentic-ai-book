"""Check the ordinary offline development service, not the IDE network overlay."""
from pathlib import Path
import os
import sys
import tempfile
from verify import network_findings


def main() -> int:
    if (sys.platform != 'linux' or os.geteuid() == 0
            or Path.cwd() != Path('/workspace')
            or not Path('/workspace/README.md').is_file()
            or not Path('/state/.etis-state').is_file()
            or Path('/var/run/docker.sock').exists()):
        print('FAIL: development runtime contract', file=sys.stderr)
        return 1
    findings = network_findings()
    if findings:
        print('FAIL: development networking: ' + '; '.join(findings), file=sys.stderr)
        return 1
    try:
        for directory in ('/workspace', '/state'):
            with tempfile.NamedTemporaryFile(dir=directory, prefix='.etis-probe-') as probe:
                probe.write(b'write-probe')
                probe.flush()
    except OSError as exc:
        print(f'FAIL: workspace/state not writable: {exc}', file=sys.stderr)
        return 1
    print('PASS: non-root offline development, writable workspace and project state')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
