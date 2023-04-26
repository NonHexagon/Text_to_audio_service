import sqlite3
import threading
from datetime import datetime, timedelta
from workwithpsswordandemail import generate_password, send_message
DataBase = sqlite3.connect('main.db', check_same_thread=False)
cursor = DataBase.cursor()


def login_check(user_email: str, user_passwd: str) -> bool | str:
    db_email = cursor.execute("SELECT email FROM users").fetchall()
    container = []
    for i in range(len(db_email)):
        container.append(db_email[i][0])
    print(container)
    if user_email in container:
        print(f'Пользователь с почтой {user_email} существует')
        db_passwd = cursor.execute(f"SELECT tmp_passwd FROM users WHERE email == '{user_email}'").fetchall()
        if str(db_passwd[0][0]) == str(user_passwd):
            print('совпадение')
            return True
        elif str(db_passwd[0][0]) != str(user_passwd):
            return False
    print('Что-то пошло не так')


def change_passwd():
    while True:
        emails = cursor.execute("SELECT email FROM users").fetchall()
        for email in emails:
            passwd_1 = generate_password()
            next_date = cursor.execute(f"SELECT next_time FROM users WHERE email == '{email[0]}'").fetchall()
            if str(datetime.now()) >= str(next_date[0][0]):
                cursor.execute(f"UPDATE users SET tmp_passwd = '{passwd_1}' WHERE email == '{email[0]}'")
                cursor.execute(f"UPDATE users SET timestamp = next_time WHERE email == '{email[0]}'")
                cursor.execute(f"UPDATE users SET next_time = '{datetime.now() + timedelta(minutes=10)}'\
                WHERE email == '{email[0]}'")
                DataBase.commit()
                print(f'Пароль изменен и выслан на почту \033[33m{email[0]}\033[0m!\
                \033[36mСледующее изменение в {datetime.now() + timedelta(minutes=10)}\033[0m')
                send_message(email[0], passwd_1)


if __name__ == '__main__':  # Создаем точку доступа
    mail = str(input('Enter e-mail address: '))
    users = cursor.execute("SELECT DISTINCT * FROM users;").fetchall()
    files = cursor.execute("SELECT DISTINCT * FROM file;").fetchall()
    passwd = cursor.execute(f"SELECT tmp_passwd FROM users WHERE email == '{mail}'").fetchall()
    users_in_db = cursor.execute(f"SELECT email, user_name FROM users").fetchall()
    print(users_in_db)
    for user in users:
        print(f'Пользователь: {user}')
    for file in files:
        print(f'Файл: {file}')

    print(*passwd)
    print(login_check(mail, '1fQI2Tgx'))
    threading.Thread(target=change_passwd())
"""
Что изменилось:
1)Отправка сообщений стала быстрее
2)Есть возможность не загружать файл с текстом, а записывать текст в строку и получать озвученный файл
3)Добавлена поддержка txt файлов
4)Теперь письма именные (Письмо содержит имя пользователя указанной почты)
5)Ускорено изменение пароля
6)Изменен шрифт на всем сайте (Пока тестируем, а дальше видно будет)
7)На некоторых страницах скорректирован стиль

Что в планах:
Сделать одно приложение для запуска всех компонентов сервиса
"""