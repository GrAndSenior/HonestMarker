from PyQt5.QtWidgets import QMainWindow, QFileDialog, QProgressBar, QMessageBox
from PyQt5.QtGui import QPixmap, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp # нужна константа Qt.KeepAspectRatio для изменения размеров с сохранением пропорций
from PIL import Image, ImageDraw, ImageFont
from time import time
import layoutui
import os
import treepoem


class Dm():
    def __init__(self, code, group = 12, inline = False):
        self.veryfy = True
        self.inline = inline
        self.code = code.replace('','')
        if group == 0:
            pass
        elif group == 1:
            pass
        elif group == 2:
            pass
        elif group == 3:
            pass
        elif group == 4:
            pass
        elif group == 5:
            pass
        elif group == 6:
            pass
        elif group == 7:
            pass
        elif group == 8:
            pass
        elif group == 9:
            pass
        elif group == 10:
            pass
        elif group == 11:
            self.gtin = f'(01){code[2:6]}'
            self.sn = f'(21){code[6:19]}'
            self.tnved = f'(240){code[22:26]}'
            self.key = f'(91){code[26:30]}'
            self.crypto = f'(92){code[32:120]}'  #!!!!!!!!!!!!!!!!! Проверить
        elif group == 12:
            self.gtin = f'(01){code[2:16]}'
            self.sn = f'(21){code[18:25]}'
            self.key = f'(93){code[28:]}'
            self.tnved = f'(240)'
        elif group == 13:
            pass
        elif group == 14:
            pass
        elif group == 15:
            pass
        elif group == 16:
            pass
        elif group == 17:
            self.gtin = f'(01){code[2:16]}'
            self.sn = f'(21){code[18:31]}'
            self.key = f'(93){code[34:]}'   # !!!!!!!!!!!!!!!!!!! Проверить
            self.tnved = f'(240)'
        elif group == 18:
            pass
        elif group == 19:
            pass
        elif group == 20:
            self.gtin = f'(01){code[2:16]}'
            self.sn = f'(21){code[18:31]}'
            if code.count('') ==  1:
                self.key = f'(93){code[34:]}'
            elif code.count('') == 2: 
                self.key = f'(91){code[34:38]}'
            else:
                self.key = ''
            self.tnved = ''
        else:
            self.gtin = ''
            self.sn = ''
            self.key = ''
            self.tnved = ''
            self.code = code
            self.veryfy = False

    def __str__(self):
        if self.inline:
            return f'{self.sn}{self.key}\n{self.gtin}'
        else:
            return self.code


