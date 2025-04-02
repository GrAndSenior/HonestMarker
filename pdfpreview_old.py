from PyQt5.QtWidgets import QMainWindow, QProgressBar, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QRegExpValidator
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QRegExp
from pylibdmtx.pylibdmtx import decode#, encode
from pandasmodel import PandasModel
from PIL import Image
from time import time
import os
import pandas as pd                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
import pdfimport
import numpy as np
import cv2
import itertools
import fitz


class AutoCropThread(QThread):
    mysignal = pyqtSignal(str)
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.running = False  # Флаг выполнения
        self.parent = parent
    def run(self):
        start = time()
        self.running = True
        self.parent.progress_bar.show()
        self.parent.btnCancel.setText('Остановить')
        pdfIn = fitz.open(self.parent.leFileName.text())
        for pg in range(pdfIn.page_count):
            if self.running:
                img = pdfIn[pg].get_pixmap(matrix=fitz.Matrix(int(self.parent.leZoom_x.text()), int(self.parent.leZoom_y.text())), alpha=False)
                img = np.array(Image.frombytes("RGB", [img.width, img.height], img.samples))
                for i in range(len(self.parent.coords)):
                    if self.parent.dm_decode(img, self.parent.coords[i], self.parent.size):
                        self.parent.data_frame.loc[len(self.parent.data_frame.index)] = self.parent.dm_decode(img, self.parent.coords[i], self.parent.size)
                        if self.parent.gbImageCrop.isChecked():    #  сохранение кодов
                            tmp = img[self.parent.coords[i][0]-2:self.parent.coords[i][0]+self.parent.size[0]+2, self.parent.coords[i][1]-2:self.parent.coords[i][1]+self.parent.size[1]+2]
                            Image.fromarray(tmp).save(os.path.join(self.parent.options['MAIN']['output'], f"page_{pg+1}_code"+str(i+1)+".png"), format='PNG')
                        
                    self.mysignal.emit(str(int(pg/pdfIn.page_count*100))) 
        pdfIn.close()
        self.parent.btnOk.setEnabled(True)
        self.parent.btnOk.setText('OK')
        self.parent.progress_bar.hide()
        self.parent.data_frame = self.parent.data_frame.reset_index()
        del self.parent.data_frame['index']                        
        if self.parent.data_frame["gs1dm"].count() > 0:
            self.parent.statusBar().showMessage(f'Готово! Время на загрузку кодов: {round(time()-start,2)}сек. Получено кодов: {self.parent.data_frame["gs1dm"].count()}', 0)
        self.parent.btnCancel.setText('Отмена')

class ManualCropThread(QThread):
    mysignal = pyqtSignal(str)
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.running = False  # Флаг выполнения
        self.parent = parent
    def run(self):
        start = time()
        self.running = True
        zoom = (int(self.parent.leZoom_x.text()), int(self.parent.leZoom_y.text()))
        size = (int(self.parent.leAreaWidth.text()), int(self.parent.leAreaHeight.text()))
        self.parent.progress_bar.show()
        self.parent.btnCancel.setText('Остановить')
        #Преобразует PDF в изображение и создает файл за страницей
        # PDF Страница конвертируется в целое изображение 1056 * 816, а затем для каждого изображения делается снимок экрана.
        # zoom = 1.33333333 -----> Размер изображения = 1056 * 816
        # zoom = 2 ---> 2 * Разрешение по умолчанию (текст четкий, текст изображения плохо читается) = маленький размер файла/размер изображения = 1584 * 1224
        # zoom = 4 ---> 4 * Разрешение по умолчанию (текст четкий, текст изображения плохо читается) = большой размер файла
        # zoom = 8 ---> 8 * Разрешение по умолчанию (текст четкий, текст изображения читается) = большой размер файла
        # Коэффициент масштабирования 8, чтобы текст был четким   

        pdfIn = fitz.open(self.parent.leFileName.text())
        for pg in range(pdfIn.page_count):
            if self.running:
                img = pdfIn[pg].get_pixmap(matrix=fitz.Matrix(zoom[0], zoom[1]), alpha=False)
                img = np.array(Image.frombytes("RGB", [img.width, img.height], img.samples))
                for i in range(int(self.parent.leRow.text())):
                    for j in range(int(self.parent.leCol.text())):
                        tmp = img[size[1]*i:size[1]*(i+1), size[0]*j:size[0]*(j+1)]
                        tmp = Image.fromarray(tmp)
                        try:
                            self.parent.data_frame.loc[len(self.parent.data_frame.index)] = bytes.decode(decode(tmp)[0].data)
                            if self.parent.gbImageCrop.isChecked():
                                tmp.save(os.path.join(self.parent.options['MAIN']['output'], f"page{pg+1}_code"+str(i+1)+str(j+1)+".png"))
                        except:
                            self.parent.statusBar().showMessage(f'Ошибка конвертации на странице {pg}',5)
                    self.mysignal.emit(str(int(pg/pdfIn.page_count*100))) 
        pdfIn.close()
        self.parent.btnOk.setEnabled(True)
        self.parent.btnOk.setText('OK')
        self.parent.progress_bar.hide()
        self.parent.data_frame = self.parent.data_frame.reset_index()
        self.parent.statusBar().showMessage(f'Готово! Время на загрузку кодов: {round(time()-start,2)}сек. Получено кодов: {self.parent.data_frame["index"].count()}', 0)
        del self.parent.data_frame['index']                        
        self.parent.btnCancel.setText('Отмена')

