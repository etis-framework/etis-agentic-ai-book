# SPDX-License-Identifier: Apache-2.0
from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from evaluate_security_gate import evaluate
from applicability import review_hint


class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.p = Path(self.tmp.name)
        self.id = 'sha256:' + 'a' * 64
        self.key = dict(role='companion', architecture='amd64', cve='CVE-2026-12345', package='sqlite', version='1:2-3')
        self.report = dict(SchemaVersion=2, ArtifactType='container_image', ArtifactName=self.id,
                           Trivy={'Version': '0.76.2'}, Metadata={'ImageID': self.id,
                           'ImageConfig': {'architecture': 'amd64', 'os': 'linux'}, 'OS': {'Family': 'debian'}},
                           Results=[{'Class':'os-pkgs','Type':'debian','Packages':[{'Name':'sqlite','ID':'sqlite@1:2-3'}], 'Vulnerabilities':[]}])
        self.sbom = {'bomFormat':'CycloneDX','metadata':{'component':{'name':self.id,'properties':[{'name':'aquasecurity:trivy:ImageID','value':self.id}]}},'components':[{'name':'sqlite','version':'1:2-3','purl':'pkg:deb/debian/sqlite@2-3?epoch=1'}]}
        self.reg = {'schema_version':1,'assessments':[dict(self.key,status='under_investigation',rationale='review required')]}
        self.risk = {'schema_version':1,'acceptances':[]}
        self.now = datetime(2026,11,28,tzinfo=timezone.utc)
        (self.p/'companion-image.txt').write_text(f'{self.id} linux/amd64 10\n')
        (self.p/'companion-packages.tsv').write_text('sqlite\t1:2-3\n')
        (self.p/'companion-hardening.txt').write_text('PASS: companion image privilege-bit and target-specific CLI checks\n')

        self.probe = dict(schema_version=1, role='companion', architecture='amd64', image_id=self.id,
                          uid=10001, capabilities={k:0 for k in ('CapInh','CapPrm','CapEff','CapBnd','CapAmb')},
                          no_new_privileges=1, seccomp=2, sqlite_version='3.46.1', sqlite_options=['ENABLE_FTS5','ENABLE_SESSION'],
                          openssl_version='OpenSSL 3.5.9', paths={k:False for k in ('/usr/bin/infocmp','/usr/lib/systemd/systemd-homed','/lib/systemd/systemd-homed','/usr/bin/homectl')},
                          commands=dict(infocmp=None, **{'systemd-homed':None}, homectl=None, perl='/usr/bin/perl', curl=None),
                          perl_inc=['/usr/share/perl5'], perl_archive_paths=[], curl_version=None, fstab_entries=[])

    def run_gate(self):
        (self.p/'companion-applicability.json').write_text(json.dumps(self.probe))
        for name, data in [('companion-vulnerabilities.json',self.report),('companion-sbom.json',self.sbom),('register.json',self.reg),('risks.json',self.risk)]:
            (self.p/name).write_text(json.dumps(data))
        return evaluate(self.p,'companion','amd64',self.id,self.p/'register.json',self.p/'risks.json',now=self.now)

    def finding(self, severity='HIGH', cve='CVE-2026-12345'):
        self.report['Results'][0]['Vulnerabilities'].append(dict(Severity=severity,VulnerabilityID=cve,PkgName='sqlite',InstalledVersion='1:2-3'))

    def test_parse_and_hash_same_evidence_bytes(self):
        original = Path.read_bytes
        reads = {}
        def read_once(path):
            if path.name.startswith('companion-'):
                reads[path.name] = reads.get(path.name, 0) + 1
                if reads[path.name] > 1:
                    raise AssertionError('evidence read again: ' + path.name)
            return original(path)
        with patch.object(Path, 'read_bytes', read_once):
            self.assertEqual(self.run_gate()['status'], 'PASS')
        self.assertEqual(len(reads), 6)

    def approve(self):
        self.finding()
        self.report['Results'][0]['Vulnerabilities'][0]['Status']='affected'
        self.risk = {'schema_version':1, 'approval':{'authority':'ETIS repository maintainer',
                     'issued_at':'2026-11-27T00:00:00Z','reviewed_at':'2026-11-27T00:00:00Z',
                     'expires_at':'2026-12-27T00:00:00Z','basis_commit':'a'*40,'basis_run':23,
                     'advisory_scope':'Debian Trixie stable and security'},
                     'acceptances':[dict(self.key, severity='HIGH', scanner_status='affected',fixed_version='',
                      disposition='risk_accepted',applicability_hint='review_required',
                      advisory='https://security-tracker.debian.org/tracker/'+self.key['cve'],
                      rationale='Bounded risk for documented educational runtime only.')]}

    def test_approved_exact_finding_passes(self):
        self.approve(); result=self.run_gate()
        self.assertEqual(result['status'],'PASS')
        self.assertEqual(result['severity_counts'],{'HIGH':1})
        self.assertEqual(result['findings'][0]['assessment'],'risk_accepted')

    def test_approved_critical_blocks(self):
        self.approve(); self.report['Results'][0]['Vulnerabilities'][0]['Severity']='CRITICAL'
        self.assertEqual(self.run_gate()['status'],'BLOCKED')

    def test_approved_new_fix_blocks(self):
        self.approve(); self.report['Results'][0]['Vulnerabilities'][0]['FixedVersion']='1:2-4'
        self.assertEqual(self.run_gate()['status'],'BLOCKED')

    def test_approved_new_finding_blocks(self):
        self.approve(); self.finding(cve='CVE-2026-99999')
        self.assertEqual(self.run_gate()['status'],'BLOCKED')

    def test_approved_changed_scanner_status_blocks(self):
        self.approve(); self.report['Results'][0]['Vulnerabilities'][0]['Status']='fix_deferred'
        self.assertEqual(self.run_gate()['status'],'BLOCKED')

    def test_approval_expires_at_boundary(self):
        self.approve(); self.now=datetime(2026,12,27,tzinfo=timezone.utc)
        self.assertEqual(self.run_gate()['status'],'BLOCKED')

    def test_approval_over_30_days_rejected(self):
        self.approve(); self.risk['approval']['expires_at']='2026-12-28T00:00:00Z'
        with self.assertRaises(ValueError): self.run_gate()

    def test_future_approval_rejected(self):
        self.approve(); self.now=datetime(2026,11,26,tzinfo=timezone.utc)
        with self.assertRaises(ValueError): self.run_gate()

    def test_revocation_blocks(self):
        self.approve(); self.risk={'schema_version':1,'acceptances':[]}
        self.assertEqual(self.run_gate()['status'],'BLOCKED')

    def test_wrong_authority_rejected(self):
        self.approve(); self.risk['approval']['authority']='candidate'
        with self.assertRaises(ValueError): self.run_gate()

    def test_approved_duplicate_rejected(self):
        self.approve(); self.risk['acceptances']*=2
        with self.assertRaises(ValueError): self.run_gate()

    def test_approved_wrong_version_blocks(self):
        self.approve(); self.report['Results'][0]['Vulnerabilities'][0]['InstalledVersion']='1:2-4'
        self.report['Results'][0]['Packages'][0]['ID']='sqlite@1:2-4'
        self.sbom['components'][0]['version']='1:2-4'
        (self.p/'companion-packages.tsv').write_text('sqlite\t1:2-4\n')
        self.assertEqual(self.run_gate()['status'],'BLOCKED')

    def test_approved_hardening_failure_blocks(self):
        self.approve(); (self.p/'companion-hardening.txt').write_text('FAIL\n')
        self.assertEqual(self.run_gate()['status'],'BLOCKED')

    def test_approved_fstab_change_blocks(self):
        self.approve(); self.probe['fstab_entries']=['unexpected']
        with self.assertRaises(ValueError): self.run_gate()

    def test_limited_absence_must_be_observed(self):
        self.approve(); self.key.update(cve='CVE-2026-9538',package='perl-base')
        self.reg['assessments']=[dict(self.key,status='under_investigation',rationale='review required')]
        self.risk['acceptances'][0].update(self.key,disposition='limited_absence',applicability_hint='candidate_module_absent_from_default_inc',advisory='https://security-tracker.debian.org/tracker/CVE-2026-9538')
        self.report['Results'][0]['Packages']=[{'Name':'perl-base','ID':'perl-base@1:2-3'}]
        self.report['Results'][0]['Vulnerabilities'][0].update(VulnerabilityID='CVE-2026-9538',PkgName='perl-base')
        self.sbom['components'][0].update(name='perl-base')
        (self.p/'companion-packages.tsv').write_text('perl-base\t1:2-3\n')
        self.assertEqual(self.run_gate()['status'],'PASS')
        self.probe['perl_archive_paths']=['/usr/share/perl5/Archive/Tar.pm']
        self.assertEqual(self.run_gate()['status'],'BLOCKED')

    def test_clean(self):
        self.assertEqual(self.run_gate()['status'],'PASS')

    def test_known_high_blocks(self):
        self.finding(); self.assertEqual(self.run_gate()['blocking_findings'],1)
        self.assertEqual(self.run_gate()['findings'][0]['assessment'],'under_investigation')

    def test_unknown_high_blocks(self):
        self.finding(cve='CVE-2026-99999'); self.assertEqual(self.run_gate()['status'],'BLOCKED')

    def test_critical_blocks(self):
        self.finding('CRITICAL'); self.assertEqual(self.run_gate()['status'],'BLOCKED')

    def test_medium_retained(self):
        self.finding('MEDIUM'); self.assertEqual(self.run_gate()['severity_counts'],{'MEDIUM':1})

    def test_unapproved_acceptance_rejected(self):
        self.risk['acceptances']=[dict(self.key,approved_by='maintainer',expires='2099-01-01')]
        with self.assertRaises(ValueError): self.run_gate()

    def test_expired_acceptance_rejected(self):
        self.risk['acceptances']=[dict(self.key,approved_by='maintainer',expires='2020-01-01')]
        with self.assertRaises(ValueError): self.run_gate()

    def test_self_declared_not_affected_rejected(self):
        self.reg['assessments'][0]['status']='not_affected'
        with self.assertRaises(ValueError): self.run_gate()

    def test_duplicate_assessment(self):
        self.reg['assessments']*=2
        with self.assertRaises(ValueError): self.run_gate()

    def test_duplicate_finding(self):
        self.finding(); self.finding()
        with self.assertRaises(ValueError): self.run_gate()

    def test_wrong_image(self):
        self.report['Metadata']['ImageID']='sha256:'+'b'*64
        with self.assertRaises(ValueError): self.run_gate()

    def test_wrong_platform(self):
        self.report['Metadata']['ImageConfig']['architecture']='arm64'
        with self.assertRaises(ValueError): self.run_gate()

    def test_wrong_sbom(self):
        self.sbom['metadata']['component']['name']='sha256:'+'b'*64
        with self.assertRaises(ValueError): self.run_gate()

    def test_missing_inventory_package(self):
        self.sbom['components']=[]
        with self.assertRaises(ValueError): self.run_gate()

    def test_empty_result(self):
        self.report['Results']=[]
        with self.assertRaises(ValueError): self.run_gate()

    def test_hardening_failure(self):
        (self.p/'companion-hardening.txt').write_text('FAIL\n')
        self.assertEqual(self.run_gate()['status'],'BLOCKED')

    def test_unknown_label(self):
        self.finding('NOT_A_SEVERITY')
        with self.assertRaises(ValueError): self.run_gate()

    def test_wrong_version(self):
        self.finding(); self.reg['assessments'][0]['version']='other'
        self.assertEqual(self.run_gate()['findings'][0]['assessment'],'unassessed')

    def test_wrong_role(self):
        self.finding(); self.reg['assessments'][0]['role']='dev'
        self.assertEqual(self.run_gate()['findings'][0]['assessment'],'unassessed')

    def test_missing_file(self):
        (self.p/'companion-hardening.txt').unlink()
        with self.assertRaises(OSError): self.run_gate()


    def test_probe_wrong_identity(self):
        self.probe['image_id']='sha256:'+'b'*64
        with self.assertRaises(ValueError): self.run_gate()

    def test_probe_wrong_scope(self):
        self.probe['role']='dev'
        with self.assertRaises(ValueError): self.run_gate()

    def test_probe_root(self):
        self.probe['uid']=0
        with self.assertRaises(ValueError): self.run_gate()

    def test_probe_capability(self):
        self.probe['capabilities']['CapEff']=1
        with self.assertRaises(ValueError): self.run_gate()

    def test_probe_missing_path(self):
        del self.probe['paths']['/usr/bin/infocmp']
        with self.assertRaises(ValueError): self.run_gate()

    def test_probe_false_type(self):
        self.probe['paths']['/usr/bin/infocmp']=0
        with self.assertRaises(ValueError): self.run_gate()

    def test_absence_hint_never_waives_high(self):
        self.key.update(cve='CVE-2026-9538',package='perl-base')
        self.reg['assessments']=[dict(self.key,status='under_investigation',rationale='review required')]
        self.report['Results'][0]['Packages']=[{'Name':'perl-base','ID':'perl-base@1:2-3'}]
        self.sbom['components'][0].update(name='perl-base')
        (self.p/'companion-packages.tsv').write_text('perl-base\t1:2-3\n')
        self.report['Results'][0]['Vulnerabilities']=[dict(Severity='HIGH',VulnerabilityID='CVE-2026-9538',PkgName='perl-base',InstalledVersion='1:2-3')]
        result=self.run_gate()
        self.assertEqual(result['findings'][0]['applicability_hint'],'candidate_module_absent_from_default_inc')
        self.assertEqual(result['status'],'BLOCKED')

    def test_homed_present_no_hint(self):
        self.probe['paths']['/usr/lib/systemd/systemd-homed']=True
        self.assertEqual(review_hint('CVE-2026-16742','libsystemd0','companion',self.probe),'review_required')

    def test_infocmp_dev_no_hint(self):
        self.assertEqual(review_hint('CVE-2025-69720','ncurses-bin','dev',self.probe),'review_required')

    def test_wrong_package_no_hint(self):
        self.assertEqual(review_hint('CVE-2026-9538','unrelated','companion',self.probe),'review_required')

    def test_perl_present_no_hint(self):
        self.probe['perl_archive_paths']=['/usr/share/perl5/Archive/Tar.pm']
        self.assertEqual(review_hint('CVE-2026-9538','perl-base','companion',self.probe),'review_required')


if __name__=='__main__': unittest.main(verbosity=2)
