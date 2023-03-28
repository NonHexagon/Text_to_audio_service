import sqlite3

DataBase = sqlite3.connect('main.db')
cursor = DataBase.cursor()
users = cursor.execute("SELECT DISTINCT * FROM users;").fetchall()
files = cursor.execute("SELECT DISTINCT * FROM file;").fetchall()
for user in users:
    print(f'Пользователь: {user}')
for file in files:
    print(f'Файл: {file}')


