from PyQt5.QtWidgets import QMainWindow, QMessageBox, QProgressBar, QFileDialog
import zebraui
from zebra import Zebra
from zebrafy import ZebrafyImage

ROTATE = 'NRIB'

class ZplPrinter(QMainWindow, zebraui.Ui_ZplWindow):
    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent)
        self.setupUi(self)  # Это для инициализации  дизайна
        self.escapes = '/|@`'
        self.parent = parent
        if self.parent.tabWidget.currentIndex() == 0:
            self.codes = self.parent.data_frame['gs1dm'].tolist()
        elif self.parent.tabWidget.currentIndex() == 1:
            self.codes = self.parent.data_frame_K['K'].tolist()
        elif self.parent.tabWidget.currentIndex() == 1:
            self.codes = self.parent.data_frame_P['P'].tolist()
        
        self.options = parent.options
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.statusBar().addPermanentWidget(self.progress_bar)
        self.progress_bar.hide()
        self.statusBar().showMessage(f'Выбрано кодов для печати: {len(self.codes)}', 0)
        self.btnOk.setEnabled(len(self.codes)>0)
        self.btnTestPrint.setEnabled(len(self.codes)>0)

        self.z = Zebra()
        self.cbPrinter.addItems(self.z.getqueues())
        self.cbBcLines.setEnabled(False)
        self.cbBcModuleSize.setEnabled(False)
        self.cbDMHeight.setEnabled(True)

        self.accept_actions()

    def accept_actions(self):
        self.btnOk.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.reject)
        self.btnTestPrint.clicked.connect(self.on_testprint)
        #self.btnExample.clicked.connect(self.on_copyclipboard)
        self.btnDefault.clicked.connect(self.on_default)
        self.btnOpenBack.clicked.connect(self.on_openBack_click)
        self.cbCodeType.currentIndexChanged.connect(self.oncodetypechange)

    def oncodetypechange(self, idx):
        if idx == 0:
            self.cbBcLines.setEnabled(False)
            self.cbBcModuleSize.setEnabled(False)
            self.cbDMHeight.setEnabled(True)
        elif idx == 1:
            self.cbBcLines.setEnabled(True)
            self.cbBcModuleSize.setEnabled(True)
            self.cbDMHeight.setEnabled(False)

    def on_openBack_click(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","PNG files (*.png);;JPG files (*.jpg);;All Files (*)", options=options)
        if fileName:
            self.options['LABEL']['back'] = fileName
            self.leBack.setText(fileName)

    def accept(self):
        self.z.setqueue(self.z.getqueues()[self.cbPrinter.currentIndex()])
        label_first = "^XA"        
        if self.gbGraphics.isChecked():
            try:
                file = open(self.leBack.text(), "rb")
            except IOError as e:
                label_first = '^XA'
            else:
                with file as image:
                    label_first ='^XA' + ZebrafyImage(
                        image.read(),
                        format="Z64",
                        invert=True,
                        dither=False,
                        pos_x=int(self.leBackLeft.text()),
                        pos_y=int(self.leBackTop.text()),
                        rotation=int(self.cbBackRotate.currentText()),
                        threshold=128,
                        complete_zpl=False,
                    ).to_zpl()
                    pass
        else:
            label_first = '^XA'            
            
        for i in range(len(self.codes)):
            ESCAPE=''
            for symbol in self.escapes:
                if symbol not in self.codes[i]:
                    ESCAPE = symbol
                    break 
            if ESCAPE != '':
                if self.cbCodeType.currentIndex() == 0:
                    label = label_first + f'''^FO{self.leCodeLeft.text()},{self.leCodeTop.text()}^BX{ROTATE[self.cbCodeRotate.currentIndex()]},{self.cbDMHeight.currentText()},200,26,26,,{ESCAPE},1^FD{ESCAPE}1{self.codes[i]}^FS'''
                elif self.cbCodeType.currentIndex() == 1:
                    pass
                if self.gbText.isChecked():
                    label = label + f'''^FB{str(self.leTextField.text())},1,0,C,0^FO{self.leTextLeft.text()},{self.leTextTop.text()},{str(self.cbTextAlign.currentIndex())}^A0{ROTATE[self.cbTextRotate.currentIndex()]},{self.sbFontSize.value()}'''
                    if self.cbNumeric.currentIndex() == 1:
                        if self.parent.tabWidget.currentIndex() == 1:
                            label = label + f'''^FD{i*int(self.parent.leKCount.text())+1}-{(i+1)*int(self.parent.leKCount.text())}\\&^FS'''
                        elif self.parent.tabWidget.currentIndex() == 2:
                            pass  # - сгенерировать штрих-код
                        else:
                            label = label + f'''^FD{i+1}\\&^FS'''
                    else:
                        label = label + f'''^FD{self.codes[i][16:self.codes[i].find('9')]}\\&^FS'''
                label = label + '^XZ'
                self.z.output(label)
            else:
                QMessageBox.warning(self, "Печать Datamatrix...", f'Код {self.codes[i]} не распечатан!')
        self.close()

    def on_testprint(self):
        from datetime import datetime

        self.z.setqueue(self.z.getqueues()[self.cbPrinter.currentIndex()])
        if self.gbGraphics.isChecked():
            try:
                file = open(self.leBack.text(), "rb")
            except IOError as e:
                label_first = '^XA'
            else:
                with file as image:
                    label_first = '^XA'+ZebrafyImage(
                        image.read(),
                        format="Z64",
                        invert=True,
                        dither=False,
                        pos_x=int(self.leBackLeft.text()),
                        pos_y=int(self.leBackTop.text()),
                        rotation=int(self.cbBackRotate.currentText()),
                        threshold=128,
                        complete_zpl=False,
                        ).to_zpl()
                    pass
        else:
            label_first = '^XA'

        '''
        Сохранение данных этикетки в файл
        with open("d:\output.zpl", "w") as zpl:
            zpl.write(label_first)     
        '''
        try:
            code = self.codes[0]
        except:
            code = ''
            QMessageBox.information(self, 'Печать ZEBRA', 'Не загужены коды для печати')            
        
        ESCAPE=''
        for symbol in self.escapes:
            if symbol not in code:
                ESCAPE = symbol
                break 
        if ESCAPE != '':
            if self.cbCodeType.currentIndex() == 0:
                label = label_first + f'''^FO{self.leCodeLeft.text()},{self.leCodeTop.text()}
^BX{ROTATE[self.cbCodeRotate.currentIndex()]},{self.cbDMHeight.currentText()},200,26,26,,{ESCAPE},1
^FD{ESCAPE}1{code}^FS'''
            elif self.cbCodeType.currentIndex() == 1:
                pass
            if self.gbText.isChecked():
                label = label + f'''^FB{str(self.leTextField.text())},1,0,C,0^FO{self.leTextLeft.text()},{self.leTextTop.text()},{str(self.cbTextAlign.currentIndex())}
^A0{ROTATE[self.cbTextRotate.currentIndex()]},{self.sbFontSize.value()}'''
                if self.cbNumeric.currentIndex() == 1:
                    if self.parent.tabWidget.currentIndex() == 1:
                        label = label + f'''^FD{self.parent.data_frame['gs1dm'].count()}-{self.parent.data_frame['gs1dm'].count()}\\&^FS'''
                    elif self.parent.tabWidget.currentIndex() == 2:
                        label = f'''^XA^FO100,400,2^BY5,3^BCN,400,Y,N,N,N^FD{self.parent.leFsrar_id.text()}{str((self.parent.cbPType.currentIndex()+1)*2)}55{datetime.today().year % 100}{self.parent.leOrderNumber.text()}00001^FS'''
                    else:
                        label = label + f'''^FD{len(self.codes)}\\&^FS'''
                else:
                    label = label + f'''^FD{code[16:code.find('9')]}\\&^FS'''
            label = label + '^XZ'
            #print(label)    
            '''
            Сохранение данных этикетки в файл
            with open("output.zpl", "w") as zpl_file:
                zpl_file.write(label)    '''            
            self.z.output(label)

    def reject(self):
        # - не предполагает изменения в БД
        self.close()

    def on_default(self):
        self.leCodeLeft.setText('100')
        self.leCodeTop.setText('100')
        self.cbCodeRotate.setCurrentIndex(0)
        self.gbText.setChecked(True)
        self.leTextLeft.setText('120')
        self.leTextTop.setText('120')
        self.cbTextAlign.setCurrentIndex(2)
        self.cbTextRotate.setCurrentIndex(0)
        self.sbFontSize.setValue(18)
        self.gbGraphics.setChecked(True)
        self.leBackLeft.setText('0')
        self.leBackTop.setText('0')
        #self.pBackImage.setText('')
    
