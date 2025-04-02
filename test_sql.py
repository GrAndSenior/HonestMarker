import sys, os  # sys нужен для передачи argv в QApplication
import mysql.connector
import pandas as pd
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QAbstractTableModel, Qt
os.system('pyuic5 sqlview.ui -o sqlview.py')

import sqlview
from pandasmodel import PandasModel

from treepoem import generate_barcode
from PIL import Image, ImageDraw, ImageFont

#from pylibdmtx.pylibdmtx import encode

#from ppf.datamatrix import DataMatrix
#from stickerdm import Stickerdm

#GS1 = chr(29)
GS1 = ''



#zlabel = Stickerdm(170,100,0,5,'ECC 200')#+++++++++++++++++++++++
#zlabel.make_label('0100000075013769215sGfqg893Gtjk')#+++++++++++++++++++++++
#zlabel.store_graphic('logo','logo.pcx')#+++++++++++++++++++++++
#zlabel.print_label()   #+++++++++++++++++++++++


#1 - Подставляются FNC1 вместо GS1
#def generate_and_print(gtin, serial_number, code):


def generate_and_print(gs1dm):
    # Generate datamatrix
    datamatrix = generate_barcode(
        barcode_type='datamatrix',
        data=f"^FNC1{gs1dm}",
        options={"parsefnc": True, "parse": True, "format": "square", "version": "26x26", "includetext": True})
    

    # 
    #datamatrix = generate_barcode(
    #    barcode_type='gs1datamatrix',
    #    data=f"(01){gtin}(21){serial_number}(93){code}",
    #    options={"parsefnc": True, "parse": True, "format": "square", "version": "26x26", "includetext": True})
    
    # Resize datamatrix to desired size
    dm_size_px = (160, 160)
    datamatrix = datamatrix.resize(dm_size_px, Image.NEAREST)

    # Create white picture  
    picture_size_px = (200, 200)
    picture = Image.new('L', picture_size_px, color='white')

    # Position the datamatrix
    barcode_position_px = (20, 5)
    picture.paste(datamatrix, barcode_position_px)

    # Draw picture for placing texts on it
    draw = ImageDraw.Draw(picture)

    # Store font for the texts
    ocrb_font = ImageFont.truetype("sources/fonts/arialnb.ttf", 22)
    # Draw texts on the Picture
    #datamatrix_text_position_px = (10,15)
    #draw.text(datamatrix_text_position_px, "This is a GS1 DataMatrix", fill='black', font=ocrb_font)
    
    #+welcome_text_position_px = (50,170)
    #+draw.text(welcome_text_position_px, gs1dm[16:gs1dm.find('9')], fill='black', font=ocrb_font)


    # Save the image
    picture.save("datamatrix.png")
    picture.show()

gs1dm = '0104015576055091215zrMYgl931sf1'
'''
gtin = "00000075013769"
serial_number = "5sGfqg8"
code = "Gtjk"
fnc1 = chr(232)
print(fnc1)
from pystrich.datamatrix import DataMatrixEncoder #не добавляется лидирующий FNC1
encoder = DataMatrixEncoder("0108594053493695215m;g1wN93dDc3")

encoder.save( "pystrich_test.png" )
#print(encoder.get_ascii())
'''
#FNC1 = chr(232)
#FNC1 = FNC1.encode("utf-8")
#FNC1 = bytes.fromhex("E8").decode('utf-8')
code = '0108594053490441215n.WEs?93nmKB'.encode('utf-8')

#from pylibdmtx.pylibdmtx import encode
#encoded = encode((FNC1+code))
#img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
#img.save('dmtx.png')

generate_and_print(gs1dm)
###1 - End

