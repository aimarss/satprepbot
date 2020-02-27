import telebot
from telebot import types
import json
from multiprocessing import Process, Queue
import random
import emoji
from sender import start_sender
from functions import *

times = ["6:00", "9:00", "12:00", "15:00", "18:00", "21:00", "0:00", "Other"]

credentials = open_json("safety/credentials.json")
TOKEN = credentials["main"]["token"]
bot = telebot.TeleBot(TOKEN)

queue = Queue(maxsize=100)
max_questions = 100
cache = {}
states = {
    "words": "asking words",
    "everyday": "asking time"
}

words = open_json("words.json")

meanings = list(map(lambda x: x["meaning"], words))
words_list = list(map(lambda x: x["word"], words))

posts_list = open_json("posts.json")
poststextlist = {v: k for k, v in enumerate(posts_list)}


bookslist = open_json("books.json")

booktextlist = {}
for i, book in enumerate(bookslist):
    booktextlist[book["text"]] = i

officialslist = open_json("officals.json")
officialstextlist = {}

for i, official in enumerate(officialslist):
    officialstextlist[official["text"]] = i

funcs = open_json("buttons.json")

with open("sat.txt", "r", encoding="utf-8") as f:
    sattext = f.read()

with open("about.txt", "r", encoding="utf-8") as k:
    abouttext = k.read()


def user_in_cache(message):
    return message.json["chat"]["id"] in cache.keys()


def cached_state(message, state):
    if user_in_cache(message):
        return cache[message.json["chat"]["id"]]["state"] == state
    return False


def standard_number_questions():
    return createKeyboardWithMenu(4, ["10", "30", "50", "70"])


def menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btns = list(
        map(
            lambda x: types.KeyboardButton(
                text=emoji.emojize(x),),
            funcs.keys()
        )
    )
    list(map(lambda x: markup.add(x), btns))
    bot.send_message(chat_id, "Menu", reply_markup=markup)


def what(message):
    chat_id = message.json["chat"]["id"]
    bot.send_message(chat_id, text=sattext)


def about(message):
    chat_id = message.json["chat"]["id"]
    bot.send_message(chat_id, text=abouttext)


@bot.message_handler(func=lambda message: message.text == "Back to menu")
def back_to_menu(message):
    chat_id = message.json["chat"]["id"]
    if user_in_cache(message):
        cache.pop(chat_id)
    menu(chat_id)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.json["chat"]["id"]
    if user_in_cache(message):
        cache.pop(chat_id)
    bot.send_message(chat_id, "Hi! This is a bot that helps you in preparation for the SAT")
    menu(chat_id)


@bot.message_handler(content_types=['document'])
def add_book(message):
    file_id = message.document.file_id
    title = message.document.file_name
    bookslist.append({"text": title, "id": file_id})
    print(bookslist[-1])


@bot.callback_query_handler(func=lambda call: call.data == "menu")
def menu_calling(call):
    chat_id = call.message.json["chat"]["id"]
    menu(chat_id)


@bot.message_handler(func=lambda message: emoji.demojize(message.text, use_aliases=True) in funcs.keys())
def calling(message):
    print(message.text)
    message_type = funcs[emoji.demojize(message.text, use_aliases=True)]
    if message_type == "books":
        books(message)
    elif message_type == "officials":
        officials(message)
    elif message_type == "tests":
        print("tests")
    elif message_type == "words":
        words_(message)
    elif message_type == "new_words":
        new_word(message)
    elif message_type == "what":
        what(message)
    elif message_type == "about":
        about(message)
    elif message_type == "everyday":
        new_word(message)
    elif message_type == "posts":
        posts(message)


def get_answer_keyboard(question, n=4, width=2):
    answers = []
    right_answer = words[words_list.index(question)]["meaning"]
    for i in range(n - 1):
        new_a = {"word": ""}
        while new_a["word"] in ["", question]:
            new_a = random.choice(words)
        answers.append(new_a["meaning"])
    answers.append(right_answer)
    random_answers = []
    for i in range(len(answers)):
        random_answers.append(answers.pop(random.randint(0, len(answers) - 1)))
    return createKeyboardWithMenu(width, random_answers)


def get_questions(n):
    questions = []
    for i in range(n):
        new_q = {"word": ""}
        while new_q["word"] in [""] + questions:
            new_q = random.choice(words)
        questions.append(new_q["word"])
    return questions


def send_question(chat_id):
    current_question = cache[chat_id]['current_question']
    bot.send_message(
        chat_id,
        f"Word #{ current_question + 1 }: {cache[chat_id]['questions'][current_question]}",
        reply_markup=get_answer_keyboard(cache[chat_id]["questions"][current_question])
    )


@bot.message_handler(func=lambda message: message.text == "words")
def words_(message):
    chat_id = message.json["chat"]["id"]
    if chat_id in cache.keys():
        send_question(chat_id)
        return
    cache[chat_id] = {
        "state": states["words"],
        "current_question": -1,
        "total_question": 0,
        "right_answers": 0,
        "questions": []
    }
    bot.send_message(
        chat_id, 
        "Choose amount of questions",
        reply_markup=standard_number_questions()
    )


