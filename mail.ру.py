import telebot
from telebot import types
import os

API_TOKEN = os.getenv("API_TOKEN", "ТОКЕН_ОТ_BOTFATHER")
ADMIN_ID = 5863481865
MANAGER_PHONE = "+79536311565"
DATA_FILE = "zayavki.txt"

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📌 Наши услуги")
    btn2 = types.KeyboardButton("📸 Примеры работ")
    btn3 = types.KeyboardButton("💬 Консультация")
    btn4 = types.KeyboardButton("📝 Заказать замер")
    btn5 = types.KeyboardButton("📞 Позвонить менеджеру")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)

    bot.send_message(
        message.chat.id,
        "👋 Привет! Я бот компании **OknaSmash** 🪟\n\n"
        "Мы занимаемся:\n"
        "✅ ПВХ окна\n"
        "✅ Алюминиевые окна\n"
        "✅ Портальные системы\n"
        "✅ Ремонт окон\n\n"
        "Выбери нужный пункт 👇",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: True)
def menu(message):
    if message.text == "📌 Наши услуги":
        bot.send_message(message.chat.id,
            "Мы предлагаем:\n"
            "— Монтаж ПВХ и алюминиевых окон\n"
            "— Установка портальных систем\n"
            "— Ремонт и обслуживание окон\n"
            "— Бесплатный замер ✅"
        )

    elif message.text == "📸 Примеры работ":
        bot.send_message(message.chat.id, "Вот несколько примеров наших работ 👇")
        try:
            media = [
                types.InputMediaPhoto(open("work1.jpg", "rb"), caption="Окна на балконе"),
                types.InputMediaPhoto(open("work2.jpg", "rb"), caption="Окно с раскладкой"),
                types.InputMediaPhoto(open("work3.jpg", "rb"), caption="Панорамные окна"),
                types.InputMediaPhoto(open("work4.jpg", "rb"), caption="Окно с тёмным профилем")
            ]
            bot.send_media_group(message.chat.id, media)
        except Exception as e:
            bot.send_message(message.chat.id, f"⚠️ Ошибка: {e}\nПроверь, что файлы work1.jpg - work4.jpg лежат рядом с ботом.")

    elif message.text == "💬 Консультация":
        bot.send_message(message.chat.id, "Напиши свой вопрос, и наш менеджер ответит!")

    elif message.text == "📝 Заказать замер":
        bot.send_message(message.chat.id, "Введите ваше имя:")
        bot.register_next_step_handler(message, get_name)

    elif message.text == "📞 Позвонить менеджеру":
        bot.send_contact(
            message.chat.id,
            phone_number=MANAGER_PHONE,
            first_name="Менеджер",
            last_name="Компания OknaSmash"
        )
        bot.send_message(message.chat.id, "Нажмите на контакт выше, чтобы сразу позвонить 📲")

def get_name(message):
    user_name = message.text
    bot.send_message(message.chat.id, "Введите ваш телефон:")
    bot.register_next_step_handler(message, get_phone, user_name)

def get_phone(message, user_name):
    user_phone = message.text
    new_request = (
        f"Имя: {user_name}\n"
        f"Телефон: {user_phone}\n"
        f"От: @{message.from_user.username if message.from_user.username else 'без username'}\n"
        "------------------------\n"
    )
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(new_request)

    bot.send_message(ADMIN_ID, f"📩 Новая заявка!\n\n{new_request}")
    bot.send_message(message.chat.id, "Спасибо! ✅ Наш менеджер свяжется с вами в ближайшее время.")

@bot.message_handler(commands=['zayavki'])
def show_requests(message):
    if message.chat.id == ADMIN_ID:
        if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                bot.send_message(message.chat.id, "📋 Список заявок:\n\n" + f.read())
        else:
            bot.send_message(message.chat.id, "📂 Заявок пока нет.")
    else:
        bot.send_message(message.chat.id, "❌ У вас нет доступа к этой команде.")

@bot.message_handler(commands=['clear'])
def clear_requests(message):
    if message.chat.id == ADMIN_ID:
        open(DATA_FILE, "w", encoding="utf-8").close()
        bot.send_message(message.chat.id, "🗑 Все заявки удалены.")
    else:
        bot.send_message(message.chat.id, "❌ У вас нет доступа к этой команде.")

bot.polling(none_stop=True)


