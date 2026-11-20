"""Separate-process E5 gate; sole reference-system owner of E6 and E7 handles.

Run locally via `demo.py`; a shared Unix UID is not a production isolation
boundary. Never give the adviser the signing secret, socket server object or DB path.
"""
import argparse
from datetime import datetime, timezone
import sqlite3
import json
import os
from pathlib import Path
import socket
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'build0'))
import refund  # E5-owned deterministic E7/E6 teaching adapter, never imported by client
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'build2'))
from identity import LocalAssertionAuthority, ScopeDenied
from contracts import (InvalidRequest,AuthorizationDenied,EffectUncertain,
                       bounded_object,verify_grant,CASE,TENANT,AMOUNT,OPERATION)

# Educational request path: bound/framing check -> strict JSON contract ->
# verified E1 assertion -> independently signed E5 finance grant ->
# server-owned E7 intent/dispatch -> simulated E6/mock E8 observation.
# The agent-side client neither issues approvals nor imports the adapter.
MAX_BYTES = 8192
# A deliberately single-worker educational service must still bound hostile
# connections. The deadline applies to the entire frame, not each recv(), so
# trickle-fed input cannot keep the worker occupied indefinitely.
FRAME_DEADLINE_SECONDS = 0.75


# Frame validation is deliberately before request authorization. An oversized
# or trickle-fed frame must not monopolize the single educational E5 worker.
def read_frame(conn: socket.socket, *, deadline_seconds: float = FRAME_DEADLINE_SECONDS) -> object:
    """Read one newline-delimited JSON object with a total monotonic deadline.

    Reject absent, oversized, trailing or malformed frames before invoking E5.
    The caller owns socket/transport fault handling; no money is touched here.
    """
    deadline = time.monotonic() + deadline_seconds
    raw = bytearray()
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise InvalidRequest('incomplete request before framing deadline')
        conn.settimeout(remaining)
        chunk = conn.recv(min(1024, MAX_BYTES + 1 - len(raw)))
        if not chunk:
            raise InvalidRequest('connection closed before complete frame')
        raw.extend(chunk)
        if len(raw) > MAX_BYTES:
            raise InvalidRequest('request frame too large')
        if b'\n' in chunk:
            if raw.count(b'\n') != 1 or not raw.endswith(b'\n'):
                raise InvalidRequest('trailing data or multiple request frames')
            return json.loads(raw[:-1].decode('utf-8'))


def serve_connection(conn: socket.socket, *, secret: bytes,
                     identity_authority: LocalAssertionAuthority,
                     local: Path, provider: Path) -> None:
    """Contain peer transport failures; never convert uncertain effects to DENIED.

    A reply write may fail *after* a financial effect. The client must treat a
    missing response as UNKNOWN and reconcile; the service must stay alive.
    """
    try:
        try:
            message = read_frame(conn)
        except (InvalidRequest, ValueError, UnicodeError, TypeError, OverflowError):
            response = {'status': 'DENIED', 'error': 'InvalidRequest'}
        except (socket.timeout, TimeoutError):
            response = {'status': 'DENIED', 'error': 'FrameDeadlineExceeded'}
        else:
            response = answer(message, secret=secret,
                              identity_authority=identity_authority,
                              local=local, provider=provider,
                              now=int(time.time()))
        conn.sendall((json.dumps(response, sort_keys=True) + '\n').encode('utf-8'))
    except (BrokenPipeError, ConnectionResetError, socket.timeout, OSError):
        # A disconnected or stalled caller cannot terminate the E5 process.
        # This is deliberately not an authorization-success or payment-failure
        # signal, and no retry is initiated from this transport handler.
        return