class PdfPreview(QMainWindow, pdfimport.Ui_PdfPreviewWindow):
    def __init__(self, parent, fileNames, **kwargs) -> None:
        super().__init__(parent)
        self.setupUi(self)  # Это для инициализации  дизайна
        self.parent = parent
        self.fileNames = fileNames
        self.options = self.parent.options
        self.autocrop = AutoCropThread(self)
        self.manualcrop = ManualCropThread(self)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0,100)
        self.statusBar().addPermanentWidget(self.progress_bar)
        self.progress_bar.hide()
        digitRegex = QRegExp('\\d+')
        digitValidator = QRegExpValidator(digitRegex, self)
        self.leRow.setValidator(digitValidator)
        self.leCol.setValidator(digitValidator)
        self.leAreaHeight.setValidator(digitValidator)
        self.leAreaWidth.setValidator(digitValidator)
        self.leZoom_x.setValidator(digitValidator)
        self.leZoom_y.setValidator(digitValidator)
        self.leFileName.setText(self.fileNames[0])
        #self.gbPdfFile.setVisible(False)
        print(self.lbImage.width(), self.lbImage.height())
        self.lbImage.setGeometry(1,1,571,843)
        
        self.btnOpenFile.setVisible(False)
        self.coords = []
        self.matrix = None
        self.size = None
        self.zoom = None
        self.accept_actions()
        if 'source' in kwargs:
            self.source = kwargs['source']
        if self.source == 'I':
            self.data_frame = pd.DataFrame(columns=['gs1dm'])
        else:
            self.data_frame = pd.DataFrame(columns=[self.source])            
        self.on_openfile(fileNames[0])        

    def accept_actions(self):
        self.btnOk.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.reject)
        #self.btnOpenFile.clicked.connect(self.on_openfile)
        self.btnDefault.clicked.connect(self.on_default)
        self.gbDmGrid.clicked.connect(self.on_manual)
        self.btnPreView.clicked.connect(self.on_preview_click)
        self.autocrop.mysignal.connect(self.on_change, Qt.QueuedConnection)
        self.manualcrop.mysignal.connect(self.on_change, Qt.QueuedConnection)

    def accept(self):
        if self.btnOk.text() == 'Импорт':
            self.statusBar().showMessage('Ожидайте...',0)
            self.progress_bar.setFixedSize(self.geometry().width() - 120, 16)
            self.progress_bar.show()
            self.options['PDF']['rows'] = self.leRow.text()
            self.options['PDF']['cols'] = self.leCol.text()
            self.options['PDF']['zoom_x'] = self.leZoom_x.text()
            self.options['PDF']['zoom_y'] = self.leZoom_y.text()
            self.options['PDF']['frame_x'] = self.leAreaWidth.text()
            self.options['PDF']['frame_y'] = self.leAreaHeight.text()
            self.parent.options = self.options

            if self.gbDmGrid.isChecked():
                if not self.manualcrop.isRunning():
                    self.btnOk.setEnabled(False)
                    self.manualcrop.start()
            else:
                if not self.autocrop.isRunning():
                    self.btnOk.setEnabled(False)
                    self.autocrop.start()
        else:        
            if self.parent.tabWidget.currentIndex() == 0:
                self.parent.data_frame = self.data_frame
                self.parent.model = PandasModel(self.parent.data_frame)
                self.parent.tvDmCodes.setModel(self.parent.model)
                self.parent.tvDmCodes.resizeColumnsToContents()
                self.parent.tvDmCodes.show()
                self.parent.statusBar().showMessage(f'Получено {self.parent.data_frame["gs1dm"].count()} кодов', 5000)

            elif self.parent.tabWidget.currentIndex() == 1:
                self.parent.data_frame_K = self.data_frame
                self.parent.model = PandasModel(self.parent.data_frame_K)
                self.parent.tvDmCodes_K.setModel(self.parent.model)
                self.parent.tvDmCodes_K.resizeColumnsToContents()
                self.parent.tvDmCodes_K.show()
                self.parent.statusBar().showMessage(f'Получено {self.parent.data_frame_K["K"].count()} кодов', 5000)
            self.close()

    def on_change(self, s):
        self.progress_bar.setValue(int(s))

    def reject(self):
        # - не предполагает изменения в БД
        self.autocrop.running = False # Изменяем флаг выполнения
        self.manualcrop.running = False
        if self.btnCancel.text() == 'Отмена':
            self.close()
        else:
            self.btnCancel.setText('Отмена')

    def closeEvent(self, event):      # Вызывается при закрытии окна
        self.hide()                   # Скрываем окно
        self.autocrop.running = False # Изменяем флаг выполнения
        self.autocrop.running = False # Изменяем флаг выполнения
        try:
            self.autocrop.wait(2000)      # Даем время, чтобы закончить
        except:
            pass
        try:
            self.manualcrop.wait(2000)      # Даем время, чтобы закончить
        except:
            pass
        event.accept()	              # Закрываем окно

    def on_manual(self):
        if self.gbDmGrid.isChecked():
            self.leRow.setEnabled(True)
            self.leCol.setEnabled(True)
            self.leAreaWidth.setEnabled(True)
            self.leAreaHeight.setEnabled(True)
            self.leZoom_x.setEnabled(True)
            self.leZoom_y.setEnabled(True)
        else:
            if self.matrix:
                self.leRow.setText(str(self.matrix[0]))
                self.leCol.setText(str(self.matrix[1]))
            if self.size:
                self.leAreaWidth.setText(str(self.size[0]))
                self.leAreaHeight.setText(str(self.size[1]))
            if self.zoom:
                self.leZoom_x.setText(str(self.zoom[0]))
                self.leZoom_y.setText(str(self.zoom[1]))
            self.leAreaHeight.setEnabled(False)
            self.leRow.setEnabled(False)
            self.leCol.setEnabled(False)
            self.leAreaWidth.setEnabled(False)
            self.leAreaHeight.setEnabled(False)
            self.leZoom_x.setEnabled(False)
            self.leZoom_y.setEnabled(False)

    def dm_decode(self, np_image, point, size):
        try:
            image = Image.fromarray(np_image[point[0]-5:point[0]+size[1]+5, point[1]-5: point[1]+size[0]+5].copy())
            return bytes.decode(decode(image)[0].data)   # !!!
        except: 
            return False

    def prescan(self, pdf_filename):
        print(self.lbImage.width(), self.lbImage.height())
        pdfIn = fitz.open(pdf_filename)
        page = pdfIn[0]
        img = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
        img = Image.frombytes("RGB", [img.width, img.height], img.samples)
        img = np.array(img).copy()
        
        
        pixmap = QPixmap()
        pixmap.convertFromImage(QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888))
        pixmap = pixmap.scaled(self.lbImage.width(), self.lbImage.height(), Qt.KeepAspectRatio)
        self.lbImage.setPixmap(pixmap)
        self.lbImage.show()

        for zoom in range(1,9):
            self.coords = []
            # Получить PixMap из страницы PDF файла и преобразовать в NumPy Array без промежуточного сохранения
            img = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
            img = np.array(Image.frombytes("RGB", [img.width, img.height], img.samples))
            # Повысить контрастность полученного изображения
            clahe = cv2.createCLAHE(clipLimit=5., tileGridSize=(8,8))          # CLAHE (Contrast Limited Adaptive Histogram Equalization)
            lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)  # convert from BGR to LAB color space
            l, a, b = cv2.split(lab)  # split on 3 different channels
            l2 = clahe.apply(l)  # apply CLAHE to the L-channel
            lab = cv2.merge((l2,a,b))  # merge channels
            img = cv2.cvtColor(cv2.cvtColor(lab, cv2.COLOR_LAB2BGR), cv2.COLOR_BGR2GRAY)  # convert from LAB to BGR, а затем в GRAY
            
            # Получаем номера столбцов и строк, в которых есть полезная информация
            bool_arr = ( img != 255)
            cols, rows = np.sum(bool_arr, axis=(0)), np.sum(bool_arr, axis=(1))
            cols, rows = np.where(cols > 0, 1, 0),  np.where(rows > 0, 1, 0)

            # Получаем размер кода в пикселях
            maxima_so_far = {}
            for t, group in itertools.groupby(cols):
                group_length = sum(1 for _ in group)
                if group_length > maxima_so_far.get(t, 0):
                    maxima_so_far[t] = group_length
            self.size = (maxima_so_far[1],  maxima_so_far[1])

            # Определяем координаты углов изображения кода
            cols, rows = cols.nonzero()[0], rows.nonzero()[0]

            # Получаем два вектора: 
            # номера столбцов с полезной информацией
            x = [cols[0]]+[cols[i] for i in range(1, len(cols)) if abs(cols[i]-cols[i-1])>1]
            # номера строк с полезной информацией
            y = [rows[0]]+[rows[i] for i in range(1, len(rows)) if abs(rows[i]-rows[i-1])>1]
            self.matrix = (len(x), len(y))   # Размерность таблицы кодов на странице
            
            # Получаем список координат левого верхнего угла всех кодов на странице
            self.coords = [(y[i], x[j]) for i in range(len(y)) for j in range(len(x))]

            # Пытаемся распознать код
            try:     # Выбираем первый код для предварительного просмотра и проверки распознавания 
                if self.dm_decode(img, self.coords[0], self.size): 
                    break
            except:  # При неудачной попытке увеличиваем масштаб
                continue
        self.zoom = (zoom, zoom)
        pdfIn.close()

    def on_imagecrop_check(self):
        self.leZoom_x.setEnabled(self.gbImageCrop.isChecked())
        self.leZoom_y.setEnabled(self.gbImageCrop.isChecked())
        self.gbImageCrop.setChecked(not self.gbImageCrop.setChecked)

    def on_preview_click(self):
        # Подготовка обрезанного изображения для отображения предпросмотра
        zoom = (int(self.leZoom_x.text()), int(self.leZoom_y.text()))
        if self.gbDmGrid.isChecked():
            size = (int(self.leAreaWidth.text()), int(self.leAreaHeight.text()))
            coords = (0,0)
        else:
            coords = self.coords[0]
            size = self.size
        
        pdfIn = fitz.open(self.leFileName.text())
        img = pdfIn[0].get_pixmap(matrix=fitz.Matrix(zoom[0], zoom[1]), alpha=False)
        pdfIn.close()
        img = Image.frombytes("RGB", [img.width, img.height], img.samples).crop((coords[0], coords[1], coords[0]+size[0], coords[1]+size[1]))
        
        
        if self.gbDmGrid.isChecked():
            if bytes.decode(decode(img)[0].data) != '':
                self.statusBar().showMessage(f'Распознанный код: {bytes.decode(decode(img)[0].data)}', 0)
            img = np.array(img).copy()
        else:
            img = np.array(img).copy()
            if self.dm_decode(img, coords, size): 
                self.statusBar().showMessage(f'Распознанный код: {self.dm_decode(img, coords, size)}', 0)

        # Отображение предпросмотра
        pixmap = QPixmap()
        try:
            pixmap.convertFromImage(QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888))
            pixmap = pixmap.scaled(self.lbCodePreView.width(), self.lbCodePreView.height(), Qt.KeepAspectRatio)
            self.lbCodePreView.setPixmap(pixmap)
            self.lbCodePreView.show()
        except:
            self.lbCodePreView.clear()

    def on_default(self):
        self.leFileName.setText('')
        self.leRow.setText('4')
        self.leCol.setText('5')
        self.leAreaWidth.setText('100')
        self.leAreaHeight.setText('173')
        self.gbImageCrop.setChecked = False
        self.gbDmGrid.setChecked = False
        self.leZoom_x.setText('1')
        self.leZoom_y.setText('1')
        self.lbCodePreView.clear()

    def on_openfile(self, fileName):
        pd.options.mode.copy_on_write = True
        #if fileNames:
            #self.leFileName.setText(fileNames[0])
        try:
            self.prescan(fileName)
            self.btnPreView.setEnabled(True)
            self.leZoom_x.setText(str(self.zoom[0]))
            self.leZoom_y.setText(str(self.zoom[1]))
            self.leRow.setText(str(self.matrix[0]))
            self.leCol.setText(str(self.matrix[1]))
            self.leAreaWidth.setText(str(self.size[0]))                
            self.leAreaHeight.setText(str(self.size[1]))
            self.lbCodePreView.clear()
        except:
            self.statusBar().showMessage(f'Ошибка при попытке открыть файл {self.leFileName.text()}', 0)

