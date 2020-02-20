import telebot
import time
import datetime as date
from multiprocessing import Process, Queue


senders = [
#    {
#       "sender": sender_id,
#       "time": time_to_send
#     }
] # must be sorted

sent = [
#   sender_id
]

number_senderP = 4


def get_time(t=None):
    t = time.time() if t == None else t
    struct_time = time.gmtime(t + 6 * 60 * 60)
    return time.strftime("%d-%m-%Y: %Hh %Mm %Ss", struct_time)


def get_current_seconds():
    now = date.datetime.now().timestamp()
    today = date.datetime.today().timestamp()
    return today - now


def get_new_message():
    # срочно TODO
    return


def send(bot: telebot.TeleBot, input: Queue):
    while True:
        try:
            data = input.get_nowait()
            print(get_time() + f" sending to { data }")
            bot.send_message(data, get_new_message())
        except Queue.Empty:
            pass


def start_sender(bot: telebot.TeleBot, input: Queue, output: Queue):
    global senders
    global sent

    senders_processes = []
    for i in range(number_senderP):
        new_p = Process(target=send, args=(bot, output))
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
            senders = sorted(senders, key=lambda x: x["time"])
        except Queue.Empty:
            pass
        for s in senders:
            id_ = s["sender"]
            time_ = s["time"]
            if id_ in sent:
                continue
            if time_ > get_current_seconds():
                break
            output.put_nowait(id)
            sent.append(id_)

    for p in senders_processes:
        p.join()
