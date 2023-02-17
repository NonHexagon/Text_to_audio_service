import pytest
import os
base_url = 'http://127.0.0.1:5000/'


posFiles = [
    ('posTest.docx', base_url),
    ('posTest_Ru.docx', base_url),
    ('posTest.pdf', base_url),
    ('posTestEn.pdf', base_url)
]

neFiles = (
    pytest.param('neTest_dif.pdf', marks=pytest.mark.xfail(reason='Набор символов, который сложно интерпритировать')),
    pytest.param('neTest.txt', marks=pytest.mark.xfail(reason='Не поддерживаемый формат файла')),
    pytest.param('neTest.jpg', marks=pytest.mark.xfail(reason='Не поддерживаемый формат файла'))
)
file_size_1 = os.path.getsize('C:\\Users\\miste\\Downloads\\Text_to_Audio\\files\\posTest.mp3')
file_size_2 = os.path.getsize('C:\\Users\\miste\\Downloads\\Text_to_Audio\\files\\posTest_Ru.mp3')
file_size_3 = os.path.getsize('C:\\Users\\miste\\Downloads\\Text_to_Audio\\files\\neTest_dif.mp3')
file_size_4 = os.path.getsize('C:\\Users\\miste\\Downloads\\Text_to_Audio\\files\\posTestEn.mp3')
uploader_test_data = [('posTest.docx', base_url, (200, f'{file_size_1}', 'attachment; filename=posTest.mp3', 'audio/mpeg')), ('posTest_Ru.docx', base_url, (200, f'{file_size_2}', 'attachment; filename=posTest_Ru.mp3', 'audio/mpeg')), ('posTestEn.pdf', base_url, (200, f'{file_size_4}', 'attachment; filename=posTestEn.mp3', 'audio/mpeg'))]

