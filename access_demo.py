from workout import Workout

workout = Workout("Кардио", 30, user_id=1)

current_user_id = 2

try:
    workout.check_access(current_user_id)
    print("Доступ разрешён")
except PermissionError:
    print("Ошибка 403 — доступ запрещён")