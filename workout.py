class Workout:
    """Класс для хранения информации о тренировке."""

    def __init__(self, title: str, duration: int, user_id: int = 1):
        self._validate_workout_data(title, duration)
        self.title = title
        self.duration = duration
        self.user_id = user_id  # ← добавили

    def get_title(self) -> str:
        """Возвращает название тренировки."""
        return self.title

    def get_duration(self) -> int:
        """Возвращает длительность тренировки в минутах."""
        return self.duration

    def update_workout(self, title: str, duration: int) -> None:
        """Обновляет название и длительность тренировки."""
        self._validate_workout_data(title, duration)
        self.title = title
        self.duration = duration

    def is_valid(self) -> bool:
        """Проверяет корректность данных тренировки."""
        return bool(self.title.strip()) and self.duration > 0

    def check_access(self, current_user_id: int) -> None:
        """Проверяет доступ пользователя к тренировке."""
        if self.user_id != current_user_id:
            raise PermissionError("Ошибка 403 — доступ запрещён")

    @staticmethod
    def _validate_workout_data(title: str, duration: int) -> None:
        """Проверяет входные данные тренировки."""
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Название тренировки не может быть пустым")

        if not isinstance(duration, int) or duration <= 0:
            raise ValueError(
                "Длительность тренировки должна быть положительным числом"
            )
