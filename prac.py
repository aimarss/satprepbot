import telebot
from telebot import types
import json
import random

bot = telebot.TeleBot("881872217:AAHjDOnnKDXr5D5LnyphqkO7Roe4QboXhTA")

chat = []

with open("words.json") as f:
    words = json.load(f)

bookslist = [{'text': 'Kaplan Prep Book 4/5', 'id': 'BQACAgIAAxkBAAMhXklypBJyY-RvQGXBWa8SARLgIycAAnMFAAL9rFBKk7m2Y4uCJmsYBA'},
             {'text': 'Cracking the SAT 5/5', 'id': 'BQACAgIAAxkBAAM0Xkl2loQAAdwDhMAIDdyN5oE9ywehAALZBAACgTRISgnQSBWIN8vDGAQ'},
             {'text': 'SAT Black Book 2nd Edition', 'id': 'BQACAgIAAxkBAAONXkm-cxWP8ihZav-GlLb5DW48SX8AArEDAAINAVBKAAHcP-gSeMQcGAQ'},
             {'text': "Erica Meltzer's SAT Grammar Workbook", 'id': 'BQACAgIAAxkBAAOOXkm_pQ_uKcSTWf4Ie7HBe3-FOfsAAosGAAJNR1BKZBaOG_zIDYYYBA'},
             {'text': "Barron's New SAT", 'id': 'BQACAgIAAxkBAAOQXknADVX98nB4lC6ybVdTKdKXpMcAAkIFAAKBNFBKvAUG_Id1rYQYBA'},
             {'text': 'The College Panda SAT Essay', 'id': 'BQACAgIAAxkBAAORXknAgSoiXHVYUYVYzR2YhFDX48IAAkMFAAKBNFBKgjxooNVL114YBA'},
             {'text': 'SAT Vocabulary', 'id': 'BQACAgIAAxkBAAOSXknAwpgJ95nT19SYozPAeI9GJP0AAkQFAAKBNFBK_P2FOyrgdyEYBA'}]
booktextlist = {}
for i, book in enumerate(bookslist):
    booktextlist[book["text"]] = {}
    booktextlist[book["text"]] = i

officialslist = [{'text': 'SAT April 2018', 'id': 'BQACAgIAAxkBAAOYXknPNk9k-4qm8nD7TJsrCrWFygoAAo0GAAJNR1BKP5B05Rukg8wYBA'},
                 {'text': 'SAT QAS April 2018.pdf', 'id': 'BQACAgIAAxkBAAOhXknUmmQnBJAyXqFg4H-EI6kL3s4AAo4GAAJNR1BKugUpnGKzuRsYBA'},
             {'text': 'SAT + Answers May 2019', 'id': 'BQACAgIAAxkBAAOaXknPe7viXXXHYhOcvB4fzXC_VskAAkUFAAKBNFBKqM9wKsiZ0PUYBA'},
             {'text': 'SAT US October 2019', 'id': 'BQACAgIAAxkBAAObXknPooj8EnGiNd9mHpV-O-KQnfAAAkYFAAKBNFBK16Q1zhuuqHMYBA'}]
officialstextlist = {}
for i, official in enumerate(officialslist):
    officialstextlist[official["text"]] = {}
    officialstextlist[official["text"]] = i


imageslist = []


def menu(id):
    markup = types.InlineKeyboardMarkup()
    btn_books = types.InlineKeyboardButton(text='Книги', callback_data="books")
    btn_officials = types.InlineKeyboardButton(text="Предыдущие SAT тесты", callback_data="officials")
    btn_tests = types.InlineKeyboardButton(text="Practice tests", callback_data="tests")
    btn_about = types.InlineKeyboardButton(text="О боте", callback_data="about")
    btn_what = types.InlineKeyboardButton(text="Что такое SAT?", callback_data="what")
    markup.add(btn_books)
    markup.add(btn_officials)
    markup.add(btn_tests)
    markup.add(btn_what)
    markup.add(btn_about)
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


@bot.message_handler(commands=["words"])
def new_word(message):
    numbers = range(500)
    for i in range(4):
        number = random.randint(0, 499)
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text=words[number]["meaning"])


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
