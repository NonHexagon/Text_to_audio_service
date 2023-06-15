import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from test_data import posFiles, neFiles, uploader_test_data, demo_test_data, login_data, logout_data

import pytest

file_name = posFiles
base_url = 'http://127.0.0.1:5000/'


@pytest.fixture()
def UploadFiles(file_name: str, base_url: str) -> tuple:
    driver = webdriver.Edge()
    driver.get('http://localhost:5000/login')
    driver.fullscreen_window()
    login_data_1 = driver.find_element(By.XPATH, '//*[@id="email"]')
    login_data_2 = driver.find_element(By.XPATH, '//*[@id="tmp_passwd"]')
    login_data_1.send_keys('mister22898@mail.ru')
    login_data_2.send_keys('DKylpOwi')
    button_4 = driver.find_element(By.XPATH, '/html/body/section/form/input[3]')
    driver.execute_script("arguments[0].click();", button_4)
    file = {'file': open(f'{file_name}', 'rb')}
    response = requests.post(base_url + '/uploader', files=file)
    filename = file_name.split('.')[0]
    status = response.status_code
    print(status, filename)
    if status == 200:
        with open(f'conv_results/{filename}.mp3', 'wb') as f:
            f.write(response.content)
    pheader = response.headers
    print(pheader)
    content_type = pheader['Content-Type']
    file_size = pheader['Content-Length']
    return status, content_type


@pytest.mark.parametrize('file_name, base_url, result', uploader_test_data)
def test_upload_file(file_name, base_url, result, UploadFiles):
    assert UploadFiles == result


@pytest.fixture()
def uploaderConnection() -> int:
    response = requests.get(base_url + '/uploader')
    return response.status_code


def test_uploaderConnection(uploaderConnection):
    assert uploaderConnection != 0 and uploaderConnection == 200


@pytest.fixture()
def main_pageConnection() -> int:
    response = requests.get(base_url)
    return response.status_code


def test_main_pageConnection(main_pageConnection):
    assert main_pageConnection != 0 and main_pageConnection == 200


@pytest.fixture()
def aboutConnection() -> int:
    response = requests.get(base_url + '/about')
    return response.status_code


def test_aboutConnection(aboutConnection):
    assert aboutConnection != 0 and aboutConnection == 200


@pytest.fixture()
def settingConnection() -> int:
    response = requests.get(base_url + '/settings')
    return response.status_code


def test_settingsConnection(settingConnection):
    assert settingConnection != 0 and settingConnection == 200


@pytest.fixture()
def guideConnection() -> int:
    response = requests.get(base_url + '/guide')
    return response.status_code


def test_guideConnection(guideConnection):
    assert guideConnection != 0 and guideConnection == 200


@pytest.fixture()
def demo(text_to_convert: str) -> bool:
    driver = webdriver.Edge()
    driver.get('http://localhost:5000/textloader')
    driver.fullscreen_window()
    input_text = driver.find_element(By.XPATH, '//*[@id="inp_text"]')
    sent_text = text_to_convert
    input_text.send_keys(sent_text)
    button_2 = driver.find_element(By.XPATH, '/html/body/section/div[2]/form/input')
    driver.execute_script("arguments[0].click();", button_2)
    file_list = os.listdir('C:/Users/miste/Downloads/Text_to_Audio/files')
    if len(file_list) > 0:
        if file_list[0].startswith('Text_to_audio'):
            return True
        else:
            return False
    else:
        return False


@pytest.mark.parametrize('text_to_convert, result', demo_test_data)
def test_demo(text_to_convert, result, demo):
    assert demo == result


@pytest.fixture()
def loggin(login: str, passwd: str) -> str:
    driver = webdriver.Edge()
    driver.get('http://localhost:5000/login')
    driver.fullscreen_window()
    login_data_1 = driver.find_element(By.XPATH, '//*[@id="email"]')
    login_data_2 = driver.find_element(By.XPATH, '//*[@id="tmp_passwd"]')
    login_data_1.send_keys(login)
    login_data_2.send_keys(passwd)
    button_3 = driver.find_element(By.XPATH, '/html/body/section/form/input[3]')
    driver.execute_script("arguments[0].click();", button_3)
    current_link = driver.current_url
    current_link = current_link.split('/')
    return current_link[-1]


@pytest.mark.parametrize('login, passwd, result', login_data)
def test_loggin(login, passwd, result, loggin):
    assert loggin == result and requests.get('http://localhost:5000/'+loggin).status_code == 200


@pytest.fixture()
def logout(login: str, passwd: str) -> str:
    driver = webdriver.Edge()
    driver.get('http://localhost:5000/login')
    driver.fullscreen_window()
    login_data_1 = driver.find_element(By.XPATH, '//*[@id="email"]')
    login_data_2 = driver.find_element(By.XPATH, '//*[@id="tmp_passwd"]')
    login_data_1.send_keys(login)
    login_data_2.send_keys(passwd)
    button_4 = driver.find_element(By.XPATH, '/html/body/section/form/input[3]')
    driver.execute_script("arguments[0].click();", button_4)
    driver.get('http://localhost:5000/account')
    logout_button = driver.find_element(By.XPATH, '//*[@id="logout"]')
    driver.execute_script("arguments[0].click();", logout_button)
    current_link = driver.current_url
    current_link = current_link.split('/')
    return current_link[-1]


@pytest.mark.parametrize('login, passwd, result', logout_data)
def test_logout(login, passwd, result, logout):
    assert logout == result and requests.get('http://localhost:5000/'+logout).status_code == 200
