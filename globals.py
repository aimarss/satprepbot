from functions import *
from db import AdapterDB

# JSONs
buttons = open_json("data/buttons.json")
funcs = open_json("data/functions.json")
db = AdapterDB()


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

with open("data/sat.txt", "r", encoding="utf-8") as f:
    sattext = f.read()


def getabout():
    with open("data/about.txt", "r", encoding="utf-8") as k:
        abouttext = k.read()
        return abouttext
# -----
