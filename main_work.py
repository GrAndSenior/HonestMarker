def convert_Ui():
    os.system('pyuic5 design.ui -o design.py')
    os.system('pyuic5 layoutui.ui -o layoutui.py')
    os.system('pyuic5 zebraui.ui -o zebraui.py')
    os.system('pyuic5 orders.ui -o orders.py')
    os.system('pyuic5 goods.ui -o goods.py')
    os.system('pyuic5 settings.ui -o settings.py')
    os.system('pyuic5 pdfimport.ui -o pdfimport.py')
    os.system('pyuic5 login.ui -o loginwindow.py')
    os.system('pyuic5 userui.ui -o userui.py')

#copyright 'Maan Icons', 'Us and Up', 'Freepik', 'flatart_icons', 'Uniconlabs', 'srip', 'pictranoosa', 'Slamlabs', 'edt.im', 'Eklip Studio', 'zafdesign'
import os, sys, pyodbc , mysql.connector
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

#convert_Ui()
from PyQt5 import QtSql
from PyQt5.QtWidgets import ( QApplication, QMainWindow, QWidget, QProgressBar, QMessageBox, QFileDialog, QSplashScreen, QLineEdit)
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtSql import *
import design, settings, loginwindow
from configparser import ConfigParser
from options import Options
from order import Order
from datetime import datetime
from zebra import Zebra
from pandasmodel import PandasModel
import platform
from cryptography.fernet import Fernet
'''
0104640255340450215TE?nHX93JWuY
"01046402553404502155=l<*N\u001D93JW0J"
'''
### ^[0][1][0-9]{14}[2][1][^]{7}[9][3]\S{4}$   - пример валидатора

#from glob import glob
#FNC1 = chr(232)
#FNC1 = FNC1.encode("utf-8")
#FNC1 = bytes.fromhex("E8").decode('utf-8')
GS1 = chr(29)

class MarkApplication(QMainWindow, design.Ui_MainWindow):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)  # Это для инициализации  дизайна
        self.gbReserve.hide()

        self.mydb = parent.mydb 
        self.options = Options().read_config()
        if self.options['MAIN']['theme'].lower() == 'dark':
            f = open('sources/dark.qss', 'r')
        else:
            f = open('sources/light.qss', 'r')
        self.styleData = f.read()
        f.close()
        self.setStyleSheet(self.styleData)

        self.setWindowTitle('Маркировка Datamatrix - HonestMarker v1.0')
        #self.setWindowIcon(QIcon('sources/img/main.png'))
        #self.resize(1440, 900)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0,100)
        self.statusBar().addPermanentWidget(self.progress_bar)
        self.progress_bar.hide()
        #if self.sqlConnect():
        if self.mydb != None:
            query = '''
                SELECT  ORDERS.NUMBER, 
                        CUSTOMER.SHORT_NAME, 
                        ORDERS.DATE_ON, 
                        ORDERS.DATE_OUT, 
                        ORDER_STATE.STATE, 
                        MANAGER.NAME
                FROM dbmarking.ORDERS
                INNER JOIN CUSTOMER 
                    ON ORDERS.id_customer = CUSTOMER.id_customer
                INNER JOIN ORDER_STATE
                    ON ORDERS.id_state = ORDER_STATE.id_state
                INNER JOIN MANAGER 
                    ON ORDERS.id_manager = MANAGER.id_manager;
            '''
            self.headers = {'NUMBER' : 'Номер заказа', 
                            'SHORT_NAME' : 'Контрагент', 
                            'DATE_ON' : 'Дата оформления', 
                            'DATE_OUT' : 'Дата завершения', 
                            'STATE' : 'Статус заказа',
                            'NAME' : 'Менеджер'}
            self.show_query_result(query)


        self.btnAddOrder.clicked.connect(self.onAddOrderClick)
        self.btnSettings.clicked.connect(self.onSettingsClick)
        self.tView.doubleClicked.connect(self.on_cell_item_dblclicked)
        self.btnOpenOrder.clicked.connect(self.on_cell_item_dblclicked)

        '''self.tCodes.cellClicked.connect(self.getClickedCell)
        self.cbPrinter.currentTextChanged.connect(self.changePrinter)
        self.cbThemes.currentTextChanged.connect(self.changeThemes)
        self.tCodes.itemDoubleClicked.connect(self.on_cell_item_clicked)
        '''
    
    def get_orderstate(self, item):
        sql = 'SELECT STATE FROM dbmarking.ORDER_STATE;'
        cursor = self.mydb.cursor()
        cursor.execute(sql)
        try:
            return list(map(lambda x: x[0], cursor.fetchall())).index(item)
        except:
            return -1

    def on_cell_item_dblclicked(self, item):
        if self.tView.currentIndex().row()>=0:        # Индекс выделенной ячейки
            order_number = self.data_frame.iloc[self.tView.currentIndex().row(),0]  # Номер выбранного заказа
            row = list(self.data_frame.iloc[self.tView.currentIndex().row()])
            self.orderWindow = Order(self, number=row[0], 
                                      id_state=self.get_orderstate(row[4]), 
                                      customer=row[1], 
                                      manager=row[5],
                                      date_on=row[2])
            self.orderWindow.show()
        else:
            QMessageBox.information(self, "Внимание!", f"Не выбран заказ для просмотра")

    def onSettingsClick(self):
        self.settingsWindow = Settings(self)
        self.settingsWindow.show()

    def onAddOrderClick(self):
        self.orderWindow = Order(self, number='', id_state=-1, customer='', manager='', date_on=datetime.now())
        #self.orderWindow.show()               # Показ окна выбора заказов
        self.orderWindow.on_btnAddGoodclick()  # Пропустить показ окна выбора заказов

    def show_query_result(self, query):
        self.data_frame = pd.read_sql_query(query, self.mydb)
        self.data_frame = self.data_frame.fillna('')
        self.data_frame = self.data_frame.rename(columns={'NUMBER' : 'Номер заказа', 
                                                          'SHORT_NAME' : 'Контрагент', 
                                                          'DATE_ON' : 'Дата оформления', 
                                                          'DATE_OUT' : 'Дата завершения', 
                                                          'STATE' : 'Статус заказа',
                                                          'NAME' : 'Менеджер'})
        self.model = PandasModel(self.data_frame)
        self.tView.setModel(self.model)
        self.tView.resizeColumnsToContents()
        self.tView.show()


    def closeEvent(self, e):
        result = QMessageBox.question(self, "Подтверждение завершения работы...", 
                    "Вы действительно хотите завершить работу с программой?", 
                    QMessageBox.Yes | QMessageBox.No, 
                    QMessageBox.No)
        if result == QMessageBox.Yes:
            e.accept()
            QWidget.closeEvent(self, e)
        else:
            e.ignore()


