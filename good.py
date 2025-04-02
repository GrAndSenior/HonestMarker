from PyQt5.QtWidgets import QMainWindow, QFileDialog, QProgressBar, QMessageBox, QAction
from PyQt5.QtCore import QDate, Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
import goods
from os import path
import pandas as pd
import xlsxwriter
from pandasmodel import PandasModel
from pdfpreview import PdfPreview
from layoutdm import LayoutDM
from zplprinter import ZplPrinter
from time import time
from csv import QUOTE_NONE
from xml.etree import ElementTree 
from datetime import datetime

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

        self.data_frame = pd.DataFrame(columns=['gs1dm'])
        self.data_frame_K = pd.DataFrame(columns=['K'])
        self.data_frame_P = pd.DataFrame(columns=['P'])


        digitRegex = QRegExp('\\d+')
        digitValidator = QRegExpValidator(digitRegex, self)
        self.leKCount.setValidator(digitValidator)
        self.lePCount.setValidator(digitValidator)
        self.leFsrar_id.setValidator(digitValidator)
        self.leOrderNumber.setValidator(digitValidator)


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
        addgrup_action.triggered.connect( self.on_zplprint_click)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tvDmCodes.setContextMenuPolicy( Qt.ActionsContextMenu )

        #Выключить неиспользуемые элементы дизайна
        self.label_6.setVisible(False)
        self.cbOrderState.setVisible(False)
        self.btnXml.setVisible(False)
        self.btnXlsx.setVisible(False)
        self.btnMakeBarcode_P.setVisible(False)
        
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


        self.setWidgetData()
        self.accept_actions()

    def keyPressEvent(self, e):
        if int(e.modifiers()) == (Qt.ControlModifier):  #+ Qt.ShiftModifier
            if e.key() == Qt.Key_1:
                self.tabWidget.setCurrentIndex(0)
            elif e.key() == Qt.Key_2:
                self.tabWidget.setCurrentIndex(1)
            elif e.key() == Qt.Key_3:
                self.tabWidget.setCurrentIndex(2)
            elif e.key() == Qt.Key_4:
                self.tabWidget.setCurrentIndex(3)
            elif e.key() == Qt.Key_O:
                self.on_open_click()
        #elif e.key() == Qt.Key_Escape:
        #    self.reject()
            
    def on_resumeprint(self, point):
        tmp = self.data_frame.iloc[self.tvDmCodes.currentIndex().row():]
        self.zplprint = ZplPrinter(self, data = tmp['gs1dm'].tolist())
        self.zplprint.show() 

    def on_printselected(self, point):
        selectedRows = []
        for sel in self.tvDmCodes.selectionModel().selectedRows():
            selectedRows.append(sel.row())
        tmp = self.data_frame.iloc[selectedRows]
        self.zplprint = ZplPrinter(self, data = tmp['gs1dm'].tolist())
        self.zplprint.show() 

    
    def generate_code_k(self, code):
        if self.data_frame_K['K'].count()>0:
            x = (self.data_frame[self.data_frame['gs1dm'] == code].index).to_list()[0] // int(self.leKCount.text())
            #print(x)
            return self.data_frame_K['K'].iloc[x]
        else:
            return code

    def generate_code_p(self, code):
        if self.data_frame_P['P'].count()>0:
            x = (self.data_frame[self.data_frame['gs1dm'] == code].index).to_list()[0] // (int(self.leKCount.text())*int(self.lePCount.text()))
            #print(x)
            return self.data_frame_P['P'].iloc[x]
        else:
            return code



    def on_tvDmCodes_dblclick(self):
        '''
        if self.tabWidget.currentIndex() == 0:
            print(self.tvDmCodes.currentIndex().row(),":",self.tvDmCodes.currentIndex().column())
        elif self.tabWidget.currentIndex() == 1:
            print()
        elif self.tabWidget.currentIndex() == 2:
            print()
        elif self.tabWidget.currentIndex() == 3:
            print()
        '''
        pass

    def aggregate(self):
        #if self.data_frame.count()>=0:  #   Переделать на один проход по датафрему
            self.data_frame_Agg = pd.DataFrame()
            self.data_frame_Agg['gs1dm'] = self.data_frame['gs1dm']
            KCodes = self.data_frame_K
            PCodes = self.data_frame_P
            
            KCodes['idx'] = KCodes.index
            PCodes['idx'] = PCodes.index

            self.data_frame_Agg['idx'] = self.data_frame_Agg.index // int(self.leKCount.text())
            self.data_frame_Agg = self.data_frame_Agg.merge(KCodes, how='left', on='idx', suffixes=('', '1'))
            self.data_frame_Agg['K'] = self.data_frame_Agg['K'].fillna('-')
            self.data_frame_Agg['idx'] = self.data_frame_Agg.index // (int(self.leKCount.text()) * int(self.lePCount.text()))
            self.data_frame_Agg = self.data_frame_Agg.merge(PCodes, how='left', on='idx', suffixes=('', '1'))
            self.data_frame_Agg['P'] = self.data_frame_Agg['P'].fillna('-')
            self.data_frame_Agg = self.data_frame_Agg.drop(['idx'], axis=True)
            self.data_frame_Agg.reset_index()

            #self.df = self.df.groupby(['P','K','gs1dm']).count()
            #self.df.reset_index()

            self.model = PandasModel(self.data_frame_Agg)
            self.tvAgg.setModel(self.model)
            self.tvAgg.resizeColumnsToContents()
            self.tabWidget.setCurrentIndex(3)
            #QMessageBox.information(self, 'Аггрегация', 'Аггрегация завершена успешно.\nСохраните отчет в файле...')
            
    '''
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
            self.statusBar().showMessage('ВНИМАНИЕ! В настоящее время ведется работа над совершенствованием данной функции', 5000)
    '''
    def on_xlsx_click(self):
        
        if self.leGoodName.text() != '':
            filename = self.leGoodName.text()+'.csv'
        else:
            filename = 'report_dm.csv'
        try:  
            if self.tabWidget.currentIndex() == 3:
                
                if 'idx' in self.data_frame_Agg.columns.tolist():
                    self.data_frame_Agg = self.data_frame_Agg.drop(['idx'], axis=True)

                self.data_frame_Agg['G'] = self.leGoodName.text()
                
                self.data_frame_Agg['I'] = ''
                self.data_frame_Agg['nk'] = self.data_frame_Agg.index // int(self.leKCount.text()) + 1
                self.data_frame_Agg = self.data_frame_Agg.reindex(columns=['I', 'G', 'nk', 'gs1dm','K'])
                #
                report = pd.DataFrame()
                for box_idx in range(self.data_frame_K['K'].count()):
                    
                    report = pd.concat([report,self.data_frame_Agg[box_idx*int(self.leKCount.text()):(box_idx+1)*int(self.leKCount.text())]], ignore_index=True) 
                    
                    line = pd.DataFrame([{'I': int(self.leKCount.text()), 'G': self.leGoodName.text(), 'nk': box_idx+1, 'gs1dm': self.data_frame_Agg['K'].iloc[box_idx*int(self.leKCount.text())], 'K': ''}])
                    report = pd.concat([report, line], ignore_index=True)
                    #print(self.data_frame_Agg[box_idx*int(self.leKCount.text()):(box_idx+1)*int(self.leKCount.text())])
                report.columns = ['Количество внутри', 'Номенклатура', 'Номер короба', 'Расшифрованный код маркировки', 'Расшифрованный код упаковки']
                report.to_excel(filename.replace('.csv','_agg.xlsx'), index=False, header=True)

                #print()
                #print(self.data_frame_Agg)
            QMessageBox.information(self,'Экспорт в Excel...', 'Выгрузка отчета в XLSX завершена успешно.')
            #self.statusBar().showMessage(f'Сохранение отчета выполнено успешно!', 5000)
        except:
            QMessageBox.critical(self.parent,'Ошибка!!!', 'В процессе выгрузки возникли ошибки. Обратитесь в техподдержку.')
            #self.statusBar().showMessage('Сохранение отчета не выполнено!', 5000)
    
    def on_report_click(self):
        if self.cbReportFormat.currentIndex() == 0:
            self.make_csv()
        elif self.cbReportFormat.currentIndex() == 1:
            self.make_xlsx()
        elif self.cbReportFormat.currentIndex() == 2:
            self.make_xml()
        
    def make_csv(self):
        if self.leGoodName.text() != '':
            filename = self.leGoodName.text()+'.csv'
        else:
            filename = 'report_dm.csv'
        try:  
            if self.tabWidget.currentIndex() == 0 and len(self.data_frame['gs1dm'])>0:
                if 'idx' in self.data_frame.columns.tolist():
                    df = self.data_frame.drop(['idx'], axis=True)
                else:
                    df = self.data_frame
                df.to_csv(filename, index=False, header=False, sep=chr(9), quoting=QUOTE_NONE)
            elif self.tabWidget.currentIndex() == 1  and len(self.data_frame_K['K'])>0:
                if 'idx' in self.data_frame_K.columns.tolist():
                    df = self.data_frame_K.drop(['idx'], axis=True)
                else:
                    df = self.data_frame_K
                df.to_csv(filename.replace('.csv','_K.csv'), index=False, header=False, sep=chr(9), quoting=QUOTE_NONE)
            elif self.tabWidget.currentIndex() == 2 and len(self.data_frame_P['P'])>0:
                if 'idx' in self.data_frame_P.columns.tolist():
                    df = self.data_frame_P.drop(['idx'], axis=True)
                else:
                    df = self.data_frame_P
                df.to_csv(filename.replace('.csv','_P.csv'), index=False, header=False, sep=chr(9), quoting=QUOTE_NONE)
            elif self.tabWidget.currentIndex() == 3 and len(self.data_frame_Agg)>0:
                if 'idx' in self.data_frame_Agg.columns.tolist():
                    df = self.data_frame_Agg.drop(['idx'], axis=True)
                else:
                    df = self.data_frame_Agg
                df.to_csv(filename.replace('.csv','_agg.csv'), index=False, header=True, sep=chr(9), quoting=QUOTE_NONE)
            QMessageBox.information(self,'Экспорт в CSV...', 'Выгрузка отчета в CSV завершена успешно.')
        except:
            QMessageBox.critical(self.parent,'Ошибка!!!', 'В процессе выгрузки возникли неустранимые ошибки.\nОбратитесь в техподдержку.')
            #self.statusBar().showMessage('Сохранение отчета не выполнено!', 5000)
        
    def make_xlsx(self):
        if self.leGoodName.text() != '':
            filename = self.leGoodName.text()+'.csv'
        else:
            filename = 'report_dm.csv'
        try:  
            if self.tabWidget.currentIndex() == 3 and len(self.data_frame_Agg['gs1dm'])>0:
                if 'idx' in self.data_frame_Agg.columns.tolist():
                    df = self.data_frame_Agg.drop(['idx'], axis=True)
                df['G'] = self.leGoodName.text()
                df['I'] = ''
                df['nk'] = self.data_frame_Agg.index // int(self.leKCount.text()) + 1
                df = df.reindex(columns=['I', 'G', 'nk', 'gs1dm','K'])
                report = pd.DataFrame()
                for box_idx in range(self.data_frame_K['K'].count()):
                    report = pd.concat([report,df[box_idx*int(self.leKCount.text()):(box_idx+1)*int(self.leKCount.text())]], ignore_index=True) 
                    line = pd.DataFrame([{'I': int(self.leKCount.text()), 'G': self.leGoodName.text(), 'nk': box_idx+1, 'gs1dm': df['K'].iloc[box_idx*int(self.leKCount.text())], 'K': ''}])
                    report = pd.concat([report, line], ignore_index=True)
                report.columns = ['Количество внутри', 'Номенклатура', 'Номер короба', 'Расшифрованный код маркировки', 'Расшифрованный код упаковки']
                report.to_excel(filename.replace('.csv','_agg.xlsx'), index=False, header=True)

                QMessageBox.information(self,'Экспорт в XLSX...', 'Выгрузка отчета в XLSX завершена успешно.')
        except:
            QMessageBox.critical(self.parent,'Ошибка!!!', 'В процессе выгрузки возникли ошибки. Обратитесь в техподдержку.')
            #self.statusBar().showMessage('Сохранение отчета не выполнено!', 5000)
        
    def make_xml(self):
        if self.tabWidget.currentIndex() == 3 and len(self.data_frame_Agg['gs1dm'])>0:
            XmlReport(self).make_report()
        else:
            QMessageBox.information(self,'Экспорт в XML...', 'Нет данных для выгрузки отчета')

    def on_find(self):
        try:
            if self.tabWidget.currentIndex() == 0:
                self.tvDmCodes.selectRow(self.data_frame[self.data_frame['gs1dm']==self.leFind.text()].index[0])
            elif self.tabWidget.currentIndex() == 1:
                self.tvDmCodes_K.selectRow(self.data_frame_K[self.data_frame_K['gs1dm']==self.leFind.text()].index[0])
            elif self.tabWidget.currentIndex() == 2:
                self.tvDmCodes_P.selectRow(self.data_frame_P[self.data_frame_P['gs1dm']==self.leFind.text()].index[0])
            #elif self.tabWidget.currentIndex() == 3:
            #    self.tvDmCodes_K.selectRow(self.data_frame_K[self.data_frame['gs1dm']==self.leFind.text()].index[0])
        except:
            self.statusBar().showMessage('Поиск завершился неудачей!', 5000)


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

        sql = 'SELECT STATE FROM ORDER_STATE;'
        self.cbOrderState.addItems(pd.read_sql_query(sql, self.parent.mydb)['STATE'].tolist())
        self.cbOrderState.setCurrentIndex(self.id_state)

        sql = '''SELECT FULL_NAME FROM CATEGORY;'''
        self.cbCategory.addItems(pd.read_sql_query(sql, self.parent.mydb)['FULL_NAME'].tolist())
        self.cbCategory.setCurrentIndex(self.id_category-1)

        if self.good != '':
            sql = 'SELECT id_goods FROM .GOODS WHERE NAME = "'+self.good+'";'
            id_good = int(pd.read_sql_query(sql, self.parent.mydb).iloc[0])

            sql = 'SELECT id_order FROM ORDERS WHERE NUMBER = "'+self.number+'";'
            id_order = int(pd.read_sql_query(sql, self.parent.mydb).iloc[0])

            sql = ''' SELECT GS1DM FROM DM WHERE GOODS =''' + str(id_good) +" AND ORDERS = "+ str(id_order) + ";"
            self.data_frame = pd.read_sql_query(sql, self.parent.mydb)
            self.data_frame = self.data_frame.fillna(' ')
            self.data_frame = self.data_frame.rename(columns={'GS1DM' : 'GS1 Datamatrix'})

            self.model = PandasModel(self.data_frame)
            self.tvDmCodes.setModel(self.model)
            self.tvDmCodes.resizeColumnsToContents()
        self.tvDmCodes.show()

    def add_from_csv(self, fileName):
        pd.options.mode.copy_on_write = True
        start = time()
        #self.progress_bar.setFixedSize(self.geometry().width() - 120, 16)
        #self.progress_bar.show()
        data_frame = pd.read_csv(fileName, sep='\t', encoding='utf-8', names=['code'])
        #self.progress_bar.setValue(int(count/len(fileNames)*100))

        
        '''
        for count, file in enumerate(fileNames):
            data_frame += pd.read_csv(file, sep='\t', encoding='utf-8', names=['gs1dm'])
            self.progress_bar.setValue(int(count/len(fileNames)*100))
        else:
            self.progress_bar.setValue(100)
            self.progress_bar.hide()
'''
        data_frame.drop_duplicates(subset=['code'], inplace=True)
        data_frame = data_frame.reset_index()
        del data_frame['index']
        if len(data_frame) > 0:
            self.statusBar().showMessage(f'Готово! Время на загрузку кодов: {round(time()-start,2)}сек. Обработано кодов: {len(data_frame)}', 5000)
        
        if self.tabWidget.currentIndex() == 0:
            self.data_frame = data_frame.rename(columns={'code' : 'gs1dm'})
            self.model = PandasModel(self.data_frame)
            self.tvDmCodes.setModel(self.model)
            self.tvDmCodes.resizeColumnsToContents()
            self.tvDmCodes.show()
        elif self.tabWidget.currentIndex() == 1:
            self.data_frame_K = data_frame.rename(columns={'code' : 'K'})
            self.model = PandasModel(self.data_frame_K)
            self.tvDmCodes_K.setModel(self.model)
            self.tvDmCodes_K.resizeColumnsToContents()
            self.tvDmCodes_K.show()
        elif self.tabWidget.currentIndex() == 2:
            self.data_frame_P = data_frame.rename(columns={'code' : 'P'})
            self.model = PandasModel(self.data_frame_P)
            self.tvDmCodes_P.setModel(self.model)
            self.tvDmCodes_P.resizeColumnsToContents()
            self.tvDmCodes_P.show()
            
            
    '''
    def add_from_csv_K(self, fileNames):
        pd.options.mode.copy_on_write = True
        start = time()
        self.progress_bar.setFixedSize(self.geometry().width() - 120, 16)
        self.progress_bar.show()
        count = 1

        #self.data_frame_K = pd.DataFrame(columns=['K'])
        for file in fileNames:
            #df = pd.read_csv(file, sep='\t', encoding='utf-8', names=['K'])
            #self.data_frame_K = pd.concat([self.data_frame_K, df], axis = 0)
            self.data_frame_K = pd.read_csv(file, sep='\t', encoding='utf-8', names=['K'])
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
        #self.gbK.setVisible(True)
        self.tvDmCodes_K.show()
        if self.data_frame_K["K"].count() > 0:
            self.statusBar().showMessage(f'Готово! Время на загрузку кодов: {round(time()-start,2)}сек. Обработано кодов: {self.data_frame_K["K"].count()}', 5000)

    def add_from_csv_P(self, fileNames):
        pd.options.mode.copy_on_write = True
        start = time()
        self.progress_bar.setFixedSize(self.geometry().width() - 120, 16)
        self.progress_bar.show()
        count = 1

        for file in fileNames:
            self.data_frame_P = pd.read_csv(file, sep='\t', encoding='utf-8', names=['P'])
            self.progress_bar.setValue(int(count/len(fileNames)*100))
            count += 1 
        else:
            self.progress_bar.setValue(100)
            self.progress_bar.hide()
        self.data_frame_P.drop_duplicates(subset=['P'],inplace=True)
        self.data_frame_P = self.data_frame_P.reset_index()
        del self.data_frame_P['index']
    
        self.model = PandasModel(self.data_frame_P)
        self.tvDmCodes_P.setModel(self.model)
        self.tvDmCodes_P.resizeColumnsToContents()
        #self.gbK.setVisible(True)
        self.tvDmCodes_P.show()
        if self.data_frame_P["P"].count() > 0:
            self.statusBar().showMessage(f'Готово! Время на загрузку кодов: {round(time()-start,2)}сек. Обработано кодов: {self.data_frame_P["P"].count()}', 5000)

'''

    def on_make_dm(self):
        from math import ceil
        from datetime import datetime        
        try:
            if self.cbCategory.currentIndex() == -1:
                #self.statusBar().showMessage(f'Внимание!!! Не указана товарная группа...', 0)
                QMessageBox.critical(self,'Внимание!!!', 'Не указана товарная группа...')
            elif ' '.join([ t for t in self.leGoodName.text().split(' ') if t ]) == '':
                #self.statusBar().showMessage(f'Внимание!!! Не указано наименование товара...', 0)
                QMessageBox.critical(self,'Внимание!!!', 'Не указано наименование товара...')
            else:
                if self.tabWidget.currentIndex() == 0:   ### Коды товара
                    if self.data_frame['gs1dm'].count() <= 0:
                        QMessageBox.critical(self, 'Внимание!!!', 'Отсутствуют коды для генерации...')
                    else:
                        self.makeDmWindow = LayoutDM(self)
                        self.makeDmWindow.show()

                elif self.tabWidget.currentIndex() == 1:  ### Коды коробов
                    if len(self.data_frame_K) <= 0:
                        last_code = 0   #  Последний код упаковки по данному контрагенту (получить из базы)
                        QMessageBox.information(self,'Внимание!!!', 
                                                'В текущем заказе отсутствуют коды для маркировки коробов.\nПеред настройкой печати будет выполнена автоматическая генерация кодов.')
                        KCodes = []
                        for i in range(ceil(self.data_frame['gs1dm'].count() / int(self.leKCount.text()))):
                            str_pallet = str(i+1 + last_code).zfill(5)
                            KCodes.append(f'{self.leFsrar_id.text().zfill(12)}{self.cbPType.currentIndex()*2+1}55{datetime.today().year % 100}{self.leOrderNumber.text()}{str_pallet}')
                        self.data_frame_K['K'] = KCodes
                        self.model = PandasModel(self.data_frame_K)
                        self.tvDmCodes_K.setModel(self.model)
                        self.tvDmCodes_K.resizeColumnsToContents()
                    self.makeDmWindow = LayoutDM(self)
                    self.makeDmWindow.show()

                elif self.tabWidget.currentIndex() == 2:  ### Коды паллет
                    if len(self.data_frame_P) <= 0:
                        last_code = 0  #  Последний код паллеты по данному контрагенту (получить из базы)
                        PCodes = []
                        for i in range( ceil(len(self.data_frame['gs1dm']) / (int(self.leKCount.text())*int(self.lePCount.text())))):
                            #str_pallet = str(i+1 + last_code).zfill(5)
                            PCodes.append(f'{self.leFsrar_id.text()}{self.cbPType.currentIndex()*2+2}55{datetime.today().year % 100}{self.leOrderNumber.text()}{ str(i+1 + last_code).zfill(5) }')
                        self.data_frame_P = pd.DataFrame(columns=['P'])
                        self.data_frame_P['P'] = PCodes
                        self.model = PandasModel(self.data_frame_P)
                        self.tvDmCodes_P.setModel(self.model)
                        self.tvDmCodes_P.resizeColumnsToContents()
                    self.makeDmWindow = LayoutDM(self)
                    self.makeDmWindow.show()
                    
                    
        except:
            #self.statusBar().showMessage(f'Ошибка!!! Невозможно отрыть форму генерации кодов. Обратитесь в техподдержку.', 0)
            QMessageBox.critical(self, 'Ошибка!!!', 'Невозможно выполнить генерацию кодов. Обратитесь в техподдержку.')

    def make_barcode_P(self):
        from math import ceil
        from datetime import datetime
        last_code = 0  #  Последний код паллеты по данному контрагенту (получить из базы)
        PCodes = []
        for i in range( ceil(len(self.data_frame['gs1dm']) / (int(self.leKCount.text())*int(self.lePCount.text())))):
            #str_pallet = str(i+1 + last_code).zfill(5)
            PCodes.append(f'{self.leFsrar_id.text()}{self.cbPType.currentIndex()*2+2}55{datetime.today().year % 100}{self.leOrderNumber.text()}{ str(i+1 + last_code).zfill(5) }')
        
        self.data_frame_P = pd.DataFrame(columns=['P'])
        
        self.data_frame_P['P'] = PCodes

        self.model = PandasModel(self.data_frame_P)
        self.tvDmCodes_P.setModel(self.model)
        self.tvDmCodes_P.resizeColumnsToContents()
        self.tabWidget.setCurrentIndex(2)
        #self.gbP.setVisible(True)

    def on_csv_import_click(self, fileName):
        if self.tabWidget.currentIndex() != 3:
            self.add_from_csv(fileName)

    def on_pdf_import_click(self, fileName):
        self.importPdf = PdfPreview(self, fileName)
        self.importPdf.show()
            

    def on_make_dm_click(self):
        self.on_make_dm()

        '''if self.tabWidget.currentIndex() == 0:
            self.on_make_dm()
        elif self.tabWidget.currentIndex() == 1:
            self.on_make_dm_K()
        elif self.tabWidget.currentIndex() == 2:
            #self.on_make_dm_P()    #Возможность генерации кода DataMatrix для паллет
            self.make_barcode_P()
'''
    def on_zplprint_click(self):            
        try:
            self.zplprint = ZplPrinter(self)
            self.zplprint.show()        
        except:
            self.statusBar().showMessage('Отсутствуют коды для печати', 5000)

    def on_open_click(self):
        filedialog = QFileDialog()
        filedialog.setDirectory(self.parent.options['MAIN']['work'])
        options = QFileDialog.Options()
        #options |= QFileDialog.ExistingFiles   # включение множественного выбора
        options |= QFileDialog.DontUseNativeDialog
        fileNames, filetype = filedialog.getOpenFileNames(self,"Выбор файлов с кодами...", "","CSV Files (*.csv);;PDF Files (*.pdf);;TXT Files (*.txt);;All Files (*)", options=options)
        if '*.pdf' in filetype:
            self.on_pdf_import_click(fileNames[0])
        elif '*.xls' in filetype:
            pass
        elif '*.csv' in filetype:
            self.on_csv_import_click(fileNames[0])
        else:
            pass
        if self.tabWidget.currentIndex() == 0 and fileNames:
            self.leGoodName.setText(path.splitext(path.basename(fileNames[0]))[0])
        
    def on_xmlreport_click(self):
        XmlReport(self).make_report()#P_codes, K_codes, codes)

        
    def on_xml_click(self):     #Пока не используется (старая версия выгрузки)
        from datetime import datetime
        '''
            Отчет формируется в разрезе 'код короба' - 'список кодов товара в коробе'
        '''
        report = [f'''<?xml version="1.0" encoding="UTF-8"?>\n<unit_pack>\n\t<Document>\n\t\t<organisation>\n\t\t\t<id_info>\n\t<LP_info LP_TIN="7706815551" />\n\t\t\t</id_info>\n\t\t</organisation>\n''']
        K_codes = self.data_frame_Agg['K'].value_counts().index.tolist()
        for pack_code in K_codes:
            report.append(f'''\t\t<pack_content>\n\t\t\t<pack_code>{pack_code}</pack_code>\n''')  
            codes = self.data_frame_Agg[self.data_frame_Agg['K']==pack_code]['gs1dm'].tolist()
            for code in codes:
                report.append(f'\t\t\t<cis>{code}</cis>\n')
            report.append('\t\t</pack_content>\n') 
        report.append('\t</Document>\n</unit_pack>\n')
        try:
            with open(f'{self.leOrderNumber.text()}-{self.leGoodName.text()}_{datetime.now().strftime("%d-%m-%Y %H-%M-%S")}.xml', 'w') as f:
                f.writelines(report)
            QMessageBox.information(self,'Экспорт в XML...', 'Выгрузка отчета в XML завершена успешно.')
        except:    
            QMessageBox.critical(self,'Ошибка!!!', 'В процессе экспорта возникли ошибки. Обратитесь в техподдержку.')            
            
            
    def on_cleardf_click(self):
        if self.tabWidget.currentIndex() == 0:
            self.data_frame = pd.DataFrame()
            self.model = PandasModel(self.data_frame)
            self.tvDmCodes.setModel(self.model)
            self.tvDmCodes.resizeColumnsToContents()
        elif self.tabWidget.currentIndex() == 1:
            self.data_frame_K = pd.DataFrame()
            self.model = PandasModel(self.data_frame_K)
            self.tvDmCodes_K.setModel(self.model)
            self.tvDmCodes_K.resizeColumnsToContents()
        elif self.tabWidget.currentIndex() == 2:
            self.data_frame_P = pd.DataFrame()
            self.model = PandasModel(self.data_frame_P)
            self.tvDmCodes_P.setModel(self.model)
            self.tvDmCodes_P.resizeColumnsToContents()
        elif self.tabWidget.currentIndex() == 3:
            self.data_frame_Agg = pd.DataFrame()
            self.model = PandasModel(self.data_frame_Agg)
            self.tvAgg.setModel(self.model)
            self.tvAgg.resizeColumnsToContents()

    def accept_actions(self):
        self.btnOk.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.reject)
        self.btnOpen.clicked.connect(self.on_open_click)
        #self.btnMakeBarcode_P.clicked.connect(self.make_barcode_P)
        self.btnMakeCode.clicked.connect(self.on_make_dm_click)
        self.btnZplPrint.clicked.connect(self.on_zplprint_click)
        self.btnFind.clicked.connect(self.on_find)
        self.btnAgg.clicked.connect(self.aggregate)
        self.btnReport.clicked.connect(self.on_report_click)
        self.btnXlsx.clicked.connect(self.on_xlsx_click)
        self.btnXml.clicked.connect(self.on_xmlreport_click)
        self.btnClear.clicked.connect(self.on_cleardf_click)
        self.tvDmCodes.doubleClicked.connect(self.on_tvDmCodes_dblclick)

