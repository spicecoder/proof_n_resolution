import unittest
from dataclasses import replace
from rba import Decision, Pulse, Signal, SituationalReality, State, Theorem, Proposal, example, resolve


class ResolutionTests(unittest.TestCase):
    def setUp(self):
        self.reality = SituationalReality("Drawing", "A triangle drawing is being reviewed", ("Same triangle",), 1, "Careful use")
        self.theorem = Theorem("Euclid I.32", "Triangle interior angles sum to 180°", "Euclidean geometry")
        self.proposal = Proposal("A", "Accept recorded angles for this drawing")
        self.requirement = Signal("Accept observed angles?", ())
        self.observation = Signal("Recorded angles", (
            Pulse("angle_A", State.YES, 50), Pulse("angle_B", State.YES, 60),
            Pulse("angle_C", State.YES, 70)))
        self.human = Decision("Reviewer", State.YES, "Checked measurement context", True)

    def run_resolution(self, observation=None, human=None):
        return resolve(self.reality, self.theorem, self.proposal, self.requirement,
                       self.observation if observation is None else observation,
                       self.human if human is None else human)

    def test_yes_requires_both(self):
        self.assertEqual(self.run_resolution()["resolution"], "Y")

    def test_human_independence_unconfirmed(self):
        result = self.run_resolution(human=replace(self.human, independence_confirmed=False))
        self.assertEqual(result["resolution"], "U")

    def test_human_rejects(self):
        result = self.run_resolution(human=replace(self.human, state=State.NO))
        self.assertEqual(result["resolution"], "N")

    def test_bad_arithmetic_does_not_pass(self):
        bad = Signal("Observed", (
            Pulse("angle_A", State.YES, 50), Pulse("angle_B", State.YES, 60),
            Pulse("angle_C", State.YES, 80)))
        self.assertEqual(self.run_resolution(observation=bad)["resolution"], "U")

    def test_missing_observation(self):
        incomplete = Signal("Observed", (Pulse("angle_A", State.YES, 50),))
        self.assertEqual(self.run_resolution(observation=incomplete)["computation"], "U")

    def test_theorem_and_assertion_explicit(self):
        result = self.run_resolution()
        self.assertEqual(result["proposal"]["identifier"], "A")
        self.assertIn("Euclid", result["theorem"]["reference"])
        self.assertIn("A", result["steps"][0]["result"]["proposal"]["identifier"])

    def test_eight_stages(self):
        self.assertEqual([s["stage"] for s in example()["steps"]], list("RFCAVPIT"))


if __name__ == "__main__":
    unittest.main()
