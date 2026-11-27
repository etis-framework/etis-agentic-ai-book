# SPDX-License-Identifier: Apache-2.0
import copy
from datetime import datetime, timezone
import unittest
from aggregate_release import aggregate, SCOPES

class AggregateTests(unittest.TestCase):
    def setUp(self):
        self.now=datetime(2026,11,27,18,tzinfo=timezone.utc)
        self.doc={'candidate_commit':'c'*40,'images':[dict(role=r,architecture=a,image_id='sha256:'+str(i)*64) for i,(r,a) in enumerate(sorted(SCOPES),1)]}
        self.results=[dict(row,candidate_commit=self.doc['candidate_commit'],policy='protected-governed-v1',status='PASS',hardening_pass=True,blocking_findings=0,production_certified=False,findings=[],authorization_expires_at='2026-11-28T00:00:00Z',authorization_id=str(i),reviewer_key_sha256='a'*64,maintainer_key_sha256='b'*64) for i,row in enumerate(self.doc['images'])]
    def reject(self):
        with self.assertRaises(ValueError): aggregate(self.doc,self.results,self.now)
    def test_pass(self): self.assertFalse(aggregate(self.doc,self.results,self.now)['release_authorized'])
    def test_missing(self): self.results.pop(); self.reject()
    def test_duplicate(self): self.results[1]=copy.deepcopy(self.results[0]); self.reject()
    def test_commit(self): self.results[0]['candidate_commit']='d'*40; self.reject()
    def test_image(self): self.results[0]['image_id']='sha256:'+'a'*64; self.reject()
    def test_blocked(self): self.results[0]['status']='BLOCKED'; self.reject()
    def test_expired(self): self.results[0]['authorization_expires_at']='2026-11-27T18:00:00Z'; self.reject()
    def test_critical(self): self.results[0]['findings']=[dict(blocking=False,severity='CRITICAL')]; self.reject()
    def test_reused_auth(self): self.results[1]['authorization_id']=self.results[0]['authorization_id']; self.reject()
    def test_keys(self): self.results[1]['reviewer_key_sha256']='c'*64; self.reject()
    def test_manifest_missing(self): self.doc['images'].pop(); self.reject()
    def test_manifest_duplicate(self): self.doc['images'][1]=copy.deepcopy(self.doc['images'][0]); self.reject()

if __name__=='__main__': unittest.main(verbosity=2)
