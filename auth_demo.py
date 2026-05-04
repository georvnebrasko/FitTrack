from auth import User

# регистрация
user = User("admin", "12345")

# попытка входа
login_password = "12345"

if user.check_password(login_password):
    print("Успешный вход")
else:
    print("Неверный пароль")
