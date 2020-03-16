from sched import scheduler
import time
import telebot
import emoji
from functions import *
from commands import Commands
from db import AdapterDB
from multiprocessing import Process, Queue
from sender import start_sender

# constants
minute = 60
times = ["6:00", "9:00", "12:00", "15:00", "18:00", "21:00", "0:00", "Other"]
# ---------

# credentials and bot init
credentials = open_json("safety/credentials.json")
TOKEN = credentials["main"]["token"]
bot = telebot.TeleBot(TOKEN)
# ------------------------

queue = Queue(maxsize=100)
db = AdapterDB()
com = Commands(bot, queue, db)

# cleaning cache
cache_threshold = 30 * minute


def clean_cache():
    for chat_id in com.cache:

        if time.time() - com.cache[chat_id]["last_update"] >= cache_threshold:
            com.cache.pop(chat_id)


cache_cleaner_delay = minute
sch = scheduler(time.time, time.sleep)
sch.enter(cache_cleaner_delay, 1, clean_cache)
# --------------

# JSONs
buttons = open_json("data/buttons.json")
funcs = open_json("data/functions.json")


def posts():
    posts_list = open_json("data/posts.json")
    return posts_list


def poststext():
    poststextlist = {v: k for k, v in enumerate(posts())}
    return poststextlist


bookslist = open_json("data/books.json")
booktextlist = {v: k for k, v in enumerate(map(lambda x: x["text"], bookslist))}

officialslist = open_json("data/officals.json")
officialstextlist = {v: k for k, v in enumerate(map(lambda x: x["text"], officialslist))}

words = open_json("data/words.json")

meanings = list(map(lambda x: x["meaning"], words))
words_list = list(map(lambda x: x["word"], words))

states = open_json("data/states.json")
reverse_states = {v: k for k, v in states.items()}

with open("safety/password") as f:
    adminpassword = f.read()


def get_all_users():
    db.get_all_users()

# -----


@bot.message_handler(func=lambda x: True)
def main(message):
    chat_id = message.chat.id
    text = emoji.demojize(message.text, use_aliases=True)
    try:
        state = com.cache[chat_id]["state"]
        print(state)
    except KeyError:
        state = states["nothing"]
    try:
        com.cache[chat_id]["time_seen"] = message.date
    except KeyError:
        pass
    try:
        message_type = buttons[text]
    except:
        message_type = None
    # В случае если он только присоединился
    if chat_id not in com.cache:
        com.cache[chat_id] = {
            "state": states["nothing"],
            "last_update": time.time(),
            "admin": False
        }
    # Если в первый раз видим его
    if db.get_user_id(chat_id) is None:
        db.add_new_user(chat_id)
        com.exe("start", chat_id)
        return
    # Сохраняем последний дествие для cache_cleaner-а
    com.cache[chat_id]["last_update"] = time.time()

    # Возвращение в меню с любой точки
    if text == "Back to menu":
        if chat_id in com.cache:
            com.cache[chat_id] = pop_keys_from_dict(com.cache[chat_id], list(com.cache[chat_id].keys()))
        com.exe("menu", chat_id)

    # Команды 
    if message.text.strip("/") in com.get_commands():
        command = message.text.strip("/")
        # Запускаем команду command
        com.exe(command, chat_id)
        return

    # Функции выбранные из меню
    if message_type is not None and state == states["nothing"]:
        com.exe(message_type, chat_id)
        return

    # Если state равен words
    if state == states["words"]:
        com.exe("next_word", message)
        return
    # ------------------------

    if state not in reverse_states:
        return
    # Использование funcs
    reverse_state = reverse_states[state]
    command = None
    if reverse_state in funcs["time"]:
        command = funcs["time"][reverse_state]
    elif reverse_state in funcs["admin"]:
        command = funcs["admin"][reverse_state]
    com.exe(command, message)


@bot.callback_query_handler(func=lambda x: True)
def callback(call):
    chat_id = call.message.json["chat"]["id"]
    data = call.data

    # Книги
    if data in booktextlist:
        book = bookslist[booktextlist[data]]
        try:
            if book["image_id"]:
                bot.send_photo(chat_id, book["image_id"])
        except:
            pass
        bot.send_document(chat_id, book["id"])

    # Practices
    if data in officialstextlist:
        bot.send_document(chat_id, officialslist[officialstextlist[data]]["id"])

    # Adding words to dictionary
    if "dictionary_append:" in data:
        word = " ".join(call.data.split(" ")[1:])
        db.add_word_to_dictionary(chat_id, word)
        bot.answer_callback_query(call.id, word + " successfully added", show_alert=True)


if __name__ == "__main__":
    p = Process(target=start_sender, args=(queue,))
    p.start()
    bot.polling()
    p.join()