def execute(message: object, *, secret: bytes, identity_authority: LocalAssertionAuthority, local: Path, provider: Path, now: int) -> dict:
    """Reject requests at E5 before touching E7 or E6. Inputs are untrusted."""
    request=bounded_object(message,frozenset({'action','case_id','tenant_id','amount_cents',
                                              'agent_assertion','approval_grant','simulate_outage'}))
    if (request['action']!='execute' or request['case_id']!=CASE or
        request['tenant_id']!=TENANT or type(request['amount_cents']) is not int or
        request['amount_cents']!=AMOUNT or
        type(request['agent_assertion']) is not str or
        len(request['agent_assertion'])>4096 or
        type(request['simulate_outage']) is not bool):
        raise InvalidRequest('invalid financial request')
    try:
        scope=identity_authority.verify(request['agent_assertion'],now=datetime.fromtimestamp(now, timezone.utc))
    except ScopeDenied as exc:
        raise AuthorizationDenied('E1 fixture identity not verified') from exc
    if scope.case_id!=CASE or scope.tenant_id!=TENANT or scope.purpose!='review_replacement_complaint':
        raise AuthorizationDenied('E1 fixture scope mismatch')
    # An agent assertion is deliberately never business authorization; even a
    # legitimately valid E1 token cannot replace an independently signed grant.
    # A *separate* business grant is checked after identity. A syntactically
    # valid or authentic agent assertion cannot authorize this refund.
    verify_grant(request['approval_grant'],secret,now=now)
    refund.initialize(local,provider)
    refund.prepare(local,case_id=CASE,tenant=TENANT,principal=refund.PRINCIPAL,
                   amount_cents=AMOUNT,refundable_cents=AMOUNT,approved=True,
                   policy_version=refund.POLICY)
    try:
        outcome=refund.dispatch(local,provider,
                    fail_before_provider_commit=request['simulate_outage'])
    except refund.ProviderUnavailable as exc:
        raise EffectUncertain('external outcome unverified; reconcile, do not retry') from exc
    except refund.Denied as exc:
        # A conflict after the E7 DISPATCHED claim is NOT a clean denial.
        # Preserve uncertainty rather than disguising an observed provider
        # inconsistency as proof that no effect could have happened.
        state=refund.status(local)
        if state is not None and state[0] in {'DISPATCHED','UNKNOWN'}:
            raise EffectUncertain('provider outcome inconsistent; reconcile') from exc
        raise AuthorizationDenied('operation already claimed or completed') from exc
    return {'result':outcome,'case_id':CASE,'operation_id':OPERATION}


def answer(message: object, *, secret: bytes, identity_authority: LocalAssertionAuthority, local: Path, provider: Path, now: int) -> dict:
    try:
        result=execute(message,secret=secret,identity_authority=identity_authority,local=local,provider=provider,now=now)
        return {'status':'CONFIRMED','data':result}
    except (AuthorizationDenied,InvalidRequest,refund.Denied) as exc:
        return {'status':'DENIED','error':type(exc).__name__}
    except EffectUncertain:
        return {'status':'UNKNOWN','error':'EffectUncertain'}
    except (OSError,ValueError,sqlite3.Error) as exc:
        # Infrastructure faults must not be reported as safely failed execution.
        return {'status':'UNKNOWN','error':'InfrastructureUnavailable'}


def serve(socket_path: Path, *, secret_path: Path, identity_secret_path: Path, data_dir: Path, ready_path: Path) -> None:
    """Single-request-at-a-time Unix socket worker; no arbitrary Python execution.

    This socket is a transport boundary only. Production requires a distinct OS
    identity/ACLs and independent authorization issuer. No network provider exists.
    """
    secret=secret_path.read_bytes()
    if len(secret)<32:
        raise ValueError('short E5 grant-verifier secret')
    identity_authority=LocalAssertionAuthority(identity_secret_path.read_bytes())
    data_dir.mkdir(mode=0o700,parents=True,exist_ok=True)
    local=data_dir/'operations.sqlite3'
    provider=data_dir/'provider.sqlite3'
    # There is no provider call, durable operation, or RF-1042 until authorization.
    with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as server:
        server.bind(str(socket_path))
        os.chmod(socket_path,0o600)
        server.listen(8)
        ready_path.write_text('READY')
        while True:
            try:
                conn, _ = server.accept()
            except InterruptedError:
                continue
            with conn:
                serve_connection(conn, secret=secret,
                                 identity_authority=identity_authority,
                                 local=local, provider=provider)



def main() -> None:
    parser=argparse.ArgumentParser(description='ETIS isolated-process fixture E5 gate')
    for name in ('socket','secret','identity-secret','data','ready'):
        parser.add_argument('--'+name,required=True,type=Path)
    args=parser.parse_args()
    serve(args.socket,secret_path=args.secret,identity_secret_path=args.identity_secret,data_dir=args.data,ready_path=args.ready)

if __name__=='__main__':main()
