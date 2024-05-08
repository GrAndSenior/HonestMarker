def convert_Ui():
    os.system('pyuic5 design.ui -o design.py')
    os.system('pyuic5 layoutui.ui -o layoutui.py')
    os.system('pyuic5 zebraui.ui -o zebraui.py')
    os.system('pyuic5 orders.ui -o orders.py')
    os.system('pyuic5 goods.ui -o goods.py')
    os.system('pyuic5 settings.ui -o settings.py')
    os.system('pyuic5 pdfimport.ui -o pdfimport.py')


#copyright 'Maan Icons', 'Us and Up', 'Freepik', 'flatart_icons', 'Uniconlabs', 'srip', 'pictranoosa', 'Slamlabs', 'edt.im', 'Eklip Studio', 'zafdesign'
import os, sys, mysql.connector
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


#convert_Ui()


from PyQt5.QtWidgets import (QMainWindow, QWidget, QProgressBar, QApplication, QMessageBox, QFileDialog, QSplashScreen)
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QPixmap
import design, settings
from options import Options
from order import Order
from datetime import datetime
from zebra import Zebra
from pandasmodel import PandasModel
import platform

### ^[0][1][0-9]{14}[2][1][^]{7}[9][3]\S{4}$   - пример валидатора

#from glob import glob
#FNC1 = chr(232)
#FNC1 = FNC1.encode("utf-8")
#FNC1 = bytes.fromhex("E8").decode('utf-8')
GS1 = chr(29)

class MarkApplication(QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это для инициализации  дизайна
        self.gbReserve.hide()
        self.options = Options().read_config()
        if self.options['MAIN']['theme'].lower() == 'dark':
            f = open('sources/dark.qss', 'r')
        else:
            f = open('sources/light.qss', 'r')
        self.styleData = f.read()
        f.close()
        self.setStyleSheet(self.styleData)

        self.setWindowTitle('Маркировка Datamatrix - v0.4')
        #self.setWindowIcon(QIcon('sources/img/main.png'))
        #self.resize(1440, 900)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0,100)
        self.statusBar().addPermanentWidget(self.progress_bar)
        self.progress_bar.hide()
        if self.sqlConnect():
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
            QMessageBox.information(None, "Внимание!", f"Не выбран заказ для просмотра")

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

    def sqlConnect(self):
        try:
            self.mydb = mysql.connector.connect(
                host='10.144.10.75',
                user="btsdba",
                password="masterkey",
                database="dbmarking"
                )
            self.statusBar().showMessage(f'Соединение с сервером MySQL установлено', 5000)
            return True
        except mysql.connector.Error as e:
            self.statusBar().showMessage(f'Соединение с сервером MySQL не установлено по причине: {e}', 0)
            return False

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
            QMessageBox.information(None, "App - Ok!", "Ok")
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

def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    if (datetime.now() < datetime(2024,5,31)) and (platform.uname().node[0]=='1'):
        splash = QSplashScreen()
        splash.setPixmap(QPixmap('sources/img/splash.png'))
        splash.show()
        if os.path.exists('sources/message.html'):
            f = open('sources/message.html', 'r', encoding='utf-8')
            message = f.read()
            f.close()
            splash.showMessage(message, Qt.AlignTop | Qt.AlignHCenter, Qt.white)    
        QThread.msleep(2000)   # 

        window = MarkApplication()     # Создаём объект класса ExampleApp
        #window.show()                 # Показываем окно
        window.onAddOrderClick()       # Пропустить подключение к базе данных

        splash.finish(window)
        sys.exit(app.exec_())          # и запускаем приложение

if __name__ == "__main__":
    main()

#QtWidgets.QMessageBox.information(None, "App - Ok!", "Ok")
#QtWidgets.QMessageBox.critical(None, "App Name - Error!", f"Database Error: {e}")
