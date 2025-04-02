import os, sys, mysql.connector, pyodbc, pymysql
from PyQt5.QtWidgets import ( QApplication, QMainWindow, QWidget, QProgressBar, QMessageBox, QFileDialog, QSplashScreen, QLineEdit)
import loginwindow

def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    loginwindow = LoginWindow()
    loginwindow.show()
    sys.exit(app.exec_())          # и запускаем приложение

class LoginWindow(QMainWindow, loginwindow.Ui_LoginWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это для инициализации  дизайна
        self.btnCreate.setEnabled(False)
        self.lePassword.setEchoMode(QLineEdit.Password)  # Маскируем вводимые символы

        self.setWindowTitle('Маркировка Datamatrix - Авторизация')
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0,100)
        self.statusBar().addPermanentWidget(self.progress_bar)
        self.progress_bar.hide()
        
        self.sqlConnect()
        self.setup_action()
        

                    


    def setup_action(self):
        self.btnSign.clicked.connect(self.sign_click)
        self.btnCancel.clicked.connect(self.cancel_click)
        self.leLogin.textChanged.connect(self.change_password)
        self.btnCreate.clicked.connect(self.sign_in)
        
    def sign_check(self, login, password):
        self.userid = -1
        
        #  загрузка ключа из внешнего источника
        #  зашифровать пароль    
        if len(login)*len(password) == 0:
            QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля.')
            return False
        #encrypted_password = self.cipher.decrypt(password).decode()
        result = None
            #connection.commit()
        #+++self.cursor.execute(f"SELECT id_manager, STATE, PASSWORD FROM dbmarking.MANAGER WHERE LOGIN = '{login}';")
        result = self.cursor.fetchone()
        if result == None:
            #self.cursor.execute(f"INSERT INTO logs (date, user_id, info) VALUES ('{datetime.today()}', '-1', 'Попытка входа с неверным логином или паролем');")
            #self.mydb.commit()
            self.showMessageBox('Ошибка', 'Неверное имя пользователя\nили пароль')
        elif result[1] and self.cipher.decrypt(result[2]).decode() == password:     
            #self.cursor.execute(f"INSERT INTO logs (date, user_id, info) VALUES ('{datetime.today()}', '{result[0]}', 'Начало сеанса');")
            #self.mydb.commit()
            self.userid = result[0]
            return True
        
        
        
        return False
        
    def sign_click(self):               
        if self.sign_check(self.leLogin.text(), self.lePassword.text()):
            self.close()
    
    def sign_in(self):
        if self.sign_check(self.leLogin.text(), self.lePassword.text()):
            from createuser import NewUser
            self.newuser = NewUser(self)
            self.newuser.show()

    def cancel_click(self):
        self.close()
        
    def change_password(self):
        self.lePassword.clear()
        self.btnCreate.setEnabled(self.leLogin.text().lower() == 'root')

    def showMessageBox(self, title, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()

    def sqlConnect(self):
        try:
            print('DB connect...')

            
            self.mydb = pymysql.connect(
                                            host='10.144.10.75',
                                            user="btsdba",
                                            password="masterkey",
                                            port=3306,
                                            database="dbmarking"
                                            )


            '''
            connection_string = "DRIVER={MySQL ODBC 9.2 ANSI Driver};"
            connection_string += "SERVER=10.144.10.75; DATABASE=dbmarking; UID=btsdba; PASSWORD=masterkey; CHARSET=cp1251"
            self.mydb = pyodbc.connect(connection_string, autocommit=True, unicode_results = True)
            '''
            
            ''' +++++++++++++++++++++++++++++++
            self.mydb = QtSql.QSqlDatabase.addDatabase("QMYSQL3")
            #con2.setHostName("10.144.10.75")
            self.mydb.setDatabaseName("DRIVER={MySQL ODBC 9.2 Unicode Driver}; SERVER=10.144.10.75;DATABASE=dbmarking; UID=btsdba; PASSWORD=masterkey;")
            self.mydb.open()
            if self.mydb.open():
                print("Успешное подключение к базе данных")
                query = QtSql.QSqlQuery()
                query.exec("SELECT * FROM DM")
                if query.isActive():
                    
                    query.first()
                    while query.isValid():
                        print(query.value(1))
                        query.next()
            else:
                # Выводим текст описания ошибки
                print(self.mydb.lastError().text())            
            '''
           
            '''
            self.mydb = mysql.connector.connect(
                                            host='10.144.10.75',
                                            user="btsdba",
                                            password="masterkey",
                                            port="3306",
                                            database="dbmarking"
                                            )
            print('Ok')
            # Проверяем успешность подключения
            self.cursor = self.mydb.cursor()
            self.statusBar().showMessage(f'Соединение с сервером MySQL установлено', 3000)
            '''
            print('Sql ok')
            return True
        except Exception as e:
            print(e)
            self.mydb = None
            self.statusBar().showMessage(f'Соединение с сервером MySQL не установлено.({e})', 0)
            return False

if __name__ == "__main__":
    main()