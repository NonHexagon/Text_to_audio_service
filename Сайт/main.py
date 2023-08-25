import os  # модуль для взаимодействия с операционной системой
import shutil
from multiprocessing import Process  # модуль для создания отдельных процессов
from pathlib import Path  # модуль для работы с путями в файловой системе
from tkinter import Tk

import docx2txt  # модуль для чтения docx файла
import langid  # модуль для определения языка
import pdfplumber  # модуль для чтения pdf файлов
import pyttsx3  # модуль для озвучки текса (используя голоса операционной системы)


class Converter:
    def __init__(self, playback_speed):
        self.audio = pyttsx3.init()
        self.voices = self.audio.getProperty('voices')
        self.playback_speed = playback_speed

    def file_to_audio(self, file_path):
        p = Process(target=self.file_to_audio_proc(file_path))
        p.start()
        p.join()

    def text_processor(self, doc_text, file_path):
        lang = langid.classify(doc_text)[0]
        self.audio.setProperty('rate', self.playback_speed)
        for voice in self.voices:
            current_lang = str(voice.name).split('-')[1][0:3].lower().strip()
            if str(lang) == current_lang:
                self.audio.setProperty('voice', voice.id)

        file_name = Path(file_path).stem
        self.audio.save_to_file(doc_text, f'files/{file_name}.mp3')
        self.audio.runAndWait()
        os.remove(file_path)
        return print(f'[+] {file_name} has been converted to audio!')

    def file_to_audio_proc(self, file_path='./'):
        root = Tk()
        if Path(file_path).is_file() and Path(file_path).suffix == '.pdf':
            print(f'[!] {Path(file_path).stem} is converting...\nStand by...')
            root.bell()
            with pdfplumber.PDF(open(file=file_path, mode='rb')) as pdf:
                pages = [pages.extract_text() for pages in pdf.pages]
            doc_text = ''.join(pages).replace('\n', ' ')
            return self.text_processor(doc_text, file_path)

        elif Path(file_path).is_file() and Path(file_path).suffix == '.docx':
            print(f'[!] {Path(file_path).stem} is converting...\nStand by...')
            root.bell()
            doc_text = str(docx2txt.process(file_path)).replace('\n', ' ')
            return self.text_processor(doc_text, file_path)

        elif Path(file_path).is_file() and Path(file_path).suffix == '.txt':
            print(f'[!] {Path(file_path).stem} is converting...\nStand by...')
            root.bell()
            with open(file_path, 'r', encoding='utf-8') as f:
                doc_text = f.read()
            doc_text = doc_text.replace('\n', ' ')
            return self.text_processor(doc_text, file_path)

        else:
            root.bell()
            return print('[!] File not found!')

    def clear_folder(self, path: str):
        folder = path
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)

            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason {e}')
        return print(f'Папка {folder} очищена')
