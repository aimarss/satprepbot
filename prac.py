import telebot
from telebot import types
import json

bot = telebot.TeleBot("881872217:AAHjDOnnKDXr5D5LnyphqkO7Roe4QboXhTA")

chat = []


@bot.message_handler(commands=['start'])
def send_welcome(message):
    id = message.json["chat"]["id"]
    chat.append(id)
    bot.send_message(id, "Привет! Это бот помогающий в подготовке к SAT")
    markup = types.InlineKeyboardMarkup()
    btn_books = types.InlineKeyboardButton(text='Книги', callback_data="books")
    btn_tests = types.InlineKeyboardButton(text="Тесты для подготоки", callback_data="tests")
    btn_about = types.InlineKeyboardButton(text="О боте", callback_data="about")
    markup.add(btn_books)
    markup.add(btn_tests)
    markup.add(btn_about)
    bot.send_message(id, "Меню", reply_markup=markup)


@bot.message_handler(func=lambda message: message.data == "books")
def books(message):
    bookslist = {"Kaplan": {"text": "Kaplan Prep Book 4/5", "id": "BQACAgIAAxkBAAMhXklypBJyY-RvQGXBWa8SARLgIycAAnMFAAL9rFBKk7m2Y4uCJmsYBA"},
             "Cracking": {"text": "Cracking the SAT 5/5", "id": "BQACAgIAAxkBAAM0Xkl2loQAAdwDhMAIDdyN5oE9ywehAALZBAACgTRISgnQSBWIN8vDGAQ"}}
    bot.send_document(chat[0], "BQACAgIAAxkBAAMhXklypBJyY-RvQGXBWa8SARLgIycAAnMFAAL9rFBKk7m2Y4uCJmsYBA")


bot.polling()
