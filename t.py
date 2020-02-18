import json

a = [
    {
        "text": "Книги",
        "callback_data": "books"
    },
    {
        "text": "Предыдущие SAT тесты",
        "callback_data": "officials"
    },
    {
        "text": "Practice tests",
        "callback_data": "tests"
    },
    {
        "text": "SAT Words Test",
        "callback_data": "words"
    },
    {
        "text": "О боте",
        "callback_data": "about"
    },
    {
        "text": "Что такое SAT?",
        "callback_data": "what"
    }
]
with open("buttons.json", "w") as f:
    json.dump(a, f)