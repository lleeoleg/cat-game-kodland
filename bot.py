"""
bot.py

@cat_game_kodland_bot - название бота в Telegram

"""
import telebot
import requests
from telebot import types

BOT_TOKEN = "8327776931:AAFfrOaaCy04khc5HgwAFvtvjIqoRRG0tek"
API_URL = "http://127.0.0.1:5000"

bot = telebot.TeleBot(BOT_TOKEN)


def main_menu():
    """_summary_

    Returns:
        _type_: _description_
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🎮 Присоединиться")
    btn2 = types.KeyboardButton("🏆 Лидерборд")
    markup.add(btn1, btn2)
    return markup


def control_menu():
    """_summary_

    Returns:
        _type_: _description_
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("⬆️")
    markup.row("⬅️", "➡️")
    markup.row("⬇️")
    markup.add("⬅️ В меню")
    return markup


@bot.message_handler(commands=["start"])
def start(message):
    """_summary_

    Args:
        message (_type_): _description_
    """
    bot.send_message(message.chat.id, "Привет! 🐱 Добро пожаловать в игру.", reply_markup=main_menu())


@bot.message_handler(func=lambda m: m.text == "🎮 Присоединиться")
def join_game(message):
    """_summary_

    Args:
        message (_type_): _description_
    """
    username = message.from_user.username or f"user{message.from_user.id}"
    try:
        response = requests.post(f"{API_URL}/join", json={"username": username})
        data = response.json()
        if response.status_code in (200, 201):
            bot.send_message(
                message.chat.id,
                f"Ты в игре! 🎉\nПозиция: {data['player']}",
                reply_markup=control_menu(),
            )
        else:
            bot.send_message(message.chat.id, f"Ошибка: {data.get('error')}")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Сервер недоступен: {e}")


@bot.message_handler(func=lambda m: m.text in ["⬆️", "⬇️", "⬅️", "➡️"])
def move(message):
    """_summary_

    Args:
        message (_type_): _description_
    """
    username = message.from_user.username or f"user{message.from_user.id}"
    directions = {
        "⬆️": "up",
        "⬇️": "down",
        "⬅️": "left",
        "➡️": "right",
    }
    action = directions.get(message.text)

    try:
        response = requests.post(f"{API_URL}/action", json={"username": username, "action": action})
        data = response.json()
        if response.status_code == 200:
            bot.send_message(
                message.chat.id,
                f"➡️ Движение: {action}\n💰 Монет: {data['player']['coins']}",
            )
        else:
            bot.send_message(message.chat.id, f"Ошибка: {data.get('error')}")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Сервер недоступен: {e}")


@bot.message_handler(func=lambda m: m.text == "⬅️ В меню")
def back_to_menu(message):
    """_summary_

    Args:
        message (_type_): _description_
    """
    bot.send_message(message.chat.id, "Главное меню:", reply_markup=main_menu())


@bot.message_handler(func=lambda m: m.text == "🏆 Лидерборд")
def show_leaderboard(message):
    """_summary_

    Args:
        message (_type_): _description_
    """
    try:
        response = requests.get(f"{API_URL}/state")
        data = response.json()
        players = data.get("players", [])
        players.sort(key=lambda p: p["coins"], reverse=True)

        if not players:
            bot.send_message(message.chat.id, "Пока нет игроков 💤")
            return

        text = "🏆 *Топ игроков:*\n\n"
        for i, p in enumerate(players, 1):
            text += f"{i}. {p['username']} — {p['coins']} монет\n"

        bot.send_message(message.chat.id, text, parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {e}")


print("Бот запущен...")
bot.polling(none_stop=True)
