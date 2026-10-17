"""Small Intention Space vocabulary for demonstrative Resolution traces.

A DN is a black box to its caller: only its designated Signals, contract,
and provenance are required at the caller's granularity.
"""
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Callable

class State(str, Enum):
    Y = "Y"  # established for the declared context
    N = "N"  # explicitly refuted or rejected
    U = "U"  # unresolved / not established

@dataclass(frozen=True)
class Phrase:
    name: str
    description: str

@dataclass(frozen=True)
class Pulse:
    phrase: Phrase
    state: State
    why: str
    provenance: str = ""

@dataclass(frozen=True)
class Signal:
    intention: Phrase
    pulses: tuple[Pulse, ...]

@dataclass(frozen=True)
class SituationalReality:
    purpose: str
    context: str
    assumptions: tuple[str, ...]
    acceptance_conditions: tuple[str, ...]

@dataclass(frozen=True)
class Proposal:
    identifier: str
    assertion: str

@dataclass(frozen=True)
class Theorem:
    reference: str
    assertion: str

@dataclass(frozen=True)
class DNContract:
    name: str
    description: str
    assumptions: tuple[str, ...]
    justification_reference: str

@dataclass(frozen=True)
class TraceStep:
    dn: DNContract
    input: Signal
    output: Signal

class DesignNode:
    """Calls a private implementation through a public, declared contract."""
    def __init__(self, contract: DNContract, operation: Callable[[Signal], Signal]):
        self.contract = contract
        self._operation = operation

    def execute(self, incoming: Signal) -> TraceStep:
        return TraceStep(self.contract, incoming, self._operation(incoming))


def pulse(name: str, meaning: str, state: State, why: str, provenance: str = "") -> Pulse:
    return Pulse(Phrase(name, meaning), state, why, provenance)


def find(signal: Signal, name: str) -> Pulse:
    for item in signal.pulses:
        if item.phrase.name == name:
            return item
    return pulse(name, f"Undeclared prerequisite {name}", State.U, "No matching observation supplied")


def human_resolution(proposal: Proposal, evidence: Pulse, decision: bool | None) -> Pulse:
    if evidence.state != State.Y:
        return pulse("resolution", proposal.assertion, State.U, "Required assertion is not established; human acceptance cannot supply a missing proof", evidence.provenance)
    if decision is None:
        return pulse("resolution", proposal.assertion, State.U, "Human judgment has not been recorded", evidence.provenance)
    if decision is False:
        return pulse("resolution", proposal.assertion, State.N, "Observer declines acceptance in this Situational Reality; this does not refute the theorem", evidence.provenance)
    return pulse("resolution", proposal.assertion, State.Y, "Observer accepts the stated assumptions, evidence and applicability in this Situational Reality", evidence.provenance)


def serialise(obj):
    return asdict(obj)
