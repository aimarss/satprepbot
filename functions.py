import json
from telebot import types
import time

def open_json(s):
    with open(s) as f:
        return json.load(f)


def is_int(s):
    try:
        int(s)
        return True
    except:
        return False


def createKeyboard(row_width: int, args):
    if not is_int(row_width):
        raise TypeError
    markup = types.ReplyKeyboardMarkup(row_width=row_width)
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
