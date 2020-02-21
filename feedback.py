import telebot
from telebot import types

TOKEN = ""
bot = telebot.TeleBot(TOKEN)

cache = {}

keyboards = {
    "marks": [
        "1", "2", "3", "4", "5",
        "6", "7", "8", "9", "10",
        "Выбрать позже"
    ],
    "yes/no": [
        "Да", "Нет"
    ],
    "menu": [
        "Поставить оценку",
        "Оставить отзыв"
    ]
}

reviews = []

commands = [
    "Меню",
    "Поставить оценку",
    "Оставить отзыв"
]


def is_int(s):
    try:
        int(s)
        return True
    except:
        return False


def createKeyboard(row_width: int, *args):
    if not is_int(row_width):
        raise TypeError
    markup = types.ReplyKeyboardMarkup(row_width=row_width)
    btns = []
    for i in args:
        btn_i = types.KeyboardButton(i)
        btns.append(btn_i)
    list(map(lambda x: markup.add(x), btns))
    return markup

def emptyKeyboard():
    return types.ReplyKeyboardRemove(selective=False)


@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.json["chat"]["id"]

    cache[user_id] = {
        "current_state": "asking mark",
        "temp_data": None,
        "mark": None
    }

    bot.send_message(
        user_id, 
        "Добрый день! Поставтье оценку нашему боту от 1 до 10",
        reply_markup=createKeyboard(
            row_width=5, 
            args=keyboards["marks"]
        )
    )


@bot.message_handler(func=lambda x: True)
def all_messages(message):
    user_id = message.json["chat"]["id"]
    if user_id not in cache.keys():
        bot.send_message(
            user_id, 
            "Добрый день! Поставтье оценку нашему боту от 0 до 10",
            reply_markup=createKeyboard(
                row_width=5, 
                args=keyboards["marks"]
            )
        )
        return
    if cache[user_id]["current_state"] == "asking mark":
        if message.text == "Выбрать позже":
            cache[user_id]["current_state"] = "nothing"
        if cache[user_id]["temp_data"] is None:
            if not is_int(message.text):
                bot.send_message(
                    user_id, 
                    f"{ message.text } не является числом. Выберите любое число от 1 до 10",
                    reply_markup=createKeyboard(
                        row_width=5, 
                        args=keyboards["marks"]
                    )
                )
                return
            user_mark = int(message.text)
            if 1 <= user_mark <= 10:
                cache[user_id]["temp_data"] = user_mark
                bot.send_message(
                    user_id, 
                    f"Вы уверены что хотите поставить оценку { user_mark }?",
                    reply_markup=createKeyboard(2, keyboards["yes/no"])
                )
                return
            else:
                bot.send_message(
                    user_id, 
                    f"{ message.text } не может быть оценкой. Выберите другое число",
                    reply_markup=createKeyboard(
                        row_width=5, 
                        args=keyboards["marks"]
                    )
                )
                return
        else:
            if message.text not in keyboards["yes/no"]:
                bot.send_message(user_id, "Выберите Да/Нет", reply_markup=createKeyboard(2, keyboards["yes/no"]))
                return
            i = keyboards["yes/no"].index(message.text)
            if i == 0:
                cache[user_id]["mark"] = cache[user_id]["temp_data"]
                cache[user_id]["temp_data"] = None
                cache[user_id]["current_state"] = "nothing"
                bot.send_message(user_id, "Спасибо за оставленную оценку, не забудьте оставить отзыв!", reply_markup=createKeyboard(1, "Меню"))
                return
            elif i == 1:
                cache[user_id]["temp_data"] = None
                cache[user_id]["current_state"] = "nothing"
                bot.send_message(
                    user_id, 
                    "Выберите любое число от 1 до 10",
                    reply_markup=createKeyboard(
                        row_width=5, 
                        args=keyboards["marks"]
                    )
                )
                return
    elif cache[user_id]["current_state"] == "nothing":
        if message.text in commands:
            i = commands.index(message.text)
            if i == 0: # Меню
                bot.send_message(
                    user_id,
                    "Меню",
                    reply_markup=createKeyboard(
                        row_width=2,
                        args=keyboards["menu"]
                    )
                )
            elif i == 1: # Поставить оценку
                cache[user_id]["current_state"] = "asking mark"
                bot.send_message(
                    user_id, 
                    "Поставтье оценку нашему боту от 1 до 10",
                    reply_markup=createKeyboard(
                        row_width=5, 
                        args=keyboards["marks"]
                    )
                )
            elif i == 2: # Оставить отзыв
                cache[user_id]["current_state"] = "asking review"
                bot.send_message(
                    user_id,
                    "Напишите отзыв в одном сообщении",
                    reply_markup=emptyKeyboard()
                )
    elif cache[user_id]["current_state"] == "asking review":
        review = message.text
        if cache[user_id]["temp_data"] is None:
            cache[user_id]["temp_data"] = review
            bot.send_message(
                user_id,
                "Вы точно хотите оставить этот отзыв?",
                reply_markup=createKeyboard(
                    2,
                    keyboards["yes/no"]
                )
            )
        else:
            if message.text not in keyboards["yes/no"]:
                bot.send_message(user_id, "Выберите Да/Нет", reply_markup=createKeyboard(2, keyboards["yes/no"]))
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

                bot.send_message(user_id, "Спасибо за оставленный отзыв!", reply_markup=createKeyboard(1, "Меню"))
                return
            elif i == 1:
                cache[user_id]["temp_data"] = None
                cache[user_id]["current_state"] = "nothing"
                bot.send_message(
                    user_id, 
                    "Напишите отзыв в одном сообщении",
                    reply_markup=emptyKeyboard()
                )
                return


bot.polling()
