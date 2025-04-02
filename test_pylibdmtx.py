#pyuic5 design.ui -o design.py
from treepoem import generate_barcode
from pylibdmtx.pylibdmtx import decode, encode
import aspose.barcode as barcode
from PIL import Image, ImageDraw, ImageFont
import os, fitz
from typing import Tuple
from time import time
from glob import glob
import mysql.connector
from pystrich.datamatrix import DataMatrixEncoder

from PyQt5 import QtCore, QtSql
from PyQt5.QtGui import QPixmap,QImage, QColor, QPalette, QFont, QPageSize, QStandardItem, QStandardItemModel
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtCore import Qt # нужна константа Qt.KeepAspectRatio для изменения размеров с сохранением пропорций
from PyQt5.QtWidgets import (QMainWindow, QProgressBar, QApplication, QFileDialog, QAbstractItemView, QLabel,
                             QButtonGroup, QTableWidget, QTableWidgetItem, QStyledItemDelegate, QWidget)

import design, os, sys, StickerDM, DataMatrix, neworder, layoutui, pdfimport, aggwindow#, zebraui  # sys нужен для передачи argv в QApplication

### ^[0][1][0-9]{14}[2][1][^]{7}[9][3]\S{4}$

#FNC1 = chr(232)
#FNC1 = FNC1.encode("utf-8")
#FNC1 = bytes.fromhex("E8").decode('utf-8')
GS1 = chr(29)

TITLE = 'DataMatrix для "Честного знака". Товарная группа: '
ORG = ''



#class ColorDelegate(QStyledItemDelegate):
#    def paint(self, painter, option, index):
#        option.palette.setColor(QPalette.Text, QColor('#2D2424'))
#        option.palette.setColor(QPalette.Background, QColor('#FFFFFF'))
#        QStyledItemDelegate.paint(self, painter, option, index)

class PdfPreview(QMainWindow, pdfimport.Ui_PdfPreviewWindow):
    def __init__(self,root, **kwargs):
        super().__init__(root, **kwargs)
        self.setupUi(self)  # Это для инициализации  дизайна
        self.window = root

        self.btnOpenFile.clicked.connect(self.open_pdf_file)
        self.btnCancel.clicked.connect(self.reject)
        self.btnPreView.clicked.connect(self.code_preview)

    def open_pdf_file(self):

        options = QFileDialog.Options()
        #options |= QFileDialog.ExistingFiles   # включение множественного выбора
        options |= QFileDialog.DontUseNativeDialog
        fileNames, _ = QFileDialog.getOpenFileNames(self,"Выбор файлов с кодами...", "","PDF Files (*.pdf);;All Files (*)", options=options)#.selectedFiles()    
        if fileNames:
            matrix = (1, 1)
            zoom = (1, 1)
            anchor = (0, 0)
            size = (100, 172)
            delta = (0, 0)
            pdfIn = fitz.open(fileNames[0])
            page = pdfIn[0]
            pix = page.get_pixmap(matrix=fitz.Matrix(int(self.zoom_x.text()), int(self.zoom_y.text())), alpha=False)
            pix.save(os.path.join('tmp.png'))
            pixmap = QPixmap('tmp.png')
            pixmap = pixmap.scaled(self.lbImage.width(), self.lbImage.height(), Qt.KeepAspectRatio)
            self.lbImage.setPixmap(pixmap)
            self.lbImage.show()
            self.leFileName.setText(fileNames[0])

    def reject(self):
        self.close()

    def code_preview(self):
        i,j = 1, 1
        pdfIn = fitz.open(self.leFileName.text())
        page = pdfIn[0]
          
        #page = fitz.open(self.leFileName.text())[0]
        pix = page.get_pixmap(matrix=fitz.Matrix(int(self.zoom_x.text()), int(self.zoom_y.text())), alpha=False)
        pix.save(os.path.join('tmp.png'))
        cr_left = int(self.leAnchor_x.text())+(int(self.leWidth.text())+int(self.leDelta_x.text()))*j
        cr_top = int(self.leAnchor_y.text())+(int(self.leHeight.text())+int(self.leDelta_y.text()))*i
        cr_right = cr_left + int(self.leWidth.text())
        cr_bottom = cr_top + int(self.leHeight.text())
        img_page = Image.open('tmp.png')
        #img_page = Image.open('tmp.png')
        image = img_page.crop((cr_left, cr_top, cr_right, cr_bottom))
        #self.lbCode.setHeight(self.lbCode.width())
        image.save('tmp.png')
        pixmap = QPixmap('tmp.png')
        pixmap = pixmap.scaled(self.lbImage.width(), self.lbImage.width(), Qt.KeepAspectRatio)
        self.lbCode.setPixmap(pixmap)
        self.lbCode.show()




                        

