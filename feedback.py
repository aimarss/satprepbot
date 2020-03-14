import telebot
import json
from telebot import types
from functions import open_json, createKeyboard, emptyKeyboard, is_int


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
    "greetings": "Hello! To leave review please write it in one message",
    "are_you_sure": "You want to leave this review?",
    "yes/no": "Choose Yes/Np",
    "thanks": "Thank you for review!",
    "condition": "Write review in one message"
}


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
    print(message.json)
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


bot.polling()
