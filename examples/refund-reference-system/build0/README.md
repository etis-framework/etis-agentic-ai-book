# Build 0 — Deterministic Refund Baseline

**Chapter 22 hands-on exercise.** The reference fixture is **not** a production payment service. It uses Python's standard library only and never sends money or uses credentials.

## Inspect the files

- `refund.py` — fixed CASE-204 / $500 (50000 integer cents) / RF-1042; trusted fixture approval, durable local intent, mock provider dispatch and reconciliation.
- `test_refund.py` — six self-contained unittest scenarios using temporary databases.
- E7 local status: `operations.sqlite3`; simulated E8 payment truth: `provider.sqlite3`. These are two different SQLite files, **not** a distributed transaction.

The fixed `approved` flag is not a real human-approval system. The provider's unique operation key models a fictional contract, not a verified live-provider guarantee.

## Exercise 1 — run the negative and recovery tests

From the repository root:

```sh
python3 -m unittest discover -s examples/refund-reference-system/build0 -p 'test_*.py' -v
```

Expected: six passing tests. Read the test names and assertions, especially the wrong-tenant, duplicate-dispatch, lost-acknowledgment, missing-provider and conflicting-provider tests. Passing them demonstrates only the tested fixture behavior.

## Exercise 2 — compare E7 and E8 after a lost acknowledgment

Use a **fresh** disposable demo directory. Run these in order from the repository root:

```sh
python3 examples/refund-reference-system/build0/refund.py prepare --directory /tmp/etis-build0-demo
python3 examples/refund-reference-system/build0/refund.py dispatch-lost-ack --directory /tmp/etis-build0-demo
python3 examples/refund-reference-system/build0/refund.py status --directory /tmp/etis-build0-demo
```

At this point E7 reports **UNKNOWN**, even though mock E8 has one RF-1042 **CONFIRMED** row. Inspect the two databases with Python (no SQLite CLI required):

```sh
python3 - <<'READ_ONLY_DEMO'
from pathlib import Path
import sqlite3
folder = Path('/tmp/etis-build0-demo')
for label, filename, table in [('E7 local','operations.sqlite3','operations'),
                               ('E8 mock','provider.sqlite3','refunds')]:
    with sqlite3.connect(folder / filename) as db:
        print(label, db.execute('SELECT * FROM ' + table).fetchall())
READ_ONLY_DEMO
```

Then reconcile under the **same operation identity** and inspect again:

```sh
python3 examples/refund-reference-system/build0/refund.py reconcile --directory /tmp/etis-build0-demo
```

| Observation | E7 local operation | Mock E8 provider |
|---|---|---|
| After `prepare` | AUTHORIZED | No refund row |
| After `dispatch-lost-ack` | UNKNOWN | RF-1042 CONFIRMED |
| After `reconcile` | CONFIRMED | Same RF-1042 CONFIRMED |

The CLI prints local E7 status only. A real provider's absence or contradictory response would leave the outcome unresolved; it would **not** permit a new $500 refund.

## Exercise 3 — judgment and limitations

Explain why wrong-tenant or missing approval cannot create E7 intent; why a timeout does not mean FAILED; why repeating dispatch after UNKNOWN is prohibited; and what external-provider contract evidence would be needed to claim a live refund occurred.

**Not demonstrated:** concurrent workers, E2 owner fencing, secure E5 isolation, live E1 authentication, credentials, network error models, full E9 audit evidence, or real-world idempotency. Never attach this fixture to a payment service. Use a fresh demo directory each time and delete only the disposable files you created. Chapter 23 will add advisory interpretation *without* payment authority.
