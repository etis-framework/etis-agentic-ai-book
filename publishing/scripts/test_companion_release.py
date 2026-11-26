"""Regression checks for the release verification gate (not fixture counts)."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import check_companion_release as runner


class RunnerEvidenceTests(unittest.TestCase):
    def test_ordinary_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            record = Path(tmp) / 'build0.json'
            record.write_text(json.dumps({'suite': 'build0', 'passed': 16}), encoding='utf-8')
            self.assertEqual(runner.read_result(record, 'build0', 16), 16)

    def test_missing_or_invalid_completion_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            record = Path(tmp) / 'result.json'
            with self.assertRaises(FileNotFoundError):
                runner.read_result(record, 'build0', 16)
            for result in ({'suite': 'build0', 'passed': 0},
                           {'suite': 'build0', 'passed': 15},
                           {'suite': 'build0', 'passed': True},
                           {'suite': 'build1', 'passed': 16},
                           {'suite': 'build0', 'passed': '16'},
                           {'suite': 'build0', 'passed': 16, 'other': 0}, []):
                with self.subTest(result=result), self.assertRaises(ValueError):
                    record.write_text(json.dumps(result), encoding='utf-8')
                    runner.read_result(record, 'build0', 16)
            record.write_text('{', encoding='utf-8')
            with self.assertRaises(ValueError):
                runner.read_result(record, 'build0', 16)

    def run_fixture(self, source):
        """Run the actual worker in a disposable source checkout, not a mocked result."""
        with tempfile.TemporaryDirectory(prefix='etis-runner-test-') as tmp:
            root = Path(tmp)
            script = root / 'publishing/scripts/check_companion_release.py'
            script.parent.mkdir(parents=True)
            shutil.copyfile(runner.__file__, script)
            fixture = root / 'examples/refund-reference-system/build0'
            fixture.mkdir(parents=True)
            if source is not None:
                (fixture / 'test_fixture.py').write_text(source, encoding='utf-8')
            record = root / 'result.json'
            result = subprocess.run([sys.executable, str(script), '--_suite', 'build0',
                                     '--_record', str(record)], capture_output=True,
                                    text=True, timeout=20)
            evidence = json.loads(record.read_text()) if record.exists() else None
            return result.returncode, evidence, result.stderr

    @staticmethod
    def fixture_source(last='    def test_last(self): pass\n'):
        return ('import unittest\nclass Fixture(unittest.TestCase):\n'
                + ''.join(f'    def test_{i:02d}(self): pass\n' for i in range(15))
                + last)

    def test_real_worker_success(self):
        code, evidence, output = self.run_fixture(self.fixture_source())
        self.assertEqual(code, 0, output)
        self.assertEqual(evidence, {'suite': 'build0', 'passed': 16})

    def test_real_worker_zero_or_missing_tests(self):
        for source in (None, self.fixture_source(last='')):
            with self.subTest(source=source):
                code, evidence, output = self.run_fixture(source)
                self.assertNotEqual(code, 0)
                self.assertIsNone(evidence)
                self.assertIn('discovered', output)

    def test_real_worker_nonordinary_outcomes(self):
        for last in ('    @unittest.skip("not executed")\n    def test_last(self): pass\n',
                     '    @unittest.expectedFailure\n    def test_last(self): self.fail()\n',
                     '    @unittest.expectedFailure\n    def test_last(self): pass\n',
                     '    def test_last(self): self.fail()\n',
                     '    def test_last(self): raise RuntimeError("fixture error")\n'):
            with self.subTest(last=last):
                code, evidence, output = self.run_fixture(self.fixture_source(last))
                self.assertNotEqual(code, 0)
                self.assertIsNone(evidence)
                self.assertIn('nonordinary unittest result', output)

    def test_worker_early_exit_cannot_write_green_record(self):
        code, evidence, _ = self.run_fixture(self.fixture_source(
            '    def test_last(self): __import__("os")._exit(0)\n'))
        self.assertEqual(code, 0)
        self.assertIsNone(evidence)

    def test_parent_rejects_zero_exit_without_record(self):
        with patch.object(runner, 'run_child', return_value=0), \
                patch.object(sys, 'argv', ['check_companion_release.py', '--portable']):
            self.assertEqual(runner.main(), 1)


if __name__ == '__main__':
    unittest.main()