class Settings(QMainWindow, layoutui.Ui_LayoutWindow):
    def __init__(self,root, **kwargs):
        super().__init__(root, **kwargs)
        self.setupUi(self)  # Это для инициализации  дизайна
        self.window = root
        #self.leLeft.setText(self.window.leLeft.text())
        self.back = ''
        self.sticker_settings = {
            'anchor'    : (0, 0),
            'size'      : (100, 100) 
        }
        self.btnOk.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.reject)
        self.btnPreView.clicked.connect(self.preview)
        self.btnOpenBack.clicked.connect(self.open_back)
        self.btnDefault.clicked.connect(self.defaultclick)
        self.cbText.toggled.connect(self.text_check)
    
    def open_back(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","PNG files (*.png);;JPG files (*.jpg);;All Files (*)", options=options)
        #fileName = 'E:/DM/pivo_blank.png'
        if fileName:
            self.back = fileName
            self.leBack.setText(self.back)

    def accept(self):
        self.window.leLeft.setText(self.leLeft.text())
        self.close()
    
    def reject(self):
        self.close()
    
    def text_check(self):
        self.leSampleText.setEnabled(True)
        self.sbFontSize.setEnabled(True)
        self.cbTextRotate.setEnabled(True)
        self.cbTextAllign.setEnabled(True)
        self.leTextLeft.setEnabled(True)
        self.leTextTop.setEnabled(True)        

    def defaultclick(self):
        self.back = ''
        self.leBack.setText('')
        self.leLeft.setText('80')
        self.leTop.setText('80')
        self.leWidth.setText('100')
        self.leHeight.setText('100')
        self.cbText.setChecked(False)
        self.sbFontSize.setEnabled(False)
        self.leSampleText.setText('12345678901234567890123456')
        self.sbFontSize.setValue(18)
        self.cbTextRotate.setCurrentIndex(0)
        self.cbTextAllign.setCurrentIndex(0)
        self.leTextLeft.setText('100')
        self.leTextTop.setText('100')
        self.cbDMHeight.setCurrentIndex(5)
        self.cbDMQuality.setCurrentIndex(5)
        self.cbDMRotate.setCurrentIndex(0)

        self.leSampleText.setEnabled(False)
        self.sbFontSize.setEnabled(False)
        self.cbTextRotate.setEnabled(False)
        self.cbTextAllign.setEnabled(False)
        self.leTextLeft.setEnabled(False)
        self.leTextTop.setEnabled(False)




    def preview(self):
        try: 
            back = Image.open(self.back)
        except:
            back = Image.new(mode = "RGB", size=(40,40), color=(255,255,255,100))
        encoder = DataMatrixEncoder('0105411858000138215!*DvTG93LswN')
        encoder.save('tmp.png')
        with Image.open('tmp.png') as encoder:
            encoder.load()
        barcode_size_px = (int(self.leWidth.text()), int(self.leHeight.text()))
        barcode_position_px = (int(self.leLeft.text()), int(self.leTop.text()))
        picture = back
        picture.paste(encoder.resize(barcode_size_px), barcode_position_px)
        if self.cbText.isChecked():
            label = '0105411858000138215!*DvTG'
            font = ImageFont.truetype('arial.ttf', int(self.sbFontSize.text()))
            fontimage = Image.new('L', (font.font.getsize(label)[0][0], sum(font.getmetrics())))
            ImageDraw.Draw(fontimage).text((0, 0), label, fill=255, font=font)
            fontimage = fontimage.rotate(int(self.cbTextRotate.currentText()), resample=Image.BICUBIC, expand=True)
            picture.paste((0,0,0), box=(int(self.leTextLeft.text()), int(self.leTextTop.text())), mask=fontimage)
                    
        
        picture.save('tmp.png')
        pixmap = QPixmap('tmp.png')
        pixmap = pixmap.scaled(self.lbImage.width(), self.lbImage.height(), Qt.KeepAspectRatio)
        self.lbImage.setPixmap(pixmap)
        self.lbImage.show()



class MyApp(QMainWindow, design.Ui_MainWindow):
    
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        

        self.dir = os.getcwd()+'/'
        self.codes = []
        self.textlabel_visible = False
        self.scale = 0
        self.read_file =  False
        self.stop = False
        self.goods = 0
        self.back = ''
        self.setupUi(self)  # Это для инициализации  дизайна
        themes = glob("sources/*.qss")
        self.cbThemes.clear()
        for t in themes:
            self.cbThemes.addItem(t.replace('sources\\','').replace('.qss',''))

        self.cbThemes.setCurrentIndex(6)
        f = open(themes[self.cbThemes.currentIndex()], 'r')
        self.styleData = f.read()
        f.close()

        #self.sti = QtGui.QStandardItemModel(parent=window)
        if self.set_connection():
            self.lbConnect.setText('Соединение с сервером установлено')
        else:
            self.lbConnect.setText('Соединение с сервером не установлено')

        self.setStyleSheet(self.styleData)
        #self.tCodes.setItemDelegate(ColorDelegate())
        self.setWindowTitle(TITLE + ORG)
        self.resize(1440, 900)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0,100)
        self.statusBar().addPermanentWidget(self.progress_bar)
        self.progress_bar.hide()
        self.outpath = ''#os.getcwd()+'\\code\\'+str(self.leAggPrefix.text())
        self.leOutPath.setText(self.outpath) 

        self.tCodes.setSelectionMode(QAbstractItemView.MultiSelection)
        self.tCodes.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.printer = StickerDM.Stickerdm(self.leLeft.text(),self.leTop.text(),self.cbDMRotate.currentText(),self.cbDMHeight.currentText(),self.cbDMQuality.currentText())
        self.cbPrinter.clear()
        self.cbPrinter.addItems(self.printer.queues)

        self.gbSettings.hide()
        self.gbWork.show()

        self.btnPdfImport.clicked.connect(self.pdfimport)
        self.btnCsvImport.clicked.connect(self.csvimport)
        self.tCodes.cellClicked.connect(self.getClickedCell)
        self.btnReadCodes.clicked.connect(self.readcodesclick)
        self.btnSettings.clicked.connect(self.settingsclick)
        self.btnCsvKCodes.clicked.connect(self.readKcodesclick)
        self.btnAgg.clicked.connect(self.aggregation)
        self.btnReport.clicked.connect(self.export_csv)
        self.btnOpenFolder.clicked.connect(self.set_source)
        self.btnMakeDatamatrix.clicked.connect(self.makeDMPNG)
        self.btnPrintDataMatrix.clicked.connect(self.printDMCode)
        self.btnMakeBarcode.clicked.connect(self.makeBarcodeclick)
        self.cbPrinter.currentTextChanged.connect(self.changePrinter)
        self.cbThemes.currentTextChanged.connect(self.changeThemes)
        self.btnPrintDataMatrixSelected.clicked.connect(self.printSelected)
        self.btnOpenBack.clicked.connect(self.open_back)
        self.btnContrLabel.clicked.connect(self.makeLabel_withBack)
        self.tCodes.itemDoubleClicked.connect(self.on_cell_item_clicked)

    def set_connection(self):
        # Открываем базу данных MySQL
        try:
            self.mydb = mysql.connector.connect(
                host=self.dbServer.text(),
                user="btsdba",
                password="masterkey",
                database="dbmarking"
                )

            sql = 'SELECT NAME FROM dbmarking.GOODS;'



            self.cursor = self.mydb.cursor()
            self.cursor.execute(sql)
            self.result = self.cursor.fetchall()

            for t in self.result:
                self.cbGoods.addItem(t[0])

            self.cbGoods.setCurrentIndex(18)


            self.model = QStandardItemModel()
            self.model.setColumnCount(len(self.result[0]))
            for row in self.result:
                line = []
                for item in row:
                    line.append(QStandardItem(str(item)))
                self.model.appendRow(line)
            self.tv.setModel(self.model)
            #!!!self.tv.hideCollumn
            self.tv.resizeColumnsToContents()


            return True
        except:
            print('!!!!!!!!!!!!!!')
            return False

    def open_back(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","PNG files (*.png);;JPG files (*.jpg);;All Files (*)", options=options)
        #fileName = 'E:/DM/pivo_blank.png'
        if fileName:
            self.back = fileName
            self.leBack.setText(self.back)
            #print(fileName)

    def makeLabel_withBack(self):
        start = time()
        self.progress_bar.setFixedSize(self.geometry().width() - 120, 16)
        self.progress_bar.show()
        if self.back:
            back = Image.open(self.back)
        else:
            #back = Image.new(mode = "RGB", size=(int(self.leWidth_px.text())+5,int(self.leHeight_px.text())+5), color=(255,255,255,100))
            back = Image.new(mode = "RGB", size=(40,40), color=(255,255,255,100))
        count = 0
        for code in self.codes:
            encoder = DataMatrixEncoder(code.gs1dm)
            encoder.save('tmp.png')
            with Image.open('tmp.png') as encoder:
                encoder.load()
            barcode_size_px = (215, 215)
            barcode_position_px = (708, 470)
            picture = back
            picture.paste(encoder.resize(barcode_size_px), barcode_position_px)
            picture.save(self.outpath+'\\'+str(count+1).zfill(len(str(len(self.codes))))+'.png')
            #picture.show()
            self.progress_bar.setValue(int(count/len(self.codes)*100))
            count += 1

        self.progress_bar.setValue(100)
        self.progress_bar.hide()
        self.statusBar().showMessage(f'Готово! Время на подготовку кодов: {round(time()-start,2)}сек. Обработано кодов: {len(self.codes)}', 0)

    def on_cell_item_clicked(self, item):
        #print(item.text())
        print(item.row())

    def changeThemes(self):
        f = open(f'sources\\{self.cbThemes.currentText()}.qss', 'r')
        self.styleData = f.read()
        f.close()
        self.setStyleSheet(self.styleData)

    def changePrinter(self):
        self.printer.set_queue(self.cbPrinter.currentIndex())

    def get_orientation(self):
        if self.cbDMRotate.currentIndex()==0:
            return 'N'
        elif self.cbDMRotate.currentIndex()==1:
            return 'R'
        elif self.cbDMRotate.currentIndex()==2:
            return 'I'
        elif self.cbDMRotate.currentIndex()==3:
            return 'B'

    def printSelected(self):
       

        '''
            sti = QStandardItemModel()#(parent=window)
            ico  = ['','','','']
            lst1 = ['Perl', 'PHP', 'Python', 'Ruby']
            lst2 = ['http://www.perl.org/', 'http://php.net/',
                    'https://www.python.org/', 'https://www.ruby-lang.org/']

            for row in range(0, 4):
                item1 = QStandardItem(ico[row])
                item2 = QStandardItem(lst1[row])
                item3 = QStandardItem(lst2[row])
                sti.appendRow([item1, item2, item3])
            sti.setHorizontalHeaderLabels(['Значок', 'Название', 'Сайт'])
            self.tv.setModel(sti)
            self.tv.setColumnWidth(0, 50)
            self.tv.setColumnWidth(2, 180)
            #self.tv.show()
            '''

        #db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        #db.setHostName("10.144.10.75")
        #db.setDatabaseName("dbmarking")
        #db.setUserName("btsdba")
        #db.setPassword("masterkey")
        #db.open()

        
        '''
        rows=[]
        #print(self.tCodes.selectedIndexes())
        for i in self.tCodes.selectionModel().selectedRows():
            idx = int(i.row())
            print(self.tCodes[x].dmgs1)
        #for idx in self.tCodes.selectedIndexes():
        #    rows.append(idx.row())
        
        #print(list(set(rows)))
        '''

    def zebraPrintDM(self,code,text=False):
        pass

    def printDMCode(self):
        #LEFT = '80'
        #TOP = '80'
        #ORIENTATION = ''
        #HEIGHT = '4'
        #QUALITY = '200'
        #GS = ''
        self.printer.LEFT = self.leLeft.text()
        self.printer.TOP = self.leTop.text()
        self.printer.HEIGHT = self.cbDMHeight.currentText()
        self.printer.QUALITY = self.cbDMQuality.currentText().split(' ')[1]
        self.printer.ORIENTATION = self.get_orientation()

        for i in range(len(self.codes)):
            self.printer.make_label(self.codes[i].gs1dm)
            print(self.printer.label)
            #self.printer.print_label(self.printer.label)

    def replace_n(self,a):
        return a.replace('\n','')

    def readKcodesclick(self):
        #!!!!!!!!!! Что делать если уже есть коды аггрегации в таблице
        start = time()
        order = Order(self)
        self.KCodes = []
        options = QFileDialog.Options()
        options |= QFileDialog.ExistingFiles   # включение множественного выбора
        fileNames, _ = QFileDialog.getOpenFileNames(self,"Выбор файлов с кодами упаковок...", "","CSV Files (*.csv);;TXT Files (*.txt);;All Files (*)", options=options)#.selectedFiles()
        count_files = 0
        if fileNames:
            
            self.progress_bar.setFixedSize(self.geometry().width() - 120, 16)
            self.progress_bar.show()

            for fileName in fileNames:
                count_files += 1
                
                with open(fileName, "r", encoding='utf-8') as file:
                    data = file.readlines()
                self.KCodes += map(self.replace_n,data)
            self.progress_bar.setValue(min(int(count_files/len(fileNames))*100+10,100))
            self.progress_bar.hide()
            self.statusBar().showMessage(f'Готово! Время на считывание кодов: {round(time()-start,2)}сек. Считано кодов: {len(order.win.codes)}', 0)
            self.tCodes.horizontalHeaderItem(3).setTextAlignment(Qt.AlignHCenter)
            ind = 0
            for K in self.KCodes:
                for i in range(self.sbPack.value()):
                    if ind+i<len(self.codes):
                        self.codes[ind].Kcode = K

                        self.tCodes.setItem(ind , 0, QTableWidgetItem('Агрегирован'))
                
                        self.tCodes.setItem(ind , 3, QTableWidgetItem(str(K)))
                        self.tCodes.update()
                    ind += 1    

            '''for ind,dm in enumerate(self.codes):
                K = self.KCodes[0]
                if (ind+1) % self.sbPack.value() == 0:  #!!!!!!!!!!!!!!!!!!!! Если кодов меньше?
                    if len(self.KCodes)>0:
                        self.KCodes.remove(K)
                    else:
                        break
                if len(self.codes) - ind>= self.sbPack.value():
                    dm.Kcode = self.KCodes[0]
                    self.KNumber.display('-')
                    self.tCodes.setItem(ind , 0, QTableWidgetItem('Агрегирован'))
            
                    self.tCodes.setItem(ind , 3, QTableWidgetItem(str(dm.Kcode)))
                    self.tCodes.update()'''
                
            self.tCodes.resizeColumnsToContents()
            '''if len(self.KCodes)>0:
                with open('Остатки (ГРУППОВАЯ).txt', "w", encoding='utf-8') as file:
                    for item in self.KCodes:
                        file.write("%s\n" % item)
                self.statusBar().showMessage(f'Агрегация завершена! Список немаркированных кодов сохранен в файле "Остатки (ГРУППОВАЯ).txt"', 0)
            else:
                self.statusBar().showMessage(f'Агрегация завершена!', 0)'''


    def readPcodesclick(self):
        start = time()
        order = Order(self)
        self.KCodes = []
        options = QFileDialog.Options()
        options |= QFileDialog.ExistingFiles   # включение множественного выбора
        fileNames, _ = QFileDialog.getOpenFileNames(self,"Выбор файлов с кодами упаковок...", "","CSV Files (*.csv);;TXT Files (*.txt);;All Files (*)", options=options)#.selectedFiles()
        count_files = 0
        if fileNames:
            
            self.progress_bar.setFixedSize(self.geometry().width() - 120, 16)
            self.progress_bar.show()

            for fileName in fileNames:
                count_files += 1
                
                with open(fileName, "r", encoding='utf-8') as file:
                    data = file.readlines()
                self.KCodes += map(self.replace_n,data)
            self.progress_bar.setValue(min(int(count_files/len(fileNames))*100+10,100))
            self.progress_bar.hide()
            self.statusBar().showMessage(f'Готово! Время на считывание кодов: {round(time()-start,2)}сек. Считано кодов: {len(order.win.codes)}', 0)


    def makeBarcodeclick(self):
        Kbarcodes = set()
        Pbarcodes = set()
        for code in self.codes:
            if code.Kcode not in Kbarcodes:
                Kbarcodes.add(code.Kcode)
            if code.Pcode not in Pbarcodes:
                Pbarcodes.add(code.Pcode)
        if len(Kbarcodes)>0:
            self.progress_bar.setFixedSize(self.geometry().width() - 250, 16)
            self.progress_bar.show()
            self.statusBar().showMessage("Генерация кодов упаковки. Ожидайте...", 0)
            count = 1
            #try:
            start = time()
            if not os.path.exists(self.outpath):
                os.mkdir(self.outpath)
            for code in Kbarcodes:
                image = generate_barcode(
                    barcode_type='code128',  # One of the supported codes.
                    data=code, 
                    ) 
                image.convert('1').save(self.outpath+'\\K'+str(count).zfill(len(str(len(Kbarcodes))))+'.png')
                
                
                #generator.print()
                self.progress_bar.setValue(int(count/len(Kbarcodes)*100))
                count += 1    
            count = 1
            for code in Pbarcodes:
                image = generate_barcode(
                    barcode_type='code128',  # One of the supported codes.
                    data=code, 
                    ) 
                image.convert('1').save(self.outpath+'\\P'+str(count).zfill(len(str(len(Pbarcodes))))+'.png')
                
                
                #generator.print()
                self.progress_bar.setValue(int(count/len(Pbarcodes)*100))
                count += 1    

            self.progress_bar.hide()
            self.statusBar().showMessage("Генерация кодов упаковок завершена успешно. Время на обработку: "+str(round(time()-start,2)), 0)        


    def readcodesclick(self):
        self.gbSettings.hide()
        self.gbWork.show()

    def set_source(self):
        self.outpath = QFileDialog.getExistingDirectory(self,"Выбрать папку для сохранения изображений...",".")
        if self.outpath:
            self.leOutPath.setText(self.outpath)

    def makeDMPNG(self):
        if len(self.codes)>0:
            self.progress_bar.setFixedSize(self.geometry().width() - 120, 16)
            self.progress_bar.show()
            self.statusBar().showMessage("Генерация кодов. Ожидайте...", 0)
            count = 1
            #try:
            start = time()
            if not os.path.exists(self.outpath):
                os.mkdir(self.outpath)
            
            for code in self.codes:
                encoder = DataMatrixEncoder(code.gs1dm)
                encoder.save(self.outpath+'\\'+str(count).zfill(len(str(len(self.codes))))+'_.png')
                
            
                '''generator = barcode.generation.BarcodeGenerator(barcode.generation.EncodeTypes.DATA_MATRIX, code.gs1dm)
                # Сгенерировать штрих-код Datamatrix
                generator.save(self.outpath+'\\'+str(count).zfill(len(str(len(self.codes))))+'.png')
                #generator.print()'''
                self.progress_bar.setValue(int(count/len(self.codes)*100))
                count += 1    

            self.progress_bar.hide()
            self.statusBar().showMessage("Генерация кодов DataMatrix завершена успешно. Время на обработку: "+str(round(time()-start,2)), 0)        

    def settingsclick(self):
        self.settingsWindow = Settings(self)
        self.settingsWindow.show()
        self.gbWork.hide()
        #self.gbGoods.hide()
        self.gbSettings.show()


    def aggregation(self):
        self.tCodes.setColumnCount(5)
        # Set the table headers
        self.tCodes.setHorizontalHeaderLabels(["Статус", "Код Datamatrix","Контроль","Код упаковки","Код паллеты"])
        #Set the tooltips to headings
        self.tCodes.horizontalHeaderItem(2).setToolTip("Информация о корректности считанного кода Datamatrix")
        self.tCodes.horizontalHeaderItem(1).setToolTip("Содержание считанного кода Datamatrix")
        self.tCodes.horizontalHeaderItem(0).setToolTip("Статус кода Datamatrix")
        self.tCodes.horizontalHeaderItem(3).setToolTip("Этикетка для нанесения на упаковку")
        self.tCodes.horizontalHeaderItem(4).setToolTip("Этикетка для нанесения на паллету")
        
        # Set the alignment to the headers
        self.tCodes.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.tCodes.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.tCodes.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)
        self.tCodes.horizontalHeaderItem(3).setTextAlignment(Qt.AlignHCenter)
        self.tCodes.horizontalHeaderItem(4).setTextAlignment(Qt.AlignHCenter)
        i = 0
        K = self.KNumber.value()
        P = self.PNumber.value()
        Y = str(self.deDate.date().year())[-2:].zfill(6)
        for ind,dm in enumerate(self.codes):
            #print(ind)
            if (ind+1) % self.sbPack.value() == 0:
                K += 1
                self.KNumber.setValue(K)
            if (ind+1) % (self.sbPack.value()*self.sbPallet.value()) == 0:
                P += 1
                self.PNumber.setValue(P)
            if (len(self.codes)-ind+1)>=self.sbPack.value():
                dm.Kcode = str(self.leAggPrefix.text())+'K'+Y+str(K).zfill(8)
                self.tCodes.setItem(ind , 0, QTableWidgetItem('Агрегирован'))
            else:
                dm.Kcode = ''
            if dm.Kcode != '':
                dm.Pcode = str(self.leAggPrefix.text())+'P'+Y+str(P).zfill(8)
            else:
                dm.Pcode = ''                

            self.tCodes.setItem(ind , 3, QTableWidgetItem(str(dm.Kcode)))
            self.tCodes.setItem(ind , 4, QTableWidgetItem(str(dm.Pcode)))
            self.tCodes.update()                
        self.tCodes.resizeColumnsToContents()
        
    def getClickedCell(self, row, column):
        self.tCodes.clearSelection()
        row_num = self.tCodes.currentRow()
        self.tCodes.selectRow(row_num)
        #self.tCodes.setCurrentIndex(row_num)

        self.lbDmImage.setScaledContents(True)

    def startselection(self):
        self.tCodes.clearSelection()
        
    def export_csv(self):
        if len(self.codes)>0:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self,"Сохранение отчета ...", "","CSV Files (*.csv);;All Files (*)", options=options)#.selectedFiles()
            if fileName:
                with open(fileName, "w") as file:
                    for line in self.codes:   
                        if line.Kcode != '':
                            file.write(line.gs1dm+' '+line.Kcode+' '+line.Pcode+'\n')
                        else:
                            file.write(line.gs1dm+'\n')

    def csvimport(self):
        start = time()
        order = Order(self)
        options = QFileDialog.Options()
        options |= QFileDialog.ExistingFiles   # включение множественного выбора
        #options |= QFileDialog.DontUseNativeDialog
        fileNames, _ = QFileDialog.getOpenFileNames(self,"Выбор файлов с кодами...", "","CSV Files (*.csv);;TXT Files (*.txt);;All Files (*)", options=options)#.selectedFiles()
        count_files = 0
        if fileNames:
            self.progress_bar.setFixedSize(self.geometry().width() - 120, 16)
            self.progress_bar.show()
            #self.statusBar().showMessage("Генерация кодов", 0)


            for fileName in fileNames:
                order.input_file = fileName
                count_files += 1
                #self.btnStop.show()
                order.import_csv()
                self.progress_bar.setValue(min(int(count_files/len(fileNames))*100+10,100))
            self.progress_bar.hide()
            self.statusBar().showMessage(f'Готово! Время на считывание кодов: {round(time()-start,2)}сек. Считано кодов: {len(order.win.codes)}', 0)
        
    def createdm(self,code):
        if code.control_code != '':
            datamatrix = generate_barcode(
                barcode_type='gs1datamatrix',
                data=f"(01){code.gtin}(21){code.serial_number}(93){code.control_code}",
                options={"parsefnc": True, "format": "square", "version": "26x26"})
        else:
            datamatrix = generate_barcode(
                barcode_type='gs1datamatrix',
                data=code.gs1dm,
                options={"parsefnc": True, "format": "square", "version": "26x26"})
        
        # Create white picture
        picture_size_px = (datamatrix.width+4, datamatrix.height+4)
        picture = Image.new('L', picture_size_px, color='white')
        # Position the datamatrix
        barcode_position_px = (2, 2)
        picture.paste(datamatrix, barcode_position_px)
        #qimage = QImage(datamatrix.tobytes(), datamatrix.width, datamatrix.height, QImage.Format_Grayscale8)
        
        qimage = QImage(picture.tobytes(), picture.width, picture.height, QImage.Format_Grayscale8)
        picture = QPixmap.fromImage(qimage)

        return picture

    def pdfimport(self):
        self.pfdimportWindow = PdfPreview(self)
        self.pfdimportWindow.show()
        
        '''
        start = time()
        order = Order(self)
        options = QFileDialog.Options()
        options |= QFileDialog.ExistingFiles   # включение множественного выбора
        #options |= QFileDialog.DontUseNativeDialog
        fileNames, _ = QFileDialog.getOpenFileNames(self,"Выбор файлов с кодами...", "","PDF Files (*.pdf);;All Files (*)", options=options)#.selectedFiles()
        count_files = 0
        if fileNames:
            self.statusBar().showMessage('Ожидайте...',0) 

            for fileName in fileNames:
                order.input_file = fileName
                count_files += 1
                order.convert_pdf()
            
            self.statusBar().showMessage(f'Готово! Время на считывание кодов: {round(time()-start,2)}сек. Считано кодов: {len(order.win.codes)}', 0)
        '''
            

