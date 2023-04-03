# -*- encoding: utf-8 -*-
import re
import sqlite3
import smtplib
from random import randint
import ssl


# from datetime import datetime  #для времени создания пароля
# now = datetime.now()
def send_message(mail, text):  # Отправка сообщения пользователю. Адрес получателя, пароль
    db = sqlite3.connect('main.db')
    cursor = db.cursor()
    name = cursor.execute(f"SELECT DISTINCT f_name FROM users WHERE email == '{mail}'").fetchall()
    user_name = cursor.execute(f"SELECT DISTINCT user_name FROM users WHERE email == '{mail}'").fetchall()
    # текст сообщения
    # name = name[0][0]
    # user_name = user_name[0][0]

    text = ("Subject: Here is your temperate password: " + text + "It will change next time").strip()
    print(text)
    our_mail = 'texttoaudiopi201@outlook.com'  # наша почта НЕ ПЕРЕНОСИТЬ С OUTLOOK
    SSL_context = ssl.create_default_context()
    with smtplib.SMTP("smtp-mail.outlook.com", 587) as server:  # подключение к почтовому серверу
        server.starttls(context=SSL_context)  # шифрование
        server.login(our_mail, 'qdf12345fd')  # вход на нашу почту
        server.sendmail(our_mail, mail, text)  # отправка


# проверка корректности ввода почта
def check_email(email):
    email_form = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # шаблон
    if re.fullmatch(email_form, email):
        return True
    else:
        return False


# альт вариант. Согласовать
# from validate_email import validate_email
# valid_email = validate_email(email_address='example@gmail.com', check_smtp = True)

# генерация пароля
def generate_password():
    passwd = str(randint(0, 99999))
    len_ = 6

    passwd = passwd.zfill(len_)  # добивание до нужной длины
    return passwd


if __name__ == '__main__':  # Создаем точку доступа
    print(generate_password())
    send_message('204543@edu.fa.ru', 'Hello there!')
