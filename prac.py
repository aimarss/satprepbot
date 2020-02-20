import telebot
from telebot import types
import json
from multiprocessing import Process, Queue
import random
import emoji
from sender import start_sender, get_current_seconds

TOKEN = "881872217:AAHjDOnnKDXr5D5LnyphqkO7Roe4QboXhTA"
bot = telebot.TeleBot(TOKEN)

queue = Queue(maxsize=100)


def open_json(s):
    with open(s) as f:
        return json.load(f)


words = open_json("words.json")

meanings = list(map(lambda x: x["meaning"], words))
bookslist = open_json("books.json")

# Нужно переделать
booktextlist = {}
for i, book in enumerate(bookslist):
    booktextlist[book["text"]] = i
# ----------------

officialslist = open_json("officals.json")
officialstextlist = {}

# Как и это
for i, official in enumerate(officialslist):
    officialstextlist[official["text"]] = i
# ---------

funcs = open_json("buttons.json")


def menu(chat_id):
    markup = types.ReplyKeyboardMarkup()
    btns = list(
        map(
            lambda x: types.KeyboardButton(
                text=emoji.emojize(x),),
            funcs.keys()
        )
    )
    list(map(lambda x: markup.add(x), btns))
    bot.send_message(chat_id, "Меню", reply_markup=markup)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.json["chat"]["id"]
    bot.send_message(chat_id, "Привет! Это бот помогающий в подготовке к SAT")
    menu(chat_id)


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
        new_word(message)
    elif message_type == "what":
        print("what")
    elif message_type == "about":
        print('about')


@bot.message_handler(func=lambda message: message.text == "words")
def new_word(message):
    chat_id = message.json["chat"]["id"]
    bot.send_message(chat_id, "Выберите количетсво ")
    numbers = list(range(500))
    answers = []
    markup = types.InlineKeyboardMarkup()

    ques_n = random.choice(numbers)

    ques = words[ques_n]["word"]
    ans = words[ques_n]["meaning"]

    answers.append(ans)
    numbers.remove(ques_n)

    for i in range(3):
        wr_n = random.choice(numbers)
        wr = words[wr_n]["meaning"]
        answers.append(wr)

        numbers.remove(wr_n)

    opt = list(range(len(answers)))
    for j in range(len(answers)):
        num = random.choice(opt)
        btn = types.InlineKeyboardButton(text=answers[num], callback_data=answers[num] + " ! " + ques)
        markup.add(btn)
        opt.remove(num)
    bot.send_message(chat_id, ques, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: (call.data.split(" ! "))[0] in meanings)
def checking(call):
    chat_id = call.message.json["chat"]["id"]
    if words[meanings.index(call.data.split(" ! ")[0])]["word"] == call.data.split(" ! ")[1]:
        bot.send_message(chat_id, "correct")
    else:
        bot.send_message(chat_id, "incorrect")


@bot.callback_query_handler(func=lambda call: call.data == "books")
def books(call):
    chat_id = call.json["chat"]["id"]
    markup = types.InlineKeyboardMarkup()
    for book in bookslist:
        btn_book = types.InlineKeyboardButton(text=book["text"], callback_data=book["text"])
        markup.add(btn_book)
    bot.send_message(chat_id, emoji.emojize("Книги для подготовки к SAT :exclamation:", use_aliases=True), reply_markup=markup)


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
    bot.send_message(chat_id, "Прошедшие SAT", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in officialstextlist.keys())
def send_books(call):
    chat_id = call.message.json["chat"]["id"]
    bot.send_document(chat_id, officialslist[officialstextlist[call.data]]["id"])


@bot.message_handler(content_types=['document'])
def add_book(message):
    file_id = message.document.file_id
    title = message.document.file_name
    bookslist.append({"text": title, "id": file_id})
    print(bookslist[-1])


@bot.message_handler(commands=["everyday"])
def everyday(message):
    chat_id = message.json["chat"]["id"]
    sec = get_current_seconds() + 10
    smth = {
        "sender_id": chat_id,
        "time": sec
    }
    try:
        queue.put_nowait(smth)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    p = Process(target=start_sender, args=(queue,))
    p.start()

    bot.polling()
    p.join()
