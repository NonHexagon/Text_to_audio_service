import time  # Импортируем модуль времени
from workwithpasswordandemail import send_message, generate_password
from Example_texts import songs_dict
from DB_manager import login_check
from DataBase import Users, File, Session
from pathlib import Path  # модуль для работы с путями, но нам нужен только инструмент для файлов
from main import pdf_to_audio  # модуль для конвертации
from flask import *  # модуль для создания веб-приложений
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy  # пакет ORM СУБД


application = Flask(__name__)  # инициализация экземпляра класса веб-приложения на котором будем собирать проект
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////First.db'  # инициализация базы данных в проекте
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # игнорируем не работающую часть пакета (она нам не нужна)
application.config['SECRET_KEY'] = 'i-could-bleed-for-a-smile-could-die-for-a-gun'


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
    keys_arr = list(songs_dict.keys())
    s_name = str(random.choice(keys_arr)).title()
    print(s_name)
    text = songs_dict.get(s_name)
    if request.method == 'POST':  # Проверка на запрос с методом POST
        file = request.files['file']  # получаем файл
        try:
            file.save(file.filename)  # сохраняем полученный файл
        except FileNotFoundError:
            print('Empty input')
            return render_template('uploader.html', message='Необходимо выбрать файл для озвучивания')
        print(f'[&] {file.filename}')  # вывод в консоль для отладки
        if str(Path(file.filename).stem).title() == s_name:
            print('True')
            return send_file(f'easter_egg/{s_name}.mp3', as_attachment=True)
        else:
            inputFile_name = (f'./{file.filename}')  # Добавляем необходимые символы для работы конвертора
            pdf_to_audio(inputFile_name)  # Производим конвертацию
            file_name = Path(file.filename).stem  # Вырезаем имя файла
            time.sleep(5)  # Ожидаем 5 секунд, на случай объемных файлов
            return send_file(f'files/{file_name}.mp3', as_attachment=True)  # Возврат получившегося файла
    if request.method == 'GET':  # Проверка запроса с методом GET

        return render_template('uploader.html', s_name=s_name, text=text)  # возвращаем страницу конвертора


@application.route('/register', methods=['POST', 'GET'])  # Объявление нужных методов
def registration():
    if request.method == 'POST':
        user_name = str(request.form['user_name']).strip()  # Получаем данные из формы
        print(user_name)
        f_name = str(request.form['f_name']).strip()
        print(f_name)
        l_name = str(request.form['l_name']).strip()
        print(l_name)
        email = str(request.form['email']).strip()
        print(email)
        tmp_passwd = str(generate_password())  # пароль пока не используется
        timestamp = str(datetime.now())
        next_time = str(datetime.now() + timedelta(minutes=5))

        new_user = Users(user_name=user_name, f_name=f_name, l_name=l_name, email=email, tmp_passwd=tmp_passwd,\
                         timestamp=timestamp, next_time=next_time)
        try:
            session_db = Session()  # Выполняем запись в бд
            session_db.add(new_user)
            session_db.commit()
            send_message(email, tmp_passwd)
            print(f'Был добавлен новый пользователь: {l_name} {f_name} с ником {user_name}')
        except AttributeError:  # Обработка ошибки атрибутов (иногда случается)
            return 'Что-то пошло не так!'
        return redirect('/login')

    elif request.method == 'GET':
        return render_template('register_form.html')  # Возвращаем рендер страницы



@application.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        input_passwd = str(request.form['tmp_passwd'])
        input_email = str(request.form['email'])
        if login_check(input_email, input_passwd):
            return redirect('/uploader')
        else:
            return redirect('/register')


if __name__ == '__main__':  # Создаем точку доступа
    application.run(debug=False)  # Запускаем приложение без опции дебага
"""
Ограничение по расширению файла прописаны в коде html странице, так что здесь их нет и не будет.
К бд обращений пока нет, так как сама схема требует доработок и исправлений.
В дальнейших версиях добавим бд и взаимодействие с ней, а пока она висит как заглушка. 
"""
