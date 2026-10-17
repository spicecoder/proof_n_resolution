import importlib.util
from pathlib import Path
import unittest
from intention_space import State

ROOT = Path(__file__).resolve().parents[1]
def load(name):
    path = ROOT / 'examples' / name
    spec = importlib.util.spec_from_file_location(name.removesuffix('.py'), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

coarse = load('01_established_theorem.py')
fine = load('02_euclid_construction.py')

class ExamplesTest(unittest.TestCase):
    def test_coarse_acceptance(self):
        self.assertEqual(coarse.run()['resolution']['state'], 'Y')
    def test_coarse_applicability(self):
        self.assertEqual(coarse.run(applicable=False)['resolution']['state'], 'U')
    def test_coarse_measurement(self):
        self.assertEqual(coarse.run(measurements_trusted=False)['resolution']['state'], 'U')
    def test_fine_acceptance(self):
        self.assertEqual(fine.run()['resolution']['state'], 'Y')
    def test_fine_warrant(self):
        self.assertEqual(fine.run(intersection_warrant=State.U)['resolution']['state'], 'U')
    def test_no_human_decision(self):
        self.assertEqual(fine.run(decision=None)['resolution']['state'], 'U')
    def test_human_rejection_not_refutation(self):
        self.assertEqual(coarse.run(decision=False)['resolution']['state'], 'N')
    def test_pulse_explanation(self):
        report = fine.run(intersection_warrant=State.U)
        self.assertTrue(all(p['why'] for s in report['trace'] for p in s['output']['pulses']))

if __name__ == '__main__': unittest.main()
