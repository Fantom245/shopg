import sqlite3


# # Здесь мы с помощью sqlite3.connect создаём нашу базу данных
# # Внутри мы указываем её название с обязательным расширением .db
# db = sqlite3.connect("data_base.db")

# # Создание таблицы

# # Создание курсора, нужен для использования разных команд
# c = db.cursor()

# # Метод для прописания и выполнения команд
# c.execute("""CREATE TABLE user (
#     name text,
#     last_name text
# )""")

# db.commit()


# # Обязательно после открытия базы данных нужно её закрыть с помощью close() чтобы не произошла утечка
# # инфорамации
# db.close()


class DataBase:
    def __init__(self, db_name):
        self.db_name = db_name
    
    def create_db(self):
        db = sqlite3.connect("self.db_name.db")
        cur = db.cursor()
        cur.execute("""CREATE TABLE users
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL
        """)
        db.commit()
        db.close()

    def add_user(self, name, email):
        db = sqlite3.connect(self.db_name)
        cur = db.cursor()
        cur.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        db.commit()
        db.close()