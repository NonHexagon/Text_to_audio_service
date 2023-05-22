import sqlite3  # импорт движка базы данных
from flask_login import UserMixin, login_manager, LoginManager
from sqlite3 import Error  # импортируем отдельно модуль ошибки (для удобства использования)
import sqlalchemy  # импортируем ORM
from datetime import timedelta
from sqlalchemy.orm import declarative_base, sessionmaker  # Импортируем необходимые модули дял сборки базы данных
from sqlalchemy import create_engine  # модуль который и будет производить сборку
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean  # Типы данных для бд
from sqlalchemy import Sequence  # Вот что это - не помню
import os  # модуль для работы с операционной системой

Base = declarative_base()  # Создаем экземпляр класса declarative_base, позволяющий работать с таблицей как с объектом класса
engine = create_engine('sqlite:///main.db', echo=False)  # Генерим базу данных
Session = sessionmaker(bind=engine)  # Экземпляр класса сессий


class Users(Base, UserMixin):  # Таблица пользователей
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    user_name = Column(String(80), nullable=False)
    f_name = Column(String(80), nullable=False)
    l_name = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False, unique=True)
    tmp_passwd = Column(String(16), nullable=False)
    timestamp = Column(String(26), nullable=False)
    next_time = Column(String(26), nullable=False)

    def __repr__(self):
        return f'<User (user name = {self.user_name}, first name = {self.f_name})>'


class File(Base):  # Таблица файлов
    __tablename__ = 'file'
    file_id = Column(Integer, Sequence('file_id_seq'), primary_key=True)
    file_name = Column(String, nullable=False)
    file_date = Column(String(26), nullable=False)
    file_owner = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'File (file name = {self.file_name} owner = {self.file_owner})'


Base.metadata.create_all(engine)  # Создаем движок для работы с бд и создаем саму бд


def get_user_name(mail_address: str) -> str:  # Функция поллучения имени пользователя из бд по почтовому ящику
    DB = sqlite3.connect('main.db', check_same_thread=False)
    cursor = DB.cursor()
    user_name = cursor.execute(f"SELECT user_name FROM users WHERE email == '{mail_address}'").fetchall()
    return str(user_name[0][0])
