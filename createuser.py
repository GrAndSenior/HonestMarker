import userui
from PyQt5.QtWidgets import ( QApplication, QMainWindow,  QMessageBox, QLineEdit)
from PyQt5.QtCore import (QCoreApplication, QRect, Qt, QMetaObject)
from PyQt5.QtGui import QIcon
from cryptography.fernet import Fernet

class NewUser(QMainWindow, userui.Ui_CreateUserWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)  # Это для инициализации  дизайна

        style = '''
QPushButton {
	background-color: #6384ff;
	color: #fff;
	border: none;
	min-width: 30px;
	border-radius: 5px;
}

QPushButton::flat {
	background-color: transparent;
	border: none;
	color: #000;
	border-radius: 5px;
}

QPushButton::disabled {
	background-color: #c0c0c0;
	color: #959595;
	border: none;
	border-radius: 5px;
}

QPushButton::hover {
	background-color: #718fff;
	border: 2px solid #718fff;
	border-radius: 5px;
}

QPushButton::pressed {
	background-color: #446cff;
	border: 1px solid #446cff;
	border-radius: 5px;
}

QPushButton::checked {
	background-color: #3761ff;
	border: 1px solid #3761ff;
	border-radius: 5px;
}
'''
        self.btnSign.setFlat(True)
        self.btnCancel.setFlat(True)
        self.btnSign.setStyleSheet(style)
        self.btnCancel.setStyleSheet(style)
        self.setFixedSize(800, 450)
        self.setWindowIcon(QIcon('sources/img/icon.png'))
        self.lePassword.setEchoMode(QLineEdit.Password)  # Маскируем вводимые символы
        self.leConfirmPassword.setEchoMode(QLineEdit.Password)  # Маскируем вводимые символы

        self.setWindowTitle('Маркировка Datamatrix - Регистрация нового пользователя')
        self.setup_action()


    def setup_action(self):
        self.btnSign.clicked.connect(self.sign_click)
        self.btnCancel.clicked.connect(self.cancel_click)
        self.leLogin.textChanged.connect(self.change_password)
        
    def cancel_click(self):
        self.close()

    def change_password(self):
        self.lePassword.clear()
        self.leConfirmPassword.clear()

    def showMessageBox(self, title, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()

    def is_correct_data(self):
        import re
        return self.lePassword.text() == self.leConfirmPassword.text() and bool(re.match(r'[\w]', self.leLogin.text())) and self.leLogin.text().lower() !='root' and len(self.lePassword.text()>0)

    def sign_click(self):
        if self.is_correct_data():
            from configparser import ConfigParser
            cfg = ConfigParser()
            cfg.read('options.ini')
            strong = 'btsbrest'
            key = f"{strong}{cfg.get('MAIN','key')}"   # загрузка ключа из внешнего источника
            cipher = Fernet(key)
            level = 1 if self.cbAdmin.isChecked() else 2
            self.parent.cursor.execute(f'SELECT id_manager FROM MANAGER WHERE MANAGER.login = "{self.leLogin.text().lower()}";')
            result = self.parent.cursor.fetchall()
            encrypted_password = cipher.encrypt(self.lePassword.text().encode()).decode()

            if len(result) == 0:    # Пользователь не существует - добавляем запись.
                query = f"INSERT INTO MANAGER (NAME, LOGIN, PASSWORD, STATE, LEVEL, PROFILE) VALUES ('{self.leName.text()}', '{self.leLogin.text().lower()}',{encrypted_password}, 1, {level}, '{self.leProfile.text()}');"
                self.parent.cursor.execute(query)
                self.parent.mydb.commit()
                #print(encrypted_password)
                #encrypted_password = cipher.decrypt(encrypted_password).decode()
                #print(encrypted_password)
            else:                   # Пользователь существует - изменям запись.
                query = f"UPDATE MANAGER SET NAME = '{self.leName.text()}', LOGIN = '{self.leLogin.text().lower()}', PASSWORD = '{encrypted_password}', STATE = 1, LEVEL = {level}, PROFILE = '{self.leProfile.text()}' WHERE id_manager = {result[0][0]};"
                self.parent.cursor.execute(query)
                self.parent.mydb.commit()
            self.close()

        else:
            self.showMessageBox('Ошибка', 'Введены некорректные данные')
