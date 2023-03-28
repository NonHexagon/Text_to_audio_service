import sqlite3  # импорт движка базы данных
from sqlite3 import Error  # импортируем отдельно модуль ошибки (для удобства использования)
import sqlalchemy  # импортируем ORM
from sqlalchemy.orm import declarative_base, sessionmaker  # Импортируем необходимые модули дял сборки базы данных
from sqlalchemy import create_engine  # модуль который и будет производить сборку
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean  # Типы данных для бд
from sqlalchemy import Sequence  # Вот что это - не помню
import os


Base = declarative_base()
engine = create_engine('sqlite:///main.db', echo=False)
Session = sessionmaker(bind=engine)


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    user_name = Column(String(80), nullable=False)
    f_name = Column(String(80), nullable=False)
    l_name = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    tmp_passwd = Column(String(16), nullable=False)

    def __repr__(self):
        return f'<User (user name = {self.user_name}, first name = {self.f_name})>'


class File(Base):
    __tablename__ = 'file'
    file_id = Column(Integer, Sequence('file_id_seq'), primary_key=True)
    file_name = Column(String, nullable=False)
    # file_date = Column(Date)
    file_owner = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'File (file name = {self.file_name} owner = {self.file_owner})'


Base.metadata.create_all(engine)
