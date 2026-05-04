import unittest
from workout import Workout


class WorkoutTest(unittest.TestCase):

    def test_workout_creation(self):
        workout = Workout("Кардио тренировка", 45)

        self.assertEqual("Кардио тренировка", workout.get_title())
        self.assertEqual(45, workout.get_duration())

    def test_workout_update(self):
        workout = Workout("Кардио тренировка", 45)
        workout.update_workout("Силовая тренировка", 60)

        self.assertEqual("Силовая тренировка", workout.get_title())
        self.assertEqual(60, workout.get_duration())

    def test_workout_validation(self):
        workout = Workout("Кардио тренировка", 45)

        self.assertTrue(workout.is_valid())


if __name__ == "__main__":
    unittest.main()
