"""Narrow first-edition planning exception; not a waiver of print or technical QA."""
from hashlib import sha256
from pathlib import Path

CHAPTER = 'manuscript/part-05-reliability-security/ch29-security-and-adversarial-agent-behavior/index.md'
DIGEST = '0fef0d48646ea87e99507e7706935758ecd63e762631144c04884dc961fbabb9'


def approved_word_overage(root: Path, path: Path, count: int, cap: int) -> bool:
    """Accept only the exact frozen Chapter 29 source and original budget."""
    return (path.resolve() == (root / CHAPTER).resolve()
            and count == 3654 and cap == 3500
            and sha256(path.read_bytes()).hexdigest() == DIGEST)
