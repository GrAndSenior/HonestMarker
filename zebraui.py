# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zebraui.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ZplWindow(object):
    def setupUi(self, ZplWindow):
        ZplWindow.setObjectName("ZplWindow")
        ZplWindow.setWindowModality(QtCore.Qt.WindowModal)
        ZplWindow.resize(667, 605)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        ZplWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(ZplWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gbZebraPrinter = QtWidgets.QGroupBox(self.centralwidget)
        self.gbZebraPrinter.setObjectName("gbZebraPrinter")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.gbZebraPrinter)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.cbPrinter = QtWidgets.QComboBox(self.gbZebraPrinter)
        self.cbPrinter.setObjectName("cbPrinter")
        self.verticalLayout_6.addWidget(self.cbPrinter)
        self.verticalLayout_2.addWidget(self.gbZebraPrinter)
        self.gbGraphics = QtWidgets.QGroupBox(self.centralwidget)
        self.gbGraphics.setCheckable(True)
        self.gbGraphics.setChecked(True)
        self.gbGraphics.setObjectName("gbGraphics")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.gbGraphics)
        self.verticalLayout_5.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_16.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_16.setSpacing(2)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.leBack = QtWidgets.QLineEdit(self.gbGraphics)
        self.leBack.setEnabled(True)
        self.leBack.setMaxLength(255)
        self.leBack.setClearButtonEnabled(False)
        self.leBack.setObjectName("leBack")
        self.horizontalLayout_16.addWidget(self.leBack)
        self.btnOpenBack = QtWidgets.QToolButton(self.gbGraphics)
        self.btnOpenBack.setMinimumSize(QtCore.QSize(30, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/1a-a.grushovets/.designer/backup/sources/img/add_box_3d.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnOpenBack.setIcon(icon)
        self.btnOpenBack.setObjectName("btnOpenBack")
        self.horizontalLayout_16.addWidget(self.btnOpenBack)
        self.verticalLayout_5.addLayout(self.horizontalLayout_16)
        self.horizontalLayout_29 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_29.setSpacing(0)
        self.horizontalLayout_29.setObjectName("horizontalLayout_29")
        self.label_24 = QtWidgets.QLabel(self.gbGraphics)
        self.label_24.setObjectName("label_24")
        self.horizontalLayout_29.addWidget(self.label_24)
        self.leBackLeft = QtWidgets.QLineEdit(self.gbGraphics)
        self.leBackLeft.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.leBackLeft.setObjectName("leBackLeft")
        self.horizontalLayout_29.addWidget(self.leBackLeft)
        self.label_35 = QtWidgets.QLabel(self.gbGraphics)
        self.label_35.setObjectName("label_35")
        self.horizontalLayout_29.addWidget(self.label_35)
        self.leBackTop = QtWidgets.QLineEdit(self.gbGraphics)
        self.leBackTop.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.leBackTop.setObjectName("leBackTop")
        self.horizontalLayout_29.addWidget(self.leBackTop)
        self.label_16 = QtWidgets.QLabel(self.gbGraphics)
        self.label_16.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_16.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_29.addWidget(self.label_16)
        self.cbBackRotate = QtWidgets.QComboBox(self.gbGraphics)
        self.cbBackRotate.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cbBackRotate.setMaxVisibleItems(4)
        self.cbBackRotate.setObjectName("cbBackRotate")
        self.cbBackRotate.addItem("")
        self.cbBackRotate.addItem("")
        self.cbBackRotate.addItem("")
        self.cbBackRotate.addItem("")
        self.horizontalLayout_29.addWidget(self.cbBackRotate)
        self.horizontalLayout_29.setStretch(0, 4)
        self.horizontalLayout_29.setStretch(1, 1)
        self.horizontalLayout_29.setStretch(3, 1)
        self.horizontalLayout_29.setStretch(4, 2)
        self.horizontalLayout_29.setStretch(5, 1)
        self.verticalLayout_5.addLayout(self.horizontalLayout_29)
        self.verticalLayout_2.addWidget(self.gbGraphics)
        self.gbBarCode = QtWidgets.QGroupBox(self.centralwidget)
        self.gbBarCode.setObjectName("gbBarCode")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.gbBarCode)
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_28 = QtWidgets.QLabel(self.gbBarCode)
        self.label_28.setObjectName("label_28")
        self.horizontalLayout.addWidget(self.label_28)
        self.cbCodeType = QtWidgets.QComboBox(self.gbBarCode)
        self.cbCodeType.setObjectName("cbCodeType")
        self.cbCodeType.addItem("")
        self.cbCodeType.addItem("")
        self.horizontalLayout.addWidget(self.cbCodeType)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_31 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_31.setSpacing(0)
        self.horizontalLayout_31.setObjectName("horizontalLayout_31")
        self.label_25 = QtWidgets.QLabel(self.gbBarCode)
        self.label_25.setObjectName("label_25")
        self.horizontalLayout_31.addWidget(self.label_25)
        self.leCodeLeft = QtWidgets.QLineEdit(self.gbBarCode)
        self.leCodeLeft.setEnabled(True)
        self.leCodeLeft.setMaxLength(4)
        self.leCodeLeft.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.leCodeLeft.setObjectName("leCodeLeft")
        self.horizontalLayout_31.addWidget(self.leCodeLeft)
        self.label_33 = QtWidgets.QLabel(self.gbBarCode)
        self.label_33.setObjectName("label_33")
        self.horizontalLayout_31.addWidget(self.label_33)
        self.leCodeTop = QtWidgets.QLineEdit(self.gbBarCode)
        self.leCodeTop.setMaxLength(4)
        self.leCodeTop.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.leCodeTop.setObjectName("leCodeTop")
        self.horizontalLayout_31.addWidget(self.leCodeTop)
        self.label_11 = QtWidgets.QLabel(self.gbBarCode)
        self.label_11.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_31.addWidget(self.label_11)
        self.cbCodeRotate = QtWidgets.QComboBox(self.gbBarCode)
        self.cbCodeRotate.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cbCodeRotate.setMaxVisibleItems(4)
        self.cbCodeRotate.setObjectName("cbCodeRotate")
        self.cbCodeRotate.addItem("")
        self.cbCodeRotate.addItem("")
        self.cbCodeRotate.addItem("")
        self.cbCodeRotate.addItem("")
        self.horizontalLayout_31.addWidget(self.cbCodeRotate)
        self.horizontalLayout_31.setStretch(0, 3)
        self.horizontalLayout_31.setStretch(1, 1)
        self.horizontalLayout_31.setStretch(3, 1)
        self.horizontalLayout_31.setStretch(4, 2)
        self.horizontalLayout_31.setStretch(5, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_31)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setSpacing(6)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.label_14 = QtWidgets.QLabel(self.gbBarCode)
        self.label_14.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_18.addWidget(self.label_14)
        self.cbBcLines = QtWidgets.QComboBox(self.gbBarCode)
        self.cbBcLines.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cbBcLines.setMaxVisibleItems(11)
        self.cbBcLines.setObjectName("cbBcLines")
        self.cbBcLines.addItem("")
        self.cbBcLines.addItem("")
        self.cbBcLines.addItem("")
        self.cbBcLines.addItem("")
        self.cbBcLines.addItem("")
        self.cbBcLines.addItem("")
        self.cbBcLines.addItem("")
        self.cbBcLines.addItem("")
        self.cbBcLines.addItem("")
        self.cbBcLines.addItem("")
        self.cbBcLines.addItem("")
        self.horizontalLayout_18.addWidget(self.cbBcLines)
        self.label_13 = QtWidgets.QLabel(self.gbBarCode)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_18.addWidget(self.label_13)
        self.cbBcModuleSize = QtWidgets.QComboBox(self.gbBarCode)
        self.cbBcModuleSize.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cbBcModuleSize.setObjectName("cbBcModuleSize")
        self.cbBcModuleSize.addItem("")
        self.cbBcModuleSize.addItem("")
        self.cbBcModuleSize.addItem("")
        self.cbBcModuleSize.addItem("")
        self.cbBcModuleSize.addItem("")
        self.cbBcModuleSize.addItem("")
        self.cbBcModuleSize.addItem("")
        self.cbBcModuleSize.addItem("")
        self.cbBcModuleSize.addItem("")
        self.cbBcModuleSize.addItem("")
        self.horizontalLayout_18.addWidget(self.cbBcModuleSize)
        self.label_9 = QtWidgets.QLabel(self.gbBarCode)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_18.addWidget(self.label_9)
        self.cbDMHeight = QtWidgets.QComboBox(self.gbBarCode)
        self.cbDMHeight.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cbDMHeight.setObjectName("cbDMHeight")
        self.cbDMHeight.addItem("")
        self.cbDMHeight.addItem("")
        self.cbDMHeight.addItem("")
        self.cbDMHeight.addItem("")
        self.cbDMHeight.addItem("")
        self.cbDMHeight.addItem("")
        self.cbDMHeight.addItem("")
        self.cbDMHeight.addItem("")
        self.cbDMHeight.addItem("")
        self.cbDMHeight.addItem("")
        self.horizontalLayout_18.addWidget(self.cbDMHeight)
        self.horizontalLayout_18.setStretch(0, 4)
        self.horizontalLayout_18.setStretch(1, 2)
        self.horizontalLayout_18.setStretch(2, 4)
        self.horizontalLayout_18.setStretch(3, 2)
        self.horizontalLayout_18.setStretch(4, 4)
        self.horizontalLayout_18.setStretch(5, 2)
        self.verticalLayout.addLayout(self.horizontalLayout_18)
        self.verticalLayout_2.addWidget(self.gbBarCode)
        self.gbText = QtWidgets.QGroupBox(self.centralwidget)
        self.gbText.setCheckable(True)
        self.gbText.setChecked(True)
        self.gbText.setObjectName("gbText")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.gbText)
        self.verticalLayout_4.setContentsMargins(9, -1, 9, 9)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_30 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_30.setSpacing(0)
        self.horizontalLayout_30.setObjectName("horizontalLayout_30")
        self.label_20 = QtWidgets.QLabel(self.gbText)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_30.addWidget(self.label_20)
        self.cbNumeric = QtWidgets.QComboBox(self.gbText)
        self.cbNumeric.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cbNumeric.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.cbNumeric.setObjectName("cbNumeric")
        self.cbNumeric.addItem("")
        self.cbNumeric.addItem("")
        self.horizontalLayout_30.addWidget(self.cbNumeric)
        self.label_15 = QtWidgets.QLabel(self.gbText)
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_30.addWidget(self.label_15)
        self.sbFontSize = QtWidgets.QSpinBox(self.gbText)
        self.sbFontSize.setEnabled(True)
        self.sbFontSize.setMinimum(1)
        self.sbFontSize.setMaximum(48)
        self.sbFontSize.setProperty("value", 18)
        self.sbFontSize.setObjectName("sbFontSize")
        self.horizontalLayout_30.addWidget(self.sbFontSize)
        self.horizontalLayout_30.setStretch(0, 3)
        self.horizontalLayout_30.setStretch(1, 4)
        self.horizontalLayout_30.setStretch(2, 4)
        self.horizontalLayout_30.setStretch(3, 1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_30)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_10 = QtWidgets.QLabel(self.gbText)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_2.addWidget(self.label_10)
        self.leTextLeft = QtWidgets.QLineEdit(self.gbText)
        self.leTextLeft.setMaxLength(4)
        self.leTextLeft.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.leTextLeft.setObjectName("leTextLeft")
        self.horizontalLayout_2.addWidget(self.leTextLeft)
        self.label_32 = QtWidgets.QLabel(self.gbText)
        self.label_32.setObjectName("label_32")
        self.horizontalLayout_2.addWidget(self.label_32)
        self.leTextTop = QtWidgets.QLineEdit(self.gbText)
        self.leTextTop.setMaxLength(4)
        self.leTextTop.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.leTextTop.setObjectName("leTextTop")
        self.horizontalLayout_2.addWidget(self.leTextTop)
        self.label_26 = QtWidgets.QLabel(self.gbText)
        self.label_26.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_26.setObjectName("label_26")
        self.horizontalLayout_2.addWidget(self.label_26)
        self.cbTextRotate = QtWidgets.QComboBox(self.gbText)
        self.cbTextRotate.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cbTextRotate.setObjectName("cbTextRotate")
        self.cbTextRotate.addItem("")
        self.cbTextRotate.addItem("")
        self.cbTextRotate.addItem("")
        self.cbTextRotate.addItem("")
        self.horizontalLayout_2.addWidget(self.cbTextRotate)
        self.horizontalLayout_2.setStretch(0, 4)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(3, 1)
        self.horizontalLayout_2.setStretch(4, 3)
        self.horizontalLayout_2.setStretch(5, 1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_12 = QtWidgets.QLabel(self.gbText)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_14.addWidget(self.label_12)
        self.leTextField = QtWidgets.QLineEdit(self.gbText)
        self.leTextField.setMaxLength(4)
        self.leTextField.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.leTextField.setObjectName("leTextField")
        self.horizontalLayout_14.addWidget(self.leTextField)
        self.label_27 = QtWidgets.QLabel(self.gbText)
        self.label_27.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_27.setObjectName("label_27")
        self.horizontalLayout_14.addWidget(self.label_27)
        self.cbTextAlign = QtWidgets.QComboBox(self.gbText)
        self.cbTextAlign.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cbTextAlign.setObjectName("cbTextAlign")
        self.cbTextAlign.addItem("")
        self.cbTextAlign.addItem("")
        self.cbTextAlign.addItem("")
        self.horizontalLayout_14.addWidget(self.cbTextAlign)
        self.horizontalLayout_14.setStretch(2, 3)
        self.horizontalLayout_14.setStretch(3, 2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_14)
        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(1, 1)
        self.verticalLayout_4.setStretch(2, 1)
        self.verticalLayout_2.addWidget(self.gbText)
        self.btnTestPrint = QtWidgets.QPushButton(self.centralwidget)
        self.btnTestPrint.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnTestPrint.sizePolicy().hasHeightForWidth())
        self.btnTestPrint.setSizePolicy(sizePolicy)
        self.btnTestPrint.setObjectName("btnTestPrint")
        self.verticalLayout_2.addWidget(self.btnTestPrint)
        self.butonBox = QtWidgets.QHBoxLayout()
        self.butonBox.setObjectName("butonBox")
        self.btnDefault = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnDefault.sizePolicy().hasHeightForWidth())
        self.btnDefault.setSizePolicy(sizePolicy)
        self.btnDefault.setObjectName("btnDefault")
        self.butonBox.addWidget(self.btnDefault)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.butonBox.addItem(spacerItem)
        self.btnOk = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnOk.sizePolicy().hasHeightForWidth())
        self.btnOk.setSizePolicy(sizePolicy)
        self.btnOk.setObjectName("btnOk")
        self.butonBox.addWidget(self.btnOk)
        self.btnCancel = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnCancel.sizePolicy().hasHeightForWidth())
        self.btnCancel.setSizePolicy(sizePolicy)
        self.btnCancel.setObjectName("btnCancel")
        self.butonBox.addWidget(self.btnCancel)
        self.butonBox.setStretch(0, 1)
        self.butonBox.setStretch(1, 2)
        self.butonBox.setStretch(2, 2)
        self.butonBox.setStretch(3, 2)
        self.verticalLayout_2.addLayout(self.butonBox)
        self.verticalLayout_2.setStretch(4, 2)
        self.verticalLayout_2.setStretch(5, 1)
        ZplWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ZplWindow)
        self.cbBackRotate.setCurrentIndex(0)
        self.cbCodeRotate.setCurrentIndex(1)
        self.cbBcLines.setCurrentIndex(0)
        self.cbBcModuleSize.setCurrentIndex(1)
        self.cbDMHeight.setCurrentIndex(5)
        self.cbTextAlign.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(ZplWindow)

    def retranslateUi(self, ZplWindow):
        _translate = QtCore.QCoreApplication.translate
        ZplWindow.setWindowTitle(_translate("ZplWindow", "ZEBRA - параметры макета"))
        self.gbZebraPrinter.setTitle(_translate("ZplWindow", "Принтер Zebra:"))
        self.gbGraphics.setTitle(_translate("ZplWindow", "Фоновое изображение:"))
        self.leBack.setPlaceholderText(_translate("ZplWindow", "Файл шаблона этикетки"))
        self.btnOpenBack.setText(_translate("ZplWindow", "..."))
        self.label_24.setText(_translate("ZplWindow", "Положение изображения на шаблоне"))
        self.leBackLeft.setText(_translate("ZplWindow", "0"))
        self.label_35.setText(_translate("ZplWindow", " , "))
        self.leBackTop.setText(_translate("ZplWindow", "0"))
        self.label_16.setText(_translate("ZplWindow", "<html><head/><body><p>Поворот:  </p></body></html>"))
        self.cbBackRotate.setItemText(0, _translate("ZplWindow", "0"))
        self.cbBackRotate.setItemText(1, _translate("ZplWindow", "90"))
        self.cbBackRotate.setItemText(2, _translate("ZplWindow", "180"))
        self.cbBackRotate.setItemText(3, _translate("ZplWindow", "270"))
        self.gbBarCode.setTitle(_translate("ZplWindow", "Параметры генерации штрих-кода:"))
        self.label_28.setText(_translate("ZplWindow", "Тип кода:"))
        self.cbCodeType.setItemText(0, _translate("ZplWindow", "GS1 Datamatrix"))
        self.cbCodeType.setItemText(1, _translate("ZplWindow", "BTS - Barcode"))
        self.label_25.setText(_translate("ZplWindow", "Положение на шаблоне:"))
        self.leCodeLeft.setToolTip(_translate("ZplWindow", "Левая граница кода Datamatrix"))
        self.leCodeLeft.setText(_translate("ZplWindow", "100"))
        self.label_33.setText(_translate("ZplWindow", " , "))
        self.leCodeTop.setToolTip(_translate("ZplWindow", "Верхняя граница кода Datamatrix"))
        self.leCodeTop.setText(_translate("ZplWindow", "100"))
        self.label_11.setText(_translate("ZplWindow", "<html><head/><body><p>Поворот:  </p></body></html>"))
        self.cbCodeRotate.setItemText(0, _translate("ZplWindow", "0"))
        self.cbCodeRotate.setItemText(1, _translate("ZplWindow", "90"))
        self.cbCodeRotate.setItemText(2, _translate("ZplWindow", "180"))
        self.cbCodeRotate.setItemText(3, _translate("ZplWindow", "270"))
        self.label_14.setText(_translate("ZplWindow", "<html><head/><body><p>Соотношение линий: </p></body></html>"))
        self.cbBcLines.setCurrentText(_translate("ZplWindow", "2.0"))
        self.cbBcLines.setItemText(0, _translate("ZplWindow", "2.0"))
        self.cbBcLines.setItemText(1, _translate("ZplWindow", "2.1"))
        self.cbBcLines.setItemText(2, _translate("ZplWindow", "2.2"))
        self.cbBcLines.setItemText(3, _translate("ZplWindow", "2.3"))
        self.cbBcLines.setItemText(4, _translate("ZplWindow", "2.4"))
        self.cbBcLines.setItemText(5, _translate("ZplWindow", "2.5"))
        self.cbBcLines.setItemText(6, _translate("ZplWindow", "2.6"))
        self.cbBcLines.setItemText(7, _translate("ZplWindow", "2.7"))
        self.cbBcLines.setItemText(8, _translate("ZplWindow", "2.8"))
        self.cbBcLines.setItemText(9, _translate("ZplWindow", "2.9"))
        self.cbBcLines.setItemText(10, _translate("ZplWindow", "3.0"))
        self.label_13.setText(_translate("ZplWindow", "<html><head/><body><p>Ширина модуля: </p></body></html>"))
        self.cbBcModuleSize.setCurrentText(_translate("ZplWindow", "2"))
        self.cbBcModuleSize.setItemText(0, _translate("ZplWindow", "1"))
        self.cbBcModuleSize.setItemText(1, _translate("ZplWindow", "2"))
        self.cbBcModuleSize.setItemText(2, _translate("ZplWindow", "3"))
        self.cbBcModuleSize.setItemText(3, _translate("ZplWindow", "4"))
        self.cbBcModuleSize.setItemText(4, _translate("ZplWindow", "5"))
        self.cbBcModuleSize.setItemText(5, _translate("ZplWindow", "6"))
        self.cbBcModuleSize.setItemText(6, _translate("ZplWindow", "7"))
        self.cbBcModuleSize.setItemText(7, _translate("ZplWindow", "8"))
        self.cbBcModuleSize.setItemText(8, _translate("ZplWindow", "9"))
        self.cbBcModuleSize.setItemText(9, _translate("ZplWindow", "10"))
        self.label_9.setText(_translate("ZplWindow", "<html><head/><body><p>Размер ячейки кода: </p></body></html>"))
        self.cbDMHeight.setCurrentText(_translate("ZplWindow", "6"))
        self.cbDMHeight.setItemText(0, _translate("ZplWindow", "1"))
        self.cbDMHeight.setItemText(1, _translate("ZplWindow", "2"))
        self.cbDMHeight.setItemText(2, _translate("ZplWindow", "3"))
        self.cbDMHeight.setItemText(3, _translate("ZplWindow", "4"))
        self.cbDMHeight.setItemText(4, _translate("ZplWindow", "5"))
        self.cbDMHeight.setItemText(5, _translate("ZplWindow", "6"))
        self.cbDMHeight.setItemText(6, _translate("ZplWindow", "7"))
        self.cbDMHeight.setItemText(7, _translate("ZplWindow", "8"))
        self.cbDMHeight.setItemText(8, _translate("ZplWindow", "9"))
        self.cbDMHeight.setItemText(9, _translate("ZplWindow", "10"))
        self.gbText.setTitle(_translate("ZplWindow", "Добавить надпись на коде:"))
        self.label_20.setText(_translate("ZplWindow", "Вид надписи:"))
        self.cbNumeric.setItemText(0, _translate("ZplWindow", "Индивидуальный код"))
        self.cbNumeric.setItemText(1, _translate("ZplWindow", "Порядковый номер"))
        self.label_15.setText(_translate("ZplWindow", "     Размер шрифта: "))
        self.label_10.setText(_translate("ZplWindow", "Положение надписи:     "))
        self.leTextLeft.setText(_translate("ZplWindow", "120"))
        self.label_32.setText(_translate("ZplWindow", ","))
        self.leTextTop.setText(_translate("ZplWindow", "120"))
        self.label_26.setText(_translate("ZplWindow", "Поворот: "))
        self.cbTextRotate.setItemText(0, _translate("ZplWindow", "0"))
        self.cbTextRotate.setItemText(1, _translate("ZplWindow", "90"))
        self.cbTextRotate.setItemText(2, _translate("ZplWindow", "180"))
        self.cbTextRotate.setItemText(3, _translate("ZplWindow", "270"))
        self.label_12.setText(_translate("ZplWindow", "Максимальная ширина поля надписи: "))
        self.leTextField.setText(_translate("ZplWindow", "236"))
        self.label_27.setText(_translate("ZplWindow", "   Выравнивание:   "))
        self.cbTextAlign.setItemText(0, _translate("ZplWindow", "Left"))
        self.cbTextAlign.setItemText(1, _translate("ZplWindow", "Right"))
        self.cbTextAlign.setItemText(2, _translate("ZplWindow", "Auto"))
        self.btnTestPrint.setText(_translate("ZplWindow", "Пробная печать"))
        self.btnDefault.setText(_translate("ZplWindow", "По умолчанию"))
        self.btnOk.setText(_translate("ZplWindow", "Печать"))
        self.btnCancel.setText(_translate("ZplWindow", "Отмена"))