class LayoutDM(QMainWindow, layoutui.Ui_LayoutWindow):
    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent)
        self.setupUi(self)  # Это для инициализации  дизайна
        self.parent = parent
        self.options = parent.options
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0,100)
        self.statusBar().addPermanentWidget(self.progress_bar)
        self.progress_bar.hide()
        if self.parent.tabWidget.currentIndex() < 2:
            self.cbCodeType.setCurrentIndex(0) 
        elif self.parent.tabWidget.currentIndex() == 2:
            self.cbCodeType.setCurrentIndex(1)
        else:
            self.cbCodeType.setCurrentIndex(-1)

        digitRegex = QRegExp('\\d+')
        digitValidator = QRegExpValidator(digitRegex, self)
        self.leLabelHeight.setValidator(digitValidator)
        self.leLabelWidth.setValidator(digitValidator)
        self.leLeft.setValidator(digitValidator)
        self.leTop.setValidator(digitValidator)
        self.leWidth.setValidator(digitValidator)
        self.leHeight.setValidator(digitValidator)
        self.leTextLeft.setValidator(digitValidator)
        self.leTextTop.setValidator(digitValidator)
        #self.leTextField.setValidator(digitValidator)

        self.leLabelWidth.setText('236')
        self.leLabelHeight.setText('236')
        self.leBack.setText(self.options['LABEL']['back'])
        self.leLeft.setText(str(self.options['LABEL']['left']))
        self.leTop.setText(str(self.options['LABEL']['top']))
        self.leWidth.setText(str(self.options['LABEL']['width']))
        self.leHeight.setText(str(self.options['LABEL']['height']))
        self.cbText.setChecked = self.options['LABEL']['label']
        self.sbFontSize.setValue(self.options['LABEL']['font_size'])
        self.cbTextRotate.setCurrentText(str(self.options['LABEL']['label_rotate']))
        self.cbTextAllign.setCurrentText(str(self.options['LABEL']['label_align']))
        self.leTextLeft.setText(str(self.options['LABEL']['label_left']))
        self.leTextTop.setText(str(self.options['LABEL']['label_top']))
        if self.cbCodeType.currentIndex() == 1:
            self.leLabelWidth.setText('1180')
            self.leLabelHeight.setText('1770')
            self.leWidth.setText('360')
            self.leHeight.setText('160')
            #self.cbText.setEnabled(False)
            self.cbCodeRotate.setCurrentIndex(0)
            self.cbCodeZoom.setEnabled(True)
        else:
            self.cbCodeZoom.setEnabled(False)

        '''self.gbZpl.setChecked = self.options['ZPL']['zpl']
        self.cbDMHeight.setCurrentText(str(self.options['ZPL']['code_size']))
        self.cbDMQuality.setCurrentText(str(self.options['ZPL']['code_quality']))
        self.cbDMRotate.setCurrentIndex(self.options['ZPL']['code_rotation'])'''

        self.accept_actions()

    def accept_actions(self):
        self.btnOk.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.reject)
        self.btnOpenBack.clicked.connect(self.on_openBack_click)
        self.btnPreView.clicked.connect(self.on_preview_click)
        self.btnDefault.clicked.connect(self.on_default_click)
        self.cbText.toggled.connect(self.on_text_check)
        self.cbCodeType.currentIndexChanged.connect(self.selectionchange)
        self.cbCodeRotate.currentIndexChanged.connect(self.selectioncodechange)
        self.cbNumeric.currentIndexChanged.connect(self.selectiontextchange)
        self.anchorText.toggled.connect(self.on_text_anchor)

    def selectiontextchange(self, i):
        self.label_14.setEnabled(i != 2)
        self.leSampleText.setEnabled(i != 2)
        
    def on_text_anchor(self):
        self.leTextLeft.setEnabled(not self.anchorText.isChecked())
        self.leTextTop.setEnabled(not self.anchorText.isChecked())
        

    def on_text_check(self):
        self.leSampleText.setEnabled(self.cbText.isChecked())
        self.sbFontSize.setEnabled(self.cbText.isChecked())
        self.cbTextRotate.setEnabled(self.cbText.isChecked())
        self.cbTextAllign.setEnabled(self.cbText.isChecked())
        self.leTextLeft.setEnabled(not self.anchorText.isChecked())
        self.leTextTop.setEnabled(not self.anchorText.isChecked())
        #self.leTextField.setEnabled(self.cbText.isChecked())
        self.cbNumeric.setEnabled(self.cbText.isChecked())


    def selectioncodechange(self, i):
        if i % 2 == 1:
            w, h  = self.leWidth.text(), self.leHeight.text()
            self.leWidth.setText(h)
            self.leHeight.setText(w)
            
    def selectionchange(self, i):
        if i == 0:
            self.leLabelWidth.setText('236')
            self.leLabelHeight.setText('236')
            self.leWidth.setText('100')
            self.leHeight.setText('100')
            #self.cbText.setEnabled(True)
            self.cbCodeZoom.setEnabled(False)
        else:
            self.leLabelWidth.setText('1180')
            self.leLabelHeight.setText('1770')
            self.leWidth.setText('360')
            self.leHeight.setText('160')
            #self.cbText.setEnabled(False)
            self.cbCodeZoom.setEnabled(True)
        self.cbCodeRotate.setCurrentIndex(0)        


    def accept(self):
        #print(self.sender().objectName())
        start = time()
        self.progress_bar.setFixedSize(self.geometry().width() - 120, 16)
        self.progress_bar.show()
        self.save_config()

        goodname = ' '.join([ t for t in self.parent.leGoodName.text().split(' ') if t ])
        if self.parent.tabWidget.currentIndex() == 1:   
            suffix = 'K'
            codes = self.parent.data_frame_K['K'].tolist()
        elif self.parent.tabWidget.currentIndex() == 2:
            suffix = 'P'
            codes = self.parent.data_frame_P['P'].tolist()
        else:
            codes = self.parent.data_frame['gs1dm'].tolist()
            suffix = 'I'


        if self.options['MAIN']['output']:
            if not(os.path.exists(os.path.join(self.options['MAIN']['output'], goodname, suffix)) or os.path.isdir(os.path.join(self.options['MAIN']['output'], goodname, suffix))):
                if not(os.path.exists(os.path.join(self.options['MAIN']['output'], goodname)) or os.path.isdir(os.path.join(self.options['MAIN']['output'], goodname))):
                    try:
                        os.mkdir(os.path.join(self.options['MAIN']['output'], goodname))
                    except:
                        QMessageBox.critical(self, 'Ошибка!!!', 'Папка для сохранения не существует.')
                if suffix != '': os.mkdir(os.path.join(self.options['MAIN']['output'], goodname, suffix)) 
            fname = os.path.join(self.options['MAIN']['output'], goodname, suffix)
        else:
            if not(os.path.exists(os.path.join(os.getcwd(), goodname, suffix)) or os.path.isdir(os.path.join(os.getcwd(), goodname, suffix))):
                if not(os.path.exists(os.path.join(self.options['MAIN']['output'], goodname)) or os.path.isdir(os.path.join(self.options['MAIN']['output'], goodname))):
                    try:
                        os.mkdir(os.path.join(self.options['MAIN']['output'], goodname))
                    except:
                        QMessageBox.critical(self, 'Ошибка!!!', 'Папка для сохранения не существует.')
                if suffix != '': os.mkdir(os.path.join(os.getcwd(), goodname, suffix))
            fname = os.path.join(os.getcwd(), goodname, suffix)

        count = 1
        
        dm_size_px = (int(self.leWidth.text()),int(self.leHeight.text()))
        dm_position_px = (int(self.leLeft.text()), int(self.leTop.text()))

        try: 
            picture = Image.open(self.options['LABEL']['back'])
            background = True
        except:
            picture = Image.new("L", (int(self.leLabelWidth.text()), int(self.leLabelHeight.text())), 255)
            background = False

        if self.cbCodeType.currentIndex() == 0:
            for idx, code in enumerate(codes):
                back = Image.new('L', (picture.size), color=255)    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                if background:
                    back.paste(picture, (0,0))
                label = self.codevalidator(code, self.parent.cbCategory.currentIndex())

                try:
                    datamatrix = treepoem.generate_barcode(
                        barcode_type='datamatrix',
                        data=f"^FNC1{label}",
                        options={"parsefnc": True, "parse": True, "format": "square", "version": "22x22", "includetext": False})
                except:
                    datamatrix = treepoem.generate_barcode(
                        barcode_type='datamatrix',
                        data=f"^FNC1{label}",
                        options={"parsefnc": True, "parse": True, "format": "square", "version": "36x36", "includetext": False})

                if self.cbCodeRotate.currentIndex() == 1:
                    datamatrix = datamatrix.transpose(Image.ROTATE_90)
                elif self.cbCodeRotate.currentIndex() == 2:
                    datamatrix = datamatrix.transpose(Image.ROTATE_180)
                elif self.cbCodeRotate.currentIndex() == 3:
                    datamatrix = datamatrix.transpose(Image.ROTATE_270)
            
                datamatrix = datamatrix.resize(dm_size_px, Image.NEAREST)
                back.paste(datamatrix, dm_position_px)
                
                if self.cbText.isChecked(): 
                    if self.cbNumeric.currentIndex() == 0:  #  В надписи серийный номер
                        label = label[16:label.find('9')]
                    elif self.cbNumeric.currentIndex() == 1:#  В надписи порядковый номер (или диапазон номеров)
                        if self.parent.tabWidget.currentIndex() == 1:
                            label = str(int(self.parent.leKCount.text())*(count-1)+1).zfill(len(str(self.parent.data_frame['gs1dm'].count())))+'-'+str(int(self.parent.leKCount.text())*count).zfill(len(str(self.parent.data_frame['gs1dm'].count())))
                        elif self.parent.tabWidget.currentIndex() == 2:
                            label = 'K'+str(int(self.parent.lePCount.text())*(count-1)+1).zfill(len(str(self.parent.data_frame_K['K'].count())))+'-'+str(int(self.parent.lePCount.text())*count).zfill(len(str(self.parent.data_frame_K['K'].count())))
                        else:
                            label = f'{idx+1}'
                    elif self.cbNumeric.currentIndex() == 2:# В надписи форматированный в 2 строки код Datamatrix
                        label = Dm(label, self.parent.cbCategory.currentIndex(), inline=False)
                    elif self.cbNumeric.currentIndex()==3:# В надписи в 1 строку код Datamatrix
                        label = code.replace('', '')
                    elif self.cbNumeric.currentIndex()==4:# В надписи порядковый номер короба
                        label = f'{idx//int(self.parent.leKCount.text())+1}'
                        
                    font = ImageFont.truetype('sources/fonts/arialnb.ttf', int(self.sbFontSize.text()))   
                    
                    if self.cbNumeric.currentIndex() == 2:
                        fontimage1 = Image.new('L', (font.font.getsize(f'{label.sn}{label.key}')[0][0], sum(font.getmetrics())))
                        fontimage2 = Image.new('L', (font.font.getsize(label.gtin)[0][0], sum(font.getmetrics())))
                        fontimage = Image.new('L', (max(fontimage1.size[0], fontimage2.size[0]), 2*sum(font.getmetrics())))
                        ImageDraw.Draw(fontimage).text((0, 0), f'{label.sn}{label.key}', fill=255, font=font)
                        ImageDraw.Draw(fontimage).text((0, fontimage1.size[1]), label.gtin, fill=255, font=font)    
                    else:
                        fontimage = Image.new('L', (font.font.getsize(label)[0][0], sum(font.getmetrics())))   ##########
                        ImageDraw.Draw(fontimage).text((0, 0), label, fill=255, font=font)
                    fontimage = fontimage.rotate(int(self.cbTextRotate.currentText()), resample=Image.BICUBIC, expand=True)

                    if self.anchorText.isChecked():
                        if self.cbTextAllign.currentIndex() == 0:
                            back.paste( mask=fontimage, 
                                        box=(int(self.leLeft.text()) + int(self.leWidth.text()) // 2 - fontimage.width // 2, 
                                            int(self.leTop.text()) + int(self.leHeight.text()) + 5),
                                        im=0)
                        elif self.cbTextAllign.currentIndex() == 1:
                            back.paste( mask=fontimage, 
                                        box=(int(self.leLeft.text()) - int(fontimage.width) - 5,
                                            int(self.leTop.text()) + int(self.leHeight.text()) // 2 - fontimage.height // 2), 
                                        im=0)    
                        elif self.cbTextAllign.currentIndex() == 2:
                            back.paste( mask=fontimage, 
                                        box=(int(self.leLeft.text()) + int(self.leWidth.text()) // 2 - fontimage.width // 2, 
                                            int(self.leTop.text()) - int(fontimage.height) - 5),
                                        im=0)    
                        elif self.cbTextAllign.currentIndex() == 3:
                            back.paste( mask=fontimage, 
                                        box=(int(self.leLeft.text()) + int(self.leWidth.text()) + 5,
                                            int(self.leTop.text()) + int(self.leHeight.text()) // 2 - fontimage.height // 2), 
                                        im=0)    
                        
                    else:
                        back.paste(mask=fontimage, box=(int(self.leTextLeft.text()), int(self.leTextTop.text())), im=0)
            
                back.save(os.path.join(fname, str(idx+self.sbStartNum.value()).zfill(len(str(len(codes))))+'.png'), optimize=True, quality=80)
                count += 1
                self.progress_bar.setValue(int(idx/len(codes)*100))
        else:
            for idx, code in enumerate(codes):
                back = Image.new('L', (picture.size), color=255)    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                if background:
                    back.paste(picture, (0,0))
                label = self.codevalidator(code, self.parent.cbCategory.currentIndex())
                
                datamatrix = treepoem.generate_barcode(
                    barcode_type="code128",  # One of the BWIPP supported codes.
                    data=f'{code}',
                    options= {"includetext": True},
                    scale=int(self.cbCodeZoom.currentText()))
                if self.cbCodeRotate.currentIndex() == 1:
                    datamatrix = datamatrix.transpose(Image.ROTATE_90)
                elif self.cbCodeRotate.currentIndex() == 2:
                    datamatrix = datamatrix.transpose(Image.ROTATE_180)
                elif self.cbCodeRotate.currentIndex() == 3:
                    datamatrix = datamatrix.transpose(Image.ROTATE_270)
                datamatrix = datamatrix.resize(dm_size_px, Image.NEAREST)
                back.paste(datamatrix, dm_position_px)

                if self.cbNumeric.currentIndex() == 1:
                    if self.parent.tabWidget.currentIndex() == 1:
                        label = f'{str(int(self.parent.leKCount.text())*(count-1)+1).zfill(len(str(len(codes))))}-{str(int(self.parent.leKCount.text())*count).zfill(len(str(len(codes))))}'
                    elif self.parent.tabWidget.currentIndex() == 2:
                        label = f'{str(int(self.parent.leKCount.text())*int(self.parent.lePCount.text())*(count-1)+1).zfill(len(str(len(codes))))}-{str(int(self.parent.leKCount.text())*int(self.parent.lePCount.text())*count).zfill(len(str(len(codes))))}      K{str(int(self.parent.lePCount.text())*(count-1)+1).zfill(len(str(len(codes))))}-{str(int(self.parent.lePCount.text())*count).zfill(len(str(len(codes))))}'
                    
                
                    font = ImageFont.truetype('sources/fonts/arialnb.ttf', int(self.sbFontSize.text()))
                    fontimage = Image.new('L', (font.font.getsize(label)[0][0], sum(font.getmetrics())))   ##########
                    ImageDraw.Draw(fontimage).text((0, 0), label, fill=255, font=font)
                    fontimage = fontimage.rotate(int(self.cbTextRotate.currentText()), resample=Image.BICUBIC, expand=True)
                    
                    back.paste(mask=fontimage, box=(int(self.leTextLeft.text()), int(self.leTextTop.text())), im=0)

                else:
                    label = ''

                back.save(os.path.join(fname, str(count+self.sbStartNum.value()).zfill(len(str(len(codes))))+'.png'), optimize=True, quality=80)
                count += 1
                self.progress_bar.setValue(int(count/len(codes)*100))

        self.progress_bar.hide()
        self.parent.statusBar().showMessage(f'Готово! Время на подготовку кодов: {round(time()-start,2)}сек. Обработано кодов: {len(codes)}', 0)
        self.close()

    def codevalidator(self, code, category):  # Переделать на регуляные выражения
        ### ^[0][1][0-9]{14}[2][1][^]{7}[9][3]\S{4}$   - пример валидатора
        if '' not in code:
            return code[:25]+''+code[25:] 
        else:
            return code  

    def reject(self):
        self.close()

    def on_openBack_click(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","PNG files (*.png);;JPG files (*.jpg);;All Files (*)", options=options)
        if fileName:
            self.options['LABEL']['back'] = fileName
            self.leBack.setText(fileName)
        self.on_preview_click()

    def getCode(self):
        if self.parent.cbCategory.currentIndex() == -1:
            return ''
        elif self.parent.cbCategory.currentIndex() == 12:
            return '01012345678901221999999993XXXX'
        elif self.parent.cbCategory.currentIndex() == 14:
            return '0103263280117616215s.xmxrtuid:>93/3Kd'
        

    def on_preview_click(self): #!!!!!!!!!!!!!!!!! Объединить вместе с accept +++
        # Получение списка кодов для маркировки
        if self.parent.tabWidget.currentIndex() == 1:
            suffix = 'K'#+++
            codes = self.parent.data_frame_K['K'].tolist()  #+++
        elif self.parent.tabWidget.currentIndex() == 2:                             #+++
            suffix = 'P'
            codes = self.parent.data_frame_P['P'].tolist()  #+++
        else:          
            suffix = ''#+++
            codes = self.parent.data_frame['gs1dm'].tolist()#+++
        
        #print(self.sender().objectName())
        barcode_size_px = (int(self.leWidth.text()), int(self.leHeight.text()))
        barcode_position_px = (int(self.leLeft.text()), int(self.leTop.text()))

        # Добавление фонового изображения
        try:
            #print(self.options['LABEL']['back'])    
            #back = Image.open(self.options['LABEL']['back'])
            
            back = Image.open(self.leBack.text())
            self.leLabelWidth.setText(str(back.size[0]))
            self.leLabelHeight.setText(str(back.size[1]))
        except:
            back = Image.new("L", (int(self.leLabelWidth.text()), int(self.leLabelHeight.text())), 255)


        # Генерация изображения кода
        if self.cbCodeType.currentIndex() == 0:
            try:
                datamatrix = treepoem.generate_barcode(
                    barcode_type='datamatrix',
                    data=f"^FNC1{codes[0]}",
                    options={"parsefnc": True, "parse": True, "format": "square", "version": "22x22", "includetext": False})
            except:
                datamatrix = treepoem.generate_barcode(
                    barcode_type='datamatrix',
                    data=f"^FNC1{codes[0]}",
                    options={"parsefnc": True, "parse": True, "format": "square", "version": "36x36", "includetext": False})

        else:
            datamatrix = treepoem.generate_barcode(
                    barcode_type="code128",  # One of the BWIPP supported codes.
                    data=f'{codes[0]}',
                    options= {"includetext": True},
                    scale=int(self.cbCodeZoom.currentText()))
        
        # Поворот изображения кода
        if self.cbCodeRotate.currentIndex() == 1:
            datamatrix = datamatrix.transpose(Image.ROTATE_90)
        elif self.cbCodeRotate.currentIndex() == 2:
            datamatrix = datamatrix.transpose(Image.ROTATE_180)
        elif self.cbCodeRotate.currentIndex() == 3:
            datamatrix = datamatrix.transpose(Image.ROTATE_270)

        # Изменение размера кода и нанесение его на шаблон
        datamatrix = datamatrix.resize(barcode_size_px, Image.NEAREST)
        back.paste(datamatrix, barcode_position_px)
        
        # Создание текстовой подписи кода
        if self.cbText.isChecked():                        
            if self.cbCodeType.currentIndex() == 0:  
                if self.cbNumeric.currentIndex() == 0:              #Серийный номер
                    label = self.leSampleText.text()
                elif self.cbNumeric.currentIndex()==1:              #Порядковый номер
                    if self.parent.tabWidget.currentIndex() == 1:
                        label = f'{str(int(self.parent.leKCount.text())*(len(codes)-1)+1).zfill(len(str(len(codes))))}-{str(int(self.parent.leKCount.text())*len(codes)).zfill(len(str(len(codes))))}'
                    elif self.parent.tabWidget.currentIndex() == 2:
                        label = f'K{str(int(self.parent.lePCount.text())*(len(codes)-1)+1).zfill(len(str(len(codes))))}-{str(int(self.parent.lePCount.text())*len(codes)).zfill(len(str(len(codes))))}'
                    else:
                        label = f'{len(codes)}'
                elif self.cbNumeric.currentIndex()==2:              #Форматированный код
                    label = f'(21)0123456(93)0123(01)01234567890123'
                elif self.cbNumeric.currentIndex()==3:              #Код Datamatrix
                    label = '011234567890123421432101293XXXX'
                elif self.cbNumeric.currentIndex()==4:              #Номер короба
                    label = '8'


            elif self.cbCodeType.currentIndex() == 1:
                if self.cbNumeric.currentIndex() == 1:
                    label = f'{suffix}{len(codes)}-{len(codes)}'
                else:
                    QMessageBox.warning(self,'Ошибка','Необходимо выбрать вид надписи: "Порядковый номер"')
                    label = ''
            # Создание изображения подписи кода
            font = ImageFont.truetype('sources/fonts/arialnb.ttf', int(self.sbFontSize.text()))
            if self.cbNumeric.currentIndex() == 2:
                fontimage1 = Image.new('L', (font.font.getsize(label[:19])[0][0], sum(font.getmetrics())))
                fontimage2 = Image.new('L', (font.font.getsize(label[19:])[0][0], sum(font.getmetrics())))
                fontimage = Image.new('L', (max(fontimage1.size[0], fontimage2.size[0]), 2*sum(font.getmetrics())))
                ImageDraw.Draw(fontimage).text((0, 0), label[:19], fill=255, font=font)
                ImageDraw.Draw(fontimage).text((0, fontimage1.size[1]), label[19:], fill=255, font=font)    
            else:
                fontimage = Image.new('L', (font.font.getsize(label)[0][0], sum(font.getmetrics())))   #!!!При генерации BarCode из датаматриксов ошибка
                ImageDraw.Draw(fontimage).text((0, 0), label, fill=255, font=font)
            
            # Вращение изображения надписи и нанесение его на шаблон
            fontimage = fontimage.rotate(int(self.cbTextRotate.currentText()), resample=Image.BICUBIC, expand=True)
            if self.anchorText.isChecked():
                if self.cbTextAllign.currentIndex() == 0:
                    back.paste( mask=fontimage, 
                                box=(int(self.leLeft.text()) + int(self.leWidth.text()) // 2 - fontimage.width // 2, 
                                    int(self.leTop.text()) + int(self.leHeight.text()) + 5),
                                im=0)
                elif self.cbTextAllign.currentIndex() == 1:
                    back.paste( mask=fontimage, 
                                box=(int(self.leLeft.text()) - int(fontimage.width) - 5,
                                    int(self.leTop.text()) + int(self.leHeight.text()) // 2 - fontimage.height // 2), 
                                im=0)    
                elif self.cbTextAllign.currentIndex() == 2:
                    back.paste( mask=fontimage, 
                                box=(int(self.leLeft.text()) + int(self.leWidth.text()) // 2 - fontimage.width // 2, 
                                    int(self.leTop.text()) - int(fontimage.height) - 5),
                                im=0)    
                elif self.cbTextAllign.currentIndex() == 3:
                    back.paste( mask=fontimage, 
                                box=(int(self.leLeft.text()) + int(self.leWidth.text()) + 5,
                                    int(self.leTop.text()) + int(self.leHeight.text()) // 2 - fontimage.height // 2), 
                                im=0)    
                
            else:
                back.paste(mask=fontimage, box=(int(self.leTextLeft.text()), int(self.leTextTop.text())), im=0)
            #back.paste(mask=fontimage, box=(int(self.leTextLeft.text()), int(self.leTextTop.text())), im=0)
            #!!!!!!!!!!!!!!!!!  Проверить поведение при повороте надписи
            #back.paste(mask=fontimage, box=(int(self.leTextLeft.text()) + int(self.leWidth.text()) // 2 - font.font.getsize(label)[0][0] // 2, int(self.leTextTop.text())), im=0)
        back.save('tmp.png')
        pixmap = QPixmap('tmp.png')
        pixmap = pixmap.scaled(self.lbImage.width(), self.lbImage.height(), Qt.KeepAspectRatio)
        self.lbImage.setPixmap(pixmap)
        self.lbImage.show()

    def on_default_click(self):
        if self.cbCodeType.currentIndex() == 0:
            self.leLabelWidth.setText('236')
            self.leLabelHeight.setText('236')
            self.leBack.setText('')
            self.leLeft.setText('80')
            self.leTop.setText('80')
            self.leWidth.setText('100')
            self.leHeight.setText('100')
            #self.cbText.setChecked(False)
            self.sbStartNum.setValue(1)
            self.sbFontSize.setValue(18)
            self.cbTextRotate.setCurrentIndex(0)
            self.cbTextAllign.setCurrentIndex(0)
            self.leTextLeft.setText('80')
            self.leTextTop.setText('80')
            self.cbNumeric.setCurrentIndex(0)
            #self.leTextField.setText(self.leLabelWidth.text())
            #self.gbZpl.setChecked = False
            #self.cbDMHeight.setCurrentText('6')
            #self.cbDMQuality.setCurrentText('ECC 200')
            #self.cbDMRotate.setCurrentText('0')
        else:
            self.leLabelWidth.setText('1180')
            self.leLabelHeight.setText('1770')
            self.leWidth.setText('360')
            self.leHeight.setText('160')
            #self.cbText.setEnabled(False)
            self.cbCodeZoom.setEnabled(True)
   

    def save_config(self):
        self.options['LABEL']['back'] = self.leBack.text()
        self.options['LABEL']['left'] = int(self.leLeft.text())
        self.options['LABEL']['top'] = int(self.leTop.text())
        self.options['LABEL']['width'] =int(self.leWidth.text())
        self.options['LABEL']['height'] = int(self.leHeight.text())
        self.options['LABEL']['label'] = bool(self.cbText.isChecked()) 
        self.options['LABEL']['font_size'] = int(self.sbFontSize.value())
        self.options['LABEL']['label_rotate'] = int(self.cbTextRotate.currentText())
#        self.options['LABEL']['label_align'] = int(self.cbTextAllign.currentText())
        self.options['LABEL']['label_left'] = int(self.leTextLeft.text())
        self.options['LABEL']['label_top'] = int(self.leTextTop.text())

        #!!!!!!!!!! Добавить сохранение параметров порядковых номеров
        
        #self.options['ZPL']['zpl'] = bool(self.gbZpl.isChecked()) 
        #self.options['ZPL']['code_size'] = int(self.cbDMHeight.currentText())
        #self.options['ZPL']['code_quality'] = self.cbDMQuality.currentText()
        #self.options['ZPL']['code_rotation'] = int(self.cbDMRotate.currentText())

        self.parent.options = self.options

