import sqlite3
mail = str(input('Enter e-mail address: '))
DataBase = sqlite3.connect('main.db')
cursor = DataBase.cursor()
users = cursor.execute("SELECT DISTINCT * FROM users;").fetchall()
files = cursor.execute("SELECT DISTINCT * FROM file;").fetchall()
passwd = cursor.execute(f"SELECT tmp_passwd FROM users WHERE email == '{mail}'").fetchall()
for user in users:
    print(f'Пользователь: {user}')
for file in files:
    print(f'Файл: {file}')

print(*passwd)
