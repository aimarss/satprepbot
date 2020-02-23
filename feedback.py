import telebot
import json
from telebot import types

def open_json(s):
    with open(s) as f:
        return json.load(f)


credentials = open_json("safety/credentials.json")
TOKEN = credentials["feedback"]["token"]
bot = telebot.TeleBot(TOKEN)

cache = {}

keyboards = {
    "yes/no": [
        "Yes", "No"
    ]
}

reviews = []

commands = [
    "Leave a comment"
]

text = {
    "greetings": "Добрый день! Чтобы оставить отзыв, напишите его в одном сообщении",
    "are_you_sure": "Вы точно хотите оставить этот отзыв?",
    "yes/no": "Выберите Да/Нет",
    "thanks": "Спасибо за оставленный отзыв!",
    "condition": "Напишите отзыв в одном сообщении"
}


def is_int(s):
    try:
        int(s)
        return True
    except:
        return False


def createKeyboard(row_width: int, args):
    if not is_int(row_width):
        raise TypeError
    markup = types.ReplyKeyboardMarkup(row_width=row_width)
    btns = []
    for i in args:
        btn_i = types.KeyboardButton(i)
        btns.append(btn_i)
    markup.add(*btns)
    return markup


def emptyKeyboard():
    return types.ReplyKeyboardRemove(selective=False)


@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.json["chat"]["id"]

    cache[user_id] = {
        "current_state": "asking review",
        "temp_data": None,
        "mark": None
    }

    bot.send_message(
        user_id, 
        text["greetings"],
        reply_markup=emptyKeyboard()
    )


@bot.message_handler(func=lambda x: True)
def all_messages(message):
    user_id = message.json["chat"]["id"]
    if user_id not in cache.keys():
        bot.send_message(
            user_id, 
            text["greetings"],
            reply_markup=emptyKeyboard()
        )
        return
    if cache[user_id]["current_state"] == "asking review":
        review = message.text
        if cache[user_id]["temp_data"] is None:
            cache[user_id]["temp_data"] = review
            bot.send_message(
                user_id,
                text["are_you_sure"],
                reply_markup=createKeyboard(
                    2,
                    keyboards["yes/no"]
                )
            )
        else:
            if message.text not in keyboards["yes/no"]:
                bot.send_message(user_id, text["yes/no"], reply_markup=createKeyboard(2, keyboards["yes/no"]))
                return
            i = keyboards["yes/no"].index(message.text)
            if i == 0:
                review = cache[user_id]["temp_data"]
                cache[user_id]["temp_data"] = None
                cache[user_id]["current_state"] = "nothing"

                reviews.append({
                    "user_id": user_id,
                    "review": review
                })

                cache.pop(user_id)

                bot.send_message(user_id, text["thanks"], reply_markup=emptyKeyboard())
                return
            elif i == 1:
                cache[user_id]["temp_data"] = None
                cache[user_id]["current_state"] = "asking review"
                bot.send_message(
                    user_id, 
                    text["condition"],
                    reply_markup=emptyKeyboard()
                )
                return
