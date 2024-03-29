import os
import time  # Импортируем модуль времени
import random
import threading
from workwithpsswordandemail import send_message, generate_password
from multiprocessing import Process  # модуль для создания отдельных процессов
from DB_manager import login_check, reset_passwd, get_user_class_uni, get_files
from Example_texts import songs_dict
from DataBase import Users, File, Session
from pathlib import Path  # модуль для работы с путями, но нам нужен только инструмент для файлов
from main import Converter  # модуль для конвертации
from flask import *  # модуль для создания веб-приложений
from flask_login import *
from datetime import datetime, timedelta

application = Flask(__name__)  # инициализация экземпляра класса веб-приложения на котором будем собирать проект
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////First.db'  # инициализация базы данных в проекте
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # игнорируем не работающую часть пакета (она нам не нужна)
application.config['SECRET_KEY'] = 'i-could-bleed-for-a-smile-could-die-for-a-gun'
login_manager = LoginManager()
login_manager.init_app(application)
playback_speed = 0
logged_user = Users()

conv = Converter(playback_speed=120)


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


@application.route('/settings', methods=['GET', 'POST'])  # путь к странице с настройками
def settings():  # поиск обращений к определенному пути
    if request.method == 'POST':
        global playback_speed
        mail = str(request.form['reset_mail'])
        tmp_passwd = str(generate_password())
        playback_speed = request.form['audio_speed']
        print(playback_speed)
        if (playback_speed != 0 or playback_speed != '') and playback_speed.isnumeric():
            print('got this', type(playback_speed))
            playback_speed = int(playback_speed)
            return redirect('/uploader')
        if mail != '':
            print(mail)
            reset_passwd(mail)
            return redirect('/login')
        elif type(playback_speed) == str:
            playback_speed = 120
    elif request.method == 'GET':
        return render_template('settings.html')  # возврат страницы с настройками


@application.route('/about', methods=['GET'])  # Страница о нас (но зачем?)
def about():  # обработчик пути
    return render_template('about.html')  # Возврат страницы (таков путь)


@application.route('/reset_passwd', methods=['GET'])
def reset():
    global logged_user
    print(logged_user.email)
    p = Process(target=reset_passwd(logged_user.email))  # инициализация процесса
    p.start()  # запуск процесса
    p.join()  # завершение процесса
    return redirect('/login')


@application.route('/uploader', methods=['GET', 'POST'])  # Страница с конвертором
@login_required
def uploader():  # обработчик
    global playback_speed, logged_user
    keys_arr = list(songs_dict.keys())
    s_name = str(random.choice(keys_arr)).title()
    text_ = songs_dict.get(s_name)
    if request.method == 'POST':  # Проверка на запрос с методом POST
        #clear_folder('./files')
        file = request.files['file']  # получаем файл
        file_name = file.filename
        try:
            file.save(file_name)  # сохраняем полученный файл
        except FileNotFoundError:
            text = str(request.form['inp_text']).strip()  # Проверяем записи в текстовом поле
            if text == "":  # Пустое поле
                print('Empty input')
                error = 'Файл для конвертации отсутствует или строка не была заполнена!'
                return render_template('uploader.html', s_name=s_name, text=text_, error=error)
            else:
                file_name = 'Text_to_audio_service' + str(time.time()) + '.txt'  # создаём файл с текстом из поля
                with open(f'./{file_name}', 'w') as f:
                    f.write(text)
                print(f'Create file {file_name} for text from textblock')
        print(f'[&] {file_name}')  # вывод в консоль для отладки
        if str(Path(file_name).stem).title() in keys_arr:
            print('True')
            return send_file(f'easter_egg/{Path(file_name).stem}.mp3', as_attachment=True)
        else:
            inputFile_name = (f'./{file_name}')  # Добавляем необходимые символы для работы конвертора
            print(playback_speed)
            conv.playback_speed = playback_speed
            conv.file_to_audio(inputFile_name)  # Производим конвертацию
            file_name = Path(file_name).stem  # Вырезаем имя файла
            time_stamp = str(datetime.now())
            user_id = logged_user.id
            print(file_name, time_stamp, user_id)
            new_file = File(file_name=file_name, file_date=time_stamp, file_owner=user_id)
            session_db = Session()  # Выполняем запись в бд
            session_db.add(new_file)
            session_db.commit()
            time.sleep(2)  # Ожидаем 5 секунд, на случай объемных файлов
            print('Данные: ', new_file.file_name, new_file.file_date)
            return send_file(f'files/{file_name}.mp3', as_attachment=True)  # Возврат получившегося файла
    if request.method == 'GET':  # Проверка запроса с методом GET
        conv.clear_folder('./files')
        return render_template('uploader.html', s_name=s_name, text=text_)  # возвращаем страницу конвертора


