"""Build 4 separate-process E5 service with E6 provider integration and C08 status query.

It retains Build 3's independent grant/identity checks, fixed CASE-204 policy,
framing deadline and transport-failure containment. Shared-UID test processes
are NOT hardened adversarial isolation. Production credentials never appear.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import socket
import sqlite3
import sys
import time

# Explicitly reuse the previously verified E1 fixture and E5 approval contract.
# This module deliberately has no `contracts.py` collision with Builds 1–3.
HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'build3'))
from contracts import (AMOUNT, CASE, TENANT, AuthorizationDenied, InvalidRequest,
                       bounded_object, decode_request, verify_grant)
sys.path.insert(0,str(HERE.parent/'build2'))
from identity import LocalAssertionAuthority, ScopeDenied
from ledger import InvalidTransition, OperationalLedger
from adapter import SQLiteFixtureProvider
from provider_contracts import ContractViolation, RefundCommand
from workflow import OutcomeUnknown, RefundWorkflow

# lose_ack/outage_before_send are demonstrator-only fault-injection fields.
# A production financial request contract MUST remove these caller-controlled flags.
MAX_BYTES = 8192
FRAME_DEADLINE = 0.75
FIELDS = frozenset({'action','case_id','tenant_id','amount_cents','agent_assertion',
                    'approval_grant','lose_ack','outage_before_send'})


def read_frame(conn: socket.socket) -> object:
    """One JSON-line request; cumulative monotonic limit prevents slow trickle."""
    deadline=time.monotonic()+FRAME_DEADLINE
    data=bytearray()
    while True:
        remain=deadline-time.monotonic()
        if remain<=0:
            raise TimeoutError('request deadline')
        conn.settimeout(remain)
        chunk=conn.recv(min(1024,MAX_BYTES+1-len(data)))
        if not chunk:
            raise InvalidRequest('truncated frame')
        data.extend(chunk)
        if len(data)>MAX_BYTES:
            raise InvalidRequest('oversized request')
        if b'\n' in chunk:
            if data.count(b'\n')!=1 or not data.endswith(b'\n'):
                raise InvalidRequest('multiple frames or trailing content')
            return decode_request(data[:-1])


def handle(message: object, *, identity: LocalAssertionAuthority, grant_key: bytes,
           ledger_path: Path, provider_path: Path, now: int) -> dict:
    """Deny before E7/E8 creation; UNKNOWN after an unresolved dispatch claim."""
    try:
        req=bounded_object(message,FIELDS)
        if (req['action'] not in ('execute','reconcile') or req['case_id']!=CASE or
            req['tenant_id']!=TENANT or type(req['amount_cents']) is not int or
            req['amount_cents']!=AMOUNT or type(req['agent_assertion']) is not str or
            len(req['agent_assertion'])>4096 or type(req['lose_ack']) is not bool or
            type(req['outage_before_send']) is not bool):
            raise InvalidRequest('out-of-scope command')
        if req['action']=='reconcile' and (req['lose_ack'] or req['outage_before_send']):
            raise InvalidRequest('reconciliation cannot dispatch or inject effects')
        try:
            scope=identity.verify(req['agent_assertion'],now=datetime.fromtimestamp(now,timezone.utc))
        except ScopeDenied as exc:
            raise AuthorizationDenied('invalid E1 fixture identity') from exc
        if scope.case_id!=CASE or scope.tenant_id!=TENANT or scope.purpose!='review_replacement_complaint':
            raise AuthorizationDenied('case/tenant/purpose mismatch')
        verify_grant(req['approval_grant'],grant_key,now=now)
        command=RefundCommand()
        ledger=OperationalLedger(ledger_path)
        provider=SQLiteFixtureProvider(provider_path)
        workflow=RefundWorkflow(ledger,provider)
        if req['action']=='execute':
            try:
                outcome=workflow.execute(command,lose_ack=req['lose_ack'],
                                         outage_before_send=req['outage_before_send'])
            except InvalidTransition as exc:
                # Refusing a second dispatch is not proof of the first outcome.
                # Match Build 3: unresolved intent stays UNKNOWN; never resend.
                row=ledger.state(command)
                if row is not None and row[4] in {'DISPATCHED','UNKNOWN'}:
                    raise OutcomeUnknown('prior dispatch unresolved; reconcile') from exc
                raise
        else:
            outcome=workflow.reconcile(command)
        return {'status':outcome,'data':{'case_id':CASE,'operation_id':command.operation_id}}
    except (InvalidRequest,AuthorizationDenied,ContractViolation,InvalidTransition,KeyError,TypeError) as exc:
        return {'status':'DENIED','error':type(exc).__name__}
    except OutcomeUnknown:
        return {'status':'UNKNOWN','error':'ProviderOutcomeUnresolved'}
    except (OSError,sqlite3.Error,ValueError) as exc:
        # A storage/transport fault is not proof an external effect failed.
        return {'status':'UNKNOWN','error':'InfrastructureUnavailable'}


def serve_connection(conn: socket.socket, *, identity: LocalAssertionAuthority,
                     grant_key: bytes, ledger_path: Path, provider_path: Path) -> None:
    try:
        try:
            message=read_frame(conn)
        except (TimeoutError,socket.timeout,InvalidRequest,UnicodeError,ValueError,TypeError,OverflowError):
            result={'status':'DENIED','error':'InvalidFrame'}
        except OSError:
            return
        else:
            result=handle(message,identity=identity,grant_key=grant_key,
                          ledger_path=ledger_path,provider_path=provider_path,now=int(time.time()))
        conn.sendall((json.dumps(result,sort_keys=True)+'\n').encode('utf-8'))
    except (BrokenPipeError,ConnectionResetError,TimeoutError,OSError):
        # A disconnect may occur after effect; never infer failure or redispatch.
        return


def serve(socket_path: Path, *, key_path: Path, identity_key_path: Path,
          data_dir: Path, ready_path: Path) -> None:
    grant_key=key_path.read_bytes()
    if len(grant_key)<32:
        raise ValueError('E5 signing fixture key too short')
    identity=LocalAssertionAuthority(identity_key_path.read_bytes())
    data_dir.mkdir(mode=0o700,parents=True,exist_ok=True)
    with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as sock:
        sock.bind(str(socket_path))
        os.chmod(socket_path,0o600)
        sock.listen(8)
        ready_path.write_text('READY')
        while True:
            try:
                conn,_=sock.accept()
            except InterruptedError:
                continue
            with conn:
                serve_connection(conn,identity=identity,grant_key=grant_key,
                    ledger_path=data_dir/'operations.sqlite3',
                    provider_path=data_dir/'provider.sqlite3')


def main() -> None:
    parser=argparse.ArgumentParser(description='ETIS Build 4 mock provider E5 gate')
    for name in ('socket','key','identity-key','data','ready'):
        parser.add_argument('--'+name,type=Path,required=True)
    a=parser.parse_args()
    serve(a.socket,key_path=a.key,identity_key_path=a.identity_key,
          data_dir=a.data,ready_path=a.ready)


if __name__=='__main__':
    main()