class Settings(QMainWindow, settings.Ui_SettingsWindow):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.setupUi(self)  # Это для инициализации  дизайна
        self.parent = parent
        self.options = self.parent.options
        self.printer = Zebra()
        self.cbPrinter.addItems(self.printer.getqueues())
        self.cbPrinter.setCurrentIndex(0)
        self.printer.setqueue(self.cbPrinter.currentIndex())
        self.accept_actions()        

    def accept_actions(self):
        self.btnOk.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.reject)
        self.btnOpenFolder.clicked.connect(self.select_source)
        self.btnDefault.clicked.connect(self.default_click)
        self.btnTestConnection.clicked.connect(self.test_connection)
        self.cbPrinter.currentTextChanged.connect(self.on_changePrinter)
        self.cbThemes.currentTextChanged.connect(self.on_changeTheme)

    def accept(self):
        self.options['MAIN']['output'] = self.leOutPath.text() 
        self.options['MYSQL']['host'] = self.dbServer.text()
        if self.cbThemes.currentIndex() == 0:
            self.options['MAIN']['theme'] = 'dark'
        else:
            self.options['MAIN']['theme'] = 'light'
        self.options['MAIN']['printer'] = self.cbPrinter.currentText()
        self.parent.options = self.options
        self.close()
    
    def reject(self):
        self.close()

    def select_source(self):
        self.outpath = QFileDialog.getExistingDirectory(self,"Выбрать папку для сохранения изображений...",".")
        if self.outpath:
            self.leOutPath.setText(self.outpath)

    def default_click(self):
        self.cbThemes.setCurrentIndex(0)
        self.dbServer.setText('10.144.10.75')
        self.leOutPath.setText('')
        self.cbPrinter.setCurrentIndex(-1)
        #  Добавить настройки по умолчанию

    def test_connection(self):
        try:
            self.mydb = mysql.connector.connect(
                host=self.dbServer.text(),
                user="btsdba",
                password="masterkey",
                database="dbmarking")
            QMessageBox.information(self, "App - Ok!", "Ok")
            return True
        except:
            QMessageBox.critical(None, "Проверка соединения!", f"Ошибка соединения с базой данных")
            return False

    def on_changeTheme(self):
        if self.cbThemes.currentIndex() == 0:
            f = open(f'sources\\dark.qss', 'r')
        else:
            f = open(f'sources\\light.qss', 'r')
        self.styleData = f.read()
        f.close()
        self.setStyleSheet(self.styleData)
        self.parent.setStyleSheet(self.styleData)   

    def on_changePrinter(self):
        self.printer.setqueue(self.cbPrinter.currentIndex())

