# Proof and Resolution — a small Intention Space example

A runnable, standard-library-only Python illustration of a **Resolution Boundary Auditor (RBA)** process. It accompanies the [Proof and Resolution discussion](https://proofsandprompts.com/2026/10/15/proof-and-resolution-two-different-forms-of-establishment/). It does **not** prove a theorem or automate human judgment.

## 1. Situational Reality

A person is evaluating a triangular drawing in Euclidean geometry. Three interior angles have been recorded as **50°, 60°, and 70°**. The person must decide whether these observations are acceptable for the intended drawing, taking account of the source of the measurements, geometric assumptions, and the practical purpose of acceptance.

This is a *declared* Situational Reality, not an objective guarantee that the measurements are correct. Its purpose, description, assumptions, tolerance and human value are represented by `SituationalReality`.

## 2. The theorem

**Euclid, Elements, Book I, Proposition 32:** the three interior angles of a Euclidean triangle add to two right angles (**180°**).

This is a general mathematical result about Euclidean triangles. The program **does not prove it**; it records the theorem and its domain as a reference relevant to this situation.

## 3. What has been proposed — assertion A

> **A:** The three recorded angles are acceptable as interior-angle measurements of the triangle in this drawing.

A is a *situated assertion*, not the general theorem. Acceptance requires more than arithmetic: the observations must be meaningful for this drawing and sufficiently reliable for its intended use.

The deterministic Design Node checks only whether the supplied numbers are valid angle values and their sum is within the declared tolerance of 180°. Thus **50 + 60 + 70 = 180** is consistent with the theorem, but cannot prove Euclid I.32 or prove that the measurements originated from the stated triangle. Even a valid sum does not establish all conditions for a geometrically valid, accurately measured drawing.

## 4. Proof, check, and Resolution

| Establishment | Question | Role here |
| --- | --- | --- |
| **Proof** | Does a general statement follow from premises? | Euclid I.32 is cited as an established theorem |
| **Computational check** | Do these three supplied values sum to 180° within tolerance? | A Design Node returns a Signal |
| **Resolution** | Should the human observer accept **A** in this Situational Reality? | Observer judges the claim using the result, assumptions and values |

Resolution is **a process, not an authority**. The final decision belongs to an observer; the protocol exposes inputs and criteria but cannot guarantee the observer's independence or correctness.

## 5. Intention Space entities

| Entity | What it represents |
| --- | --- |
| `SituationalReality` | Purpose, narrative description, assumptions, tolerance, human value |
| `Theorem` | Referenced theorem, statement, and mathematical domain |
| `Proposal` | Explicit proposed assertion **A** |
| `Intention` | Purpose conveyed in a `Signal` |
| `Pulse` | Named observation with a measure and `Y`, `N`, or `U` |
| `Signal` | Intention paired with Pulses |
| `AngleCheckDN` | Deterministic Design Node that emits a check Signal |
| `Decision` | Hypothetical human observer's explicit judgment, explanation, and independence declaration |

## 6. The eight visible RBA stages

`R` Requirement, theorem, and proposal → `F` artefact snapshot → `C` correspondence → `A` assumptions / Situational Reality → `V` deterministic check → `P` provenance → `I` interpretation → `T` terminal Resolution.

| State | Meaning |
| --- | --- |
| `Y` | Check passes **and** observer explicitly accepts A with an explanation and independence declaration |
| `N` | Observer explicitly rejects A |
| `U` | Resolution unresolved, including missing independent judgment or a failed/incomplete check without explicit human rejection |

The example observer's decision is **hypothetical test input** and not an actual review. Independence is *self-declared*, not independently validated; the snapshot hash is not a guarantee of authenticity; correspondence only checks expected observation names, not deep semantic meaning.

## 7. Run

Python 3.10+; no external packages:

```bash
python rba.py
python -m unittest discover -s tests -v
```

The program prints JSON with the Situational Reality, cited theorem, proposed assertion **A**, and eight-stage Resolution trace. `sample_trace.json` provides an example.

Note : ###  On Terminology and Conceptual Foundation

This example adopts certain concepts and terminology from **Intention Space**, a framework for representing intentions and coordinating computational components, as introduced by [IntentixLab](https://intentixlab.com/).

In particular:

- **Situational Reality:** The declared context within which a proposed assertion is examined, including its assumptions, observations, requirements and relevant human judgments.
- **Intention:** An explicit representation of what is to be established or accomplished.
- **Pulse:** A structured representation of an observation or condition.
- **Signal:** An intention associated with relevant Pulses, providing the context for computational interaction.
- **Design Node (DN):** A computational component that receives designated Signals and produces Signals representing its results.

These concepts are used here to illustrate the **Resolution process**, not to redefine mathematical proof or prescribe how mathematicians should conduct their work.

For further background, see [IntentixLab](https://intentixlab.com/).



**Question for discussion:** A machine can verify a relation among the supplied values. What would justify accepting the situated assertion **A**, and how does a human observer recognise when their judgment is insufficiently independent?
# proof_n_resolution
