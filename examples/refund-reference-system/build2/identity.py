"""Educational E1/C01 assertion issuer/verifier, NOT enterprise authentication.

A fixture-only HMAC key models an independent identity assertion. Both issuer and
verifier run in the same Python trust domain; a malicious process can steal the key.
This module models claim integrity and expiry, not a security boundary.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import hmac
import json
from typing import Any

class ScopeDenied(ValueError):
    """Identity, scope, freshness or provenance does not meet the contract."""

class ContextUnavailable(RuntimeError):
    """A context dependency failed; no advisory proposal may be issued."""

CLAIMS = frozenset({'subject','tenant_id','case_id','purpose','allowed_sources','issued_at','expires_at','issuer'})
PURPOSE = 'review_replacement_complaint'
ISSUER = 'local-fixture-issuer-v1'


def _time(value: datetime) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ScopeDenied('aware UTC timestamp required')
    return value.astimezone(timezone.utc)


def _identifier(value: Any, name: str) -> str:
    if not isinstance(value, str) or not (3 <= len(value) <= 64) or not all(
        c.isascii() and (c.isalnum() or c in '_:-.') for c in value
    ):
        raise ScopeDenied(f'invalid {name}')
    return value


@dataclass(frozen=True)
class VerifiedScope:
    """Trusted only within the fixture verifier; never E5 financial authority."""
    subject: str
    tenant_id: str
    case_id: str
    purpose: str
    allowed_sources: tuple[str, ...]
    expires_at: int


# Both issuer and verifier must sign/check the *same bytes*. Sorted keys and
# compact separators prevent two JSON spellings of one claim set from drifting.
# Canonicalization establishes encoding agreement, not issuer independence.
def _canonical(claims: dict[str, Any]) -> bytes:
    return json.dumps(claims, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')


class LocalAssertionAuthority:
    """Simulates separate issuance and verification; no real identity provider."""
    def __init__(self, fixture_key: bytes):
        if type(fixture_key) is not bytes or len(fixture_key) < 32:
            raise ValueError('fixture signing key must be at least 32 bytes')
        self._key = fixture_key

    def issue(self, *, subject: str, tenant_id: str, case_id: str,
              allowed_sources: tuple[str, ...], now: datetime, lifetime_seconds: int = 300) -> str:
        stamp = int(_time(now).timestamp())
        if type(lifetime_seconds) is not int or not 1 <= lifetime_seconds <= 3600:
            raise ScopeDenied('invalid bounded lifetime')
        claims = dict(subject=_identifier(subject, 'subject'), tenant_id=_identifier(tenant_id, 'tenant'),
                      case_id=_identifier(case_id, 'case'), purpose=PURPOSE, issuer=ISSUER,
                      allowed_sources=list(allowed_sources), issued_at=stamp,
                      expires_at=stamp + lifetime_seconds)
        self._validate_claims(claims)
        # Construct the integrity envelope from validated scope claims. Possession
        # of the fixture key is sufficient to forge it; keep that limitation visible.
        payload = _canonical(claims)
        signature = hmac.new(self._key, payload, hashlib.sha256).hexdigest()
        return payload.hex() + '.' + signature

    @staticmethod
    def _validate_claims(claims: dict[str, Any]) -> None:
        if type(claims) is not dict or frozenset(claims) != CLAIMS:
            raise ScopeDenied('invalid assertion field set')
        for name in ('subject','tenant_id','case_id'):
            _identifier(claims[name], name)
        if claims['purpose'] != PURPOSE or claims['issuer'] != ISSUER:
            raise ScopeDenied('issuer or purpose mismatch')
        sources = claims['allowed_sources']
        if type(sources) is not list or not 1 <= len(sources) <= 8 or any(
            not isinstance(v, str) for v in sources
        ) or len(set(sources)) != len(sources):
            raise ScopeDenied('invalid source scope')
        for source in sources:
            _identifier(source, 'source')
        if any(type(claims[n]) is not int for n in ('issued_at','expires_at')):
            raise ScopeDenied('invalid assertion timestamp')
        if not 1 <= claims['expires_at'] - claims['issued_at'] <= 3600:
            raise ScopeDenied('invalid assertion interval')

    def verify(self, token: str, *, now: datetime) -> VerifiedScope:
        stamp = int(_time(now).timestamp())
        if type(token) is not str or len(token) > 4096 or token.count('.') != 1:
            raise ScopeDenied('malformed identity assertion')
        payload_hex, signature = token.split('.')
        if not payload_hex or len(payload_hex) > 3500 or len(payload_hex) % 2:
            raise ScopeDenied('malformed identity assertion')
        try:
            payload = bytes.fromhex(payload_hex)
            claims = json.loads(payload.decode('ascii'))
            if type(claims) is not dict or _canonical(claims) != payload:
                raise ScopeDenied('noncanonical assertion')
        except (ValueError, UnicodeError, TypeError, RecursionError) as exc:
            raise ScopeDenied('malformed identity assertion') from exc
        # Recompute on the received canonical bytes, then use constant-time
        # digest comparison. A valid HMAC authenticates these fixture claims,
        # but is NOT the separate transaction-specific finance approval.
        digest = hmac.new(self._key, payload, hashlib.sha256).hexdigest()
        if (not signature.isascii() or len(signature) != len(digest)
                or not hmac.compare_digest(signature, digest)):
            raise ScopeDenied('assertion integrity failure')
        self._validate_claims(claims)
        # Check both ends of the lifetime after signature verification: a valid
        # signature must not make a future-dated or expired assertion usable.
        if not claims['issued_at'] <= stamp < claims['expires_at'] or claims['issued_at'] > stamp:
            raise ScopeDenied('assertion expired or not yet valid')
        return VerifiedScope(claims['subject'], claims['tenant_id'], claims['case_id'],
                             claims['purpose'], tuple(claims['allowed_sources']), claims['expires_at'])