'''
if __name__ == "__main__":
    filename = 'd:/dm/103336_gtin_08410660053902_quantity_23760.pdf'
    start = time()
    zoom = (1, 1)
    zoom = 1
    matrix = (13, 13)  # Размерность таблицы кодов на странице (строк-стоблцов)
    size = (168, 247)  #
    pdfIn = fitz.open(filename)
    #Преобразует PDF в изображение и создает файл за страницей
    # PDF Страница конвертируется в целое изображение 1056 * 816, а затем для каждого изображения делается снимок экрана.
    # zoom = 1.33333333 -----> Размер изображения = 1056 * 816
    # zoom = 2 ---> 2 * Разрешение по умолчанию (текст четкий, текст изображения плохо читается) = маленький размер файла/размер изображения = 1584 * 1224
    # zoom = 4 ---> 4 * Разрешение по умолчанию (текст четкий, текст изображения плохо читается) = большой размер файла
    # zoom = 8 ---> 8 * Разрешение по умолчанию (текст четкий, текст изображения читается) = большой размер файла
    # Коэффициент масштабирования 8, чтобы текст был четким   
    codes = pd.DataFrame()
    count = 0
    page_number = 0
    for page in pdfIn:
    #for i in range(1):
        #page = pdfIn[143]
        page_number += 1
        #pix = page.get_pixmap(matrix=fitz.Matrix(zoom[0], zoom[1]), alpha=False)
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        pix.save(os.path.join('tmp.png'))
        #img_page = Image.open('tmp.png').crop((115,115, 2260, 3300))   # Кадрирование страницы по положению левого верхнего угла первого кода на странице
        img_page = Image.open('tmp.png')#.convert(mode='L')
        #img_page.save('tmp.png')

        #-----Определяем левое и верхнее поля для кадрирования 
        anchor = [0, 0]
        count = 0
        y = 0
        while y < img_page.height and anchor[1] == 0:
            x = 0
            while x < img_page.width and anchor[0] == 0:
                if img_page.getpixel((x, y)) < (255,255,255): #(255): 
                    count += 1 
                    if count>10:
                        anchor = (x-10, y-10, img_page.width-x+10, img_page.height-y+10)
                        break
                x += 1
            y += 1
        #print(anchor)
        img_page = img_page.crop(anchor).save('tmp.png')
        #----------------------------------------------------
        #
        for i in range(matrix[0]):
            for j in range(matrix[1]):
                cr_left = size[0]*j     #(size[0]+delta[0])*j  #+anchor[0]
                cr_top = size[1]*i      #(size[1]+delta[1])*i  #+anchor[1]
                cr_right = cr_left + size[0]
                cr_bottom = cr_top + size[1]
                #image = img_page.crop((cr_left, cr_top, cr_right, cr_bottom))
                #codes.loc[len(codes.index)] = bytes.decode(decode(image)[0].data)
                #count += 1
                
                try:
                    image = img_page.crop((cr_left, cr_top, cr_right, cr_bottom))
                    #image.save('image.png')
                    codes.loc[len(codes.index)] = bytes.decode(decode(image)[0].data)
                    count += 1
                except:

                    print(f'Страница {page_number}: не распознан код {i+1}:{j+1}')
                    
        print(f'Страница {page_number} из {len(pdfIn)} обработана. Всего получено {count} кодов. {round(time()-start, 2)} сек')
        codes.to_csv(filename, index=False, header=False, sep=chr(9), quoting=csv.QUOTE_NONE)


    pdfIn.close()

'''

'''
# Тестирование ручного вырезания и дальнейшего распознавания кодов
if __name__ == "__main__":
    filename = 'd:/dm/Вода минеральная питьевая негазирова 0,33_quantity_500.pdf'
    pdfIn = fitz.open(filename)
    zoom = (1, 1)
    size = (100, 173)

    img = pdfIn[0].get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)

    img = np.array(Image.frombytes("RGB", [img.width, img.height], img.samples))
    pdfIn.close()
    for i in range(4):
        for j in range(5):
            tmp = img[size[1]*i:size[1]*(i+1), size[0]*j:size[0]*(j+1)]
            tmp = Image.fromarray(tmp)
            tmp.show()
            print(bytes.decode(decode(tmp)[0].data))


'''