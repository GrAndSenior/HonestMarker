from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import QDate
import orders
import pandas as pd
from datetime import datetime
from good import Good
from pandasmodel import PandasModel



class Order(QMainWindow, orders.Ui_OrderWindow):
    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent)
        self.setupUi(self)  # Это для инициализации  дизайна
        self.parent = parent
        self.options = parent.options

        self.mydb = parent.mydb
        for key, value in kwargs.items():
            if key == 'number':
                self.number = value
                if value != '':
                    self.setWindowTitle('Маркировка Datamatrix - информация о заказе')
                else:
                    self.setWindowTitle('Маркировка Datamatrix - добавление заказа')
            elif key == 'customer':
                self.customer = value
            elif key == 'id_state':
                self.id_state = value
            elif key == 'date_on':
                if isinstance(value, str):
                    self.date_on = QDate.fromString(value, "dd.MM.yyyy")
                else:
                    self.date_on = value
            elif key == 'manager':
                self.manager = value
        self.setWidgetData()


        self.accept_actions()


    def accept_actions(self):
        self.btnOk.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.reject)
        self.btnAddGood.clicked.connect(self.on_btnAddGoodclick)
        self.btnDelGood.clicked.connect(self.on_btnDelGoodclick)
        self.btnViewGood.clicked.connect(self.on_btnViewGoodclick)
        self.btnReport.clicked.connect(self.on_btnReportclick)
        self.tvGoods.doubleClicked.connect(self.on_btnViewGoodclick)

    def setWidgetData(self):
        self.leOrderNumber.setText(self.number)
        self.leCustomer.setText(self.customer)
        self.leManager.setText(self.manager)
        self.deDateOn.setDate(self.date_on)
        self.cbOrderState.setCurrentIndex(self.id_state)

        sql = 'SELECT STATE FROM ORDER_STATE;'
        self.cbOrderState.addItems(pd.read_sql_query(sql, self.parent.mydb)['STATE'].tolist())
        self.cbOrderState.setCurrentIndex(self.id_state)
        '''
        sql = 'SELECT STATE FROM ORDER_STATE;'
        self.cursor = self.parent.mydb.cursor()
        self.cursor.execute(sql)
        self.result = self.cursor.fetchall()
        for t in self.result:
            self.cbOrderState.addItem(t[0])
        self.cbOrderState.setCurrentIndex(self.id_state)
        '''
        if self.number == '':
            self.number = 'Error'
        sql = ''' 
                SELECT GOODS.NAME, CATEGORY.SHORT_NAME
                FROM DM
                INNER JOIN GOODS ON DM.GOODS = GOODS.id_goods
                INNER JOIN CATEGORY ON GOODS.CATEGORY = CATEGORY.id_category
                WHERE DM.ORDERS = "''' + self.number +'";'
        self.data_frame = pd.read_sql_query(sql, self.parent.mydb)
        self.data_frame = self.data_frame.fillna(' ')
        self.data_frame = self.data_frame.rename(columns={'NAME' : 'Наименование товара', 
                                                          'SHORT_NAME' : 'Категория товара'})
        self.model = PandasModel(self.data_frame)
        self.tvGoods.setModel(self.model)
        self.tvGoods.resizeColumnsToContents()
        self.tvGoods.show()




    def accept(self):
        self.close()

    def reject(self):
        # - не предполагает изменения в БД
        self.close()

    def on_btnAddGoodclick(self):
        #row = self.data_frame.iloc[self.tvGoods.currentIndex().row()].tolist()
        #sql = '''SELECT id_category FROM dbmarking.CATEGORY WHERE SHORT_NAME = "Error";'''
        self.goodsWindow = Good(self, number='', 
                                      id_state=-1, 
                                      customer='', 
                                      manager='',
                                      date_on=datetime.now(),
                                      good = '',
                                      category = -1)

        '''
        self.goodsWindow = Good(self, number=self.leOrderNumber.text(), 
                                      id_state=self.cbOrderState.currentIndex(), 
                                      customer=self.leCustomer.text(), 
                                      manager=self.leManager.text(),
                                      date_on=self.deDateOn().currentText(),
                                      good = '',
                                      category = -1)
        ''' 
        self.goodsWindow.show()   

    def on_btnDelGoodclick(self):
        pass

    def on_btnViewGoodclick(self):
        if self.tvGoods.currentIndex().row()>=0:
            row = self.data_frame.iloc[self.tvGoods.currentIndex().row()].tolist()
            sql = '''SELECT id_category FROM CATEGORY WHERE SHORT_NAME = "''' + row[1] +'";'
            
            self.goodsWindow = Good(self, number=self.leOrderNumber.text(), 
                                      id_state=self.cbOrderState.currentIndex(), 
                                      customer=self.leCustomer.text(), 
                                      manager=self.leManager.text(),
                                      date_on=self.deDateOn.date(),
                                      good = row[0],
                                      category = int(pd.read_sql_query(sql, self.parent.mydb).iloc[0]))
            self.goodsWindow.show()
        else:
            QMessageBox.information(self, "Внимание!", f"Не выбран товар для просмотра")

    def on_btnReportclick(self):
        pass
