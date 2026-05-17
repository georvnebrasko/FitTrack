import json
import os

from telegram import BotCommand, ReplyKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

BOT_TOKEN = "YOUR_BOT_TOKEN"
DATA_FILE = "workouts.json"

WAITING_TITLE, WAITING_DURATION, WAITING_DELETE = range(3)

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        ["Добавить тренировку", "Список тренировок"],
        ["Удалить тренировку", "Помощь"],
    ],
    resize_keyboard=True,
)


def load_data():
    """Загружает данные всех пользователей."""
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_data(data):
    """Сохраняет данные всех пользователей."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_user_id(update: Update) -> str:
    """Возвращает Telegram ID пользователя в виде строки."""
    return str(update.effective_user.id)


def get_user_workouts(update: Update):
    """Возвращает список тренировок конкретного пользователя."""
    data = load_data()
    user_id = get_user_id(update)

    if user_id not in data:
        data[user_id] = []
        save_data(data)

    return data[user_id]


def save_user_workouts(update: Update, workouts):
    """Сохраняет список тренировок конкретного пользователя."""
    data = load_data()
    user_id = get_user_id(update)

    data[user_id] = workouts
    save_data(data)


async def set_commands(application):
    """Устанавливает команды Telegram-бота."""
    commands = [
        BotCommand("start", "Запустить бота"),
        BotCommand("add", "Добавить тренировку"),
        BotCommand("list", "Показать список тренировок"),
        BotCommand("delete", "Удалить тренировку"),
        BotCommand("help", "Помощь"),
        BotCommand("cancel", "Отменить действие"),
    ]

    await application.bot.set_my_commands(commands)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает команду /start."""
    await update.message.reply_text(
        "Привет! Я FitTrack Bot 💪\n\n"
        "Я помогу сохранять и отслеживать тренировки.\n\n"
        "Доступные действия:\n"
        "• Добавить тренировку\n"
        "• Показать список тренировок\n"
        "• Удалить тренировку\n"
        "• Получить помощь\n\n"
        "Можешь использовать кнопки снизу или команды.",
        reply_markup=MAIN_KEYBOARD,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает справку по работе с ботом."""
    await update.message.reply_text(
        "Как пользоваться FitTrack Bot:\n\n"
        "Добавление тренировки:\n"
        "1. Нажми «Добавить тренировку» или введи /add\n"
        "2. Напиши название тренировки\n"
        "3. Напиши длительность тренировки\n\n"
        "Другие действия:\n"
        "• «Список тренировок» или /list — показать тренировки\n"
        "• «Удалить тренировку» или /delete — удалить тренировку\n"
        "• /cancel — отменить текущее действие",
        reply_markup=MAIN_KEYBOARD,
    )


async def add_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запускает сценарий добавления тренировки."""
    await update.message.reply_text("Введи название тренировки.")

    return WAITING_TITLE


async def get_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получает название тренировки."""
    title = update.message.text.strip()

    if not title:
        await update.message.reply_text("Введи название тренировки.")
        return WAITING_TITLE

    context.user_data["title"] = title

    await update.message.reply_text("Введи длительность тренировки.")

    return WAITING_DURATION


def parse_duration(text: str):
    """Преобразует текст длительности в число минут."""
    digits = ""

    for char in text:
        if char.isdigit():
            digits += char

    if not digits:
        return None

    return int(digits)


async def get_duration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получает длительность тренировки и сохраняет её."""
    duration = parse_duration(update.message.text)

    if duration is None or duration <= 0:
        await update.message.reply_text("Введи длительность тренировки числом.")
        return WAITING_DURATION

    title = context.user_data["title"]
    workouts = get_user_workouts(update)

    workout = {
        "id": len(workouts) + 1,
        "title": title,
        "duration": duration,
    }

    workouts.append(workout)
    save_user_workouts(update, workouts)

    await update.message.reply_text(
        "Тренировка сохранена в список ✅\n\n"
        f"Название: {title}\n"
        f"Длительность: {duration} мин.",
        reply_markup=MAIN_KEYBOARD,
    )

    context.user_data.clear()
    return ConversationHandler.END


async def list_workouts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает список тренировок пользователя."""
    workouts = get_user_workouts(update)

    if not workouts:
        await update.message.reply_text(
            "Твой список тренировок пока пуст.",
            reply_markup=MAIN_KEYBOARD,
        )
        return

    text = "Твои тренировки:\n\n"

    for workout in workouts:
        text += (
            f"{workout['id']}. {workout['title']} — "
            f"{workout['duration']} мин.\n"
        )

    await update.message.reply_text(text, reply_markup=MAIN_KEYBOARD)


async def delete_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запускает сценарий удаления тренировки."""
    workouts = get_user_workouts(update)

    if not workouts:
        await update.message.reply_text(
            "Удалять нечего, твой список тренировок пуст.",
            reply_markup=MAIN_KEYBOARD,
        )
        return ConversationHandler.END

    text = "Какую тренировку удалить? Введи номер:\n\n"

    for workout in workouts:
        text += (
            f"{workout['id']}. {workout['title']} — "
            f"{workout['duration']} мин.\n"
        )

    await update.message.reply_text(text)

    return WAITING_DELETE


async def delete_workout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удаляет тренировку пользователя по номеру."""
    text = update.message.text.strip()

    try:
        workout_id = int(text)
    except ValueError:
        await update.message.reply_text("Нужно ввести номер тренировки.")
        return WAITING_DELETE

    workouts = get_user_workouts(update)

    selected_workout = None
    updated_workouts = []

    for workout in workouts:
        if workout["id"] == workout_id:
            selected_workout = workout
        else:
            updated_workouts.append(workout)

    if selected_workout is None:
        await update.message.reply_text("Тренировка с таким номером не найдена.")
        return WAITING_DELETE

    for index, workout in enumerate(updated_workouts, start=1):
        workout["id"] = index

    save_user_workouts(update, updated_workouts)

    await update.message.reply_text(
        "Тренировка удалена ✅\n\n"
        f"{selected_workout['title']} — "
        f"{selected_workout['duration']} мин.",
        reply_markup=MAIN_KEYBOARD,
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отменяет текущее действие."""
    context.user_data.clear()

    await update.message.reply_text(
        "Действие отменено.",
        reply_markup=MAIN_KEYBOARD,
    )

    return ConversationHandler.END


async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает текстовые кнопки меню."""
    text = update.message.text

    if text == "Добавить тренировку":
        return await add_start(update, context)

    if text == "Список тренировок":
        await list_workouts(update, context)
        return ConversationHandler.END

    if text == "Удалить тренировку":
        return await delete_start(update, context)

    if text == "Помощь":
        await help_command(update, context)
        return ConversationHandler.END

    await update.message.reply_text(
        "Я не понял сообщение.\n\n"
        "Используй кнопки снизу или команду /help.",
        reply_markup=MAIN_KEYBOARD,
    )

    return ConversationHandler.END


async def post_init(application):
    """Действия после запуска приложения."""
    await set_commands(application)


def main():
    """Запускает Telegram-бота."""
    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    add_handler = ConversationHandler(
        entry_points=[
            CommandHandler("add", add_start),
            MessageHandler(filters.Regex("^Добавить тренировку$"), add_start),
        ],
        states={
            WAITING_TITLE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_title)
            ],
            WAITING_DURATION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_duration)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    delete_handler = ConversationHandler(
        entry_points=[
            CommandHandler("delete", delete_start),
            MessageHandler(filters.Regex("^Удалить тренировку$"), delete_start),
        ],
        states={
            WAITING_DELETE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, delete_workout)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("list", list_workouts))
    app.add_handler(CommandHandler("cancel", cancel))

    app.add_handler(add_handler)
    app.add_handler(delete_handler)

    app.add_handler(
        MessageHandler(filters.Regex("^Список тренировок$"), list_workouts)
    )

    app.add_handler(MessageHandler(filters.Regex("^Помощь$"), help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    app.run_polling()


if __name__ == "__main__":
    main()