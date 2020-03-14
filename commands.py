from functions import *
import emoji
import random

max_questions = 100

# JSONS
funcs = open_json("data/buttons.json")

posts_list = open_json("data/posts.json")
poststextlist = {v: k for k, v in enumerate(posts_list)}

bookslist = open_json("data/books.json")
booktextlist = {v: k for k, v in enumerate(map(lambda x: x["text"], bookslist))}

officialslist = open_json("data/officals.json")
officialstextlist = {v: k for k, v in enumerate(map(lambda x: x["text"], officialslist))}

words_json = open_json("data/words.json")

meanings = list(map(lambda x: x["meaning"], words_json))
words_list = list(map(lambda x: x["word"], words_json))

states = open_json("data/states.json")

with open("data/sat.txt", "r", encoding="utf-8") as f:
    sattext = f.read()


def getabout():
    with open("data/about.txt", "r", encoding="utf-8") as k:
        abouttext = k.read()
        return abouttext
# ------


times = ["6:00", "9:00", "12:00", "15:00", "18:00", "21:00", "0:00", "Other"]


class Commands:
    def __init__(self, bot, q, db):
        self.bot = bot
        self.queue = q
        self.db = db

        self.commands = {
            "start": self.start,
            "menu": self.menu
        }
        self.cache = {
            # state, last_update
        }
        self.commands.update({
            x: self.__getattribute__(x) for x in dir(Commands) if callable(getattr(Commands, x)) and not x.startswith("__") and x not in ["get_commands", "exe"]
        })
    
    def get_commands(self):
        return self.commands.keys()
    
    def exe(self, command, chat_id):
        return self.commands[command](chat_id)

    def start(self, chat_id):
        self.bot.send_message(chat_id, "Hi! This is a bot that helps you in preparation for the SAT")
        self.menu(chat_id)

    def menu(self, chat_id):
        self.bot.send_message(
            chat_id, 
            "Menu", 
            reply_markup=createKeyboard(
                2,
                list(
                    map(
                        lambda x:
                        emoji.emojize(x),
                        funcs.keys()
                    )
                )
            )
        )
    
    def books(self, chat_id):
        markup = types.InlineKeyboardMarkup()
        for book in bookslist:
            btn_book = types.InlineKeyboardButton(text=book["text"], callback_data=book["text"])
            markup.add(btn_book)
        self.bot.send_message(chat_id, emoji.emojize("SAT Books :exclamation:", use_aliases=True), reply_markup=markup)
    
    def officials(self, chat_id):
        markup = types.InlineKeyboardMarkup()
        for offical in officialslist:
            btn_book = types.InlineKeyboardButton(text=offical["text"], callback_data=offical["text"])
            markup.add(btn_book)
        self.bot.send_message(chat_id, "Past SAT tests", reply_markup=markup)
    
    def tests(self, chat_id):
        self.bot.send_message(chat_id, "Coming soon!")
    
    def words(self, chat_id):
        if "questions" in self.cache[chat_id]:
            self.send_question(chat_id)
            return
        self.cache[chat_id].update({
            "state": states["words"],
            "current_question": -1,
            "total_question": 0,
            "right_answers": 0,
            "questions": []
        })
        self.bot.send_message(
            chat_id, 
            "Choose amount of questions",
            reply_markup=self.standard_number_questions()
        )

    def standard_number_questions(self):
        return createKeyboardWithMenu(4, ["10", "30", "50", "70"])

    def get_answer_keyboard(self, question, n=4, width=2):
        answers = []
        right_answer = words_json[words_list.index(question)]["meaning"]
        for i in range(n - 1):
            new_a = {"word": ""}
            while new_a["word"] in ["", question]:
                new_a = random.choice(words_json)
            answers.append(new_a["meaning"])
        answers.append(right_answer)
        random_answers = []
        for i in range(len(answers)):
            random_answers.append(answers.pop(random.randint(0, len(answers) - 1)))
        return createKeyboardWithMenu(width, random_answers)

    def get_questions(self, n):
        questions = []
        for i in range(n):
            new_q = {"word": ""}
            while new_q["word"] in [""] + questions:
                new_q = random.choice(words_json)
            questions.append(new_q["word"])
        return questions

    def send_question(self, chat_id):
        current_question = self.cache[chat_id]['current_question']
        self.bot.send_message(
            chat_id,
            f"Word #{ current_question + 1 }: {self.cache[chat_id]['questions'][current_question]}",
            reply_markup=self.get_answer_keyboard(self.cache[chat_id]["questions"][current_question])
        )
    
    def next_word(self, message):
        chat_id = message.json["chat"]["id"]
        if len(self.cache[chat_id]["questions"]) == 0:
            if not is_int(message.text):
                self.bot.send_message(
                    chat_id, 
                    "Choose amount of questions",
                    reply_markup=self.standard_number_questions()
                )
                return
            number_questions = int(message.text)
            if number_questions > max_questions:
                self.bot.send_message(
                    chat_id, 
                    "Choose amount of questions" + f" not bigger than{ max_questions }",
                    reply_markup=self.standard_number_questions()
                )
                return
            self.cache[chat_id].update({
                "state": states["words"],
                "current_question": 0,
                "total_question": number_questions,
                "right_answers": 0,
                "questions": self.get_questions(number_questions)
            })
            self.send_question(chat_id)
            return
        
        answer = message.text

        right_answer = words_json[words_list.index(self.cache[chat_id]["questions"][self.cache[chat_id]["current_question"]])]["meaning"]
        if answer == right_answer:
            self.bot.send_message(chat_id, emoji.emojize("Correct :white_check_mark:", use_aliases=True))
            self.cache[chat_id]["right_answers"] += 1
        else:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Add to the dictionary", callback_data="dictionary_append: " +
                self.cache[chat_id]["questions"][self.cache[chat_id]["current_question"]]))
            self.bot.send_message(chat_id, emoji.emojize("Incorrect :x: \n", use_aliases=True) +
                            "Right answer is " + right_answer, reply_markup=markup)

        if self.cache[chat_id]["current_question"] == self.cache[chat_id]["total_question"] - 1:
            self.cache[chat_id]["state"] = states["nothing"]
            self.bot.send_message(
                chat_id,
                f"You have finished the test! You have { self.cache[chat_id]['right_answers'] }"
                f" out of { self.cache[chat_id]['total_question'] } questions",
                reply_markup=createKeyboardWithMenu(1, [])
            )
            self.cache[chat_id] = pop_keys_from_dict(d=self.cache[chat_id], keys=[
                "current_question",
                "total_question",
                "right_answers",
                "questions"
            ])
            return
        self.cache[chat_id]["current_question"] += 1
        self.send_question(chat_id)
    
    def everyday(self, message):
        chat_id = message.json["chat"]["id"]
        timezone = self.cache[chat_id]["timezone"]
        text = message.text
        if text == "Other":
            self.othertime(message)
        else:
            user_time = text.split(":")
            sec = (int(user_time[0]) - timezone) % 24 * 3600 + int(user_time[1]) * 60
            smth = {
                "sender_id": chat_id,
                "time": sec,
                "hours": text
            }
            print(smth)
            try:
                self.queue.put_nowait(smth)
            except Exception as e:
                print(e)
            self.cache[chat_id]["state"] = states["nothing"]

    def timezone(self, message):
        chat_id = message.json["chat"]["id"]
        text = message.text
        if text == "Other":
            self.othertz(message)
        else:
            time = text.split("UTC")[-1].replace(")", "")
            timezone = int(time)
            print(timezone)
            self.cache[chat_id]["timezone"] = timezone
            self.bot.send_message(chat_id, "Choose Hour",
                                  reply_markup=createKeyboardWithMenu(row_width=4, args=times, onetime=True))
            self.cache[chat_id]["state"] = states["settime"]

    def settz(self, chat_id):
        self.cache[chat_id]["state"] = states["settz"]
        self.bot.send_message(chat_id, "Choose Timezone", reply_markup=createKeyboardWithMenu(1, ["AST (UTC+6)",
                                                                                                  "EST (UTC-5)",
                                                                                                  "Other"],
                                                                                              onetime=True))
        return

    def othertz(self, chat_id):
        self.cache[chat_id]["state"] = states["othertz"]
        self.bot.send_message(chat_id, "Enter timezone (e.g. UTC+10)")

    def othertime(self, message):
        chat_id = message.json["chat"]["id"]
        self.bot.send_message(chat_id, "Enter time in 24 hour format (e.g. 13:15)")
        self.cache[chat_id]["state"] = states["othertime"]
    
    def what(self, chat_id):
        self.bot.send_message(chat_id, text=sattext)
    
    def about(self, chat_id):
        self.bot.send_message(chat_id, text=getabout())

    def dictionary(self, chat_id):
        d = self.db.get_dictionary(chat_id)
        if len(d) == 0:
            self.bot.send_message(chat_id, "There is no words in your dictionary")
        else:
            self.bot.send_message(chat_id, "Dictionary:\n    " + "\n    ".join(d))

    def admin(self, chat_id):
        if not self.cache[chat_id]["admin"]:
            self.bot.send_message(chat_id, "Enter password")
        self.cache[chat_id]["state"] = states["admin"]

    def stats(self, chat_id):
        cur = time.time()
        self.bot.send_message(chat_id, "Number of users: " + str(len(self.cache.keys())))
        n = 0
        for c in self.cache.keys():
            if (cur - self.cache[c]["time_seen"]) < (24 * 3600):
                n += 1
        self.bot.send_message(chat_id, "Number of users in last 24 hours: " + str(n))

    def newpost(self, chat_id):
        self.bot.send_message(chat_id, "Enter post here")
        self.cache[chat_id]["state"] = states["newpost"]

    def editabout(self, chat_id):
        self.bot.send_message(chat_id, "Enter new text")
        self.cache[chat_id]["state"] = states["editabout"]
