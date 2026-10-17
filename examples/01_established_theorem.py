"""Coarse granularity: a previously established theorem behaves as a DN black box."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from intention_space import (DNContract, DesignNode, Phrase, Proposal, Pulse, Signal,
                             SituationalReality, State, Theorem, find, human_resolution,
                             pulse, serialise)

REALITY = SituationalReality(
    purpose="Decide whether three recorded angles can be accepted as measurements of a Euclidean triangle",
    context="A drawing is reported to depict a nondegenerate Euclidean triangle ABC; angles recorded as 50, 60 and 70 degrees",
    assumptions=("Euclidean plane", "Nondegenerate triangle ABC", "Recorded angles are intended as its interior angles"),
    acceptance_conditions=("The established theorem applies", "The reported angles sum to 180 degrees", "The observer accepts the measurement provenance"),
)
THEOREM = Theorem("Euclid, Elements I.32", "The three interior angles of a Euclidean triangle sum to 180 degrees")
PROPOSAL = Proposal("A", "The three recorded angles are acceptable for the intended drawing")
CONTRACT = DNContract("EstablishedAngleSumTheoremDN", "Apply an already established theorem without re-running its finer-grained proof", ("Euclidean plane", "Nondegenerate triangle"), "Euclid, Elements I.32; the proof is external to this demonstration")


def _theorem_impl(signal: Signal) -> Signal:
    applicable = find(signal, "euclidean_triangle")
    result = pulse("angle_sum_theorem", "Interior-angle sum is 180 degrees for the given triangle", State.Y if applicable.state == State.Y else State.U,
                   "I.32 applies under the declared assumptions" if applicable.state == State.Y else "Theorem applicability has not been established", THEOREM.reference)
    return Signal(Phrase("apply_theorem", "Apply the established theorem to the declared triangle"), (result,))

THEOREM_DN = DesignNode(CONTRACT, _theorem_impl)


def run(*, applicable: bool = True, measurements_trusted: bool = True, decision: bool | None = True) -> dict:
    incoming = Signal(Phrase("check_triangle", "Check eligibility to reuse Euclid I.32"), (
        pulse("euclidean_triangle", "Given object is a Euclidean nondegenerate triangle", State.Y if applicable else State.U, "Assumed from declared context" if applicable else "Triangle assumptions unconfirmed"),
    ))
    step = THEOREM_DN.execute(incoming)
    values = (50, 60, 70)
    theorem_pulse = find(step.output, "angle_sum_theorem")
    numeric = pulse("reported_sum", "The three recorded angles total 180 degrees", State.Y if sum(values) == 180 else State.N, f"Calculated {values[0]} + {values[1]} + {values[2]} = {sum(values)}")
    measurement = pulse("measurement_provenance", "The three recordings are trustworthy observations of the depicted triangle", State.Y if measurements_trusted else State.U, "Observer supplies confidence in measurements" if measurements_trusted else "Measurement reliability not established")
    checks = (theorem_pulse, numeric, measurement)
    accepted = all(p.state == State.Y for p in checks)
    supporting = pulse("assertion_supported", PROPOSAL.assertion, State.Y if accepted else State.U, "All declared acceptance conditions have supporting evidence" if accepted else "One or more acceptance conditions remain unestablished", "Theorem DN + numeric check + observer-supplied reliability")
    resolution = human_resolution(PROPOSAL, supporting, decision)
    return dict(granularity="coarse: established proof reused as a black-box DN", situational_reality=serialise(REALITY), theorem=serialise(THEOREM), proposal=serialise(PROPOSAL), theorem_step=serialise(step), other_evidence=[serialise(p) for p in (numeric, measurement, supporting)], resolution=serialise(resolution), limitations=["I.32 is referenced, not proved by this program", "The supplied angles are not verified against physical measurements", "Observer choice does not create mathematical truth"])

if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
