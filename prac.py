import telebot
from telebot import types
import json
import random

bot = telebot.TeleBot("881872217:AAHjDOnnKDXr5D5LnyphqkO7Roe4QboXhTA")

chat = []

def open_json(s):
    with open(s) as f:
        return json.load(f)

words = open_json("words.json")

meanings = list(map(lambda x: x["meaning"], words))
bookslist = open_json("books.json")

# Нужно переделать
booktextlist = {}
for i, book in enumerate(bookslist):
    booktextlist[book["text"]] = {}
    booktextlist[book["text"]] = i
# ----------------

officialslist = open_json("officals.json")
officialstextlist = {}

# Как и это
for i, official in enumerate(officialslist):
    officialstextlist[official["text"]] = {}
    officialstextlist[official["text"]] = i
# ---------

imageslist = []

buttons_list = open("buttons.json")


def menu(id):
    markup = types.InlineKeyboardMarkup()
    # Берем кнопки из json файла buttons.json
    btns = list(
        map(
            lambda x: types.InlineKeyboardButton(
                text=x["text"],
                callback_data=x["callback_text"]), 
            buttons_list
        )
    )

    # Добавляем их в markup
    list(map(lambda x: markup.add(x), btns))
    bot.send_message(id, "Меню", reply_markup=markup)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    id = message.json["chat"]["id"]
    chat.append(id)
    bot.send_message(id, "Привет! Это бот помогающий в подготовке к SAT")
    menu(id)


@bot.message_handler(commands=['menu'])
@bot.callback_query_handler(func=lambda call: call.data == "menu")
def menu_calling(call):
    menu(chat[0])


@bot.callback_query_handler(func=lambda message: message.data == "words")
@bot.message_handler(commands=["words"])
def new_word(message):
    bot.send_message(chat[0], "Выберите количетсво ")
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
    bot.send_message(chat[0], ques, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: (call.data.split(" ! "))[0] in meanings)
def checking(call):
    if words[meanings.index(call.data.split(" ! ")[0])]["word"] == call.data.split(" ! ")[1]:
        bot.send_message(chat[0], "correct")
    else:
        bot.send_message(chat[0], "incorrect")


@bot.callback_query_handler(func=lambda call: call.data == "books")
def books(call):
    markup = types.InlineKeyboardMarkup()
    for book in bookslist:
        btn_book = types.InlineKeyboardButton(text=book["text"], callback_data=book["text"])
        markup.add(btn_book)
    bot.send_message(chat[0], "Книги", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in booktextlist.keys())
def send_books(call):
    bot.send_document(chat[0], bookslist[booktextlist[call.data]]["id"])


@bot.callback_query_handler(func=lambda call: call.data == "officials")
def officials(call):
    markup = types.InlineKeyboardMarkup()
    for offical in officialslist:
        btn_book = types.InlineKeyboardButton(text=offical["text"], callback_data=offical["text"])
        markup.add(btn_book)
    bot.send_message(chat[0], "Прошедшие SAT", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in officialstextlist.keys())
def send_books(call):
    bot.send_document(chat[0], officialslist[officialstextlist[call.data]]["id"])


@bot.message_handler(content_types=['document'])
def add_book(message):
    file_id = message.document.file_id
    title = message.document.file_name
    bookslist.append({"text": title, "id": file_id})
    print(bookslist[-1])


bot.polling()
