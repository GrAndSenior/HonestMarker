from PyQt5.QtWidgets import QMainWindow, QFileDialog, QProgressBar
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt # нужна константа Qt.KeepAspectRatio для изменения размеров с сохранением пропорций
from pylibdmtx.pylibdmtx import decode, encode
from pandasmodel import PandasModel
from PIL import Image
from typing import Tuple
from time import time
import fitz
import os
import pandas as pd                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
#from time import time

import pdfimport
class PdfPreview(QMainWindow, pdfimport.Ui_PdfPreviewWindow):
    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent)
        self.setupUi(self)  # Это для инициализации  дизайна
        self.parent = parent
        self.options = parent.options
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0,100)
        self.statusBar().addPermanentWidget(self.progress_bar)
        self.progress_bar.hide()
        self.accept_actions()
        if 'source' in kwargs:
            self.source = kwargs['source']
        if self.source == 'I':
            self.data_frame = pd.DataFrame(columns=['gs1dm'])
        else:
            self.data_frame = pd.DataFrame(columns=[self.source])            

    def accept_actions(self):
        self.btnOk.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.reject)
        self.btnOpenFile.clicked.connect(self.on_openfile)
        self.btnDefault.clicked.connect(self.on_default)
        self.gbImageCrop.toggled.connect(self.on_imagecrop_check)
        self.btnPreView.clicked.connect(self.on_preview_click)

    def accept(self):
        start = time()
        self.statusBar().showMessage('Ожидайте...',0)
        #self.parent.statusBar().showMessage(f'Готово! Время на загрузку кодов: {round(time()-start,2)}сек. Обработано кодов: {self.data_frame["gs1dm"].count()}', 0)
        self.progress_bar.setFixedSize(self.geometry().width() - 120, 16)
        self.progress_bar.show()
        self.options['PDF']['rows'] = self.leRow.text()
        self.options['PDF']['cols'] = self.leCol.text()
        self.options['PDF']['zoom_x'] = self.leZoom_x.text()
        self.options['PDF']['zoom_y'] = self.leZoom_y.text()
        self.options['PDF']['frame_x'] = self.leAreaWidth.text()
        self.options['PDF']['frame_y'] = self.leAreaHeight.text()
        self.parent.options = self.options

        self.convert_pdf(self.leFileName.text())
        if self.source == 'I':
            self.parent.data_frame = self.data_frame
            self.parent.model = PandasModel(self.parent.data_frame)
            self.parent.tvDmCodes.setModel(self.parent.model)
            self.parent.tvDmCodes.resizeColumnsToContents()
            self.parent.tvDmCodes.show()
            self.parent.statusBar().showMessage(f'Готово! Время на загрузку кодов: {round(time()-start,2)}сек. Обработано кодов: {self.data_frame["gs1dm"].count()}', 0)
        elif self.source == 'K':
            self.parent.data_frame_K = self.data_frame
            self.parent.model = PandasModel(self.parent.data_frame_K)
            self.parent.tvDmCodes_K.setModel(self.parent.model)
            self.parent.tvDmCodes_K.resizeColumnsToContents()
            self.parent.gbK.setVisible(True)
            self.parent.tvDmCodes_K.show()
            self.parent.statusBar().showMessage(f'Готово! Время на загрузку кодов: {round(time()-start,2)}сек. Обработано кодов: {self.data_frame["K"].count()}', 0)
         
        self.close()

    def reject(self):
        # - не предполагает изменения в БД
        self.close()

    def on_imagecrop_check(self):
        self.leZoom_x.setEnabled(self.gbImageCrop.isChecked())
        self.leZoom_y.setEnabled(self.gbImageCrop.isChecked())

    def on_preview_click(self):
        pdfIn = fitz.open(self.leFileName.text())
        page = pdfIn[0]
        pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
        pix.save(os.path.join('tmp.png'))
        pdfIn.close()
        image = Image.open('tmp.png')
        image = image.crop((0, 0, int(self.leAreaWidth.text()), int(self.leAreaHeight.text())))
        if self.gbImageCrop.isChecked():
            r = decode(image)[0].rect
            tmp = image.crop((r[0], image.size[1]-r[1]-r[3], r[0]+r[2], image.size[1]-r[1]))
        else:
            tmp = image.crop((0, 0, int(self.leAreaWidth.text()), int(self.leAreaHeight.text())))
        tmp.save('tmp.png')
        self.preview = QPixmap('tmp.png')
        self.preview = self.preview.scaled(self.lbCodePreView.width(), self.lbCodePreView.height(), Qt.KeepAspectRatio)
        self.lbCodePreView.setPixmap(self.preview)
        #self.lbCodePreView.setScaledContents(True)
        self.lbCodePreView.show()

            #self.statusBar().showMessage(f'Ошибка при формировании изображения из файла {pdfIn}',5)

    def on_default(self):
        self.leFileName.setText('')
        self.leRow.setText('4')
        self.leCol.setText('5')
        self.leAreaWidth.setText('100')
        self.leAreaHeight.setText('173')
        self.gbImageCrop.setChecked = False
        self.leZoom_x.setText('1')
        self.leZoom_y.setText('1')

    def on_openfile(self):
        pd.options.mode.copy_on_write = True
        options = QFileDialog.Options()
        #options |= QFileDialog.ExistingFiles   # включение множественного выбора
        options |= QFileDialog.DontUseNativeDialog
        fileNames, _ = QFileDialog.getOpenFileNames(self,"Выбор файлов с кодами...", "","PDF Files (*.pdf);;All Files (*)", options=options)
        self.leFileName.setText(fileNames[0])
        try:
            pdfIn = fitz.open(self.leFileName.text())
            page = pdfIn[0]
            pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
            pix.save(os.path.join('tmp.png'))
            pdfIn.close()
            pixmap = QPixmap('tmp.png')
            pixmap = pixmap.scaled(self.lbImage.width(), self.lbImage.height(), Qt.KeepAspectRatio)
            self.lbImage.setPixmap(pixmap)
            self.lbImage.show()
            self.btnPreView.setEnabled(True)
        except:
            self.statusBar().showMessage(f'Ошибка при попытке открыть файл {self.leFileName.text()}', 0)


    def convert_pdf(self, filename, pages: Tuple = None):
        zoom = (int(self.leZoom_x.text()), int(self.leZoom_y.text()))
        matrix = (int(self.leRow.text()), int(self.leCol.text()))
        size = (int(self.leAreaWidth.text()), int(self.leAreaHeight.text()))
        pdfIn = fitz.open(filename)
        #Преобразует PDF в изображение и создает файл за страницей
        # PDF Страница конвертируется в целое изображение 1056 * 816, а затем для каждого изображения делается снимок экрана.
        # zoom = 1.33333333 -----> Размер изображения = 1056 * 816
        # zoom = 2 ---> 2 * Разрешение по умолчанию (текст четкий, текст изображения плохо читается) = маленький размер файла/размер изображения = 1584 * 1224
        # zoom = 4 ---> 4 * Разрешение по умолчанию (текст четкий, текст изображения плохо читается) = большой размер файла
        # zoom = 8 ---> 8 * Разрешение по умолчанию (текст четкий, текст изображения читается) = большой размер файла
        # Коэффициент масштабирования 8, чтобы текст был четким   
        for pg in range(pdfIn.page_count):
            if str(pages) != str(None):
                if str(pg) not in str(pages):
                    continue
            page = pdfIn[pg]
            
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom[0], zoom[1]), alpha=False)
            pix.save(os.path.join('tmp.png'))
            img_page = Image.open('tmp.png')
            for i in range(matrix[0]):
                for j in range(matrix[1]):
                    cr_left = size[0]*j     #(size[0]+delta[0])*j #+anchor[0]
                    cr_top = size[1]*i      #(size[1]+delta[1])*i  #+anchor[1]
                    cr_right = cr_left + size[0]
                    cr_bottom = cr_top + size[1]
                    try:
                        image = img_page.crop((cr_left, cr_top, cr_right, cr_bottom))
                        self.data_frame.loc[len(self.data_frame.index)] = bytes.decode(decode(image)[0].data)
                        if self.gbImageCrop.isChecked():
                            r = decode(image)[0].rect
                            tmp = image.crop((r[0], image.size[1]-r[1]-r[3], r[0]+r[2], image.size[1]-r[1]))
                            tmp.save(os.path.join(self.options['MAIN']['output'], f"_page{pg+1}_code"+str(i+1)+str(j+1)+".png"))
                            ####################print(decode(image)[0].rect)           # Размер области с кодом на изображении image.  !!! Система координат - как в математике
                        #self.progress_bar.setValue(int(int(self.data_frame['gs1dm'].count())/(pdfIn.page_count*matrix[0]*matrix[1])*100))
                        self.progress_bar.setValue(int(int(self.data_frame[self.source].count())/(pdfIn.page_count*matrix[0]*matrix[1])*100))
                             
                    except:
                        self.statusBar().showMessage(f'Ошибка конвертации файла {pdfIn}',5)
        self.data_frame = self.data_frame.reset_index()
        del self.data_frame['index']                        
        pdfIn.close()
