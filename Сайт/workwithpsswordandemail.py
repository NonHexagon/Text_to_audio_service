# -*- encoding: utf-8 -*-
import re
import sqlite3
import smtplib
from email.mime.text import MIMEText
from random import choice
import ssl
from keys import _mail, _passwd


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

    our_mail = str(_mail)  # наша почта
    message = MIMEText('{user_name} Here is your temperate password: {text} '.format(user_name="Спасибо",text=text))
    message['From'] = our_mail
    message['To'] = mail
    message['Subject'] = 'Your password'
    SSL_context = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", 587) as server:  # подключение к почтовому серверу
        server.ehlo()
        server.starttls(context=SSL_context)  # шифрование
        server.login(our_mail, _passwd)  # вход на нашу почту | используется пароль приложения Google почты!
        server.sendmail(our_mail, mail, message.as_string())  # отправка


# проверка корректности ввода почты
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
    simbols = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    passwd = ''
    for i in range(8):
        passwd += choice(simbols)
    return passwd


if __name__ == '__main__':  # Создаем точку доступа
    print(generate_password())
    send_message('204543@edu.fa.ru', 'Hello there, you filthy bastard!')
