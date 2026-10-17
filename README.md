# Proof and Resolution — Two Granularities

A small, standard-library-only Python illustration of the distinction between **establishing mathematical validity** and **resolving an assertion in a declared Situational Reality**. It is intended for mathematicians and software developers; no CPUX runtime or LLM is required.

The terminology **Intention**, **Pulse**, **Signal**, **Design Node (DN)** and **Situational Reality** follows the Intention Space approach described by [IntentixLab](https://intentixlab.com/). These are illustrative implementations, not a normative specification of that framework.

## The core idea

A **DN is a black box at its caller's chosen granularity**. Its internal reasoning or computation may be hidden from the caller, but the DN must expose the contract needed for responsible reuse: designated input/output Signals, assumptions, relevant justification, and provenance. Black-box *execution* is not permission for black-box *authority*.

A **Pulse** has a named **Phrase** with a description of what is being asserted; its `state` is `Y` (established), `N` (rejected/refuted), or `U` (unresolved). Its `why` explains *why this particular state was emitted*, with optional provenance. These descriptions make a Pulse inspectable; they **do not** independently validate an unsound inference.

A **Signal** groups an explicit Intention Phrase with relevant Pulses. A **Situational Reality** declares purpose, context, assumptions, and acceptance conditions. An **A** (proposal) is the assertion to be resolved. Human Resolution is a distinct decision on the applicability and sufficiency of evidence in that reality—not a way to turn false mathematics into true mathematics.

## Why two examples?

| | 01 — Established theorem as a DN | 02 — Euclid's resolution at fine granularity |
|---|---|---|
| Situational Reality | Decide whether reported triangle angles are acceptable for a drawing | Construct an equilateral triangle on segment AB |
| Proposed A | Those recorded angles are acceptable | The constructed triangle ABC is equilateral |
| Mathematical source | Euclid *Elements* I.32 (angle sum) | Euclid *Elements* I.1 (construction) |
| Granularity | The proof of I.32 is already established and invoked as one black-box DN | Construction, observation and inference are separate DNs |
| What is made visible | Applicability of a theorem, arithmetic, measurement reliability, observer decision | Individual dependencies and reasons for the state at each step |
| What remains external | The actual proof of I.32 | An explicit circle-intersection warrant and soundness of rules |

**These are different propositions, not a claim that I.1 is a finer-grained proof of I.32.** They demonstrate the *same discipline* at two chosen granularities. One could replace any established fine-grained chain by a contracted DN at a coarser level, provided its obligations remain accessible.

### 01 — Established proof, reused

A theorem that has already been established may be encapsulated by `EstablishedAngleSumTheoremDN`. The caller sees only its declared applicability, conclusion and proof reference. Recorded angles 50°, 60°, 70° sum to 180°, but the result does **not** prove that the angles actually came from the claimed triangle. A separate reliability Pulse and an explicit human decision remain necessary. Failure to establish the assumptions yields `U` rather than automatic acceptance.

### 02 — Establishing Euclid I.1

The argument is decomposed into DNs for drawing AB, drawing two circles, obtaining common point C, joining sides, using the definition of a circle, inferring equality, and concluding equilateralness. Each DN emits a Pulse describing **why** it has the state it has. The common-point step requires an *explicit circle-intersection warrant*. If that warrant is `U`, later claims remain `U`, and the final Resolution is `U`.

This is **not** a machine-checked formal proof. A true formal checker would need a precise axiomatization, validated inference rules and a proof of the intersection lemma under the chosen geometry.

## Try it

Python 3.10+; no installation needed:

```bash
python examples/01_established_theorem.py
python examples/02_euclid_construction.py
python -m unittest discover -s tests -v
```

From another Python script, you may import the examples using `importlib` or run the scripts directly. Every example's `run(...)` returns serialisable data that includes its declared reality, theorem, A, DN trace and final Resolution.

## Three experiments

- Set `applicable=False` in example 01: theorem applicability becomes unresolved.
- Set `measurements_trusted=False` in example 01: a valid arithmetic sum cannot certify observed measurements.
- Set `intersection_warrant=State.U` in example 02: dependent assertions become unresolved.

In both examples `decision=None` represents a missing human Resolution; `decision=False` represents an observer's rejection **within the Situational Reality**, not a disproof of Euclid.

## Scope and limitations

1. `Y/N/U` record the status of an *assertion in a declared process*, not absolute mathematical truth.
2. A DN can be implemented by a person, software or AI; neither source alone establishes authority.
3. Phrase descriptions and `why` are explanations for audit, not proof certificates.
4. Observer independence and quality of judgment must be examined separately; they cannot be guaranteed by following this program.
5. This repository illustrates a principle of preserving validity obligations across **granularity changes**. It does not claim that all mathematical reasoning is algorithmic or that mathematics should serve machine requirements.

Read the motivating article: [Proof and Resolution: Two Different Forms of Establishment](https://proofsandprompts.com/2026/10/15/proof-and-resolution-two-different-forms-of-establishment/).
