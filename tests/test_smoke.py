import unittest

class SmokeTest(unittest.TestCase):
    def test_ci_runs(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()