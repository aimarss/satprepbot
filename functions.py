import json
from telebot import types
import time


def open_json(s) -> dict:
    with open(s) as f:
        return json.load(f)


def is_int(s):
    try:
        int(s)
        return True
    except:
        return False


def createKeyboardWithMenu(row_width: int, args, onetime=False):
    return createKeyboard(row_width, args + ["Back to menu"], onetime)


def createKeyboard(row_width: int, args, onetime=False):
    if not is_int(row_width):
        raise TypeError
    markup = types.ReplyKeyboardMarkup(row_width=row_width, one_time_keyboard=onetime)
    btns = []
    for i in args:
        btn_i = types.KeyboardButton(i)
        btns.append(btn_i)
    markup.add(*btns)
    return markup


def emptyKeyboard():
    return types.ReplyKeyboardRemove(selective=False)


def time_check(text):
    text = text.split(":")
    if int(text[0]) in range(24) and int(text[1]) in range(60):
        return True
    else:
        return False


def get_time(t=None):
    t = time.time() if t is None else t
    struct_time = time.gmtime(t + 6 * 60 * 60)
    return time.strftime("%d-%m-%Y: %Hh %Mm %Ss", struct_time)


def pop_keys_from_dict(d: dict, keys):
    if isinstance(keys, tuple) or isinstance(keys, list):
        for k in keys:
            if k != "dictionary" and k != "state":
                d.pop(k)
    else:
        d.pop(keys)
    return d


def addnewpost(title, text):
    old = open_json("data/posts.json")
    new = {title: text}
    old.update(new)
    with open("data/posts.json", "w") as f:
        json.dump(old, f, ensure_ascii=False)