def transffile(file_name, playback_speed, logged_user=False):
    inputFile_name = (f'./{file_name}')  # Добавляем необходимые символы для работы конвертора
    print(playback_speed)
    conv.playback_speed = playback_speed
    conv.file_to_audio(inputFile_name)  # Производим конвертацию
    file_name = Path(file_name).stem  # Вырезаем имя файла
    time_stamp = str(datetime.now())
    if logged_user:
        user_id = logged_user.id
        print(file_name, time_stamp, user_id)
        new_file = File(file_name=file_name, file_date=time_stamp, file_owner=user_id)
        session_db = Session()  # Выполняем запись в бд
        session_db.add(new_file)
        session_db.commit()
    time.sleep(5)  # Ожидаем 5 секунд, на случай объемных файлов
    if logged_user:
        print('Данные: ', new_file.file_name, new_file.file_date)
    return send_file(f'files/{file_name}.mp3', as_attachment=True)  # Возврат получившегося файла


@application.route('/textloader', methods=['GET', 'POST'])  # Страница с конвертором
def textloader():  # обработчик
    global playback_speed
    if request.method == 'POST':  # Проверка на запрос с методом POST
        conv.clear_folder('./files')
        text = str(request.form['inp_text']).strip()  # Проверяем записи в текстовом поле
        if text == "":  # Пустое поле
            print('Empty input')
            error = 'Текстовое поле не было заполнено!'
            return render_template('textloader.html', error=error)
        else:
            file_name = 'Text_to_audio_service' + str(time.time()) + '.txt'  # создаём файл с текстом из поля
            with open(f'./{file_name}', 'w') as f:
                f.write(text)
            print(f'Create file {file_name} for text from textblock')
        print(f'[&] {file_name}')  # вывод в консоль для отладки
        return transffile(file_name, playback_speed)
    if request.method == 'GET':  # Проверка запроса с методом GET
        conv.clear_folder('./files')
        return render_template('textloader.html')  # возвращаем страницу конвертора


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

        new_user = Users(user_name=user_name, f_name=f_name, l_name=l_name, email=email, tmp_passwd=tmp_passwd,
                         timestamp=timestamp, next_time=next_time)
        try:
            session_db = Session()  # Выполняем запись в бд
            session_db.add(new_user)
            session_db.commit()
            threading.Thread(target=(send_message(email, tmp_passwd, user_name)))
            print(f'Был добавлен новый пользователь: {l_name} {f_name} с ником {user_name}')
        except AttributeError:  # Обработка ошибки атрибутов (иногда случается)
            return 'Что-то пошло не так!'
        return redirect('/login')

    elif request.method == 'GET':
        return render_template('register_form.html')  # Возвращаем рендер страницы


@login_manager.user_loader
def load_user(user):
    global logged_user
    user_ = list(user)
    print(type(user_[0]))
    print(user_[0])
    user_fin = int(user_[0])
    logged_user = get_user_class_uni(user_fin)
    return logged_user


@application.route('/login', methods=['POST', 'GET'])
def login():
    global logged_user
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        input_passwd = str(request.form['tmp_passwd'])
        input_email = str(request.form['email'])
        if login_check(input_email, input_passwd):
            logged_user = get_user_class_uni(user_email=input_email)
            login_user(logged_user)
            return redirect('/uploader')
        else:
            return redirect('/register')


@application.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    global logged_user
    name = logged_user.f_name
    user = logged_user.user_name
    l_name = logged_user.l_name
    files_ = get_files(logged_user.id)
    if request.method == 'GET':
        return render_template('account.html', name=name, user=user, l_name=l_name,
                               tables=[files_.to_html(classes='data', header='true', index=False, justify='center')],
                               files_=files_)


@application.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('main')


@application.after_request
def redirect_to_sing_in(response):
    if response.status_code == 401:
        return redirect(url_for('login') + '?next=' + request.url)
    return response
    pass


if __name__ == '__main__':  # Создаем точку доступа
    port = int(os.environ.get("PORT", 5050))
    application.run(host='0.0.0.0', port=port, debug=True)  # Запускаем приложение без опции дебага