@bot.message_handler(func=lambda message: cached_state(message, states["words"]))
def next_word(message):
    chat_id = message.json["chat"]["id"]
    if len(cache[chat_id]["questions"]) == 0:
        if not is_int(message.text):
            bot.send_message(
                chat_id, 
                "Choose amount of questions",
                reply_markup=standard_number_questions()
            )
            return
        number_questions = int(message.text)
        if number_questions > max_questions:
            bot.send_message(
                chat_id, 
                "Choose amount of questions" + f" not bigger than{ max_questions }",
                reply_markup=standard_number_questions()
            )
            return
        cache[chat_id] = {
            "state": states["words"],
            "current_question": 0,
            "total_question": number_questions,
            "right_answers": 0,
            "questions": get_questions(number_questions),

        }
        send_question(chat_id)
        return
    
    answer = message.text

    right_answer = words[words_list.index(cache[chat_id]["questions"][cache[chat_id]["current_question"]])]["meaning"]
    if answer == right_answer:
        bot.send_message(chat_id, emoji.emojize("Correct :white_check_mark:", use_aliases=True))
        cache[chat_id]["right_answers"] += 1
    else:
        bot.send_message(chat_id, emoji.emojize("Incorrect :x: \n", use_aliases=True) +
                         "Right answer is " + right_answer)

    if cache[chat_id]["current_question"] == cache[chat_id]["total_question"] - 1:
        bot.send_message(
            chat_id,
            f"You have finished the test! You have { cache[chat_id]['right_answers'] }"
            f" out of { cache[chat_id]['total_question'] } questions",
            reply_markup=emptyKeyboard()
        )
        return
    cache[chat_id]["current_question"] += 1
    send_question(chat_id)


@bot.callback_query_handler(func=lambda call: call.data == "books")
def books(call):
    chat_id = call.json["chat"]["id"]
    markup = types.InlineKeyboardMarkup()
    for book in bookslist:
        btn_book = types.InlineKeyboardButton(text=book["text"], callback_data=book["text"])
        markup.add(btn_book)
    bot.send_message(chat_id, emoji.emojize("SAT Books :exclamation:", use_aliases=True), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in booktextlist.keys())
def send_books(call):
    chat_id = call.message.json["chat"]["id"]
    book = bookslist[booktextlist[call.data]]
    try:
        if book["image_id"]:
            bot.send_photo(chat_id, book["image_id"])
    except:
        pass
    bot.send_document(chat_id, book["id"])


@bot.callback_query_handler(func=lambda call: call.data == "officials")
def officials(call):
    chat_id = call.json["chat"]["id"]
    markup = types.InlineKeyboardMarkup()
    for offical in officialslist:
        btn_book = types.InlineKeyboardButton(text=offical["text"], callback_data=offical["text"])
        markup.add(btn_book)
    bot.send_message(chat_id, "Past SAT tests", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in officialstextlist.keys())
def send_books(call):
    chat_id = call.message.json["chat"]["id"]
    bot.send_document(chat_id, officialslist[officialstextlist[call.data]]["id"])


@bot.message_handler(commands=["everyday"])
def new_word(message):
    chat_id = message.json["chat"]["id"]
    bot.send_message(chat_id, "Choose Hour", reply_markup=createKeyboardWithMenu(row_width=4,args=times, onetime=True))


@bot.message_handler(func= lambda message: message.text in times)
def set_time(message):
    chat_id = message.json["chat"]["id"]
    text = message.text
    if text == "Other":
        other(message)
    else:
        time = text.split(":")
        sec = int(time[0]) * 3600 + int(time[1]) * 60
        smth = {
            "sender_id": chat_id,
            "time": sec,
            "hours": text
        }
        try:
            queue.put_nowait(smth)
        except Exception as e:
            print(e)


def other(message):
    chat_id = message.json["chat"]["id"]
    cache[chat_id] = {
        "state": states["everyday"]
    }
    bot.send_message(chat_id, "Enter time in 24 hour format (e.g. 13:15)")


@bot.message_handler(func=lambda message: cached_state(message, states["everyday"]))
def opt_time(message):
    chat_id = message.json["chat"]["id"]
    text = message.text
    time = text.split(":")
    sec = int(time[0]) * 3600 + int(time[1]) * 60
    smth = {
        "sender_id": chat_id,
        "time": sec,
        "hours": text
    }
    try:
        queue.put_nowait(smth)
    except Exception as e:
        print(e)
    cache.pop(chat_id)


#gAy and push
@bot.message_handler(func=lambda message: message.text == "posts")
def posts(message):
    chat_id = message.json["chat"]["id"]
    markup = types.InlineKeyboardMarkup()
    for post in posts_list:
        btn_book = types.InlineKeyboardButton(text=post["text"], callback_data=post["text"])
        markup.add(btn_book)
    bot.send_message(chat_id, "Posts and advices", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in poststextlist.keys())
def send_books(call):
    chat_id = call.message.json["chat"]["id"]
    bot.send_document(chat_id, posts_list[poststextlist[call.data]]["text"])


if __name__ == "__main__":
    p = Process(target=start_sender, args=(queue,))
    p.start()

    bot.polling()
    p.join()
