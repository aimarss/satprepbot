import telebot
import time
import datetime as date
import json
import random
from multiprocessing import Process, Queue


senders = [
#   {
#   "sender": sender_id,
#       "time": time_to_send
#     }
] # must be sorted

sent = [
#   sender_id
]

def open_json(s):
    with open(s) as f:
        return json.load(f)


words = open_json("words.json")

number_senderP = 4


def get_time(t=None):
    t = time.time() if t is None else t
    struct_time = time.gmtime(t + 6 * 60 * 60)
    return time.strftime("%d-%m-%Y: %Hh %Mm %Ss", struct_time)


def get_current_seconds():
    now = date.datetime.now()
    today = date.datetime(now.year, now.month, now.day)
    return now.timestamp() - today.timestamp()


def get_new_message():
    word = random.choice(words)
    return "Word of the Day: " + word["word"] + " - " + word["meaning"]


def send(input: Queue):
    TOKEN = "881872217:AAHjDOnnKDXr5D5LnyphqkO7Roe4QboXhTA"
    bot = telebot.TeleBot(TOKEN)
    while True:
        try:
            sender_id = input.get_nowait()
            print(get_time() + f" sending to { sender_id }")
            bot.send_message(sender_id, get_new_message())
        except Exception:
            pass


def start_sender(input):
    global senders
    global sent

    output = Queue(maxsize=100)

    senders_processes = []
    for i in range(number_senderP):
        new_p = Process(target=send, args=(output,))
        new_p.start()
        senders_processes.append(new_p) 
    
    while True:
        try:
            data = input.get_nowait()
            print(get_time() + f" new data recieved { data }")
            senders.append(
                {
                    "sender": data["sender_id"],
                    "time": data["time"]
                }
            )
            senders = list(sorted(senders, key=lambda x: x["time"]))
        except Exception:
            pass
        current = get_current_seconds()
        for s in senders:
            sender_id = s["sender"]
            time_ = s["time"]
            if sender_id in sent:
                continue
            if time_ > current:
                break
            print(f"start Sending to { sender_id }")
            output.put_nowait(sender_id)
            sent.append(sender_id)

    for p in senders_processes:
        p.join()
