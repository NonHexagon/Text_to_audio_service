with open('keys.txt', 'r', encoding='utf-8') as file:
    lines = file.read()
_mail = lines.split(' ')[0]
_passwd = lines.split(' ')[-1]
