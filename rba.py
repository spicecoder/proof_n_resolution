"""Small, dependency-free illustration of human-led Resolution in Intention Space.

Run: python rba.py
Tests: python -m unittest discover -s tests
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from hashlib import sha256
import json
from typing import Any


class State(str, Enum):
    YES = "Y"
    NO = "N"
    UNKNOWN = "U"


@dataclass(frozen=True)
class Pulse:
    """Named observation with a trivalent state and an optional measure."""
    name: str
    state: State
    value: Any = None


@dataclass(frozen=True)
class Signal:
    """Intention (purpose) paired with the Pulses that provide context."""
    intention: str
    pulses: tuple[Pulse, ...]


@dataclass(frozen=True)
class SituationalReality:
    """Declared context and acceptance conditions, not universal truth."""
    purpose: str
    description: str
    assumptions: tuple[str, ...]
    tolerance_degrees: float
    human_value: str


@dataclass(frozen=True)
class Theorem:
    """A proven general proposition, cited rather than proved by this program."""
    reference: str
    statement: str
    domain: str


@dataclass(frozen=True)
class Proposal:
    """A situated assertion A, distinct from the general theorem."""
    identifier: str
    assertion: str


@dataclass(frozen=True)
class Decision:
    """Decision made by an identified human; never manufactured by the DN."""
    observer: str
    state: State
    explanation: str
    independence_confirmed: bool


class AngleCheckDN:
    """Design Node: checks supplied numbers, NOT Euclid's general theorem."""
    name = "AngleCheckDN"

    def execute(self, signal: Signal, reality: SituationalReality) -> Signal:
        values = {pulse.name: pulse for pulse in signal.pulses}
        names = ("angle_A", "angle_B", "angle_C")
        if any(n not in values or values[n].state != State.YES for n in names):
            result = Pulse("observed_sum_within_tolerance", State.UNKNOWN,
                           "Required angle observations unavailable")
        else:
            angles = [values[n].value for n in names]
            if any(type(v) not in (int, float) or not 0 < v < 180 for v in angles):
                result = Pulse("observed_sum_within_tolerance", State.NO,
                               "One or more angles are invalid")
            else:
                total = sum(angles)
                ok = abs(total - 180) <= reality.tolerance_degrees
                result = Pulse("observed_sum_within_tolerance",
                               State.YES if ok else State.NO,
                               {"sum": total, "tolerance": reality.tolerance_degrees})
        return Signal("Report arithmetic check of supplied triangle angles", (result,))


def digest(value: Any) -> str:
    """Anchor a declared snapshot; a hash does not authenticate its source."""
    blob = json.dumps(value, sort_keys=True, default=str).encode("utf-8")
    return sha256(blob).hexdigest()[:16]


def resolve(reality: SituationalReality, theorem: Theorem, proposal: Proposal,
            requirement: Signal, observation: Signal, decision: Decision) -> dict[str, Any]:
    """Eight visible stages; human judgment is distinct from machine checking."""
    if reality.tolerance_degrees < 0:
        raise ValueError("Tolerance cannot be negative")
    if not decision.observer.strip():
        raise ValueError("An observer must be identified")
    steps: list[dict[str, Any]] = []

    def record(letter: str, description: str, value: Any) -> None:
        steps.append({"stage": letter, "description": description, "result": value})

    # R — Requirement is a Signal whose Intention states what must be resolved.
    record("R", "Theorem, proposed assertion A, and requirement",
           {"theorem": asdict(theorem), "proposal": asdict(proposal),
            "requirement_intention": requirement.intention})

    # F — Identify and anchor the specific artefact, not an abstract theorem.
    artefact = asdict(observation)
    record("F", "Observed artefact snapshot", {"sha256_prefix": digest(artefact)})

    # C — Explicit correspondence: the required pulse names must be present.
    expected = {"angle_A", "angle_B", "angle_C"}
    available = {p.name for p in observation.pulses}
    correspondence = expected.issubset(available)
    record("C", "Declared semantic correspondence", correspondence)

    # A — Make situational assumptions and value commitments inspectable.
    record("A", "Situational Reality", asdict(reality))

    # V — Isolated deterministic computation, not a mathematical proof.
    report = AngleCheckDN().execute(observation, reality) if correspondence else Signal(
        "Report missing observations", (Pulse("observed_sum_within_tolerance", State.UNKNOWN),))
    check = report.pulses[0]
    record("V", "Design Node check (not proof)", asdict(check))

    # P — Preserve origin; the emitted Signal has a different Intention.
    record("P", "Provenance", {"input_anchor": digest(artefact),
                                "design_node": AngleCheckDN.name,
                                "emitted_intention": report.intention})

    # I — Observer's interpretation cannot be filled in by code.
    record("I", "Human interpretation", {"observer": decision.observer,
                                            "explanation": decision.explanation,
                                            "independence_confirmed": decision.independence_confirmed})

    # T — The machine cannot force acceptance. Unexamined independence => U.
    if not decision.independence_confirmed or not decision.explanation.strip():
        terminal = State.UNKNOWN
    elif decision.state == State.NO:
        terminal = State.NO
    elif decision.state == State.YES and check.state == State.YES:
        terminal = State.YES
    else:
        terminal = State.UNKNOWN
    record("T", "Requirement-relative human Resolution", terminal.value)
    return {"reality": asdict(reality), "theorem": asdict(theorem),
            "proposal": asdict(proposal), "steps": steps,
            "computation": check.state.value, "resolution": terminal.value}


def example() -> dict[str, Any]:
    reality = SituationalReality(
        purpose="Assess a triangular drawing using recorded angle measurements",
        description="A person has a triangular drawing with recorded interior angles "
                    "50°, 60°, and 70°. The person must decide whether those "
                    "observations are acceptable for the intended drawing.",
        assumptions=("Angles are from the same triangle",
                     "Measurements are in degrees", "Measurement method is trusted by observer"),
        tolerance_degrees=1.0,
        human_value="Do not claim a general theorem from three measured numbers")
    theorem = Theorem(
        reference="Euclid, Elements, Book I, Proposition 32",
        statement="The interior angles of a Euclidean triangle sum to two right angles (180°).",
        domain="Euclidean plane geometry")
    proposal = Proposal(
        identifier="A",
        assertion="The three recorded angles are acceptable as interior-angle "
                  "measurements of the triangle in this drawing.")
    requirement = Signal("Decide whether assertion A should be accepted for this drawing",
                         (Pulse("acceptance_requested", State.YES),))
    observation = Signal("Record three measured interior angles", (
        Pulse("angle_A", State.YES, 50),
        Pulse("angle_B", State.YES, 60),
        Pulse("angle_C", State.YES, 70)))
    # This decision is a declared example input, NOT a simulated human review.
    human_decision = Decision(
        observer="Example reviewer (hypothetical)", state=State.YES,
        explanation="Assuming the measurements and drawing context are reliable, accept this record only.",
        independence_confirmed=True)
    return resolve(reality, theorem, proposal, requirement, observation, human_decision)


if __name__ == "__main__":
    print(json.dumps(example(), indent=2, default=str))
