#from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QProgressBar, QApplication, QFileDialog
#from PyQt5.QtGui import QPixmap # оптимизированная для показа на экране картинки
#from PyQt5.QtCore import Qt # нужна константа Qt.KeepAspectRatio для изменения размеров с сохранением пропорций

from PIL import Image, ImageDraw, ImageFont, ImageWin
#import numpy as np
#from pystrich.datamatrix import DataMatrixEncoder
from time import time
import treepoem 
#from time import sleep
import win32print
import win32ui
import aspose.barcode as barcode

#from pydmtx import DataMatrix
#import pandas as pd

import mwin, os, sys  # sys нужен для передачи argv в QApplication


class MyApp(QMainWindow, mwin.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()

        self.dir = os.getcwd()+'/'
        self.csv_file = ''
        self.codeslist = []
        self.back = ''
        self.outpath = os.getcwd()+'\\code'
        self.left = 0
        self.top = 0
        self.textlabel_visible = False
        self.scale = 0
        self.read_file =  False

        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0,100)
        self.statusBar().addPermanentWidget(self.progress_bar)
        self.progress_bar.hide()


        self.sbScale.valueChanged.connect(self.set_zoom)
        self.btnOpenSource.clicked.connect(self.read_codes)
        self.btnOpenBack.clicked.connect(self.read_back)
        self.btnOpenFolder.clicked.connect(self.set_source)
        self.btnMakeSticker.clicked.connect(self.make_sticker)
        self.cbText.stateChanged.connect(self.text_checked)
        self.btnView.clicked.connect(self.view_sticker)
        self.leLeft.textChanged.connect(self.set_margins)
        self.leTop.textChanged.connect(self.set_margins)
        self.codes.textChanged.connect(self.set_listcodes)
        self.cbGroupPrint.stateChanged.connect(self.set_groupPrint)
        self.leOutPath.textChanged.connect(self.set_outpath)
        self.leLeft.setText(str(self.left))
        self.leTop.setText(str(self.top))
        self.sbScale.setValue(4)
        self.scale = self.sbScale.value()
        self.leOutPath.setText(self.outpath)



    def set_outpath(self):
        if self.leOutPath.text() != '':
            self.outpath = self.leOutPath.text().strip()
        

    def set_groupPrint(self):
        self.sbCodeCount.setEnabled(self.cbGroupPrint.isChecked())


    def set_listcodes(self):
        if not self.read_file:
            self.codeslist = self.codes.toPlainText().split('\n')

    def set_zoom(self):
        if self.sbScale.value() == 1:
            self.leWidth_px.setText ('40')
            self.leHeight_px.setText ('40')
            self.leWidth_cm.setText ('3')
            self.leHeight_cm.setText ('3')
            self.sbFontSize.setValue(4)
        elif self.sbScale.value() == 2:
            self.leWidth_px.setText ('80')
            self.leHeight_px.setText ('80')
            self.leWidth_cm.setText ('8')
            self.leHeight_cm.setText ('8')
            self.sbFontSize.setValue(9)
        elif self.sbScale.value() == 3:
            self.leWidth_px.setText ('120')
            self.leHeight_px.setText ('120')
            self.leWidth_cm.setText ('11')
            self.leHeight_cm.setText ('11')
            self.sbFontSize.setValue(14)
        elif self.sbScale.value() == 4:
            self.leWidth_px.setText ('160')
            self.leHeight_px.setText ('160')
            self.leWidth_cm.setText ('15')
            self.leHeight_cm.setText ('15')
            self.sbFontSize.setValue(18)
        elif self.sbScale.value() == 5:
            self.leWidth_px.setText ('200')
            self.leHeight_px.setText ('200')
            self.leWidth_cm.setText ('19')
            self.leHeight_cm.setText ('19')
            self.sbFontSize.setValue(21)
        elif self.sbScale.value() == 6:
            self.leWidth_px.setText ('240')
            self.leHeight_px.setText ('240')
            self.leWidth_cm.setText ('23')
            self.leHeight_cm.setText ('23')
            self.sbFontSize.setValue(24)
        elif self.sbScale.value() == 7:
            self.leWidth_px.setText ('280')
            self.leHeight_px.setText ('280')
            self.leWidth_cm.setText ('27')
            self.leHeight_cm.setText ('27')
            self.sbFontSize.setValue(28)
        elif self.sbScale.value() == 8:
            self.leWidth_px.setText ('320')
            self.leHeight_px.setText ('320')
            self.leWidth_cm.setText ('30')
            self.leHeight_cm.setText ('30')
            self.sbFontSize.setValue(32)
        elif self.sbScale.value() == 9:
            self.leWidth_px.setText ('360')
            self.leHeight_px.setText ('360')
            self.leWidth_cm.setText ('35')
            self.leHeight_cm.setText ('35')
            self.sbFontSize.setValue(38)
        elif self.sbScale.value() == 10:
            self.leWidth_px.setText ('400')
            self.leHeight_px.setText ('400')
            self.leWidth_cm.setText ('38')
            self.leHeight_cm.setText ('38')
            self.sbFontSize.setValue(42)
        self.scale = self.sbScale.value()


    def read_codes(self):
        self.read_file = True
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","CSV Files (*.csv);;All Files (*)", options=options)
        if fileName:
            try:
                self.csv_file = fileName
                self.leSource.setText(str(self.csv_file))
                with open(self.csv_file, 'r') as file:
                    self.codeslist = file.readlines()
                print(self.codeslist)
                self.codes.clear()  #______________________
                self.codes.setText(''.join(self.codeslist))
                self.statusbar.showMessage(f'Успешно считано {len(self.codeslist)} кодов...',5000)
            except:
                self.statusbar.showMessage('Ошибка. Файл не может быть декодирован...',5000)
        self.read_file = False

    def read_back(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","PNG Files (*.png);;All Files (*)", options=options)
        if fileName:
            self.back = fileName
            self.leBack.setText(self.back)

    def set_source(self):
        self.outpath = QFileDialog.getExistingDirectory(self,"Выбрать папку для сохранения изображений...",".")
        if self.outpath:
            self.leOutPath.setText(self.outpath)

    def text_checked(self):
        self.textlabel_visible = self.cbText.isChecked()
        self.sbFontSize.setEnabled(self.textlabel_visible)
    
    def make_sticker(self):
        if len(self.codeslist)>0:
            self.progress_bar.setFixedSize(self.geometry().width() - 120, 16)
            self.progress_bar.show()
            self.statusBar().showMessage("Генерация кодов", 0)
            blankCode = Image.open(self.dir+'/spacer.png')

            #font1 = ImageFont.truetype('sources/fonts/Roboto-Bold.ttf', size=20)
            fontLabel = ImageFont.truetype('c:/windows/fonts/arialnb.ttf', size=self.sbFontSize.value())    
            count = 0
            #try:
            start = time()
            if not os.path.exists(self.outpath):
                os.mkdir(self.outpath)
            for code in self.codeslist:
                if len(code.replace(' ',''))>0:
                    if self.back:
                        back = Image.open(self.back)
                    else:
                        #back = Image.new(mode = "RGB", size=(int(self.leWidth_px.text())+5,int(self.leHeight_px.text())+5), color=(255,255,255,100))
                        back = Image.new(mode = "RGB", size=(40,40), color=(255,255,255,100))
                    #image = treepoem.generate_barcode(barcode_type='datamatrix',data=code,scale=self.scale,) +++++++
                    '''
                    image = treepoem.generate_barcode(barcode_type='datamatrix',data=code,scale=1,) 
                    if self.cbRotate.isChecked():
                        image.rotate(90)
                    image.convert('1').save('tmp.png')
                    #imcode = Image.open('tmp.png')
                    back.paste(image, (self.left, self.top))
                    if self.textlabel_visible:
                        draw_text = ImageDraw.Draw(back)
                        draw_text.text((self.left, self.top+image.size[1]+20),code[:19],fill='black',font=fontLabel)
                        draw_text.text((self.left, self.top+image.size[1]+int(self.sbFontSize.value())+25),code[19:],fill='black',font=fontLabel)
                    back.save(self.outpath+'\\'+str(count).zfill(len(str(len(self.codeslist))))+'.png', quality=100)  #!!!!!!!!!!!!!!!!!!!!
                        #self.statusbar.showMessage(str(count).zfill(len(str(len(self.codeslist))))+'.png - Ok...',1000)
                    if self.cbPrint.isChecked():
                        self.print_sticker_code(self.outpath+'\\'+str(count).zfill(len(str(len(self.codeslist))))+'.png')
                        '''
                    # Инициализировать объект класса BarcodeGenerator
                    generator = barcode.generation.BarcodeGenerator(barcode.generation.EncodeTypes.DATA_MATRIX, code)
                    # Сгенерировать штрих-код Datamatrix
                    generator.save(self.outpath+'\\'+str(count).zfill(len(str(len(self.codeslist))))+'.png')
                    #generator.print()
                    if self.cbPrint.isChecked():
                        self.print_sticker_code(self.outpath+'\\'+str(count).zfill(len(str(len(self.codeslist))))+'.png')
                    count += 1
                    #print(count)
                    if self.cbBlankPrint.isChecked() and count % self.sbCodeCount.value() == 0 and count > 0: 
                        #self.print_sticker_code(Image.new(mode = "RGB", size=(1,1), color=(255,255,255,100)))
                        blankCode.save(self.outpath+'\\'+str(count).zfill(len(str(len(self.codeslist))))+'b.png')
                        if self.cbPrint.isChecked():
                            self.print_sticker_code(self.outpath+'\\'+str(count).zfill(len(str(len(self.codeslist))))+'b.png')

                        #print('spacer')
                    self.progress_bar.setValue(int(count/len(self.codeslist)*100))    

            end = time()
            t = end - start
            self.progress_bar.hide()
            self.statusBar().showMessage("Генерация кодов DataMatrix завершена успешно. Время на обработку: "+str(round(t,2)), 0)

            #except:
            #    self.statusbar.showMessage('Ошибка. Проверьте настройки программы...',5000)
        else:
            self.statusbar.showMessage('Отсутствуют данные для обработки...',5000)

    def view_sticker(self):
        #if len(self.codeslist) >0:
            fontLabel = ImageFont.truetype('c:/windows/fonts/arialnb.ttf', size=self.sbFontSize.value())
            testcode = b'\x1D'+'0105200120690210215mk.3UOWO%knt'+chr(29)+'93VgDi'
            image = treepoem.generate_barcode(barcode_type='datamatrix',data=testcode,scale=self.scale,) 
            image.convert('1').save('D:/tmp.png')
            imcode = Image.open('D:/tmp.png')
            imcode.show()
            # Инициализировать объект класса BarcodeGenerator
            generator = barcode.generation.BarcodeGenerator(barcode.generation.EncodeTypes.DATA_MATRIX, testcode)
            # Сгенерировать штрих-код Datamatrix
            generator.save('D:/tmp.png')
            imcode = Image.open('D:/tmp.png')

            if len(self.leBack.text())>0:
                back = Image.open(self.back)
                back.paste(imcode, (self.left, self.top))
            else:
                back = Image.new(mode = "RGB", size=(int(self.leWidth_px.text())+5,int(self.leHeight_px.text())+5), color=(255,255,255,100))
                back.paste(imcode, (self.left, self.top))
            if self.textlabel_visible:
                draw_text = ImageDraw.Draw(back)
                draw_text.text((self.left, self.top+imcode.size[1]+20),testcode[:19],fill='black',font=fontLabel)
                draw_text.text((self.left, self.top+imcode.size[1]+int(self.sbFontSize.value())+25),testcode[19:],fill='black',font=fontLabel)
            imcode.show()
        #else:
            #self.statusbar.showMessage('Отсутствуют данные для обработки...',5000)

    def set_margins(self):
        if self.leLeft.text()!='':
            self.left = int(self.leLeft.text())
        else:
            self.left = 0
        if self.leTop.text()!='':
            self.top = int(self.leTop.text())
        else:
            self.top = 0

    def print_sticker_code(self,file_name):
        # Constants for GetDeviceCaps
        # HORZRES / VERTRES = printable area
        HORZRES = 8
        VERTRES = 10
        
        # LOGPIXELS = dots per inch
        LOGPIXELSX = 88
        LOGPIXELSY = 90
        
        # PHYSICALWIDTH/HEIGHT = total area
        PHYSICALWIDTH = 110
        PHYSICALHEIGHT = 111
        
        # PHYSICALOFFSETX/Y = left / top margin
        PHYSICALOFFSETX = 112
        PHYSICALOFFSETY = 113

        printer_name = win32print.GetDefaultPrinter ()
        #print(printer_name)
        #file_name = "test.jpg"

        #
        # You can only write a Device-independent bitmap
        #  directly to a Windows device context; therefore
        #  we need (for ease) to use the Python Imaging
        #  Library to manipulate the image.
        #
        # Create a device context from a named printer
        #  and assess the printable size of the paper.
        #
        hDC = win32ui.CreateDC ()
        hDC.CreatePrinterDC (printer_name)
        printable_area = hDC.GetDeviceCaps (HORZRES), hDC.GetDeviceCaps (VERTRES)
        printer_size = hDC.GetDeviceCaps (PHYSICALWIDTH), hDC.GetDeviceCaps (PHYSICALHEIGHT)
        printer_margins = hDC.GetDeviceCaps (PHYSICALOFFSETX), hDC.GetDeviceCaps (PHYSICALOFFSETY)

        #
        # Open the image, rotate it if it's wider than
        #  it is high, and work out how much to multiply
        #  each pixel by to get it as big as possible on
        #  the page without distorting.
        #
        bmp = Image.open (file_name)
        if bmp.size[0] > bmp.size[1]:
            bmp = bmp.rotate (90)

        ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
        scale = min (ratios)

        #
        # Start the print job, and draw the bitmap to
        #  the printer device at the scaled size.
        #
        hDC.StartDoc (file_name)
        hDC.StartPage ()

        dib = ImageWin.Dib (bmp)
        scaled_width, scaled_height = [int (scale * i) for i in bmp.size]
        x1 = int ((printer_size[0] - scaled_width) / 2)
        y1 = int ((printer_size[1] - scaled_height) / 2)
        x2 = x1 + scaled_width
        y2 = y1 + scaled_height
        dib.draw (hDC.GetHandleOutput (), (x1, y1, x2, y2))

        hDC.EndPage ()
        hDC.EndDoc ()
        hDC.DeleteDC ()




# Zoom  1 - 40x40
#       2 - 79x79
#       3 - 119x119  
#       4 - 159x159
#       5 - 199x199
#       6 - 238x238 
  
def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MyApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == "__main__":
    main()