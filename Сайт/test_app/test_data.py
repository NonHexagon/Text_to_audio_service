import pytest
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
uploader_test_data = [('posTest.docx', base_url, (200,  'text/html; charset=utf-8')),
                      ('posTest_Ru.docx', base_url, (200, 'text/html; charset=utf-8')),
                      ('posTestEn.pdf', base_url, (200,  'text/html; charset=utf-8'))]

demo_test_data = [('No more defending the lie behind a never-ending war', (True)),
                  ('Вася - Хороший человек, но на пары не ходит', (True)),
                  ('', (False))]

login_data = [('mister22898@mail.ru', 'NiRBbl8Y', 'uploader'),
              ('201932@edu.fa.ru', 'gWb5lbhn', 'uploader'),
              ('fakeemail@mail.ru', '23453212', 'register')]

logout_data = [('mister22898@mail.ru', 'NiRBbl8Y', 'main'),
               ('201932@edu.fa.ru', 'gWb5lbhn', 'main')]

