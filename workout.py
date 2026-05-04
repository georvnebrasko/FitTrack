class Workout:
    """Класс для хранения информации о тренировке."""

    def __init__(self, title: str, duration: int):
        self.title = title
        self.duration = duration

    def get_title(self) -> str:
        """Возвращает название тренировки."""
        return self.title

    def get_duration(self) -> int:
        """Возвращает длительность тренировки в минутах."""
        return self.duration

    def update_workout(self, title: str, duration: int) -> None:
        """Обновляет название и длительность тренировки."""
        self.title = title
        self.duration = duration

    def is_valid(self) -> bool:
        """Проверяет корректность данных тренировки."""
        return bool(self.title) and self.duration > 0
