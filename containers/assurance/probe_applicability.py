#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Observe bounded runtime facts in the exact image selected by the host scanner.
No exploits, network requests, modifications, or vulnerability authorizations.
"""
import json
import os
from pathlib import Path
import platform
import shutil
import sqlite3
import ssl
import subprocess
import sys


def exists(path):
    try:
        path.lstat()
        return True
    except FileNotFoundError:
        return False


def observe(role, image_id):
    arch = {'x86_64': 'amd64', 'aarch64': 'arm64'}[platform.machine()]
    status = dict(line.split(':', 1) for line in Path('/proc/self/status').read_text().splitlines() if ':' in line)
    caps = {k: int(status[k].strip(), 16) for k in ('CapInh', 'CapPrm', 'CapEff', 'CapBnd', 'CapAmb')}
    with sqlite3.connect(':memory:') as db:
        options = sorted(row[0] for row in db.execute('PRAGMA compile_options'))
    paths = {str(p): exists(p) for p in map(Path, (
        '/usr/bin/infocmp', '/usr/lib/systemd/systemd-homed',
        '/lib/systemd/systemd-homed', '/usr/bin/homectl'))}
    commands = {name: shutil.which(name) for name in ('infocmp', 'systemd-homed', 'homectl', 'perl', 'curl')}
    # Inspect Perl's actual default module resolution without loading the module.
    # A failing Perl invocation is an error, not evidence of absence.
    perl = subprocess.run(['perl', '-e', 'for (@INC) { die "non-path INC" if ref($_); print "$_\\n" }'],
                          capture_output=True, text=True, check=True, timeout=10)
    inc = perl.stdout.splitlines()
    if not inc or not all(Path(p).is_absolute() for p in inc):
        raise ValueError('unexpected Perl search path')
    archive_paths = []
    for base in inc:
        path = Path(base) / 'Archive/Tar.pm'
        try:
            path.lstat()
        except FileNotFoundError:
            continue
        archive_paths.append(str(path))
    curl = None
    if commands['curl']:
        curl = subprocess.run([commands['curl'], '--version'], capture_output=True,
                              text=True, check=True, timeout=10).stdout
    return dict(schema_version=1, image_id=image_id, role=role, architecture=arch,
                uid=os.getuid(), capabilities=caps, no_new_privileges=int(status['NoNewPrivs']),
                seccomp=int(status['Seccomp']), sqlite_version=sqlite3.sqlite_version,
                sqlite_options=options, openssl_version=ssl.OPENSSL_VERSION,
                paths=paths, commands=commands, perl_inc=inc, perl_archive_paths=archive_paths,
                curl_version=curl, fstab_entries=[x for x in Path('/etc/fstab').read_text().splitlines()
                                                  if x.strip() and not x.lstrip().startswith('#')])


if __name__ == '__main__':
    print(json.dumps(observe(sys.argv[1], sys.argv[2]), sort_keys=True))
