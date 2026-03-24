import unittest
from workout import Workout

class WorkoutTest(unittest.TestCase):
    def test_workout_creation(self):
        workout = Workout("Кардио тренировка", 45)
        self.assertEqual("Кардио тренировка", workout.get_title())
        self.assertEqual(45, workout.get_duration())

if __name__ == "__main__":
    unittest.main()