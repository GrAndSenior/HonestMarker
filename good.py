from PyQt5.QtWidgets import QMainWindow, QFileDialog, QProgressBar, QMenu, QMessageBox, QAction
from PyQt5.QtCore import QDate, Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
import goods
import pandas as pd
from pandasmodel import PandasModel
from pdfpreview import PdfPreview
from layoutdm import LayoutDM
from zplprinter import ZplPrinter
from time import time
from csv import QUOTE_NONE

class Good(QMainWindow, goods.Ui_GoodWindow):
    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent)
        self.setupUi(self)  # Это для инициализации  дизайна
        self.parent = parent
        self.options = parent.options
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0,100)
        self.statusBar().addPermanentWidget(self.progress_bar)
        self.progress_bar.hide()
        self.gbK.hide()
        self.gbP.hide()

        digitRegex = QRegExp('\d+')
        digitValidator = QRegExpValidator(digitRegex, self)
        self.leKCount.setValidator(digitValidator)
        self.lePCount.setValidator(digitValidator)

        addgrup_action = QAction( u"Печать с текущего кода", self )
        addgrup_action.setToolTip( u"Продолжить печать с выбранного кода" )
        self.tvDmCodes.addAction( addgrup_action )
        addgrup_action.triggered.connect( self.on_resumeprint )
        addgrup_action = QAction( u"Печать выделенных кодов", self )
        addgrup_action.setToolTip( u"Распечатать только выбранные коды" )
        self.tvDmCodes.addAction( addgrup_action )
        addgrup_action.triggered.connect( self.on_printselected )

        addgrup_action = QAction( u"Печать всех кодов", self )
        addgrup_action.setToolTip( u"Распечатать все коды по товару" )
        self.tvDmCodes.addAction( addgrup_action )
        addgrup_action.triggered.connect( self.on_zplprint )

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tvDmCodes.setContextMenuPolicy( Qt.ActionsContextMenu )

        for key, value in kwargs.items():
            if key == 'number':
                self.number = value
                if value != '':
                    self.setWindowTitle('Маркировка Datamatrix - информация по товару')
                else:
                    self.setWindowTitle('Маркировка Datamatrix - добавление нового товара')
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
            elif key == 'good':
                self.good = value
            elif key == 'category':
                self.id_category = value

        self.data_frame = pd.DataFrame(columns=['gs1dm'])
        self.data_frame_K = pd.DataFrame(columns=['K'])
        self.data_frame_P = pd.DataFrame(columns=['P'])

        self.setWidgetData()
        self.accept_actions()

    def on_resumeprint(self, point):
        tmp = self.data_frame.iloc[self.tvDmCodes.currentIndex().row():]
        self.zplprint = ZplPrinter(self, tmp['gs1dm'].tolist())
        self.zplprint.show() 

    def on_printselected(self, point):
        selectedRows = []
        for sel in self.tvDmCodes.selectionModel().selectedRows():
            selectedRows.append(sel.row())
        tmp = self.data_frame.iloc[selectedRows]
        self.zplprint = ZplPrinter(self, tmp['gs1dm'].tolist())
        self.zplprint.show() 

    
    def generate_code_k(self, code):
        #if self.data_frame_K['K'].count()>0:
            x = (self.data_frame[self.data_frame['gs1dm'] == code].index).to_list()[0] // int(self.leKCount.text())
            #print(x)
            return self.data_frame_K['K'].iloc[x]
        #else:
        #    return code

    def generate_code_p(self, code):
        #if self.data_frame_P['P'].count()>0:
            x = (self.data_frame[self.data_frame['gs1dm'] == code].index).to_list()[0] // (int(self.leKCount.text())*int(self.lePCount.text()))
            #print(x)
            return self.data_frame_P['P'].iloc[x]
        #else:
        #    return code



    def on_tvDmCodes_dblclick(self):
        print(self.tvDmCodes.currentIndex().row(),":",self.tvDmCodes.currentIndex().column())

    def aggregate(self):
        #if self.data_frame.count()>=0:  #   Переделать на один проход по датафрему
            self.data_frame['K'] = self.data_frame['gs1dm'].apply(self.generate_code_k)
            self.data_frame['P'] = self.data_frame['gs1dm'].apply(self.generate_code_p)           
            #print(self.data_frame)


            self.model = PandasModel(self.data_frame)
            self.tvDmCodes.setModel(self.model)
            self.tvDmCodes.resizeColumnsToContents()
            QMessageBox.information(self, 'Аггрегация', 'Аггрегация завершена успешно.\nСохраните отчет в файле...')

    def on_aggregate(self):   #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        try:
            KCodes = []
            PCodes = []
            k = 1      #Получить номер последней коробки
            self.progress_bar.setFixedSize(self.geometry().width(), 16)
            self.progress_bar.show()

            for i in range(self.data_frame['gs1dm'].count()):
                
                k = i // int(self.leKCount.text())
                if int(self.data_frame_K.count()) > 0:
                    KCodes.append(self.data_frame_K['K'][k])
                else:
                    KCodes.append(self.generate_code_K(k))
                
                #___________________________________________________
                #if int(self.data_frame_P.count()) > 0:
                #    PCodes.append(self.data_frame_P['P'][k // int(self.lePCount.text())])
                #else:
                #    PCodes.append(self.generate_code_P(k // int(self.lePCount.text())))
                PCodes.append(k // int(self.lePCount.text())+1)
                self.progress_bar.setValue(int(i / self.data_frame['gs1dm'].count()*100))
            self.progress_bar.setValue(100)
            self.progress_bar.hide()
            self.data_frame['K'] = KCodes
            self.data_frame['P'] = PCodes
            
            

            self.model = PandasModel(self.data_frame)
            self.tvDmCodes.setModel(self.model)
            self.tvDmCodes.resizeColumnsToContents()
        except:
            self.progress_bar.setValue(100)
            self.progress_bar.hide()
            self.statusBar().showMessage('ВНИМАНИЕ! В настоящее время ведется работа над совершенствованием данной функции', 0)

    def on_report_click(self):
        if self.leGoodName.text() != '':
            filename = self.leGoodName.text()+'.csv'
        else:
            filename = 'report_dm.csv'
        try:   #!!!!!!!!!!!!!!!!!Проверить сохранение отчета
            self.data_frame.to_csv(filename, index=False, header=False, sep=chr(9), quoting=QUOTE_NONE)
            self.statusBar().showMessage('Сохранение отчета выполнено успешно!', 5000)
        except:
            self.statusBar().showMessage('Сохранение отчета не выполнено!', 5000)

    def on_find(self):
        try:
            self.tvDmCodes.selectRow(self.data_frame[self.data_frame['gs1dm']==self.leFind.text()].index[0])
        except:
            self.statusBar().showMessage('Поиск завершился с ошибкой!', 5000)

    def on_zplprint(self):
        try:
            self.zplprint = ZplPrinter(self, self.data_frame['gs1dm'].tolist())
            self.zplprint.show()        
        except:
            self.statusBar().showMessage('Отсутствуют коды для печати', 5000)

    def on_zplprint_K(self):
        try:
            self.zplprint = ZplPrinter(self, self.data_frame_K['K'].tolist(), group = 'K')
            self.zplprint.show()
        except:
            self.statusBar().showMessage('Отсутствуют коды для печати', 5000)

    def on_zplprint_P(self):
        try:
            self.zplprint = ZplPrinter(self, self.data_frame_P['P'].tolist(), group = 'P')
            self.zplprint.show()
        except:
            self.statusBar().showMessage('Отсутствуют коды для печати', 5000)

    def accept(self):
        self.close()

    def reject(self):
        # - не предполагает изменения в БД
        self.close()

    def setWidgetData(self):
        self.leOrderNumber.setText(self.number)
        #self.cbCustomer.itemText(self.customer)
        self.leManager.setText(self.manager)
        self.deDateOn.setDate(self.date_on)
        self.leGoodName.setText(self.good)

        sql = 'SELECT STATE FROM dbmarking.ORDER_STATE;'
        self.cbOrderState.addItems(pd.read_sql_query(sql, self.parent.mydb)['STATE'].tolist())
        self.cbOrderState.setCurrentIndex(self.id_state)

        sql = '''SELECT FULL_NAME FROM dbmarking.CATEGORY;'''
        self.cbCategory.addItems(pd.read_sql_query(sql, self.parent.mydb)['FULL_NAME'].tolist())
        self.cbCategory.setCurrentIndex(self.id_category-1)

        if self.good != '':
            sql = 'SELECT id_goods FROM dbmarking.GOODS WHERE NAME = "'+self.good+'";'
            id_good = int(pd.read_sql_query(sql, self.parent.mydb).iloc[0])

            sql = 'SELECT id_order FROM dbmarking.ORDERS WHERE NUMBER = "'+self.number+'";'
            id_order = int(pd.read_sql_query(sql, self.parent.mydb).iloc[0])

            sql = ''' SELECT GS1DM FROM dbmarking.DM WHERE GOODS =''' + str(id_good) +" AND ORDERS = "+ str(id_order) + ";"
            self.data_frame = pd.read_sql_query(sql, self.parent.mydb)
            self.data_frame = self.data_frame.fillna(' ')
            self.data_frame = self.data_frame.rename(columns={'GS1DM' : 'GS1 Datamatrix'})

            self.model = PandasModel(self.data_frame)
            self.tvDmCodes.setModel(self.model)
            self.tvDmCodes.resizeColumnsToContents()
        self.tvDmCodes.show()

    def add_from_csv(self):
        pd.options.mode.copy_on_write = True
        options = QFileDialog.Options()
        #options |= QFileDialog.ExistingFiles   # включение множественного выбора
        options |= QFileDialog.DontUseNativeDialog
        fileNames, _ = QFileDialog.getOpenFileNames(self,"Выбор файлов с кодами...", "","CSV Files (*.csv);;TXT Files (*.txt);;All Files (*)", options=options)
        start = time()
        self.progress_bar.setFixedSize(self.geometry().width() - 120, 16)
        self.progress_bar.show()
        count = 1

        #self.data_frame = pd.DataFrame(columns=['gs1dm'])
        for file in fileNames:
            df = pd.read_csv(file, sep='\t', encoding='utf-8', names=['gs1dm'])
            self.data_frame = pd.concat([self.data_frame, df], axis = 0)
            self.progress_bar.setValue(int(count/len(fileNames)*100))
            count += 1 
        else:
            self.progress_bar.setValue(100)
            self.progress_bar.hide()

        self.data_frame = self.data_frame.reset_index()
        del self.data_frame['index']
    
        self.model = PandasModel(self.data_frame)
        self.tvDmCodes.setModel(self.model)
        self.tvDmCodes.resizeColumnsToContents()
        self.tvDmCodes.show()
        
        self.statusBar().showMessage(f'Готово! Время на загрузку кодов: {round(time()-start,2)}сек. Обработано кодов: {self.data_frame["gs1dm"].count()}', 0)


    def add_from_pdf(self):
        self.importPdf = PdfPreview(self, source='I')
        self.importPdf.show()
        

    def add_from_csv_K(self):
        pd.options.mode.copy_on_write = True
        options = QFileDialog.Options()
        #options |= QFileDialog.ExistingFiles   # включение множественного выбора
        options |= QFileDialog.DontUseNativeDialog
        fileNames, _ = QFileDialog.getOpenFileNames(self,"Выбор файла с групповыми кодами...", "","CSV Files (*.csv);;TXT Files (*.txt);;All Files (*)", options=options)
        start = time()
        self.progress_bar.setFixedSize(self.geometry().width() - 120, 16)
        self.progress_bar.show()
        count = 1

        #self.data_frame_K = pd.DataFrame(columns=['K'])
        for file in fileNames:
            df = pd.read_csv(file, sep='\t', encoding='utf-8', names=['K'])
            self.data_frame_K = pd.concat([self.data_frame_K, df], axis = 0)
            self.progress_bar.setValue(int(count/len(fileNames)*100))
            count += 1 
        else:
            self.progress_bar.setValue(100)
            self.progress_bar.hide()
        self.data_frame_K.drop_duplicates(subset=['K'],inplace=True)
        self.data_frame_K = self.data_frame_K.reset_index()
        del self.data_frame_K['index']
    
        self.model = PandasModel(self.data_frame_K)
        self.tvDmCodes_K.setModel(self.model)
        self.tvDmCodes_K.resizeColumnsToContents()
        self.gbK.setVisible(True)
        self.tvDmCodes_K.show()
        
        self.statusBar().showMessage(f'Готово! Время на загрузку кодов: {round(time()-start,2)}сек. Обработано кодов: {self.data_frame_K["K"].count()}', 0)

    def add_from_pdf_K(self):
        self.importPdf = PdfPreview(self, source='K')
        self.importPdf.show()
        



    def on_make_dm(self):
        try:
            if self.data_frame['gs1dm'].count() <= 0:
                QMessageBox.critical(None,'Внимание!!!', 'Отсутствуют коды для генерации...')
            elif self.cbCategory.currentIndex() == -1:
                QMessageBox.critical(None,'Внимание!!!', 'Не указана товарная группа...')
            elif ' '.join([ t for t in self.leGoodName.text().split(' ') if t ]) == '':
                QMessageBox.critical(None,'Внимание!!!', 'Не указано наименование товара...')
            else:
                self.makeDmWindow = LayoutDM(self)
                self.makeDmWindow.show()
        except:
            QMessageBox.critical(None,'Ошибка!!!', 'Невозможно отрыть форму генерации кодов. Обратитесь в техподдержку.')

            
    def on_make_dm_K(self):
        last_code = 0   #  Последний код упаковки по данному контрагенту (получить из базы)
        try:
            if self.data_frame_K['K'].count() <= 0:
                QMessageBox.information(None,'Внимание!!!', 
                                        'В текущем заказе отсутствуют коды для маркировки коробов.\nПеред настройкой печати будет выполнена автоматическая генерация кодов.')
                KCodes = []
                #print(self.data_frame['gs1dm'].count(), self.data_frame['gs1dm'].count() // int(self.leKCount.text())*int(self.lePCount.text()))
                for i in range(self.data_frame['gs1dm'].count() // int(self.leKCount.text())):
                    str_pallet = str(i+1 + last_code).zfill(5)
                    KCodes.append(f'{self.leFsrar_id.text()}{self.cbPType.currentIndex()*2+1}5524{self.leOrderNumber.text()}{str_pallet}')
                self.data_frame_K['K'] = KCodes

                self.model = PandasModel(self.data_frame_K)
                self.tvDmCodes_K.setModel(self.model)
                self.tvDmCodes_K.resizeColumnsToContents()
                self.gbK.setVisible(True)
                self.makeDmWindow = LayoutDM(self, group='K')
                self.makeDmWindow.show()
            else:
                self.makeDmWindow = LayoutDM(self, group='K')
                self.makeDmWindow.show()
        except:
            QMessageBox.critical(None,'Ошибка!!!', 'Невозможно отрыть форму генерации кодов коробов. Обратитесь в техподдержку.')
        
    def on_make_dm_P(self):
        try:
            if self.data_frame_P['P'].count() <= 0:
                QMessageBox.information(None,'Внимание!!!', 
                                        'В текущем заказе отсутствуют коды для маркировки паллет.\nПеред настройкой печати необходимо выполнить генерацию кодов.')
            else:
                self.makeDmWindow = LayoutDM(self, group='P')
                self.makeDmWindow.show()
        except:
            QMessageBox.critical(None,'Ошибка!!!', 'Невозможно отрыть форму генерации кодов. Обратитесь в техподдержку.')

    def on_make_barcode_P(self):
        last_code = 0  #  Последний код паллеты по данному контрагенту (получить из базы)
        PCodes = []
        #print(self.data_frame['gs1dm'].count(), self.data_frame['gs1dm'].count() // int(self.leKCount.text())*int(self.lePCount.text()))
        for i in range(self.data_frame['gs1dm'].count() // (int(self.leKCount.text())*int(self.lePCount.text()))):
            str_pallet = str(i+1 + last_code).zfill(5)
            PCodes.append(f'{self.leFsrar_id.text()}{self.cbPType.currentIndex()*2+2}5524{self.leOrderNumber.text()}{str_pallet}')
        self.data_frame_P['P'] = PCodes

        self.model = PandasModel(self.data_frame_P)
        self.tvDmCodes_P.setModel(self.model)
        self.tvDmCodes_P.resizeColumnsToContents()
        self.gbP.setVisible(True)

    def accept_actions(self):
        self.btnOk.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.reject)
        self.btnCsvImport.clicked.connect(self.add_from_csv)
        self.btnPdfImport.clicked.connect(self.add_from_pdf)
        self.btnCsvImport_K.clicked.connect(self.add_from_csv_K)
        self.btnPdfImport_K.clicked.connect(self.add_from_pdf_K)
        self.btnMakeBarcode_P.clicked.connect(self.on_make_barcode_P)
        self.btnMakeDm.clicked.connect(self.on_make_dm)
        self.btnMakeDm_K.clicked.connect(self.on_make_dm_K)
        self.btnMakeDm_P.clicked.connect(self.on_make_dm_P)
        self.btnZplPrint.clicked.connect(self.on_zplprint)
        self.btnZplPrint_K.clicked.connect(self.on_zplprint_K)
        self.btnZplPrint_P.clicked.connect(self.on_zplprint_P)
        self.btnFind.clicked.connect(self.on_find)
        #self.btnAgg.clicked.connect(self.on_aggregate)
        self.btnAgg.clicked.connect(self.aggregate)
        self.btnReport.clicked.connect(self.on_report_click)
        self.tvDmCodes.doubleClicked.connect(self.on_tvDmCodes_dblclick)


