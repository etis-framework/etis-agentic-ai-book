"""Port for untrusted candidate generation, not an execution tool API."""
from typing import Mapping, Protocol, Any
from contracts import Evidence, WorkRequest

class CandidateModel(Protocol):
    """No E5/E6/E7 capability is accepted or exposed by this port."""
    def propose(self, work: WorkRequest, evidence: Evidence) -> Mapping[str, Any]: ...
