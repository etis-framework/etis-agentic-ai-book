"""Fail-closed, disposable container verification; not production attestation."""
from pathlib import Path
import os
import re
import socket
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def source_mounts(mountinfo: str, source: Path) -> list[str]:
    """Reject bind/volume mounts at, above or within the image source tree."""
    source = source.resolve()
    overlaps = []
    for line in mountinfo.splitlines():
        fields = line.split()
        if len(fields) < 6:
            raise ValueError('malformed mountinfo')
        # Linux mountinfo escapes whitespace and backslashes as octal sequences.
        mount = Path(re.sub(r'\\([0-7]{3})', lambda m: chr(int(m.group(1), 8)), fields[4]))
        if not mount.is_absolute():
            raise ValueError('nonabsolute mountpoint')
        if mount != Path('/') and (source.is_relative_to(mount) or mount.is_relative_to(source)):
            overlaps.append(str(mount))
    return overlaps


def interface_flags(name: str) -> int:
    """Linux SIOCGIFFLAGS, queried in the process network namespace."""
    import fcntl
    import struct

    encoded = os.fsencode(name)
    if not encoded or len(encoded) >= 16 or b'\x00' in encoded:
        raise ValueError('invalid interface name')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        request = struct.pack('16s24x', encoded)
        result = fcntl.ioctl(sock.fileno(), 0x8913, request)
    return struct.unpack_from('H', result, 16)[0]


def network_findings() -> list[str]:
    """Require loopback and no administratively enabled non-loopback links.

    Linux can instantiate inactive tunnel devices even in a network=none
    namespace. Their names alone do not imply connectivity. Never allow an
    enabled non-loopback device, regardless of its name or carrier state.
    Compose separately requires network_mode: none; this is a runtime check,
    not independent attestation of the host's network configuration.
    """
    try:
        interfaces = {name for _, name in socket.if_nameindex()}
        if 'lo' not in interfaces:
            return ['verification requires loopback interface lo']
        flags = {name: interface_flags(name) for name in sorted(interfaces)}
        if not flags['lo'] & 0x8:  # IFF_LOOPBACK
            return ['lo is not a loopback interface']
        enabled = [name for name, flag in flags.items()
                   if name != 'lo' and flag & 0x1]  # IFF_UP
        if enabled:
            return ['verification has enabled non-loopback interfaces: ' + ', '.join(enabled)]
        if {name for _, name in socket.if_nameindex()} != interfaces:
            return ['network interface inventory changed during inspection']
    except (OSError, ValueError) as exc:
        return [f'network interface enumeration unavailable: {exc}']
    return []


def runtime_findings() -> list[str]:
    errors = []
    if sys.platform != 'linux' or os.geteuid() == 0:
        errors.append('verification requires non-root Linux')
        return errors
    if not os.statvfs(ROOT).f_flag & os.ST_RDONLY:
        errors.append('verification source filesystem must be read-only')
    if not os.statvfs('/').f_flag & os.ST_RDONLY:
        errors.append('verification root filesystem must be read-only')
    overlaps = source_mounts(Path('/proc/self/mountinfo').read_text(), ROOT)
    if overlaps:
        errors.append('verification must use image-contained source, not mounted source: ' + ', '.join(overlaps))
    errors.extend(network_findings())
    status = dict(line.split(':', 1) for line in Path('/proc/self/status').read_text().splitlines() if ':' in line)
    for field in ('CapEff', 'CapPrm', 'CapBnd'):
        if int(status.get(field, '1').strip(), 16) != 0:
            errors.append(f'{field} must be zero')
    if status.get('NoNewPrivs', '').strip() != '1':
        errors.append('no-new-privileges must be enabled')
    if Path('/var/run/docker.sock').exists() or Path('/run/docker.sock').exists():
        errors.append('Docker socket must not be exposed')
    if Path('/state').exists() or Path('/workspace').exists():
        errors.append('development mounts must not appear in verification')
    for folder in ('.git', 'archive', 'review', 'assets', 'dist', '.etis-local'):
        if (ROOT / folder).exists():
            errors.append(f'excluded authoring/local content in image: {folder}')
    with tempfile.TemporaryDirectory(prefix='etis-runtime-') as directory:
        # Exercise Unix sockets, SQLite and subprocesses through the real suites below.
        (Path(directory) / 'write-test').write_text('ok', encoding='utf-8')
    return errors


def main() -> int:
    try:
        errors = runtime_findings()
    except (OSError, ValueError) as exc:
        errors = [f'runtime preflight unavailable: {exc}']
    if errors:
        for error in errors:
            print('FAIL:', error, file=sys.stderr)
        return 1
    print('PASS: offline, non-root, read-only verification runtime preflight', flush=True)
    for script in ('containers/test_container_tools.py',
                   'publishing/scripts/test_companion_release.py',
                   'publishing/scripts/check_companion_release.py',
                   'publishing/scripts/check_active_reader_links.py'):
        result = subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT, check=False)
        if result.returncode:
            print(f'FAIL: {script} exited {result.returncode}', file=sys.stderr)
            return 1
    print('PASS: container runtime, tool regressions, companion suites and reader links.', flush=True)
    print('Educational local fixture verification only; production certification not established.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
