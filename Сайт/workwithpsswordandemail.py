# -*- coding: utf-8 -*-
import re
import smtplib
from random import randint
import ssl
#from datetime import datetime  #для времени создания пароля
#now = datetime.now()
def send_message(mail, text):#отправка сообщения пользователю. адрес получателя, пароль
    #текст сообщения
    text = """
Subject: This is your password
"""+text
    our_mail='texttoaudiopi201@outlook.com'#наша почта НЕ ПЕРЕНОСИТЬ С OUTLOCK
    SSL_context = ssl.create_default_context()
    with smtplib.SMTP("smtp-mail.outlook.com", 587) as server:#подключение к почт серверу
        server.starttls(context=SSL_context)#шифрование
        server.login(our_mail, 'qdf12345fd')#вход на нашу почту
        server.sendmail(our_mail, mail, text)#отправка

#прооверка корректности ввода почтф
def check_email(email):
    email_form = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'#шаблрн
    if re.fullmatch(email_form, email):
        return(True)
    else:
        return(False)
#альт вариант. Соглосовать
#from validate_email import validate_email
#valid_email = validate_email(email_address='example@gmail.com', check_smtp = True)

#генерация пароля
def generate_pasword():
    pasw = str(randint(0,99999))
    lenn = 5
 
    pasw= pasw.zfill(lenn)#добивание до нужной длины
    return(pasw)

