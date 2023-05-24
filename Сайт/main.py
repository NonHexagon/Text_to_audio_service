import os  # модуль для взаимодействия с операционной системой
import shutil
from multiprocessing import Process  # модуль для создания отдельных процессов
from pathlib import Path  # модуль для работы с путями в файловой системе
from tkinter import Tk

import docx2txt  # модуль для чтения docx файла
import langid  # модуль для определения языка
import pdfplumber  # модуль для чтения pdf файлов
import pyttsx3  # модуль для озвучки текса (используя голоса операционной системы)


def pdf_to_audio(file_path='/', playbackspeed=120):  # Функция для запуска конвертора в отдельном процессе
    p = Process(target=pdf_to_audio_processor(file_path, playbackspeed))  # инициализация процесса
    p.start()  # запуск процесса
    p.join()  # завершение процесса


audio = pyttsx3.init()


def work_with_text(doc_text, file_path, playbackspeed):  # конвертор
    print(playbackspeed)
    print(doc_text)  # вывод строки
    lang = langid.classify(doc_text)[0]  # определение языка текста
    # инициализация чтения
    print(lang)  # вывод языка
    audio.setProperty('rate', playbackspeed)
    ru = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0'  # читалка на русском
    en = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'  # читалка на англ

    if lang == 'en':  # проверка языка текста
        audio.setProperty('voice', en)  # используем соответствующий язык читалки
    if lang == 'ru':
        audio.setProperty('voice', ru)
    file_name = Path(file_path).stem  # получаем название файла
    audio.save_to_file(doc_text, f'files/{file_name}.mp3')  # указываем куда сохранить данные
    audio.runAndWait()  # запускаем читалку
    os.remove(file_path)  # удаляем исходный файл
    return print(f'[+] {file_name} has been converted to audio!')  # маркер готовности файла


def clear_folder(path: str):
    folder = path
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def pdf_to_audio_processor(file_path='./', playbackspeed=120):  # Считывает файл и вызывает конвертор
    root = Tk()
    if Path(file_path).is_file() and Path(file_path).suffix == '.pdf':  # проверка на pdf файл
        print(f'[!] {Path(file_path).stem} is processing...')  # маркер начала конвертации
        with pdfplumber.PDF(open(file=file_path, mode='rb')) as pdf:  # чтение файла
            pages = [pages.extract_text() for pages in pdf.pages]  # переносим все в одну строку
        doc_text = ''.join(pages).replace('\n', ' ')
        return work_with_text(doc_text, file_path, playbackspeed)

    elif Path(file_path).is_file() and Path(file_path).suffix == '.docx':  # проверка на docx файл
        print(f'[!] {Path(file_path).stem} is processing...')  # маркер начала конвертации
        doc_text = str(docx2txt.process(file_path)).replace('\n', ' ')  # переносим все в одну строку
        root.bell()
        return work_with_text(doc_text, file_path, playbackspeed)
    elif Path(file_path).is_file() and Path(file_path).suffix == '.txt':  # проверка на txt файл
        print(f'[!] {Path(file_path).stem} is processing...')  # маркер начала конвертации
        with open(file_path, 'r') as f:
            doc_text = f.read()
        doc_text = doc_text.replace('\n', ' ')  # переносим все в одну строку
        return work_with_text(doc_text, file_path, playbackspeed)
    else:  # если файл не был найден или не имеет поддерживаемого расширения
        root.bell()
        return print('[!] File not found')  # выводим в консоль сообщение


if __name__ == "__main__":  # создаем точку доступа
    p = Process(target=pdf_to_audio_processor('./californication.docx', 120))  # инициализируем процесс для проверки
    p.start()  # запускаем процесс
    p.join()  # завершаем процесс
