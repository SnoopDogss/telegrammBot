import telebot
from telebot import types

API_TOKEN = "7991271351:AAG8md8t4hkYaco2GwpRkZNDunTSpZgr5lU"
bot = telebot.TeleBot(API_TOKEN)

# Твой ID
ADMIN_ID = 5863481865


def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("🪟 Установить окна", "🔧 Ремонт окон")
    keyboard.add("🚪 Портальные системы", "📞 Заказать консультацию")
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! 👋 Я помогу выбрать услугу:\n\n"
        "🪟 Установка окон\n"
        "🔧 Ремонт\n"
        "🚪 Портальные системы\n"
        "📞 Консультация\n\n"
        "Выберите из меню ниже 👇",
        reply_markup=main_menu()
    )


@bot.message_handler(func=lambda m: True)
def menu(message):
    if message.text == "🪟 Установить окна":
        bot.send_message(message.chat.id, "Вы выбрали УСТАНОВКУ окон. Хотите оставить заявку? Напишите 'Заявка'.")
    elif message.text == "🔧 Ремонт окон":
        bot.send_message(message.chat.id, "Вы выбрали РЕМОНТ окон. Напишите 'Заявка', чтобы оставить данные.")
    elif message.text == "🚪 Портальные системы":
        bot.send_message(message.chat.id, "Вы выбрали ПОРТАЛЬНЫЕ системы. Напишите 'Заявка', чтобы оставить данные.")
    elif message.text == "📞 Заказать консультацию":
        bot.send_message(message.chat.id, "Оставьте свои контакты, и мы свяжемся с вами.\nНапишите 'Заявка'.")
    elif message.text.lower() == "заявка":
        bot.send_message(message.chat.id, "Введите ваше *имя*:", parse_mode="Markdown")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.chat.id, "Выберите действие из меню 👇", reply_markup=main_menu())


def get_name(message):
    name = message.text
    bot.send_message(message.chat.id, "Введите ваш *номер телефона* 📱:", parse_mode="Markdown")
    bot.register_next_step_handler(message, get_phone, name)

def get_phone(message, name):
    phone = message.text
    bot.send_message(message.chat.id, "Введите ваш *адрес/город* 🏠:", parse_mode="Markdown")
    bot.register_next_step_handler(message, send_request, name, phone)

def send_request(message, name, phone):
    address = message.text

    bot.send_message(
        ADMIN_ID,
        f"📩 Новая заявка!\n\n"
        f"👤 Имя: {name}\n"
        f"📱 Телефон: {phone}\n"
        f"🏠 Адрес: {address}\n"
        f"От @{message.from_user.username if message.from_user.username else 'без username'}"
    )

    bot.send_message(message.chat.id, "✅ Спасибо! Ваша заявка отправлена, скоро свяжемся с вами.")


bot.polling(none_stop=True)



