from random import choices
from cryptography.fernet import Fernet
from configparser import ConfigParser

cfg = ConfigParser()
cfg.read('options.ini')

# Ключ для шифрования
# key = Fernet.generate_key() # Генерация случайного ключа
strong = 'btsbrest'
key = f"{strong}{cfg.get('MAIN','key')[::-1]}"   # загрузка ключа из внешнего источника



#key = f"{strong}m8W7cDnxBTcIBhIEmQ1NihgjH9fzeou4K_0="   

alphabet = '~!@#$%^&*()_+=-0123456789QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
cipher = Fernet(key)

def add_digits(input_string):
    new_string = ''
    for char in input_string:
        random_digits = ''.join(choices(alphabet, k=4))
        new_string += random_digits + char
    return new_string

#  Дешифровка пароля
#cod = 'gAAAAABm1Vyx2TzSwRi0aoFzR8SS6LabzlPdmtnNCrnDrpT_6aGx0TU0hhJY4Ytt42yzwKv-z-M7wCk-TLrIkBXexlQVE4CGwg=='
#s = cipher.decrypt(cod).decode()
#print(s)

# # Шифрование пароля
#password = 'masterkey'
#s = cipher.encrypt(password.encode()).decode()
#print(s)

input_string = input("Введите дату(год, месяц и день): ")
input_string += input("Введите имя компьютера: ").lower()
combined_string = add_digits(input_string)

# Шифрование содержимого файла
encrypted_data = cipher.encrypt(combined_string.encode())

with open("license.pem", 'wb') as file:
    file.write(encrypted_data)

# 108-ws-12557      \\108-ws-12557\D$\output\
# 173-ws-00150      \\173-ws-00150\d$\Install\Markirovka\
# 108-WS-00002









