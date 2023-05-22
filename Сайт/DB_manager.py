import sqlite3  # Импортируем драйвер для подкулчения к бд
import threading  # Импортирем модульь для работы с потоками
from DataBase import Users, File  # Берем из БАзы данных классы файла и пользователя
from datetime import datetime, timedelta  # Импортируем модуль времени
from workwithpsswordandemail import generate_password, send_message  # Из модуля для работы с почтой импортируем генератор пароля и функцию отпарвки сообщения

DataBase = sqlite3.connect('main.db', check_same_thread=False)  # Подключаемся к базе данных
cursor = DataBase.cursor()  # Созадем курсор базы данных


def login_check(user_email: str, user_passwd: str) -> bool | str:  # Функция проверки наличия пользователя в бд
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


def change_passwd():  # Функция смены пароля 
    while True:
        emails = cursor.execute("SELECT email FROM users").fetchall()
        for email in emails:
            passwd_1 = generate_password()
            next_date = cursor.execute(f"SELECT next_time FROM users WHERE email == '{email[0]}'").fetchall()
            if str(datetime.now()) >= str(next_date[0][0]):
                cursor.execute(f"UPDATE users SET tmp_passwd = '{passwd_1}' WHERE email == '{email[0]}'")
                cursor.execute(f"UPDATE users SET timestamp = next_time WHERE email == '{email[0]}'")
                cursor.execute(f"UPDATE users SET next_time = '{datetime.now() + timedelta(minutes=120)}'\
                WHERE email == '{email[0]}'")
                DataBase.commit()
                print(f'Пароль изменен и выслан на почту \033[33m{email[0]}\033[0m!\
                \033[36mСледующее изменение в {datetime.now() + timedelta(minutes=120)}\033[0m')
                send_message(email[0], passwd_1)


def get_user_class_id(user_id: int) -> DataBase:  # Получение получения пользователя по id
    if user_id != 0:
        _id = user_id
        _user_name = cursor.execute(f"SELECT user_name FROM users WHERE id = {_id}").fetchone()
        print('Имя пользователя: ', _user_name)
        if _user_name:
            _f_name = cursor.execute(f"SELECT f_name FROM users WHERE id = {_id}").fetchone()
            _l_name = cursor.execute(f"SELECT l_name FROM users WHERE id = {_id}").fetchone()
            _email = cursor.execute(f"SELECT email FROM users WHERE id = {_id}").fetchone()
            _tmp_passwd = cursor.execute(f"SELECT tmp_passwd FROM users WHERE id = {_id}").fetchone()
            _timestamp = cursor.execute(f"SELECT timestamp FROM users WHERE id = {_id}").fetchone()
            _next_time = cursor.execute(f"SELECT next_time FROM users WHERE id = {_id}").fetchone()

        else:
            print('Ну нет такого!')
            exit()
        current_user = Users(id=_id, user_name=_user_name, f_name=_f_name, l_name=_l_name, email=_email,
                             tmp_passwd=_tmp_passwd, timestamp=_timestamp, next_time=_next_time)
        print(type(current_user))
        return current_user


def get_user_class_email(user_email: str) -> DataBase:  # Функция получения пользователя из бд по почтовому адресу
    if user_email != '':
        _id = cursor.execute(f"SELECT id FROM users WHERE email == '{user_email}'").fetchone()
        if _id:
            _user_name = cursor.execute(f"SELECT user_name FROM users WHERE email == '{user_email}'").fetchone()
            _f_name = cursor.execute(f"SELECT f_name FROM users WHERE email == '{user_email}'").fetchone()
            _l_name = cursor.execute(f"SELECT l_name FROM users WHERE email == '{user_email}'").fetchone()
            _email = user_email
            _tmp_passwd = cursor.execute(f"SELECT tmp_passwd FROM users WHERE email == '{user_email}'").fetchone()
            _timestamp = cursor.execute(f"SELECT timestamp FROM users WHERE email == '{user_email}'").fetchone()
            _next_time = cursor.execute(f"SELECT next_time FROM users WHERE email == '{user_email}'").fetchone()
        else:
            print('Ну нет такого!')
            exit()
        current_user = Users(id=_id, user_name=_user_name, f_name=_f_name, l_name=_l_name, email=_email,
                             tmp_passwd=_tmp_passwd, timestamp=_timestamp, next_time=_next_time)
        return current_user


def reset_passwd(user_mail: str,):  # Сброс пароля пользователя по мейлу
    passwd_1 = generate_password()
    next_date = cursor.execute(f"SELECT next_time FROM users WHERE email == '{user_mail}'").fetchall()
    cursor.execute(f"UPDATE users SET tmp_passwd = '{passwd_1}' WHERE email == '{user_mail}'")
    cursor.execute(f"UPDATE users SET timestamp = next_time WHERE email == '{user_mail}'")
    cursor.execute(f"UPDATE users SET next_time = '{datetime.now() + timedelta(minutes=120)}'\
    WHERE email == '{user_mail}'")
    DataBase.commit()
    print(f'Пароль сброшен и выслан на почту \033[36m{user_mail}\033[0m!\
    \033[36mСледующее изменение в {datetime.now() + timedelta(minutes=120)}\033[0m')
    send_message(user_mail, passwd_1)


user_mails = cursor.execute("SELECT email FROM users").fetchall()


if __name__ == '__main__':  # Создаем точку доступа
    username_id = cursor.execute("SELECT user_name FROM users WHERE id == 1").fetchone()
    files = cursor.execute("SELECT * FROM file").fetchall()
    print(files)
    print(username_id)
    mail = str(input('Enter e-mail address: '))
    users = cursor.execute("SELECT DISTINCT * FROM users;").fetchall()
    files = cursor.execute("SELECT DISTINCT * FROM file;").fetchall()
    passwd = cursor.execute(f"SELECT tmp_passwd FROM users WHERE email == '{mail}'").fetchall()
    print(user_mails)
    for user in users:
        print(f'Пользователь: {user}')
    for file in files:
        print(f'Файл: {file}')

    print(*passwd)
    print(login_check(mail, '1fQI2Tgx'))
    get_user_class_email('mister22898@mail.ru')
    get_user_class_id(1)
    threading.Thread(target=change_passwd())
