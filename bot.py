import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters, CommandHandler

TOKEN = "8873438835:AAFEy-mzaajNlMeF0zCqrsZ6Uc-dyvo_9J0"

LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"

keyboard = [
    ["📘 Правила футбола", "🧠 Тактики"],
    ["⚽ Игроки", "🏟 Команды"]
]

markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я твой футбольный AI-ассистент.\n"
        "Выбери тему или задай вопрос ⚽",
        reply_markup=markup
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # кнопки
    if user_text == "📘 Правила футбола":
        user_text = "Объясни правила футбола простыми словами"

    elif user_text == "🧠 Тактики":
        user_text = "Объясни футбольные схемы 4-3-3, 4-4-2, 3-5-2"

    elif user_text == "⚽ Игроки":
        user_text = "Какие роли есть у игроков в футболе"

    elif user_text == "🏟 Команды":
        user_text = "Назови топ футбольных клубов мира"

    payload = {
        "model": "local-model",  # LM Studio сам подставит загруженную модель
        "messages": [
            {
                "role": "system",
                "content": (
                    "Ты футбольный AI-аналитик.\n"
                    "Отвечай кратко и по делу.\n"
                    "Не выдумывай факты.\n"
                    "Если не знаешь — скажи 'нет данных'."
                )
            },
            {
                "role": "user",
                "content": user_text
            }
        ],
        "temperature": 0.6,
        "max_tokens": 800,
        "stream": False
    }

    try:
        response = requests.post(LM_STUDIO_URL, json=payload, timeout=300)
        result = response.json()

        answer = result["choices"][0]["message"]["content"]

        await update.message.reply_text(answer, reply_markup=markup)

    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}", reply_markup=markup)


# запуск
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Бот запущен")
app.run_polling()
