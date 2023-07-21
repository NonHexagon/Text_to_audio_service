import threading
from DB_manager import change_passwd

print(f'Запушена функция сброса паролей пользователей')
runner = threading.Thread(target=change_passwd())
runner.start()
runner.join()