class XmlReport():
    def __init__(self, parent):
        self.parent = parent
        self.root = ElementTree.Element('Documents')
        self.document = ElementTree.SubElement(self.root, 'Document', xmlxsi="http://www.w3.org/2001/XMLSchema-instance", Version="1")
        self.invoice_aggregation = ElementTree.SubElement(self.document, 'Invoice_aggregation')
        self.header = ElementTree.SubElement(self.invoice_aggregation, 'Header')
        self.version = ElementTree.SubElement(self.header, 'Version')
        self.invioceNumber = ElementTree.SubElement(self.header, 'InvoiceNumber')
        self.invoiceDate = ElementTree.SubElement(self.header, 'InvoiceDate')
        self.content = ElementTree.SubElement(self.invoice_aggregation, 'Content')
        self.palettequantity = ElementTree.SubElement(self.content, 'PaletteQuantity')
        self.boxquantity = ElementTree.SubElement(self.content, 'BoxQuantity')
        self.unitquantity = ElementTree.SubElement(self.content, 'UnitQuantity')
        self.weight = ElementTree.SubElement(self.content, 'Weight')
        self.sku = ElementTree.SubElement(self.content, 'SKU')
        self.position = ElementTree.SubElement(self.content, 'Position')
        self.identity = ElementTree.SubElement(self.position, 'Identity')
        self.fullname = ElementTree.SubElement(self.position, 'FullName')
        self.ean = ElementTree.SubElement(self.position, 'EAN')
        self.boxcapacity = ElementTree.SubElement(self.position, 'BoxCapacity')
        self.quantity = ElementTree.SubElement(self.position, 'Quantity')
        self.markinfo = ElementTree.SubElement(self.position, 'MarkInfo')

    def indent(self, elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
   
    def make_report(self):
        amcs = self.parent.data_frame['gs1dm'].tolist()
        boxnumbers = self.parent.data_frame_K['K'].tolist()
        pallets = self.parent.data_frame_P['P'].tolist()
        self.version.text = "1"
        self.invoiceDate.text = str(self.parent.deDateOn.date().toString('yyyy-MM-dd'))
        self.invioceNumber.text = self.parent.leOrderNumber.text() 
        self.palettequantity.text = str(len(pallets))
        self.boxquantity.text = str(len(boxnumbers))
        self.unitquantity.text = str(len(amcs))
        self.weight.text = self.parent.leWeight.text()
        self.sku.text = self.parent.leSku.text()
        self.identity.text = str(1)
        self.fullname.text = self.parent.leGoodName.text()
        self.ean.text = self.parent.leEan.text()
        self.boxcapacity.text = self.parent.leKCount.text()
        self.quantity.text = str(int(self.parent.leKCount.text())*int(self.parent.lePCount.text()))
        for p, pcode in enumerate(pallets):
            palletpos = ElementTree.SubElement(self.markinfo, 'PalletPos')
            palletnum = ElementTree.SubElement(palletpos, 'PalletNum')
            bottlingdate = ElementTree.SubElement(palletpos, 'BottlingDate')
            boxpos = ElementTree.SubElement(palletpos, 'BoxPos')
            palletnum.text = pcode
            bottlingdate.text = str(self.parent.deDateBottled.date().toString('yyyy-MM-dd'))
            for b in range(int(self.parent.lePCount.text())):
                boxnumber = ElementTree.SubElement(boxpos, 'boxnumber')
                try:
                    boxnumber.text = boxnumbers[p*int(self.parent.lePCount.text())+b]
                    amclist = ElementTree.SubElement(boxpos, 'amclist')
                    for i in range(int(self.parent.leKCount.text())):
                        amc = ElementTree.SubElement(amclist, 'amc')
                        try:
                            amc.text = amcs[p*int(self.parent.lePCount.text())*int(self.parent.leKCount.text()) + b*int(self.parent.leKCount.text()) + i]
                        except:
                            break
                except:
                    break
        self.indent(self.root)
        etree = ElementTree.ElementTree(self.root)
        myfile = open(f"{self.parent.leGoodName.text()}_{self.parent.leOrderNumber.text()}_{self.parent.deDateOn.text()}.xml" , "wb")
        try:
            etree.write(myfile, encoding='utf-8', xml_declaration=True)
            QMessageBox.information(self.parent,'Экспорт в XML...', 'Выгрузка отчета в XML завершена успешно.')
        except:    
            QMessageBox.critical(self.parent,'Ошибка!!!', 'В процессе выгрузки возникли ошибки. Обратитесь в техподдержку.')