class ExampleApp(QtWidgets.QMainWindow, sqlview.Ui_SqlView):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.setupAction()

        #for i in range(self.model.columnCount()):
        #    self.comboBox.addItem(self.model.headerData(i, Qt.Horizontal))

    def setupAction(self):
        self.btnClose.clicked.connect(self.closeAction)
        self.btnRun.clicked.connect(self.runAction)
        self.tvSql.doubleClicked.connect(self.onItemDoubleClick)

    def onItemDoubleClick(self):
        current_index = self.tvSql.currentIndex().row()  #  Индекс выделенной ячейки
        current_row = self.data_frame.iloc[current_index]['NUMBER']  # Номер выбранного заказа
        
        print(current_row)

    def closeAction(self):
        self.close()
    
    def runAction(self):
        if self.sqlConnect():
            '''
            con = QSqlDatabase.addDatabase('QSQLITE')
            con.setHostName('10.144.10.75')
            con.setDatabaseName('dbmarking')
            con.setUserName('btsdba')
            con.setPassword('masterkey')
            con.open()
            newquery = QSqlQuery()
            newquery.exec(  
                'SELECT * FROM dbmarking.ORDERS;
                '
            )
            
            '''






            query = '''
                SELECT ORDERS.NUMBER, CUSTOMER.SHORT_NAME, ORDERS.DATE_ON, ORDERS.DATE_OUT, 
                       ORDER_STATE.STATE, MANAGER.NAME
                FROM dbmarking.ORDERS
                INNER JOIN CUSTOMER 
                    ON ORDERS.id_customer = CUSTOMER.id_customer
                INNER JOIN ORDER_STATE
                    ON ORDERS.id_state = ORDER_STATE.id_state
                INNER JOIN MANAGER 
                    ON ORDERS.id_manager = MANAGER.id_manager
            '''
            #query += '''WHERE ORDERS.NUMBER = '00002' '''
            query += ';'

            self.data_frame = pd.read_sql_query(query, self.mydb)
            self.data_frame = self.data_frame.fillna('')
            print(self.data_frame)

            self.model = PandasModel(self.data_frame)
            self.tvSql.setModel(self.model)
            self.tvSql.show()

            ''' ### Рабочий фрагмент
            self.cursor = self.mydb.cursor()
            self.cursor.execute(query)
            self.result = self.cursor.fetchall()
            self.model = QStandardItemModel()
            for row in self.result:
                line = []
                for item in row:
                    line.append(QStandardItem(str(item)))
                self.model.appendRow(line)

            #self.model.setEditTriger(0)
            self.model.setHeaderData(0, QtCore.Qt.Horizontal, "Номер заказа")
            self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Контрагент")
            self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Дата оформления")    
            self.model.setHeaderData(3, QtCore.Qt.Horizontal, "Дата завершения")    
            self.model.setHeaderData(4, QtCore.Qt.Horizontal, "Статус заказа")    
            self.model.setHeaderData(5, QtCore.Qt.Horizontal, "Менеджер")
            '''
            #self.tvSql.view.vericalHeader().hide()
            self.tvSql.setModel(self.model)

            self.tvSql.resizeColumnsToContents()
            
            FNC1 = chr(232)
            #FNC1 = FNC1.encode("utf-8")
            #FNC1 = bytes.fromhex("E8").decode('utf-8')

            
            gs1dm = '\\F0105411858000138215!*DvTG93LswN'
            encoder = DataMatrixEncoder('0105411858000138215!*DvTG93LswN')
            encoder.save('tmp.png')
            with Image.open('tmp.png') as encoder:
                encoder.load()
            encoder.show()

    def sqlConnect(self):
        try:
            self.mydb = mysql.connector.connect(
                host='10.144.10.75',
                user="btsdba",
                password="masterkey",
                database="dbmarking"
                )
            #QtWidgets.QMessageBox.information(None, "App - Ok!", "Ok")
            print('Ok')


            return True
        except self.mydb.Error as e:
            print(e)
            QtWidgets.QMessageBox.critical(None, "App Name - Error!", f"Database Error: {e}")
            return False
        #finally:
        #    if self.mydb:
        #        self.mydb.close()


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()