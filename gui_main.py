# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DoseVerificationGUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(742, 706)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBoxLeftUp = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxLeftUp.setTitle("")
        self.groupBoxLeftUp.setObjectName("groupBoxLeftUp")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBoxLeftUp)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBoxLeftUp)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBoxLeftUp)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 2, 1, 1)
        self.doubleSpinBoxYSize = QtWidgets.QDoubleSpinBox(self.groupBoxLeftUp)
        self.doubleSpinBoxYSize.setProperty("value", 1.0)
        self.doubleSpinBoxYSize.setObjectName("doubleSpinBoxYSize")
        self.gridLayout.addWidget(self.doubleSpinBoxYSize, 1, 1, 1, 1)
        self.doubleSpinBoxXSize = QtWidgets.QDoubleSpinBox(self.groupBoxLeftUp)
        self.doubleSpinBoxXSize.setSingleStep(1.0)
        self.doubleSpinBoxXSize.setProperty("value", 1.0)
        self.doubleSpinBoxXSize.setObjectName("doubleSpinBoxXSize")
        self.gridLayout.addWidget(self.doubleSpinBoxXSize, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBoxLeftUp)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBoxLeftUp)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)
        self.doubleSpinBoxZSize = QtWidgets.QDoubleSpinBox(self.groupBoxLeftUp)
        self.doubleSpinBoxZSize.setProperty("value", 1.0)
        self.doubleSpinBoxZSize.setObjectName("doubleSpinBoxZSize")
        self.gridLayout.addWidget(self.doubleSpinBoxZSize, 1, 2, 1, 1)
        self.verticalLayout_5.addWidget(self.groupBoxLeftUp)
        self.groupBox_LeftCenter = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_LeftCenter.setTitle("")
        self.groupBox_LeftCenter.setObjectName("groupBox_LeftCenter")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_LeftCenter)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_7 = QtWidgets.QLabel(self.groupBox_LeftCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 2, 1, 1, 1)
        self.spinBoxShapeX = QtWidgets.QSpinBox(self.groupBox_LeftCenter)
        self.spinBoxShapeX.setMaximum(1000000)
        self.spinBoxShapeX.setProperty("value", 320)
        self.spinBoxShapeX.setObjectName("spinBoxShapeX")
        self.gridLayout_2.addWidget(self.spinBoxShapeX, 1, 0, 1, 1)
        self.spinBoxShapeY = QtWidgets.QSpinBox(self.groupBox_LeftCenter)
        self.spinBoxShapeY.setMaximum(1000000)
        self.spinBoxShapeY.setProperty("value", 320)
        self.spinBoxShapeY.setObjectName("spinBoxShapeY")
        self.gridLayout_2.addWidget(self.spinBoxShapeY, 1, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox_LeftCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 2, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox_LeftCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_LeftCenter)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 1, 1, 1)
        self.spinBoxShapeZ = QtWidgets.QSpinBox(self.groupBox_LeftCenter)
        self.spinBoxShapeZ.setMaximum(1000000)
        self.spinBoxShapeZ.setProperty("value", 200)
        self.spinBoxShapeZ.setObjectName("spinBoxShapeZ")
        self.gridLayout_2.addWidget(self.spinBoxShapeZ, 1, 2, 1, 1)
        self.verticalLayout_5.addWidget(self.groupBox_LeftCenter)
        self.groupBox_LeftDown = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_LeftDown.setTitle("")
        self.groupBox_LeftDown.setObjectName("groupBox_LeftDown")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_LeftDown)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_6 = QtWidgets.QFrame(self.groupBox_LeftDown)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_15 = QtWidgets.QLabel(self.frame_6)
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.verticalLayout_2.addWidget(self.label_15)
        self.label_10 = QtWidgets.QLabel(self.frame_6)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_2.addWidget(self.label_10)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButton_X = QtWidgets.QRadioButton(self.frame_6)
        self.radioButton_X.setObjectName("radioButton_X")
        self.horizontalLayout.addWidget(self.radioButton_X)
        self.radioButton_Y = QtWidgets.QRadioButton(self.frame_6)
        self.radioButton_Y.setChecked(True)
        self.radioButton_Y.setObjectName("radioButton_Y")
        self.horizontalLayout.addWidget(self.radioButton_Y)
        self.radioButton_Z = QtWidgets.QRadioButton(self.frame_6)
        self.radioButton_Z.setObjectName("radioButton_Z")
        self.horizontalLayout.addWidget(self.radioButton_Z)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.frame_6)
        self.frame_5 = QtWidgets.QFrame(self.groupBox_LeftDown)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.spinBox_layerNumber = QtWidgets.QSpinBox(self.frame_5)
        self.spinBox_layerNumber.setObjectName("spinBox_layerNumber")
        self.horizontalLayout_3.addWidget(self.spinBox_layerNumber)
        self.label_16 = QtWidgets.QLabel(self.frame_5)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_3.addWidget(self.label_16)
        self.verticalLayout.addWidget(self.frame_5)
        self.frame_3 = QtWidgets.QFrame(self.groupBox_LeftDown)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_showLayer3D = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_showLayer3D.setEnabled(False)
        self.pushButton_showLayer3D.setObjectName("pushButton_showLayer3D")
        self.horizontalLayout_4.addWidget(self.pushButton_showLayer3D)
        self.pushButton_layerDoseMap = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_layerDoseMap.setEnabled(False)
        self.pushButton_layerDoseMap.setObjectName("pushButton_layerDoseMap")
        self.horizontalLayout_4.addWidget(self.pushButton_layerDoseMap)
        self.pushButton_saveLayer = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_saveLayer.setEnabled(False)
        self.pushButton_saveLayer.setObjectName("pushButton_saveLayer")
        self.horizontalLayout_4.addWidget(self.pushButton_saveLayer)
        self.verticalLayout.addWidget(self.frame_3)
        self.verticalLayout_5.addWidget(self.groupBox_LeftDown)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMaximumSize(QtCore.QSize(421, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.textBrowser = QtWidgets.QTextBrowser(self.frame)
        self.textBrowser.setMaximumSize(QtCore.QSize(391, 259))
        self.textBrowser.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_3.addWidget(self.textBrowser, 2, 0, 1, 1)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_4)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.frame_8 = QtWidgets.QFrame(self.frame_4)
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.frame_8)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_13 = QtWidgets.QLabel(self.frame_8)
        self.label_13.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.gridLayout_7.addWidget(self.label_13, 2, 2, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.frame_8)
        self.label_12.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout_7.addWidget(self.label_12, 4, 2, 1, 1)
        self.doubleSpinBox_RotX = QtWidgets.QDoubleSpinBox(self.frame_8)
        self.doubleSpinBox_RotX.setDecimals(2)
        self.doubleSpinBox_RotX.setMinimum(-90.0)
        self.doubleSpinBox_RotX.setMaximum(90.0)
        self.doubleSpinBox_RotX.setObjectName("doubleSpinBox_RotX")
        self.gridLayout_7.addWidget(self.doubleSpinBox_RotX, 3, 1, 1, 1)
        self.doubleSpinBox_RotZ = QtWidgets.QDoubleSpinBox(self.frame_8)
        self.doubleSpinBox_RotZ.setMinimum(-90.0)
        self.doubleSpinBox_RotZ.setMaximum(90.0)
        self.doubleSpinBox_RotZ.setObjectName("doubleSpinBox_RotZ")
        self.gridLayout_7.addWidget(self.doubleSpinBox_RotZ, 4, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.frame_8)
        self.label_14.setObjectName("label_14")
        self.gridLayout_7.addWidget(self.label_14, 0, 2, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.frame_8)
        self.label_11.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.gridLayout_7.addWidget(self.label_11, 3, 2, 1, 1)
        self.doubleSpinBox_PlaceY = QtWidgets.QDoubleSpinBox(self.frame_8)
        self.doubleSpinBox_PlaceY.setMinimum(0.0)
        self.doubleSpinBox_PlaceY.setMaximum(1000.0)
        self.doubleSpinBox_PlaceY.setSingleStep(1.0)
        self.doubleSpinBox_PlaceY.setObjectName("doubleSpinBox_PlaceY")
        self.gridLayout_7.addWidget(self.doubleSpinBox_PlaceY, 2, 1, 1, 1)
        self.gridLayout_4.addWidget(self.frame_8, 1, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.frame_4)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_4.addWidget(self.label_9, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.frame_4, 0, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.pushButton_ShowResult2D = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_ShowResult2D.setEnabled(False)
        self.pushButton_ShowResult2D.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pushButton_ShowResult2D.setObjectName("pushButton_ShowResult2D")
        self.gridLayout_6.addWidget(self.pushButton_ShowResult2D, 2, 0, 1, 1)
        self.pushButton_Run = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_Run.setEnabled(False)
        self.pushButton_Run.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pushButton_Run.setObjectName("pushButton_Run")
        self.gridLayout_6.addWidget(self.pushButton_Run, 1, 0, 1, 1)
        self.pushButton_Show3D = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_Show3D.setEnabled(False)
        self.pushButton_Show3D.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pushButton_Show3D.setObjectName("pushButton_Show3D")
        self.gridLayout_6.addWidget(self.pushButton_Show3D, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.frame_2, 1, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 742, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_LoadTomo = QtWidgets.QAction(MainWindow)
        self.action_LoadTomo.setObjectName("action_LoadTomo")
        self.action_ChoosePath = QtWidgets.QAction(MainWindow)
        self.action_ChoosePath.setObjectName("action_ChoosePath")
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.menu.addAction(self.action_LoadTomo)
        self.menu.addAction(self.action_ChoosePath)
        self.menu.addAction(self.action)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Dose Verification"))
        self.label_2.setText(_translate("MainWindow", "Размер по X, мм"))
        self.label_4.setText(_translate("MainWindow", "Размер по Z, мм"))
        self.label.setText(_translate("MainWindow", "Размеры вокселя"))
        self.label_3.setText(_translate("MainWindow", "Размер по Y, мм"))
        self.label_7.setText(_translate("MainWindow", "Число вокселей по Y"))
        self.label_8.setText(_translate("MainWindow", "Число вокселей по Z"))
        self.label_6.setText(_translate("MainWindow", "Число вокселей по X"))
        self.label_5.setText(_translate("MainWindow", "Форма томограммы"))
        self.label_15.setText(_translate("MainWindow", "Визуализация слоя"))
        self.label_10.setText(_translate("MainWindow", "Слой перпендикулярен оси:"))
        self.radioButton_X.setText(_translate("MainWindow", "X"))
        self.radioButton_Y.setText(_translate("MainWindow", "Y"))
        self.radioButton_Z.setText(_translate("MainWindow", "Z"))
        self.label_16.setText(_translate("MainWindow", "Номер слоя"))
        self.pushButton_showLayer3D.setText(_translate("MainWindow", "Положение слоя (показать 3D)"))
        self.pushButton_layerDoseMap.setText(_translate("MainWindow", "Распределение дозы"))
        self.pushButton_saveLayer.setText(_translate("MainWindow", "Сохранить"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Для начала работы загрузите файл томограммы в формате .dose</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">(Файл --&gt; Загрузить Томо)</p></body></html>"))
        self.label_13.setText(_translate("MainWindow", "Смещение по Y , мм"))
        self.label_12.setText(_translate("MainWindow", "Поворот отн. Z, градусов"))
        self.label_14.setText(_translate("MainWindow", "Поворот, градусов"))
        self.label_11.setText(_translate("MainWindow", "Поворот отн. X, градусов"))
        self.label_9.setText(_translate("MainWindow", "Положение измерительной пластины"))
        self.pushButton_ShowResult2D.setText(_translate("MainWindow", "Результат расчёта 2D"))
        self.pushButton_Run.setText(_translate("MainWindow", "Запустить расчёт"))
        self.pushButton_Show3D.setText(_translate("MainWindow", "Показать 3D"))
        self.menu.setTitle(_translate("MainWindow", "Файл"))
        self.action_LoadTomo.setText(_translate("MainWindow", "Загрузить файл *.dose"))
        self.action_ChoosePath.setText(_translate("MainWindow", "Выбрать путь сохранения"))
        self.action.setText(_translate("MainWindow", "Открыть сохранённую диаграмму *.npy"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
