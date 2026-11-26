"""Chapter 31 assurance registry tests: never issue a consequential operation."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from collect import CASES, FixtureCase, ROOT, PRODUCTION_GAPS, result_status, run_case, validate_registry


class AssuranceTests(unittest.TestCase):
    def test_registry_names_existing_source_and_tests(self):
        validate_registry(ROOT)
        self.assertEqual(len(CASES), 7)
        self.assertEqual(len({c.claim_id for c in CASES}), 7)

    def test_each_claim_has_explicit_non_guarantee(self):
        for case in CASES:
            self.assertGreater(len(case.excluded), 15)
            self.assertGreater(len(case.expected), 15)

    def test_cannot_elevate_unimplemented_to_executed(self):
        statuses = {entry['id']: entry['status'] for entry in PRODUCTION_GAPS}
        self.assertEqual(statuses['E5_EPOCH'], 'NOT_IMPLEMENTED')
        self.assertEqual(statuses['PROTECTED_AUDIT'], 'NOT_IMPLEMENTED')
        self.assertNotIn('EXECUTED_PASS', statuses.values())

    def test_missing_test_module_fails_closed(self):
        bad = (FixtureCase('FAIL_MISSING', 'security', 'missing_module.TestClass.test_name',
                           ('security/test_adversarial_cases.py',), 'narrow claim', 'excluded claim'),)
        with self.assertRaisesRegex(ValueError, 'Missing evidence source'):
            validate_registry(ROOT, bad)

    def test_path_escape_fails_closed(self):
        bad = (FixtureCase('FAIL_ESCAPE', 'security', 'test_adversarial_cases.HijackedInvestigatorAgainstRealE5.test_forged_advisory_fields_denied',
                           ('../../outside',), 'narrow claim', 'excluded claim'),)
        with self.assertRaisesRegex(ValueError, 'Unsafe source pathname'):
            validate_registry(ROOT, bad)

    def test_duplicate_claim_identity_fails_closed(self):
        with self.assertRaisesRegex(ValueError, 'duplicated'):
            validate_registry(ROOT, (CASES[0], CASES[0]))

    def test_nonzero_and_zero_executions_fail_closed(self):
        self.assertEqual(result_status(1, True, 1), 'EXECUTED_FAIL')
        self.assertEqual(result_status(0, True, 0), 'EXECUTED_FAIL')
        self.assertEqual(result_status(0, True, 2), 'EXECUTED_FAIL')
        self.assertEqual(result_status(None, False, 1), 'EXECUTED_FAIL')
        self.assertEqual(result_status(0, True, 1), 'EXECUTED_PASS')

    def test_output_is_digest_only_not_raw_secrets(self):
        secret = 'PROVIDER_SECRET_DO_NOT_LOG'
        def simulated(*args, **kwargs):
            return subprocess.CompletedProcess(args, 0, '', f'Ran 1 test in 0.001s\nOK\n{secret}')
        record = run_case(CASES[0], ROOT, runner=simulated)
        self.assertEqual(record['status'], 'EXECUTED_PASS')
        self.assertNotIn(secret, str(record))
        self.assertEqual(len(record['output_sha256']), 64)
        self.assertNotIn('command', record)

    def test_skipped_named_test_is_not_executed_pass(self):
        def simulated(*args, **kwargs):
            return subprocess.CompletedProcess(args,0,'','Ran 1 test in 0.001s\n\nOK (skipped=1)\n')
        record = run_case(CASES[0], ROOT, runner=simulated)
        self.assertEqual(record['status'], 'EXECUTED_FAIL')

    def test_authorization_claim_hashes_shared_verifiers(self):
        record = run_case(CASES[0], ROOT, runner=lambda a, **kw: subprocess.CompletedProcess(a,0,'','Ran 1 test in 0.1s\nOK\n'))
        for path in ('build2/identity.py','build3/contracts.py','build3/client.py','build0/refund.py'):
            self.assertIn(path, record['source_sha256'])

    def test_incomplete_summary_and_expected_failure_are_not_passes(self):
        for summary in ('Ran 1 test in 0.001s\n', 'Ran 1 test in 0.001s\nOK (expected failures=1)\n'):
            with self.subTest(summary=summary):
                record=run_case(CASES[0],ROOT,runner=lambda a,**kw:subprocess.CompletedProcess(a,0,'',summary))
                self.assertEqual(record['status'],'EXECUTED_FAIL')

    def test_source_changes_during_execution_cannot_produce_green_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            case=FixtureCase('SOURCE_DRIFT','reliability','sample.Test.test_one',('source.py',),'narrow test claim','not production evidence')
            source=root/'source.py';source.write_text('before')
            def mutate(*args,**kwargs):
                source.write_text('after')
                return subprocess.CompletedProcess(args,0,'','Ran 1 test in 0.001s\nOK\n')
            record=run_case(case,root,runner=mutate)
            self.assertEqual(record['status'],'EXECUTED_FAIL')

    def test_timeout_fails_without_output(self):
        def timeout(*args, **kwargs):
            raise subprocess.TimeoutExpired(args[0], 1, output=b'SECRET')
        record = run_case(CASES[0], ROOT, runner=timeout)
        self.assertEqual(record['execution'], 'TIMEOUT')
        self.assertEqual(record['status'], 'EXECUTED_FAIL')
        self.assertIsNone(record['output_sha256'])
        self.assertNotIn('SECRET', str(record))

    def test_missing_program_fails_without_green(self):
        def missing(*args, **kwargs):
            raise FileNotFoundError('python unavailable')
        self.assertEqual(run_case(CASES[1], ROOT, runner=missing)['status'], 'EXECUTED_FAIL')

    def test_source_sha_changes_with_content(self):
        record = run_case(CASES[2], ROOT, runner=lambda a, **kw: subprocess.CompletedProcess(a, 0, '', 'Ran 1 test in 0.1s\nOK\n'))
        self.assertEqual(len(record['source_sha256']), 2)
        self.assertTrue(all(len(v) == 64 for v in record['source_sha256'].values()))

    def test_no_payment_or_credential_imports(self):
        source = (HERE / 'collect.py').read_text()
        for forbidden in ('from adapter import', 'from client import', 'provider.send(', 'issue_fixture_grant(', 'execute_refund('):
            self.assertNotIn(forbidden, source)


if __name__ == '__main__':
    unittest.main()
