# SPDX-License-Identifier: Apache-2.0
import copy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from authorize_release import decide, finding_fingerprint, openvex, signed_document


class AuthorizationTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026,11,27,18,tzinfo=timezone.utc)
        self.scan = self.now-timedelta(hours=1)
        self.commit = 'c'*40
        self.finding = dict(role='companion',architecture='amd64',cve='CVE-2026-9538',package='perl-base',version='1',severity='HIGH',fixed_version='',scanner_status='affected',assessment='under_investigation',applicability_hint='candidate_module_absent_from_default_inc',blocking=True)
        self.strict = dict(role='companion',architecture='amd64',image_id='sha256:'+'a'*64,evidence_sha256={'report':'b'*64},policy='strict-no-exceptions',hardening_pass=True,findings=[self.finding],status='BLOCKED')
        self.row = dict(finding_sha256=finding_fingerprint(self.finding),disposition='risk_accepted',rationale='Reviewed residual exposure and documented compensating controls.',advisory='https://security-tracker.debian.org/tracker/CVE-2026-9538',supported_fix=False,review_note_sha256='e'*64,absence_confirmed=False,reviewed_at='2026-11-27T17:10:00Z')
        self.auth = dict(schema_version=1,authorization_id='review-1',candidate_commit=self.commit,role='companion',architecture='amd64',image_id=self.strict['image_id'],evidence_sha256=self.strict['evidence_sha256'].copy(),issued_at='2026-11-27T17:20:00Z',expires_at='2026-12-27T17:20:00Z',decisions=[self.row])
    def run_decision(self, revoked=()):
        return decide(self.strict,self.auth,set(revoked),self.commit,self.scan,self.now)
    def reject(self):
        with self.assertRaises(ValueError): self.run_decision()
    def rebind(self): self.row['finding_sha256']=finding_fingerprint(self.finding)
    def test_valid_risk(self):
        r=self.run_decision(); self.assertEqual(r['status'],'PASS'); self.assertIsNone(openvex(r,'reviewer',self.now)); self.assertTrue(self.finding['blocking'])
    def test_valid_absence(self):
        self.row['disposition']='not_affected'; self.row['absence_confirmed']=True; r=self.run_decision(); self.assertEqual(openvex(r,'reviewer',self.now)['statements'][0]['status'],'not_affected')
    def test_critical(self): self.finding['severity']='CRITICAL'; self.rebind(); self.reject()
    def test_fix_reported(self): self.finding['fixed_version']='2'; self.rebind(); self.reject()
    def test_supported_fix(self): self.row['supported_fix']=True; self.reject()
    def test_unknown_fix(self): self.row['supported_fix']=None; self.reject()
    def test_expired(self): self.auth['expires_at']='2026-11-27T18:00:00Z'; self.reject()
    def test_too_long(self): self.auth['expires_at']='2026-12-28T17:20:00Z'; self.reject()
    def test_future_approval(self): self.auth['issued_at']='2026-11-27T19:00:00Z'; self.reject()
    def test_stale_scan(self): self.scan-=timedelta(days=2); self.reject()
    def test_stale_review(self): self.row['reviewed_at']='2026-11-26T17:10:00Z'; self.reject()
    def test_revoked(self):
        with self.assertRaises(ValueError): self.run_decision(['review-1'])
    def test_commit(self): self.auth['candidate_commit']='d'*40; self.reject()
    def test_image(self): self.auth['image_id']='sha256:'+'d'*64; self.reject()
    def test_role(self): self.auth['role']='dev'; self.reject()
    def test_arch(self): self.auth['architecture']='arm64'; self.reject()
    def test_changed_evidence(self): self.auth['evidence_sha256']['report']='d'*64; self.reject()
    def test_changed_version(self): self.finding['version']='2'; self.reject()
    def test_unregistered(self): self.finding['assessment']='unassessed'; self.reject()
    def test_duplicate(self): self.auth['decisions'].append(copy.deepcopy(self.row)); self.reject()
    def test_absence_no_hint(self): self.row['disposition']='not_affected'; self.row['absence_confirmed']=True; self.finding['applicability_hint']='review_required'; self.rebind(); self.reject()
    def test_missing_note_digest(self): self.row['review_note_sha256']=''; self.reject()
    def test_unconfirmed_absence(self): self.row['disposition']='not_affected'; self.reject()
    def test_hardening(self): self.strict['hardening_pass']=False; self.reject()
    def test_missing_decision(self): self.auth['decisions']=[]; self.assertEqual(self.run_decision()['status'],'BLOCKED')
    def test_new_finding(self):
        self.strict['findings'].append(dict(self.finding,cve='CVE-2026-99999')); self.assertEqual(self.run_decision()['status'],'BLOCKED')
    def test_advisory_mismatch(self): self.row['advisory']='https://security-tracker.debian.org/tracker/CVE-2026-99999'; self.reject()
    def test_mixed_cve_no_vex(self):
        self.row['disposition']='not_affected'; self.row['absence_confirmed']=True; other=dict(self.finding,package='other'); self.strict['findings'].append(other)
        self.auth['decisions'].append(dict(self.row,finding_sha256=finding_fingerprint(other),disposition='risk_accepted',absence_confirmed=False))
        self.assertIsNone(openvex(self.run_decision(),'reviewer',self.now))


class SignatureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory(); cls.addClassCleanup(cls.tmp.cleanup); cls.p=Path(cls.tmp.name)
        for name in ('reviewer','maintainer','other'):
            subprocess.run(['openssl','genpkey','-algorithm','RSA','-pkeyopt','rsa_keygen_bits:2048','-out',str(cls.p/(name+'.key'))],check=True,capture_output=True)
            subprocess.run(['openssl','pkey','-in',str(cls.p/(name+'.key')),'-pubout','-out',str(cls.p/(name+'.pem'))],check=True,capture_output=True)
    def setUp(self):
        self.doc=self.p/'authorization.json'; self.doc.write_text('{"test": true}')
        for name in ('reviewer','maintainer'):
            subprocess.run(['openssl','dgst','-sha256','-sign',str(self.p/(name+'.key')),'-out',str(self.doc)+'.'+name+'.sig',str(self.doc)],check=True,capture_output=True)
    def verify(self, reviewer='reviewer',maintainer='maintainer'):
        return signed_document(self.doc,self.p/(reviewer+'.pem'),self.p/(maintainer+'.pem'))
    def test_two_signatures(self): self.assertEqual(self.verify()[0],{'test':True})
    def test_tampered_payload(self):
        self.doc.write_text('{"test": false}')
        with self.assertRaises(subprocess.CalledProcessError): self.verify()
    def test_wrong_key(self):
        with self.assertRaises(subprocess.CalledProcessError): self.verify(maintainer='other')
    def test_same_key(self):
        with self.assertRaises(ValueError): self.verify(maintainer='reviewer')
    def test_missing_signature(self):
        Path(str(self.doc)+'.maintainer.sig').unlink()
        with self.assertRaises(subprocess.CalledProcessError): self.verify()

if __name__=='__main__': unittest.main(verbosity=2)
