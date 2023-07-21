import select
import sqlite3
import threading
import pandas as pd
from sqlalchemy import *
from DataBase import Users, engine, File, Session
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


def data_extractor(req_column, where_state=False, com_stmt='', comp_to='', to_array=False):
    result_arr = []
    if where_state:
        stmt = select(req_column).where(com_stmt == comp_to)
        with engine.connect() as conn:
            if to_array:
                for row in conn.execute(stmt):
                    result_arr.append([*row])
                return result_arr
            else:
                for row in conn.execute(stmt):
                    return row[0]
    else:
        stmt = select(req_column)
        with engine.connect() as conn:
            if to_array:
                for row in conn.execute(stmt):
                    result_arr.append([*row])
                return result_arr
            else:
                for row in conn.execute(stmt):
                    return row[0]


def change_passwd():
    while True:
        emails = data_extractor(Users.email, to_array=True)
        for email in emails:
            user_name = data_extractor(Users.user_name, True, Users.email, email[0])
            passwd_1 = generate_password()
            next_date = data_extractor(Users.next_time, True, Users.email, email[0])
            if str(datetime.now()) >= str(next_date):
                update_passwd = update(Users).where(Users.email == email[0]).values(tmp_passwd=passwd_1)
                next_t = data_extractor(Users.next_time, True, Users.email, email[0])
                update_stamp = update(Users).where(Users.email == email[0]).values(timestamp=next_t)
                update_next = update(Users).where(Users.email == email[0]).values(
                    next_time=(datetime.now() + timedelta(minutes=120)))

                with Session.begin() as conn:
                    conn.execute(update_passwd)
                    conn.execute(update_stamp)
                    conn.execute(update_next)

                print(f'Пароль изменен и выслан на почту \033[33m{email[0]}\033[0m!\
                \033[36mСледующее изменение в {datetime.now() + timedelta(minutes=120)}\033[0m')
                trunner = threading.Thread(target=send_message(email[0], passwd_1, user_name))
                trunner.start()
                trunner.join()


def get_user_class_uni(user_id=0, user_email=''):
    prepared_data = []
    needed_data_arr = [Users.id,
                       Users.user_name,
                       Users.f_name,
                       Users.l_name,
                       Users.tmp_passwd,
                       Users.email,
                       Users.timestamp,
                       Users.next_time]
    if user_id > 0:
        user_email = ''
        user_id = str(user_id)

        for data in needed_data_arr:
            prepared_data.append(data_extractor(data, True, Users.id, user_id))
        prepared_data = tuple(prepared_data)
        print(prepared_data)

    if len(user_email) > 0:
        for data in needed_data_arr:
            prepared_data.append(data_extractor(data, True, Users.email, user_email))
        prepared_data = tuple(prepared_data)
        print(prepared_data)

    _id, _user_name, _f_name, _l_name, _tmp_passwd, _email, _timestamp, _next_time = prepared_data

    current_user = Users(id=_id,
                         user_name=_user_name,
                         f_name=_f_name,
                         l_name=_l_name,
                         email=_email,
                         tmp_passwd=_tmp_passwd,
                         timestamp=_timestamp,
                         next_time=_next_time)
    return current_user


def reset_passwd(user_mail: str):
    mailboxes_query = cursor.execute("SELECT email FROM users").fetchall()
    mailboxes = []
    for i in range(len(mailboxes_query)):
        mailboxes.append(mailboxes_query[i][0])
    if user_mail in mailboxes:
        passwd_1 = generate_password()
        user_name = data_extractor(Users.user_name, True, Users.email, user_mail)

        update_passwd = update(Users).where(Users.email == user_mail).values(tmp_passwd=passwd_1)
        next_t = data_extractor(Users.next_time, True, Users.email, user_mail)
        update_stamp = update(Users).where(Users.email == user_mail).values(timestamp=next_t)
        print(datetime.now() + timedelta(minutes=120))
        update_next = update(Users).where(Users.email == user_mail).values(
            next_time=(datetime.now() + timedelta(minutes=120))
        )
        with Session.begin() as conn:
            conn.execute(update_passwd)
            conn.execute(update_stamp)
            conn.execute(update_next)

        print(f'Пароль сброшен и выслан на почту \033[36m{user_mail}\033[0m!\
        \033[36mСледующее изменение в {datetime.now() + timedelta(minutes=120)}\033[0m')
        trunner = threading.Thread(target=send_message(user_mail, passwd_1, user_name))
        trunner.start()
        trunner.join()
    else:
        return print('User with this email is not exist')


def get_files(user_id):
    stmt = File.file_name, File.file_date
    user_files = data_extractor(stmt, True, File.file_owner, user_id, to_array=True)
    df = pd.DataFrame(columns=['Название файла', 'Дата конвертации'])
    for i in range(len(user_files)):
        df.loc[i] = [user_files[i][0]] + [user_files[i][1]]
    return df


if __name__ == '__main__':  # Создаем точку доступа
    stmt_2 = Users.email, Users.tmp_passwd, Users.id, Users.next_time, Users.timestamp
    print(data_extractor(stmt_2, to_array=True))
