import telebot
from telebot import types

TOKEN = "1064402448:AAGtL_ll-qtDRf2onRHr931KeZg1qolzFXQ"
bot = telebot.TeleBot(TOKEN)

cache = {}


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
        "temp_mark": None,
        "mark": None
    }

    bot.send_message(
        user_id, 
        "Добрый день! Поставтье оценку нашему боту от 1 до 10",
        reply_markup=createKeyboard(
            5, 
            "1", "2", "3", "4", "5",
            "6", "7", "8", "9", "10",
            "Выбрать позже"
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
                5, 
                "1", "2", "3", "4", "5",
                "6", "7", "8", "9", "10",
                "Выбрать позже"
            )
        )
        return
    if cache[user_id]["current_state"] == "asking mark":
        if message.text == "Выбрать позже":
            cache[user_id]["current_state"] = "nothing"
        if cache[user_id]["temp_mark"] is None:
            if not is_int(message.text):
                bot.send_message(
                    user_id, 
                    f"{ message.text } не является числом. Выберите любое число от 1 до 10",
                    reply_markup=createKeyboard(
                        5, 
                        "1", "2", "3", "4", "5",
                        "6", "7", "8", "9", "10",
                        "Выбрать позже"
                    )
                )
                return
            user_mark = int(message.text)
            if 1 <= user_mark <= 10:
                cache[user_id]["temp_mark"] = user_mark
                bot.send_message(
                    user_id, 
                    f"Вы уверены что хотите поставить оценку { user_mark }?",
                    reply_markup=createKeyboard(2, "Да", "Нет")
                )
                return
            else:
                bot.send_message(
                    user_id, 
                    f"{ message.text } не может быть оценкой. Выберите другое число",
                    reply_markup=createKeyboard(
                        5, 
                        "1", "2", "3", "4", "5",
                        "6", "7", "8", "9", "10",
                        "Выбрать позже"
                    )
                )
                return
        else:
            if message.text == "Да":
                cache[user_id]["mark"] = cache[user_id]["temp_mark"]
                cache[user_id]["temp_mark"] = None
                cache[user_id]["current_state"] = "nothing"
                bot.send_message(user_id, f" { cache[user_id]['mark'] } Успешно сохранено", reply_markup=emptyKeyboard())
                return
            elif message.text == "Нет":
                cache[user_id]["temp_mark"] = None
                cache[user_id]["current_state"] = "nothing"
                bot.send_message(
                    user_id, 
                    "Выберите любое число от 1 до 10",
                    reply_markup=createKeyboard(
                        5, 
                        "1", "2", "3", "4", "5",
                        "6", "7", "8", "9", "10",
                        "Выбрать позже"
                    )
                )
                return


bot.polling()