class DateProcessor():
    def __init__(self, filename, key):
        self.filename = filename
        self.current_datetime = datetime.now()
        #key = "m8W77bmMUEsJcDnxBTcIBhIEmQ1NihgjH9fzeou4K_0="
        self.cipher = Fernet(key)

        

    def read_date_from_file(self):
        if os.path.exists(os.path.abspath('license.pem')):
            with open(self.filename, 'rb') as file:
                data = file.read()
            # Расшифровка данных
            data = self.cipher.decrypt(data).decode()
            # Извлекаем дату из файла, предполагая, что каждый пятый символ - это число даты
            date_from_file = data[4::5]
            return date_from_file
        else:
            return '19000101'

    def process_date(self, date_string):
        # Извлекаем год, месяц, день и имя компьютера из строки
        try:
            year_from_file = int(date_string[:4])
            month_from_file = int(date_string[4:6])
            day_from_file = int(date_string[6:8])
            pc_from_file = date_string[8:]
            # Создаем объект datetime из полученных значений
            return datetime(year_from_file, month_from_file, day_from_file, 0, 0, 0), pc_from_file
        except:
            return datetime(1900, 1, 1, 0, 0, 0), ''

    def check_target_date(self):
        date_from_file = self.read_date_from_file()
        target_date_from_file, target_pc_from_file = self.process_date(date_from_file)
        # Явно преобразуем текущую дату в объект datetime
        current_datetime = datetime(self.current_datetime.year, self.current_datetime.month,
                                    self.current_datetime.day, 0, 0, 0)
        if current_datetime > target_date_from_file or (platform.uname().node.lower() != target_pc_from_file): #Добавить проверку текущего пользователя Брестскому филиалу
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Лицензия')
            msgBox.setText(f'Срок действия сертификата на использование\nпрограммы закончился {str(target_date_from_file.day).zfill(2)}.{str(target_date_from_file.month).zfill(2)}.{target_date_from_file.year}.\n\nОбратитесь к разработчику...')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec_()

            sys.exit()
        if int(str(target_date_from_file - current_datetime).split()[0].replace(':','')) <=5:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Лицензия')
            msgBox.setText(f'Срок действия сертификата на использование\nпрограммы заканчивается {str(target_date_from_file.day).zfill(2)}.{str(target_date_from_file.month).zfill(2)}.{target_date_from_file.year}.\n\nОбратитесь к разработчику...')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec_()

class LoginWindow(QMainWindow, loginwindow.Ui_LoginWindow):
    
    def __init__(self):
        self.cfg = ConfigParser()
        self.cfg.read('options.ini')
        strong = 'btsbrest'
        self.key = f"{strong}{self.cfg.get('MAIN','key')}"   # загрузка ключа из внешнего источника
        processor = DateProcessor(os.path.abspath('license.pem'), self.key)
        processor.check_target_date()

        self.cipher = Fernet(self.key)
        
        super().__init__()
        self.setupUi(self)  # Это для инициализации  дизайна

        self.setWindowIcon(QIcon('sources/img/icon.png'))
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
        self.cursor.execute(f"SELECT id_manager, STATE, PASSWORD FROM dbmarking.MANAGER WHERE LOGIN = '{login}';")
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
            splash = QSplashScreen()
            splash.setPixmap(QPixmap('sources/img/splash.png'))
            splash.show()
            if os.path.exists('sources/message.html'):
                message = ''
                with open('sources/message.html', 'r', encoding='utf-8') as f:
                    message = f.read()
                splash.showMessage(message, Qt.AlignBottom | Qt.AlignRight, Qt.white)    
            QThread.msleep(2000)   # 

            window = MarkApplication(self)      # Создаём объект класса ExampleApp
            #window.show()                      # Показываем окно
            window.onAddOrderClick()            # Пропустить подключение к базе данных
            splash.finish(window)
    
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
            '''print('DB connect...')
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
            
            self.mydb = mysql.connector.connect(
                                            host='10.144.10.75',
                                            user="btsdba",
                                            password="masterkey",
                                            port="3306",
                                            database="dbmarking"
                                            )
            # Проверяем успешность подключения
            self.cursor = self.mydb.cursor()
            print('Ok')
            self.statusBar().showMessage(f'Соединение с сервером MySQL установлено', 3000)
            print('Sql ok')
            return True
        except pyodbc.Error as e:
            print(e)
            self.mydb = None
            self.statusBar().showMessage(f'Соединение с сервером MySQL не установлено.({e})', 0)
            return False

def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    loginwindow = LoginWindow()
    loginwindow.show()
    sys.exit(app.exec_())          # и запускаем приложение


if __name__ == "__main__":
    main()

#QtWidgets.QMessageBox.information(self, "App - Ok!", "Ok")
#QtWidgets.QMessageBox.critical(None, "App Name - Error!", f"Database Error: {e}")
