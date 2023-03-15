import time  # Импортируем модуль времени
from pathlib import Path  # модуль для работы с путями, но нам нужен только инструмент для файлов
from main import pdf_to_audio  # модуль для конвертации
from flask import *  # модуль для создания веб-приложений
from flask_sqlalchemy import SQLAlchemy  # пакет ORM СУБД
from datetime import datetime


application = Flask(__name__)  # инициализация экземпляра класса веб-приложения на котором будем собирать проект
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////First.db'  # инициализация базы данных в проекте
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # игнорируем не работающую часть пакета (она нам не нужна)
db = SQLAlchemy(application)  # создаем экземпляр класса ORM


class User(db.Model):  # таблица User базы данных
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # графа идентификатора
    user_name = db.Column(db.String(32), nullable=False)  # графа с именем пользователя
    e_mail = db.Column(db.String(64), nullable=False)  # поле данных почты
    passwd = db.Column(db.String(32), nullable=False)  # поле пароля (позже будет храниться в зашифрованном виде)

    def __init__(self, file_id, user_name, passwd, e_mail):  # инициализация класса User (она же таблица, но у нас ORM)
        self.passwd = passwd.strip()  # присваиваем соответствующие значения, при этом удаляем пробелы
        self.e_mail = e_mail.srtip()
        self.user_name = user_name.strip()
        self.file_id = [File(file_id=file_id)]  # делаем ссылку на вторую таблицу, где есть нужная нам строка


class File(db.Model):  # таблица файла в бд
    __tablename__ = 'file'
    file_id = db.Column(db.Integer, primary_key=True)  # id
    file_name = db.Column(db.String(32), nullable=False)  # имя файла
    file = db.Column(db.BLOB)  # сам файл в типе blob (используется для хранения файлов в бд)
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # id пользователя-владельца
    user_id = db.relationship("User", backref=db.backref('file_id', lazy=True))  # ссылка на другую таблицу


@application.route('/home', methods=['GET'])  # прописываем пути для достижения домашней страницы
@application.route('/', methods=['GET'])
@application.route('/main', methods=['GET'])
@application.route('/main_page', methods=['GET'])
def home():  # функция для отлова запроса домашней страницы
    return render_template('main.html')  # возвращаем главную страницу


@application.route('/index', methods=['GET'])  # тестовое оформление (на нее не попасть, если не знать о ней)
def index():  # отлов запроса к странице индекса
    return render_template('index.html')  # возвращаем страницу


@application.route('/guide', methods=['GET'])  # путь для страницы с инструкцией пользователя
@application.route('/instruction', methods=['GET'])  # альтернативный путь
def guide():  # отлов путей
    return render_template('guide.html')  # возврат страницы


@application.route('/settings', methods=['GET'])  # путь к странице с настройками
def settings():  # поиск обращений к определенному пути
    return render_template('settings.html')  # возврат страницы с настройками


@application.route('/about', methods=['GET'])  # Страница о нас (но зачем?)
def about():  # обработчик пути
    return render_template('about.html')  # Возврат страницы (таков путь)


@application.route('/uploader', methods=['GET', 'POST'])  # Страница с конвертором
def uploader():  # обработчик
    if request.method == 'POST':  # Проверка на запрос с методом POST
        file = request.files['file']  # получаем файл
        try:
            file.save(file.filename)  # сохраняем полученный файл
        except FileNotFoundError:
            print('Empty input')
            return render_template('uploader.html', message ='Необходимо выбрать файл для озвучивания')
        print(f'[&]{file.filename}')  # вывод в консоль для отладки
        if Path(file.filename).stem == 'Californication':
            print('True')
            return send_file(f'easter_egg/Californication.mp3', as_attachment=True)
        else:
            inputFile_name = (f'./{file.filename}')  # Добавляем необходимые символы для работы конвертора
            pdf_to_audio(inputFile_name)  # Производим конвертацию
            file_name = Path(file.filename).stem  # Вырезаем имя файла
            time.sleep(5)  # Ожидаем 5 секунд, на случай объемных файлов
            return send_file(f'files/{file_name}.mp3', as_attachment=True)  # Возврат получившегося файла
    if request.method == 'GET':  # Проверка запроса с методом GET
        return render_template('uploader.html')  # возвращаем страницу конвертора


if __name__ == '__main__':  # Создаем точку доступа
    application.run(debug=False)  # Запускаем приложение без опции дебага
"""
Ограничение по расширению файла прописаны в коде html странице, так что здесь их нет и не будет.
К бд обращений пока нет, так как сама схема требует доработок и исправлений.
В дальнейших версиях добавим бд и взаимодействие с ней, а пока она висит как заглушка. 
"""
