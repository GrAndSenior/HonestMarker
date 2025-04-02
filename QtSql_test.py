from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QTableView, QWidget, QGridLayout, QPushButton, QComboBox,
QFileDialog, QMessageBox, QMenu)
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery, QSqlRecord
 
class View(QWidget):
    def __init__(self):
        super().__init__()
        self.dbname = ''
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.view = QTableView()
        self.view.horizontalHeader().setSectionResizeMode(1)
        self.btnOpen = QPushButton('Открыть базу данных')
        self.btnOpen.clicked.connect(self.open_db)
        self.box = QComboBox()
        self.box.currentIndexChanged.connect(self.on_index)
        grid = QGridLayout(self)
        grid.setContentsMargins(0,0,0,0)
        grid.addWidget(self.view,0,0,4,4)
        grid.addWidget(self.box,4,0,1,1)
        grid.addWidget(self.btnOpen,4,1,1,1)
        self.model = QSqlTableModel()
        #self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.setEditStrategy(QSqlTableModel.OnRowChange)
 
    def open_db(self):
        dbname,_ = QFileDialog.getOpenFileName(self,'Открыть базу данных',self.dbname,'*.db *.sqlite')
        if not dbname: return
        self.dbname = dbname
        self.db.setDatabaseName(self.dbname)
        if not(self.db.open()):
            QMessageBox.critical(self,"",self.db.lastError().text())
            return
        self.box.clear()
        self.box.addItems(self.db.tables())
    
    def on_index(self):
        table = self.box.currentText()
        self.model.setTable(table)
        if table == 'tbl':
            self.model.setHeaderData(0, Qt.Horizontal, "Вопрос")
            self.model.setHeaderData(1, Qt.Horizontal, "Ответ")
        self.view.setModel(self.model)
        self.model.select()
 
    def contextMenuEvent(self,event):
        pos = self.view.mapToGlobal(event.pos())
        mnu = QMenu()
        mnu.addAction('Open DB').setObjectName('open')
        mnu.addAction('Add record').setObjectName('add')
        mnu.addAction('Delete record').setObjectName('del')
        mnu.addAction('Submit all').setObjectName('submit')
        ret = mnu.exec_(pos)
        if not ret: 
            return
        obj = ret.objectName()
        if obj == 'open':
            self.open_db()
        if obj == 'add':
            row = self.model.rowCount()
            self.model.insertRow(row)
            self.model.setData(self.model.index(row,0),None)
            self.model.submit()
        elif obj == 'del':
            idx = self.view.currentIndex()
            self.model.removeRow(idx.row())
            self.model.submit()
        self.view.setCurrentIndex(self.model.index(-1,-1))
        self.model.select()
        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = View()
    w.resize(600,400)
    w.show()
    sys.exit(app.exec_())