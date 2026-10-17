"""Fine granularity: explicit construction and inference DNs for Euclid I.1."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from intention_space import (DNContract, DesignNode, Phrase, Proposal, Signal,
                             SituationalReality, State, Theorem, find, human_resolution,
                             pulse, serialise)

REALITY = SituationalReality(
    purpose="Construct and justify an equilateral triangle on a given segment AB",
    context="Euclidean plane with distinct points A and B; permitted constructions are joining points and drawing circles",
    assumptions=("A and B are distinct", "Euclidean postulates and definitions", "Circle intersection requires a separate warrant"),
    acceptance_conditions=("Every required construction and inference is justified", "Circle intersection warrant is established", "Observer explicitly accepts the reasoning trace"),
)
THEOREM = Theorem("Euclid, Elements I.1", "Construct an equilateral triangle on a given finite straight line")
PROPOSAL = Proposal("A", "The construction yields an equilateral triangle ABC on AB")
# Output phrase, meaning, required inputs, rationale / rule reference.
STEPS = (
    ("JoinAB", "line_AB", "Line AB has been drawn", ("distinct_A_B",), "Postulate 1: join any two points"),
    ("CircleA", "circle_A", "Circle centred A radius AB exists", ("line_AB",), "Postulate 3: draw a circle with given centre and distance"),
    ("CircleB", "circle_B", "Circle centred B radius BA exists", ("line_AB",), "Postulate 3: draw a circle with given centre and distance"),
    ("Intersection", "common_C", "The two circles share a point C", ("circle_A", "circle_B", "intersection_warrant"), "Common point C follows only if intersection is warranted"),
    ("JoinAC", "line_AC", "Segment AC is drawn", ("common_C",), "Postulate 1"),
    ("JoinBC", "line_BC", "Segment BC is drawn", ("common_C",), "Postulate 1"),
    ("RadiusA", "AC_eq_AB", "AC equals AB", ("circle_A", "common_C", "line_AC"), "Definition of circle: A-centred radii are equal"),
    ("RadiusB", "BC_eq_AB", "BC equals AB", ("circle_B", "common_C", "line_BC"), "Definition of circle: B-centred radii are equal"),
    ("Equality", "AC_eq_BC", "AC equals BC", ("AC_eq_AB", "BC_eq_AB"), "Common Notion 1: things equal to the same thing are equal"),
    ("Equilateral", "equilateral_ABC", "All three sides of ABC are equal", ("AC_eq_AB", "BC_eq_AB", "AC_eq_BC", "line_AB", "line_AC", "line_BC"), "Definition of equilateral triangle"),
)


def make_dn(name: str, output: str, meaning: str, prerequisites: tuple[str, ...], rule: str) -> DesignNode:
    contract = DNContract(name + "DN", meaning, prerequisites, rule)
    def implementation(signal: Signal) -> Signal:
        inputs = [find(signal, key) for key in prerequisites]
        ready = all(p.state == State.Y for p in inputs)
        explanation = rule if ready else "Not established because: " + ", ".join(p.phrase.name + "=" + p.state.value for p in inputs if p.state != State.Y)
        return Signal(Phrase("establish_" + output, "Establish " + meaning), (pulse(output, meaning, State.Y if ready else State.U, explanation, rule),))
    return DesignNode(contract, implementation)


def run(*, intersection_warrant: State = State.Y, decision: bool | None = True) -> dict:
    observations = {
        "distinct_A_B": pulse("distinct_A_B", "A and B are different points", State.Y, "Given finite, nonzero segment AB"),
        "intersection_warrant": pulse("intersection_warrant", "Constructed circles have a common point", intersection_warrant,
            "Separately accepted Euclidean circle-intersection principle" if intersection_warrant == State.Y else "Intersection principle not established; must not be inferred from the drawing alone"),
    }
    trace = []
    for name, output, meaning, prerequisites, rule in STEPS:
        dn = make_dn(name, output, meaning, prerequisites, rule)
        input_signal = Signal(Phrase("establish_" + output, meaning), tuple(observations[key] for key in prerequisites))
        execution = dn.execute(input_signal)
        trace.append(serialise(execution))
        observations[output] = execution.output.pulses[0]
    resolution = human_resolution(PROPOSAL, observations["equilateral_ABC"], decision)
    return dict(granularity="fine: constructions and inferences are exposed as individual DNs", situational_reality=serialise(REALITY), theorem=serialise(THEOREM), proposal=serialise(PROPOSAL), trace=trace, resolution=serialise(resolution), limitations=["Educational trace, not a formal Euclidean proof checker", "The circle-intersection warrant is external and explicit", "DN rules are trusted implementations, not mechanically verified axioms", "A human's independence is not established by the code"])

if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
