import sqlite3
import functools


fp = "data/cache.db"

# Декоратор который при вызове функции обновляет self.conn и self.cursor
# self.conn и self.cursor имеет свойство перестовать БЫТЬ и их нужно обновлять


def update_conn(s):
    def f(fun):
        @functools.wraps(fun)
        def wrapped(*args, **kwargs):
            conn = sqlite3.connect(s.path)
            cursor = conn.cursor()
            result = fun(cursor, *args, **kwargs)
            conn.commit()
            return result
        return wrapped
    return f


funcs_needed_to_be_update = [
    "ready_tables",
    "exe" 
]


class DB:
    def __init__(self, fp: str, tables: dict):
        self.path = fp
        self.tables = tables
        # Using decorator update_conn to funcs that are in "func_needed_to_be_update"
        method_list = [func for func in dir(DB)]
        for i, method in enumerate(method_list):
            if callable(getattr(DB, method)) and not method.startswith("__")\
                    and method in funcs_needed_to_be_update:
                setattr(self, method, update_conn(self)(getattr(self, method)))
        # ---------------------------------------------------------------------------
        self.ready_tables()
    
    def ready_tables(self, cursor):
        for table in self.tables:
            schema = list(map(lambda k: k + " " + self.tables[table][k], self.tables[table]))
            try:
                cursor.execute(
                    f"CREATE TABLE { table }({ ','.join(schema) })"    
                )
            except Exception as e:
                pass # table already exists
    
    def exe(self, cursor, s, *args):
        return cursor.execute(s, args)


class AdapterDB:
    def __init__(self):
        self.db = DB(
            fp, 
            {
                "users": {
                    "id": "INTEGER PRIMARY KEY NOT NULL",
                    "telegram_id": "INTEGER NOT NULL UNIQUE"
                },
                "dictionary": {
                    "id": "INTEGER PRIMARY KEY NOT NULL",
                    "user_id": "INTEGER",
                    "word": "STRING"
                }
            }
        )
    
    def get_user_id(self, telegram_id):
        try:
            return self.db.exe(
                "SELECT id FROM users WHERE telegram_id=?", telegram_id
            ).fetchone()[0]
        except TypeError:
            return None
    
    def add_new_user(self, telegram_id):
        self.db.exe(
            "INSERT INTO users(telegram_id) VALUES (?)", telegram_id
        )
    
    def add_word_to_dictionary_by_user_id(self, user_id, word):
        self.db.exe(
            "INSERT INTO dictionary(user_id, word) VALUES (?, ?)", user_id, word
        )
    
    def add_word_to_dictionary(self, telegram_id, word):
        self.add_word_to_dictionary_by_user_id(
            self.get_user_id(telegram_id),
            word
        )
    
    def get_dictionary_by_user_id(self, user_id):
        return list(map(lambda x: x[0], self.db.exe(
            "SELECT word FROM dictionary WHERE user_id=?", user_id
        ).fetchall()))
    
    def get_dictionary(self, telegram_id):
        return self.get_dictionary_by_user_id(
            self.get_user_id(telegram_id)
        )