class Order():
    def __init__(self,win):
        self.dir = os.getcwd()
        self.input_file = ''
        self.repaired = 0
        self.win = win

    def convert_pdf(self, pages: Tuple = None):


        #   Необходимо вынести на форму настройку параметров 
        zoom = (1, 1)
        delta = (0, 0)
        matrix = (1, 1)
        anchor = (0, 0)
        size = (100, 172)

        pdfIn = fitz.open(self.input_file)


        self.win.progress_bar.setFixedSize(self.win.geometry().width() - 120, 16)
        self.win.progress_bar.show()
        self.win.tCodes.clear()
        self.win.tCodes.setRowCount(0)
        self.win.tCodes.setColumnCount(5)
         # Set the table headers
        self.win.tCodes.setHorizontalHeaderLabels(["Статус", "Код Datamatrix", "Контроль","Код упаковки","Код паллеты"])
         #Set the tooltips to headings
        self.win.tCodes.horizontalHeaderItem(2).setToolTip("Информация о корректности считанного кода Datamatrix")
        self.win.tCodes.horizontalHeaderItem(1).setToolTip("Содержание считанного кода Datamatrix")
        self.win.tCodes.horizontalHeaderItem(0).setToolTip("Статус кода Datamatrix")
        self.win.tCodes.horizontalHeaderItem(3).setToolTip("Этикетка для нанесения на упаковку")
        self.win.tCodes.horizontalHeaderItem(4).setToolTip("Этикетка для нанесения на паллету")
        
         # Set the alignment to the headers
        self.win.tCodes.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.win.tCodes.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.win.tCodes.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)
        self.win.tCodes.horizontalHeaderItem(3).setTextAlignment(Qt.AlignHCenter)
        self.win.tCodes.horizontalHeaderItem(4).setTextAlignment(Qt.AlignHCenter)

        self.win.codes.clear()

        #Преобразует PDF в изображение и создает файл за страницей
        for pg in range(pdfIn.page_count):
        #for pg in range(1):
            if str(pages) != str(None):
                if str(pg) not in str(pages):
                    continue
            page = pdfIn[pg]
            #rotate = int(0)
            # PDF Страница конвертируется в целое изображение 1056 * 816, а затем для каждого изображения делается снимок экрана.
            # zoom = 1.33333333 -----> Размер изображения = 1056 * 816
            # zoom = 2 ---> 2 * Разрешение по умолчанию (текст четкий, текст изображения плохо читается) = маленький размер файла/размер изображения = 1584 * 1224
            # zoom = 4 ---> 4 * Разрешение по умолчанию (текст четкий, текст изображения плохо читается) = большой размер файла
            # zoom = 8 ---> 8 * Разрешение по умолчанию (текст четкий, текст изображения читается) = большой размер файла
            # Коэффициент масштабирования 8, чтобы текст был четким   
            
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom[0], zoom[1]), alpha=False)
            pix.save(os.path.join(self.dir,'tmp.png'))
            #output_file = f"{os.path.splitext(os.path.basename(self.input_file))[0]}_page{pg+1}.png"

            img_page = Image.open('tmp.png')
            self.win.tCodes.hide()
            # ------WORK WITH PDF --------------------------------------------
            for i in range(matrix[0]):
                for j in range(matrix[1]):
                    if not self.win.stop:
                        cr_left = anchor[0]+(size[0]+delta[0])*j
                        cr_top = anchor[1]+(size[1]+delta[1])*i
                        cr_right = cr_left + size[0]
                        cr_bottom = cr_top + size[1]
                        #output_file = f"{os.path.splitext(os.path.basename(self.input_file))[0]}_page{pg+1}_pic"+str(i+1)+str(j+1)+".png"
                        
                        #img.crop((cr_left, cr_top, cr_right, cr_bottom)).show()#.save(output_file, quality=100)
                        
                        try:
                            image = img_page.crop((cr_left, cr_top, cr_right, cr_bottom))
                            dm = DataMatrix.Datamatrix(bytes.decode(decode(image)[0].data),self.win.goods)

                            rowPosition = self.win.tCodes.rowCount()
                            self.win.tCodes.insertRow(rowPosition)
                            self.win.tCodes.setItem(rowPosition , 2, QTableWidgetItem(str(dm.control)))
                            self.win.tCodes.setItem(rowPosition , 1, QTableWidgetItem(str(dm.gs1dm)))
                            self.win.tCodes.setItem(rowPosition , 0, QTableWidgetItem("Прочитан"))
                            self.win.codes.append(dm)                                
                            self.win.progress_bar.setValue(int(rowPosition/(pdfIn.page_count*matrix[0]*matrix[1])*100))
                        except:
                            self.win.statusBar().showMessage(f'Ошибка конвертации файла {pdfIn}',5)
                    else:
                        
                        break     
        self.win.progress_bar.hide()            
        self.win.tCodes.update()
        self.win.tCodes.show()
        self.stop = False
        pdfIn.close()
        self.win.tCodes.resizeColumnsToContents()
        self.win.tCodes.resizeRowsToContents()


    def import_csv(self):
        digits = '0123456789'
        with open(self.input_file, "r", encoding='utf-8') as file:
            data = file.readlines()
        self.win.tCodes.clear()
        self.win.tCodes.setRowCount(0)
        self.win.codes.clear()
        self.win.tCodes.setColumnCount(5)
         # Set the table headers
        self.win.tCodes.setHorizontalHeaderLabels(["Статус", "Код Datamatrix","Контроль" ,"Код упаковки","Код паллеты"])
         #Set the tooltips to headings
        self.win.tCodes.horizontalHeaderItem(2).setToolTip("Информация о корректности считанного кода Datamatrix")
        self.win.tCodes.horizontalHeaderItem(1).setToolTip("Содержание считанного кода Datamatrix")
        self.win.tCodes.horizontalHeaderItem(0).setToolTip("Статус кода Datamatrix")
        self.win.tCodes.horizontalHeaderItem(3).setToolTip("Этикетка для нанесения на упаковку")
        self.win.tCodes.horizontalHeaderItem(4).setToolTip("Этикетка для нанесения на паллету")
        
         # Set the alignment to the headers
        self.win.tCodes.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.win.tCodes.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.win.tCodes.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)
        self.win.tCodes.horizontalHeaderItem(3).setTextAlignment(Qt.AlignHCenter)
        self.win.tCodes.horizontalHeaderItem(4).setTextAlignment(Qt.AlignHCenter)
        for line in data:
            try:
                if line[1] in digits:
                    line = line.replace('\n','') 
                    if len(line)>=37 and line[0]=='"':
                        line = line[1:line.find('",')]
                        
                    dm = DataMatrix.Datamatrix(line,self.win.goods)
                    rowPosition = self.win.tCodes.rowCount()
                    self.win.tCodes.insertRow(rowPosition)

                    self.win.tCodes.setItem(rowPosition , 2, QTableWidgetItem(dm.control))
                    #self.generate()

                    
                    self.win.codes.append(dm)
                    
                    self.win.tCodes.setItem(rowPosition , 1, QTableWidgetItem(str(dm.gs1dm)))
                    self.win.tCodes.setItem(rowPosition , 0, QTableWidgetItem('Прочитан'))
                    self.win.tCodes.update()
                        
                    self.progress_bar.setValue(int(rowPosition/len(data)*100))
                                
            except:
                pass
        self.win.tCodes.resizeColumnsToContents()
        self.win.tCodes.resizeRowsToContents()







style = '''
QWidget {
    background-color: #12B39A;
}

QGroupBox {
    background-color: #12B39A;
    border: None;               
    border-radius: 2px;
    margin-top: 10px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top center;
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 2px;
}

QFrame {
    background-color: #017069;
    border: None;               
}
#frameTop {
    border-top-left-radius:  20%;
    border-top-right-radius:  20%;
}
#frameLeft {
    border-top-left-radius:  20%;
    border-bottom-left-radius:  20%;
}
#frameRight {
    border-top-right-radius:  20%;
    border-bottom-right-radius:  20%;
}
#frameBottom {
    border-bottom-left-radius:  20%;
    border-bottom-right-radius:  20%;
}

QPushButton {
    color: #017069; 
}

'''




def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MyApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    #app.exec_()  # и запускаем приложение

    sys.exit(app.exec_())



if __name__ == "__main__":
    main()

#Decoded(data=b'0104810268050169212mzgp6C593L&V1', rect=Rect(left=9, top=10, width=120, height=119))    