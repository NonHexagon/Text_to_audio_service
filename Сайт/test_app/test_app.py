import requests
import os
from test_data import posFiles, neFiles, uploader_test_data

import pytest

file_name = posFiles
base_url = 'http://127.0.0.1:5000/'

@pytest.fixture()
def UploadFiles(file_name: str, base_url: str) -> tuple:
    file = {'file': open(f'{file_name}', 'rb')}
    response = requests.post(base_url + 'uploader', files=file)
    filename = file_name.split('.')[0]
    status = response.status_code
    if status == 200:
        with open(f'conv_results\{filename}.mp3', 'wb') as f:
            f.write(response.content)
    pheader = response.headers
    file_type = pheader['Content-Disposition']
    content_type = pheader['Content-Type']
    file_size = pheader['Content-Length']
    return status, file_size, file_type, content_type


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
