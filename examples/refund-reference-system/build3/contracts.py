"""Build 3's strict, versioned E5 request and approval-envelope contracts.

Transport cannot establish business authorization; all fields are validated again
inside the E5 service process. No approval can be supplied as advisory C04 text.
"""
import hashlib
import hmac
import json
from typing import Any

CASE='CASE-204'
TENANT='retailer_a'
AMOUNT=50_000
POLICY='refund-policy-v12'
APPROVER='finance_approver_204'
APPROVAL='APP-204'
OPERATION='RF-1042'

class InvalidRequest(ValueError):
    """Unsupported input shape, size, or business scope."""

class AuthorizationDenied(ValueError):
    """Independently evaluated E5 policy denial; no intent created."""

class EffectUncertain(RuntimeError):
    """Dispatch started but provider outcome is not established."""


def bounded_object(value: Any, fields: frozenset[str]) -> dict[str, Any]:
    if type(value) is not dict or frozenset(value) != fields:
        raise InvalidRequest('incorrect contract fields')
    return value


def canonical(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')


def signature(secret: bytes, payload: bytes) -> str:
    return hmac.new(secret,payload,hashlib.sha256).hexdigest()


def issue_fixture_grant(secret: bytes, *, now: int, case_id: str=CASE,
                        tenant_id: str=TENANT, amount_cents: int=AMOUNT,
                        approver: str=APPROVER, approval_id: str=APPROVAL) -> str:
    """Trusted *test harness only*. This is NOT exposed as a server endpoint.

    Production replacement is a separately administered approval/identity issuer,
    with its own OS principal and protected signing key; see README.
    """
    if type(secret) is not bytes or len(secret)<32 or type(now) is not int:
        raise InvalidRequest('invalid fixture issuer inputs')
    claims={'schema':'etis-e5-grant-v1','case_id':case_id,'tenant_id':tenant_id,
            'amount_cents':amount_cents,'approver':approver,'approval_id':approval_id,
            'policy_version':POLICY,'expires_at':now+60,'issued_at':now}
    raw=canonical(claims)
    return raw.hex()+'.'+signature(secret,raw)


def verify_grant(value: Any, secret: bytes, *, now: int) -> dict[str, Any]:
    if type(value) is not str or len(value)>4096 or value.count('.')!=1:
        raise AuthorizationDenied('missing or malformed transaction approval')
    payload_hex,mac=value.split('.')
    if not payload_hex or len(payload_hex)%2 or len(payload_hex)>3500:
        raise AuthorizationDenied('malformed transaction approval')
    try:
        raw=bytes.fromhex(payload_hex)
        obj=json.loads(raw.decode('ascii'))
        bounded_object(obj,frozenset({'schema','case_id','tenant_id','amount_cents','approver',
                        'approval_id','policy_version','issued_at','expires_at'}))
        if canonical(obj)!=raw:
            raise AuthorizationDenied('noncanonical transaction approval')
    except (ValueError,UnicodeError,TypeError,OverflowError) as exc:
        raise AuthorizationDenied('invalid transaction approval') from exc
    expected=signature(secret,raw)
    if len(mac)!=len(expected) or not hmac.compare_digest(mac,expected):
        raise AuthorizationDenied('transaction approval integrity failure')
    if (obj['schema']!='etis-e5-grant-v1' or obj['case_id']!=CASE or
            obj['tenant_id']!=TENANT or type(obj['amount_cents']) is not int or
            obj['amount_cents']!=AMOUNT or obj['approver']!=APPROVER or
            obj['approval_id']!=APPROVAL or obj['policy_version']!=POLICY or
            type(obj['issued_at']) is not int or type(obj['expires_at']) is not int or
            not 0<=now-obj['issued_at']<=60 or
            not obj['issued_at']<=now<obj['expires_at'] or
            obj['expires_at']-obj['issued_at']!=60):
        raise AuthorizationDenied('transaction approval outside policy and scope')
    return obj
