import telebot
from telebot import types
import json
import random

bot = telebot.TeleBot("881872217:AAHjDOnnKDXr5D5LnyphqkO7Roe4QboXhTA")

chat = []

with open("words.json") as f:
    words = json.load(f)

meanings = ["lessen", "deviation, not normal", "hatred", "difficult to understand", "confront", "bitter animosity",
            "insightfulness", "not yielding", "skillful", "skillful", "haughty", "eagerness", "assign, portion",
            "generous", "yielding", "friendly", "friendly", "very old", "study of human beings", "dislike", "lacking interest", "appropriate, inclined", "mysterious, known only by a few", "influence, domination", "one who practices self-denial as a spiritual discipline", "strive for", "belittle", "diligent", "relieve, appease", "waste away", "weaken, reduce", "dignified", "air, feeling", "favorable", "dictator, dictatorial", "a person who acts like a robot", "greed", "common", "bombardment, torrent", "give a false impression", "aggressive, warlike", "generous", "hand down (through a will)", "scold harshly", "supported by two opposing groups (political parties)", "destroyed", "marsh, swamp", "support", "pompous", "crude", "cheerful, floating", "grow, flourish", "support", "convoluted, complex", "discordant sound", "coax", "insensitive", "irritable", "fickle", "belittle", "bitter", "harshly critical", "scold", "intellectual", "mortification", "swindler", "belittle", "belittle", "vulgar, boorish", "indirect", "restrict", "escape, avoid", "secretive", "blend, fuse", "succinct", "self-satisfaction, smugness", "yielding", "compromising, apologizing", "agree", "large destructive fire", "a place where things merge or flow together", "pleasant", "careful", "dismay", "disdainful", "despicable", "belligerent, quarrelsome", "sociable, lively", "abundant", "strengthen or support with additional evidence", "sophisticated, urbane", "the trait of trusting others too much", "blameworthy", "hasty, superficial", "courageous", "scarcity", "failure", "weaken(ed)", "prove wrong", "destroy", "order, politeness", "respectful submission, yielding", "humiliation", "harmful", "list, explain", "openly emotional", "overly modest", "make clear and comprehensible", "belittle", "dethrone, remove from power", "moral corruption", "disapprove, belittle", "decrease in value", "make fun of", "not original", "disparaging, belittling", "violate the sacredness of", "sad, depressed", "dictator", "poor", "hindrance, impediment", "lacking", "(often excessively) morally instructive", "shy", "spread out", "stray from the subject at hand", "tending to waste time", "extremely small", "urgent, dreadful", "perceive, perceptive", "disappointed, defeated", "disregard", "discouraging", "disenchantment, disappointment", "insincere", "belittle", "unemotional", "to drive away or disprove", "quarrelsome", "(causing) anxiety", "scatter widely", "dislike, aversion", "different, conflicting", "creating conflict", "make known", "religious, political, or philosophical principles or teachings", "tending to force one's own opinions on other people", "inactive", "deceive", "deliberately deceptive", "enthusiastic", "from diverse sources", "erase", "bubble, fizz", "belief in equality", "joyful", "bring about", "clarify", "evade", "difficulty to catch or define", "make worse", "involve in an argument or conflict", "compassionate", "based on observation and experiment (not theory)", "include, surround", "intrusive", "burden", "mystery, mysterious", "list", "short-lived", "sudden realization", "representative example", "calmness", "even-handed", "ambiguous", "scholarly", "understood only by a few", "alienate, alienation", "praising speech", "bring about, stir up", "demanding, severe requirements", "unearth, dig up", "representative example", "deliberately behaving a certain way to attract attention", "encourage", "too expensive", "useful", "a report designed to reveal the truth to the public", "praise", "disentangle", "superficial, effortless", "group within a larger group", "deceitful, incorrect", "false belief", "excessive enthusiasm", "careful", "understand", "well-suited, happy", "tact, elegant skill", "evident, obvious", "disrespectful", "flushed, flowery", "confuse", "foolishness", "recklessly daring", "sad", "courage", "fortunate, lucky", "deceitful", "cheap(ness)", "commotion, anger", "sneaky", "hopeless", "manner of walking", "courageous", "gigantic", "tastelessly showy", "friendly", "(cause to) grow", "someone who eats and drinks too much", "pompous, pretentious", "common", "hinder, restrict", "robust, sturdy", "speed up the progress of", "belief contrary to the established opinion", "excessively dramatic or emotional", "arrogance", "unique personal trait, quirky", "simply tranquil", "dishonor, humiliation", "illegal", "obstacle", "arrogant", "rash, passionate", "disrespectful, insolent", "senseless, stupid", "inappropriateness, discrepancy", "skeptical", "accuse someone of a crime", "develop, grow", "left doubtful, inconclusive", "formally accuse of a crime", "native to a region", "angered (by injustice)", "unselective, random", "lazy", "too strong to be defeated", "cause", "lenient", "impossible to express in words", "incompetence", "not moving or active", "unsophisticated and trusting, na\u0413\u0407ve", "intrinsic, natural", "restrain(ing)", "intrinsic, natural", "harmless", "implicit suggestion", "mysterious", "dull, boring", "disrespectful", "provoke, start", "related to or similar to an island", "courageous", "flood", "call forth, appeal to", "angry", "incongruity between what is expected and what actually results", "disrespectful", "tired, bored", "cheerful", "cheerful", "fair", "lacking energy, lethargic", "concise", "lazy person", "inactive, dreamy", "the state of being not yet evident or active", "praise", "languid, sluggish", "graceful, supple", "clear, easily understood", "profitable", "short period of calm", "sensational, shocking", "lush, elaborate", "generosity, generous", "capable of being shaped, pliable", "scarred", "overly sentimental", "bleak", "motivated by money", "fickle", "cheap, stingy", "moderate, alleviate", "small amount", "depressed", "diverse, heterogeneous", "many types", "vague", "evil", "beginner", "infamous, ill fame", "poisonous", "subtle difference", "stubborn", "stubborn(ness)", "meddlesome, interfering", "difficult, trying", "a person who takes advantage of opportunities, often unethically", "prophet", "conservative, traditional", "apparent, seeming", "mistake", "one who completely opposes violence", "soothe, calm", "careful", "relieve pain without curing", "clear example", "make dry", "intentional mockery", "someone with biased beliefs", "financially support, be condescending towards", "scarcity", "a person who makes a great show of his knowledge", "unpleasant", "preference", "cheap, stingy", "bossy, decisive", "done routinely with little interest or care", "outermost, secondary", "additional payment, bonus", "irritable", "someone who supports charity", "religious devotion", "calm someone down", "calm", "malleability, the ability to be shaped or molded", "likely true", "surplus", "easily shaped or influenced", "controversial", "babble", "dangerous, unstable", "outcome", "prevent", "early development in maturity and intelligence", "too bold, arrogant", "misleading claim or appearance", "liar", "get or provide", "huge", "intense, significant", "plentiful", "restrictive", "grow, increase", "fertile, fruitful", "formal declaration", "inclination, tendency", "supporter", "lacking imagination, dull", "likely or expected to become", "prudent, frugal", "narrow-minded, unsophisticated", "meticulous, attentive to detail", "a knowledgeable commentator", "suppress, quench", "foolish", "unrestrained, growing", "poorly constructed", "bitter resentment", "relationship", "approve, confirm", "harsh, rowdy", "insatiable, having a huge appetite", "destroy, demolish", "harvest, gather", "defense, counterargument", "stubborn", "reject", "tending to go backward", "hermit", "put right, correct", "reminiscent, having smell", "arguing that a claim is false", "tending to return or revert", "demote", "give back", "reject", "collection", "blameworthy", "belittle", "scold", "reject", "offensive, disgusting", "annull, retract", "emotionally reserved", "respectful, pious", "(related to) elegant speech/writing, elegant speaker/writer", "provoke, excite", "wise", "pretending to be religious, hypocritical", "formally approve", "holiness", "cheerfully confident, optimistic", "satisfy fully", "sarcastic imitation", "flood, soak", "barely sufficient", "harshly critical", "lively, effervescent", "opportunity, range", "very careful and precise", "examine carefully", "smug, holier-than-thou", "selfish", "luck", "submissive, subservient", "astute, smart", "hide, obscure", "comparison", "insult, snub", "careless, sloppy", "comfort, consolation", "expressing care or concern, often too much", "bleak", "deceptive reasoning", "simple, self-disciplined", "occurring at irregular intervals", "false, inauthentic", "reject with contempt", "waste", "not moving", "harsh, plain", "not moving", "strong and loyal", "not yielding", "standard, hackneyed", "loud and harsh", "bewilder", "yielding", "confirm, establish as genuine", "one who intends to overthrow the government", "delicious", "arrogant", "more than necessary", "to take the place of", "surplus", "easily influenced or affected", "suck up, flatterer", "digressive, irrelevant", "abundant", "moody", "delay, evade", "stubborn, determined", "insignificant, flimsy", "critical speech", "suck-up", "drowsiness, apathy", "undemocratic, rigid political control", "praise", "easily managed or controlled", "lasting for only a short time", "extensive written argument about some topic", "apprehension", "suffering", "frivolous, unimportant", "common", "aggressive, bad-tempered", "ever-present, pervasive", "not embarrassed", "extraordinary, weird", "crude", "incomprehensible, unbelievable", "clumsy", "boisterous, unrestrained", "unintentional", "elegant, sophisticated", "seize power without authority", "empty", "conquer, defeat", "dull, uninteresting", "willing to accept bribes", "commanding respect because of age, dignity", "wordy, long-winded", "felt indirectly by imagining someone else's experiences", "watchful, alert", "clear of blame or suspicion", "seeking revenge",
            "one with exceptional musical skill", "poisonous", "thick, sticky", "career", "striving", "lessening", "selfish, stubborn", "anger", "clever or grim sense of humor", "fanatic"]

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
    btn_words = types.InlineKeyboardButton(text="SAT Words Test", callback_data="words")
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
