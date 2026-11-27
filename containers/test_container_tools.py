"""Infrastructure regression tests; no Docker daemon required for these unit tests."""
import copy
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

import demo
import export_evidence
import verify


def report_fixture():
    return {'schema': 'ch31-fixture-evidence-v1', 'case': 'CASE-204',
            'operation': 'RF-1042', 'production_certified': False,
            'overall_fixture_status': 'EXECUTED_PASS',
            'evidence': [{'claim_id': claim, 'status': 'EXECUTED_PASS', 'tests_run': 1}
                         for claim in sorted(export_evidence.CLAIMS)]}


class ContainerToolTests(unittest.TestCase):
    def test_valid_evidence_envelope(self):
        export_evidence.validate_report(report_fixture())

    def test_reject_failed_or_production_certified_envelope(self):
        for key, value in (('overall_fixture_status', 'EXECUTED_FAIL'),
                           ('production_certified', True), ('production_certified', 0),
                           ('operation', 'wrong'), ('schema', 'wrong')):
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                report = report_fixture()
                report[key] = value
                export_evidence.validate_report(report)

    def test_reject_incomplete_duplicate_and_nonordinary_evidence(self):
        for alteration in ('missing', 'duplicate', 'failure', 'boolean-count', 'malformed'):
            with self.subTest(alteration=alteration), self.assertRaises(ValueError):
                report = report_fixture()
                entries = report['evidence']
                if alteration == 'missing':
                    entries.pop()
                elif alteration == 'duplicate':
                    entries[0] = copy.deepcopy(entries[1])
                elif alteration == 'failure':
                    entries[0]['status'] = 'EXECUTED_FAIL'
                elif alteration == 'boolean-count':
                    entries[0]['tests_run'] = True
                else:
                    entries[0] = None
                export_evidence.validate_report(report)

    def test_export_fails_without_runtime_and_writes_no_json(self):
        out = io.StringIO()
        with patch.object(export_evidence, 'runtime_findings', return_value=['invalid runtime']), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()), \
                patch.object(export_evidence.subprocess, 'run') as child:
            self.assertEqual(export_evidence.main(), 1)
            child.assert_not_called()
        self.assertEqual(out.getvalue(), '')

    def test_network_namespace_loopback_only(self):
        with patch.object(verify.socket, 'if_nameindex', return_value=[(1, 'lo')]), \
                patch.object(verify, 'interface_flags', return_value=0x9):
            self.assertEqual(verify.network_findings(), [])

    def test_network_namespace_extra_or_missing_interfaces_rejected(self):
        for interfaces in ([(1, 'lo'), (2, 'eth0')], [], [(2, 'eth0')]):
            with self.subTest(interfaces=interfaces), \
                    patch.object(verify.socket, 'if_nameindex', return_value=interfaces), \
                    patch.object(verify, 'interface_flags', side_effect=lambda n: 0x9 if n == 'lo' else 1):
                self.assertTrue(verify.network_findings())

    def test_network_namespace_enumeration_failure_rejected(self):
        with patch.object(verify.socket, 'if_nameindex', side_effect=OSError('unavailable')):
            self.assertIn('enumeration unavailable', verify.network_findings()[0])

    def test_inactive_tunnel_devices_are_not_connectivity(self):
        names = ['erspan0', 'gre0', 'gretap0', 'ip6_vti0', 'ip6gre0',
                 'ip6tnl0', 'ip_vti0', 'lo', 'sit0', 'tunl0']
        with patch.object(verify.socket, 'if_nameindex', return_value=list(enumerate(names, 1))), \
                patch.object(verify, 'interface_flags', side_effect=lambda n: 0x9 if n == 'lo' else 0x80):
            self.assertEqual(verify.network_findings(), [])

    def test_enabled_tunnel_or_bridge_is_rejected_even_without_carrier(self):
        for name in ('gre0', 'tunl0', 'eth0', 'dummy0'):
            with self.subTest(name=name), \
                    patch.object(verify.socket, 'if_nameindex', return_value=[(1, 'lo'), (2, name)]), \
                    patch.object(verify, 'interface_flags', side_effect=lambda n: 0x9 if n == 'lo' else 1):
                self.assertIn(name, verify.network_findings()[0])

    def test_network_flags_failure_or_fake_loopback_rejected(self):
        with patch.object(verify.socket, 'if_nameindex', return_value=[(1, 'lo')]):
            with patch.object(verify, 'interface_flags', side_effect=OSError('flags unavailable')):
                self.assertTrue(verify.network_findings())
            with patch.object(verify, 'interface_flags', return_value=1):
                self.assertTrue(verify.network_findings())

    def test_changing_network_inventory_rejected(self):
        with patch.object(verify.socket, 'if_nameindex', side_effect=[[(1, 'lo')], [(1, 'lo'), (2, 'eth0')]]), \
                patch.object(verify, 'interface_flags', return_value=0x9):
            self.assertIn('changed', verify.network_findings()[0])

    def test_root_is_not_verification_runtime(self):
        with patch.object(verify.sys, 'platform', 'linux'), \
                patch.object(verify.os, 'geteuid', return_value=0, create=True):
            self.assertIn('verification requires non-root Linux', verify.runtime_findings())

    def test_source_mount_overlap_rejected(self):
        entries = ('1 0 0:1 / / ro - overlay overlay ro\n'
                   '2 1 0:2 / /tmp rw - tmpfs tmpfs rw\n'
                   '3 1 0:3 / /opt ro - ext4 /dev/vda ro\n'
                   '4 1 0:4 / /opt/etis ro - ext4 /dev/vda ro\n'
                   '5 1 0:5 / /opt/etis/examples ro - ext4 /dev/vda ro\n'
                   '6 1 0:6 / /opt/etis-other ro - ext4 /dev/vda ro\n')
        self.assertEqual(verify.source_mounts(entries, Path('/opt/etis')),
                         ['/opt', '/opt/etis', '/opt/etis/examples'])

    def test_source_mount_escape_and_malformed_input(self):
        entries = r'1 0 0:1 / /opt/etis/example\040data ro - ext4 /dev/vda ro'
        self.assertEqual(verify.source_mounts(entries, Path('/opt/etis')),
                         ['/opt/etis/example data'])
        with self.assertRaises(ValueError):
            verify.source_mounts('invalid', Path('/opt/etis'))

    def test_verification_stops_on_runtime_failure(self):
        with patch.object(verify, 'runtime_findings', return_value=['invalid runtime']), \
                patch.object(verify.subprocess, 'run') as child, \
                contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(verify.main(), 1)
            child.assert_not_called()

    def test_verification_propagates_child_failure(self):
        out = io.StringIO()
        with patch.object(verify, 'runtime_findings', return_value=[]), \
                patch.object(verify.subprocess, 'run', return_value=subprocess.CompletedProcess([], 7)) as child, \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(verify.main(), 1)
            self.assertEqual(child.call_count, 1)
        self.assertNotIn('PASS: container runtime, tool regressions', out.getvalue())

    def test_real_build0_demo(self):
        result = subprocess.run([sys.executable, str(demo.ROOT / 'containers/demo.py'), '--build', '0'],
                                capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([json.loads(line)['local'][0] for line in result.stdout.splitlines()],
                         ['AUTHORIZED', 'UNKNOWN', 'UNKNOWN', 'CONFIRMED'])

    def test_demo_does_not_treat_nonzero_as_success(self):
        with patch.object(demo.subprocess, 'run', return_value=subprocess.CompletedProcess([], 2)):
            self.assertEqual(demo.run_build(3), 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
