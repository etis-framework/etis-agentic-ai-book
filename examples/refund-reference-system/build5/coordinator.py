"""Build 5: durable, fenced E2 work ownership; never a financial authority.

The coordinator stores only ownership/intent/observation. It cannot mint an E5
approval, invoke E6 or alter E7/E8. Its workflow state is NOT payment truth.
SQLite BEGIN IMMEDIATE serializes this single-host teaching fixture; a real
multi-site coordinator needs an authoritative store with equivalent fencing.
"""
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
import sqlite3
import time

CASE = 'CASE-204'
OPERATION = 'RF-1042'
VALID_STATES = frozenset({'READY', 'EXECUTE_IN_FLIGHT', 'NEEDS_RECONCILIATION',
                          'CONFIRMED', 'DENIED', 'ESCALATED'})

class CoordinationError(ValueError):
    """Invalid ownership, state, request or fencing epoch."""

class StaleOwner(CoordinationError):
    """The caller no longer holds the authoritative lease and epoch."""

@dataclass(frozen=True)
class Ownership:
    """Short-lived exclusive work lease; not a business authorization token."""
    worker: str
    epoch: int
    expires_at: int

class DurableCoordinator:
    def __init__(self, path: Path, *, lease_seconds: int = 15):
        if type(lease_seconds) is not int or not 1 <= lease_seconds <= 300:
            raise ValueError('lease duration outside teaching bound')
        self.path = Path(path)
        self.lease_seconds = lease_seconds

    @contextmanager
    def _transaction(self):
        self.path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        db = sqlite3.connect(self.path, timeout=2, isolation_level=None)
        try:
            db.execute('PRAGMA busy_timeout=2000')
            db.execute('BEGIN IMMEDIATE')
            db.execute('''CREATE TABLE IF NOT EXISTS work (
                case_id TEXT PRIMARY KEY, operation_id TEXT NOT NULL,
                phase TEXT NOT NULL, worker TEXT, epoch INTEGER NOT NULL,
                expires_at INTEGER NOT NULL, last_outcome TEXT NOT NULL)''')
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    def _check_now(self, now: int):
        # SQLite INTEGER is signed 64-bit; reserve space for a new lease.
        if type(now) is not int or not 0 <= now <= 2**63-1-self.lease_seconds:
            raise CoordinationError('invalid authoritative fixture clock')

    @staticmethod
    def _check_worker(worker: str):
        if type(worker) is not str or not 1 <= len(worker) <= 48 or not all(c.isascii() and (c.isalnum() or c in '-_') for c in worker):
            raise CoordinationError('invalid worker identity')

    def initialize(self):
        """Idempotently establish one fixed case; never invent an operation ID."""
        with self._transaction() as db:
            db.execute('''INSERT OR IGNORE INTO work VALUES (?,?,?,?,?,?,?)''',
                       (CASE, OPERATION, 'READY', None, 0, 0, 'not attempted'))
            row = db.execute('SELECT operation_id FROM work WHERE case_id=?',(CASE,)).fetchone()
            if row != (OPERATION,):
                raise CoordinationError('case identity conflicts with durable state')

    # A monotonically increasing epoch rejects a stale worker's E2 writes.
    # This is deliberately NOT a complete E5-side fencing protocol: the trusted
    # financial service does not check the E2 epoch in this fixture.
    def acquire(self, worker: str, *, now: int) -> Ownership:
        """Acquire after expiration; each takeover permanently increases epoch."""
        self._check_worker(worker)
        self._check_now(now)
        with self._transaction() as db:
            row = db.execute('SELECT worker,epoch,expires_at FROM work WHERE case_id=?',(CASE,)).fetchone()
            if row is None:
                raise CoordinationError('initialize workflow before ownership')
            current, epoch, expiration = row
            if current is not None and now < expiration:
                raise CoordinationError('workflow already leased')
            if epoch >= 2**63-2:
                raise CoordinationError('epoch exhausted')
            new_epoch = epoch+1
            expiration=now+self.lease_seconds
            db.execute('UPDATE work SET worker=?,epoch=?,expires_at=? WHERE case_id=?',
                       (worker,new_epoch,expiration,CASE))
            return Ownership(worker,new_epoch,expiration)

    @staticmethod
    def _require(db, owner: Ownership, now: int):
        if not isinstance(owner, Ownership) or type(owner.epoch) is not int:
            raise StaleOwner('invalid ownership token')
        row=db.execute('SELECT worker,epoch,expires_at,phase FROM work WHERE case_id=?',(CASE,)).fetchone()
        if (row is None or row[0]!=owner.worker or row[1]!=owner.epoch or
            row[2]!=owner.expires_at or now>=row[2]):
            raise StaleOwner('stale or expired lease; no further action allowed')
        return row[3]

    def renew(self, owner: Ownership, *, now: int) -> Ownership:
        self._check_now(now)
        with self._transaction() as db:
            self._require(db,owner,now)
            expiry=now+self.lease_seconds
            # Preserve monotonic expiration; do not shorten an existing lease.
            expiry=max(expiry,owner.expires_at)
            db.execute('UPDATE work SET expires_at=? WHERE case_id=?',(expiry,CASE))
            return Ownership(owner.worker,owner.epoch,expiry)

    # An unresolved prior execute can only choose a status-only reconcile.
    # Never choose another execute just because a lease was transferred.
    def choose(self, owner: Ownership, *, now: int) -> str:
        """Return exactly one permitted E5 action; no execution side effect."""
        self._check_now(now)
        with self._transaction() as db:
            phase=self._require(db,owner,now)
            return ('execute' if phase=='READY' else
                    'reconcile' if phase in ('EXECUTE_IN_FLIGHT','NEEDS_RECONCILIATION') else
                    'none')

    def mark_execute_intent(self, owner: Ownership, *, now: int):
        """Persist the attempt BEFORE crossing E5; takeover must never resend.

        A crash after this commit but before the E5 call is conservatively
        unresolved. E7 may have no operation; operator adjudication is needed.
        """
        self._check_now(now)
        with self._transaction() as db:
            if self._require(db,owner,now)!='READY':
                raise CoordinationError('execute intent may be recorded only once')
            db.execute('''UPDATE work SET phase='EXECUTE_IN_FLIGHT',
                last_outcome='E5 response not yet known' WHERE case_id=?''',(CASE,))

    def observe(self, owner: Ownership, *, now: int, action: str, outcome: str):
        """Record E5 observation, never infer payment truth from an exception."""
        self._check_now(now)
        if action not in ('execute','reconcile') or outcome not in ('CONFIRMED','DENIED','UNKNOWN'):
            raise CoordinationError('unsupported E5 response category')
        with self._transaction() as db:
            old=self._require(db,owner,now)
            if action=='execute' and old!='EXECUTE_IN_FLIGHT':
                raise CoordinationError('execute response without one durable intent')
            if action=='reconcile' and old not in ('EXECUTE_IN_FLIGHT','NEEDS_RECONCILIATION'):
                raise CoordinationError('reconcile response without unresolved execution')
            if outcome=='CONFIRMED':
                phase='CONFIRMED'
            elif outcome=='UNKNOWN':
                phase='NEEDS_RECONCILIATION'
            elif action=='execute':
                # E5 DENIED proves this call did not pass its gate; do not assert
                # previous provider effects or permit another execute.
                phase='DENIED'
            else:
                # DENIED on recovery can mean expired approval, not payment failure.
                phase='ESCALATED'
            db.execute('UPDATE work SET phase=?,last_outcome=? WHERE case_id=?',
                       (phase,f'{action}:{outcome}',CASE))

    def state(self) -> dict:
        with self._transaction() as db:
            row=db.execute('SELECT operation_id,phase,worker,epoch,expires_at,last_outcome FROM work WHERE case_id=?',(CASE,)).fetchone()
            if row is None:
                raise CoordinationError('workflow not initialized')
            return dict(zip(('operation_id','phase','worker','epoch','expires_at','last_outcome'),row))
