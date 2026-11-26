"""Unprivileged request transport; intentionally lacks grant issuer and E6 imports."""
import json
from pathlib import Path
import socket
from typing import Any

class ServiceUnavailable(RuntimeError):
    """Transport error; do not infer that financial effect failed."""


def request(socket_path: Path, body: dict[str, Any]) -> dict[str, Any]:
    """Send one bounded framed request. Server alone evaluates financial approval."""
    try:
        raw=json.dumps(body,sort_keys=True,allow_nan=False).encode('utf-8')+b'\n'
        if len(raw)>8192:
            raise ValueError('request too large')
        with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as sock:
            sock.settimeout(3.0)
            sock.connect(str(socket_path))
            sock.sendall(raw)
            chunks=bytearray()
            while len(chunks)<=8192:
                part=sock.recv(1024)
                if not part: break
                chunks.extend(part)
                if b'\n' in part: break
        if len(chunks)>8192 or not chunks.endswith(b'\n'):
            raise ServiceUnavailable('incomplete service response; outcome uncertain')
        response=json.loads(chunks[:-1])
        if type(response) is not dict or response.get('status') not in {'CONFIRMED','DENIED','UNKNOWN'}:
            raise ServiceUnavailable('invalid service response; outcome uncertain')
        return response
    except (OSError,TimeoutError,ValueError,TypeError,RecursionError) as exc:
        raise ServiceUnavailable('trusted service unavailable; reconcile before retry') from exc
