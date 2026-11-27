# SPDX-License-Identifier: Apache-2.0
"""Review-only applicability hints. Never grants release authority."""
CAPS = {'CapInh', 'CapPrm', 'CapEff', 'CapBnd', 'CapAmb'}
PATHS = {'/usr/bin/infocmp', '/usr/lib/systemd/systemd-homed', '/lib/systemd/systemd-homed', '/usr/bin/homectl'}
COMMANDS = {'infocmp', 'systemd-homed', 'homectl', 'perl', 'curl'}


def validate_probe(probe, role, arch, image_id):
    def require(ok):
        if not ok:
            raise ValueError('invalid or inconsistent applicability evidence')
    require(probe['schema_version'] == 1 and (probe['role'], probe['architecture'], probe['image_id']) == (role, arch, image_id))
    require(type(probe['uid']) is int and probe['uid'] > 0)
    require(set(probe['capabilities']) == CAPS and all(type(v) is int and v == 0 for v in probe['capabilities'].values()))
    require(type(probe['no_new_privileges']) is int and probe['no_new_privileges'] == 1)
    require(type(probe['seccomp']) is int and probe['seccomp'] == 2)
    require(set(probe['paths']) == PATHS and all(type(v) is bool for v in probe['paths'].values()))
    require(set(probe['commands']) == COMMANDS and all(v is None or isinstance(v, str) and v.startswith('/') for v in probe['commands'].values()))
    require(isinstance(probe['commands']['perl'], str))
    for key in ('sqlite_options', 'perl_inc', 'perl_archive_paths', 'fstab_entries'):
        require(isinstance(probe[key], list) and all(isinstance(x, str) and x for x in probe[key]))
    require(bool(probe['sqlite_options']) and bool(probe['perl_inc']) and all(x.startswith('/') for x in probe['perl_inc']))
    require(all(isinstance(probe[k], str) and probe[k] for k in ('sqlite_version', 'openssl_version')))
    require((probe['curl_version'] is None and probe['commands']['curl'] is None) or
            (isinstance(probe['curl_version'], str) and bool(probe['curl_version']) and probe['commands']['curl'] is not None))
    return probe


def review_hint(cve, package, role, probe):
    # Only specific package families, and only positive observed absence of named paths.
    # These are review candidates, NOT OpenVEX statements or final reachability proofs.
    if cve == 'CVE-2026-16742' and package in {'libsystemd0', 'libudev1'}:
        if not any(probe['paths'][p] for p in PATHS if 'homed' in p or 'homectl' in p) and all(probe['commands'][n] is None for n in ('systemd-homed', 'homectl')):
            return 'candidate_service_absent'
    if cve == 'CVE-2026-9538' and package == 'perl-base' and not probe['perl_archive_paths']:
        return 'candidate_module_absent_from_default_inc'
    if cve == 'CVE-2025-69720' and package in {'libncursesw6', 'libtinfo6', 'ncurses-base', 'ncurses-bin'}:
        if role == 'companion' and not probe['paths']['/usr/bin/infocmp'] and probe['commands']['infocmp'] is None:
            return 'candidate_cli_absent_from_standard_location_and_path'
    return 'review_required'
