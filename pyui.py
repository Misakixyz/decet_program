# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(938, 685)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 931, 661))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.tabWidget.setFont(font)
        self.tabWidget.setFocusPolicy(QtCore.Qt.TabFocus)
        self.tabWidget.setObjectName("tabWidget")
        self.Camera = QtWidgets.QWidget()
        self.Camera.setObjectName("Camera")
        self.Camera_Stream_widget = QtWidgets.QWidget(self.Camera)
        self.Camera_Stream_widget.setGeometry(QtCore.QRect(0, 0, 511, 331))
        self.Camera_Stream_widget.setObjectName("Camera_Stream_widget")
        self.label = QtWidgets.QLabel(self.Camera_Stream_widget)
        self.label.setGeometry(QtCore.QRect(0, 0, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.CS_label = QtWidgets.QLabel(self.Camera_Stream_widget)
        self.CS_label.setGeometry(QtCore.QRect(160, 0, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.CS_label.setFont(font)
        self.CS_label.setObjectName("CS_label")
        self.Streamlabel = QtWidgets.QLabel(self.Camera_Stream_widget)
        self.Streamlabel.setGeometry(QtCore.QRect(0, 30, 501, 301))
        self.Streamlabel.setStyleSheet("border-width: 1px;border-style: solid;border-color: rgb(255, 170, 0);background-color: rgb(100, 149, 237);")
        self.Streamlabel.setFrameShape(QtWidgets.QFrame.Box)
        self.Streamlabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Streamlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.Streamlabel.setObjectName("Streamlabel")
        self.IO_label = QtWidgets.QLabel(self.Camera_Stream_widget)
        self.IO_label.setGeometry(QtCore.QRect(380, 0, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.IO_label.setFont(font)
        self.IO_label.setObjectName("IO_label")
        self.label_6 = QtWidgets.QLabel(self.Camera_Stream_widget)
        self.label_6.setGeometry(QtCore.QRect(290, 0, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.Camera_widget = QtWidgets.QWidget(self.Camera)
        self.Camera_widget.setGeometry(QtCore.QRect(620, 340, 211, 271))
        self.Camera_widget.setObjectName("Camera_widget")
        self.OpenCamera = QtWidgets.QPushButton(self.Camera_widget)
        self.OpenCamera.setGeometry(QtCore.QRect(10, 10, 141, 41))
        self.OpenCamera.setObjectName("OpenCamera")
        self.PhotoButton = QtWidgets.QPushButton(self.Camera_widget)
        self.PhotoButton.setGeometry(QtCore.QRect(10, 60, 141, 31))
        self.PhotoButton.setObjectName("PhotoButton")
        self.ImportButton = QtWidgets.QPushButton(self.Camera_widget)
        self.ImportButton.setGeometry(QtCore.QRect(10, 150, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ImportButton.setFont(font)
        self.ImportButton.setObjectName("ImportButton")
        self.ImgRecoButton = QtWidgets.QPushButton(self.Camera_widget)
        self.ImgRecoButton.setGeometry(QtCore.QRect(10, 110, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ImgRecoButton.setFont(font)
        self.ImgRecoButton.setObjectName("ImgRecoButton")
        self.OUTButton = QtWidgets.QPushButton(self.Camera_widget)
        self.OUTButton.setGeometry(QtCore.QRect(10, 220, 61, 31))
        self.OUTButton.setObjectName("OUTButton")
        self.INButton = QtWidgets.QPushButton(self.Camera_widget)
        self.INButton.setGeometry(QtCore.QRect(90, 220, 61, 31))
        self.INButton.setObjectName("INButton")
        self.CameratableWidget = QtWidgets.QTableWidget(self.Camera)
        self.CameratableWidget.setGeometry(QtCore.QRect(0, 340, 601, 271))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.CameratableWidget.setFont(font)
        self.CameratableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.CameratableWidget.setObjectName("CameratableWidget")
        self.CameratableWidget.setColumnCount(3)
        self.CameratableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.CameratableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.CameratableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.CameratableWidget.setHorizontalHeaderItem(2, item)
        self.CameratableWidget.horizontalHeader().setDefaultSectionSize(190)
        self.CameratableWidget.horizontalHeader().setMinimumSectionSize(50)
        self.CameratableWidget.horizontalHeader().setStretchLastSection(True)
        self.CameratableWidget.verticalHeader().setDefaultSectionSize(50)
        self.label_2 = QtWidgets.QLabel(self.Camera)
        self.label_2.setGeometry(QtCore.QRect(530, 10, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.thresholdlineEdit = QtWidgets.QLineEdit(self.Camera)
        self.thresholdlineEdit.setGeometry(QtCore.QRect(620, 10, 71, 20))
        self.thresholdlineEdit.setObjectName("thresholdlineEdit")
        self.thresholdButton = QtWidgets.QPushButton(self.Camera)
        self.thresholdButton.setGeometry(QtCore.QRect(700, 10, 51, 23))
        self.thresholdButton.setObjectName("thresholdButton")
        self.Imglabel = QtWidgets.QLabel(self.Camera)
        self.Imglabel.setGeometry(QtCore.QRect(530, 40, 381, 251))
        self.Imglabel.setStyleSheet("border-width: 1px;border-style: solid;border-color: rgb(255, 170, 0);background-color: rgb(100, 100, 100);")
        self.Imglabel.setScaledContents(False)
        self.Imglabel.setAlignment(QtCore.Qt.AlignCenter)
        self.Imglabel.setObjectName("Imglabel")
        self.tabWidget.addTab(self.Camera, "")
        self.DataBase = QtWidgets.QWidget()
        self.DataBase.setObjectName("DataBase")
        self.DataBasetableWidget = QtWidgets.QTableWidget(self.DataBase)
        self.DataBasetableWidget.setGeometry(QtCore.QRect(0, 340, 421, 271))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.DataBasetableWidget.setFont(font)
        self.DataBasetableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.DataBasetableWidget.setObjectName("DataBasetableWidget")
        self.DataBasetableWidget.setColumnCount(2)
        self.DataBasetableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.DataBasetableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.DataBasetableWidget.setHorizontalHeaderItem(1, item)
        self.DataBasetableWidget.horizontalHeader().setDefaultSectionSize(105)
        self.DataBasetableWidget.horizontalHeader().setMinimumSectionSize(50)
        self.DataBasetableWidget.horizontalHeader().setStretchLastSection(True)
        self.DataBasetableWidget.verticalHeader().setDefaultSectionSize(50)
        self.widget = QtWidgets.QWidget(self.DataBase)
        self.widget.setGeometry(QtCore.QRect(0, 0, 511, 331))
        self.widget.setObjectName("widget")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(130, 0, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.DataBasetableView = QtWidgets.QTableView(self.widget)
        self.DataBasetableView.setGeometry(QtCore.QRect(0, 30, 501, 291))
        self.DataBasetableView.setObjectName("DataBasetableView")
        self.DataBasetableView.horizontalHeader().setDefaultSectionSize(200)
        self.dataImglabel = QtWidgets.QLabel(self.DataBase)
        self.dataImglabel.setGeometry(QtCore.QRect(520, 30, 391, 281))
        self.dataImglabel.setStyleSheet("border-width: 1px;border-style: solid;border-color: rgb(255, 170, 0);background-color: rgb(100, 100, 100);")
        self.dataImglabel.setScaledContents(False)
        self.dataImglabel.setAlignment(QtCore.Qt.AlignCenter)
        self.dataImglabel.setObjectName("dataImglabel")
        self.widget_2 = QtWidgets.QWidget(self.DataBase)
        self.widget_2.setGeometry(QtCore.QRect(430, 340, 481, 271))
        self.widget_2.setObjectName("widget_2")
        self.AddButton = QtWidgets.QPushButton(self.widget_2)
        self.AddButton.setGeometry(QtCore.QRect(10, 120, 121, 31))
        self.AddButton.setObjectName("AddButton")
        self.DeleteButton = QtWidgets.QPushButton(self.widget_2)
        self.DeleteButton.setGeometry(QtCore.QRect(10, 160, 141, 31))
        self.DeleteButton.setObjectName("DeleteButton")
        self.OriginButton = QtWidgets.QPushButton(self.widget_2)
        self.OriginButton.setGeometry(QtCore.QRect(250, 90, 131, 31))
        self.OriginButton.setObjectName("OriginButton")
        self.NameSearch = QtWidgets.QPushButton(self.widget_2)
        self.NameSearch.setGeometry(QtCore.QRect(250, 10, 131, 31))
        self.NameSearch.setObjectName("NameSearch")
        self.label_4 = QtWidgets.QLabel(self.widget_2)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 91, 31))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.widget_2)
        self.label_5.setGeometry(QtCore.QRect(10, 50, 81, 21))
        self.label_5.setObjectName("label_5")
        self.name_lineEdit = QtWidgets.QLineEdit(self.widget_2)
        self.name_lineEdit.setGeometry(QtCore.QRect(110, 20, 113, 21))
        self.name_lineEdit.setObjectName("name_lineEdit")
        self.id_lineEdit = QtWidgets.QLineEdit(self.widget_2)
        self.id_lineEdit.setGeometry(QtCore.QRect(110, 50, 113, 21))
        self.id_lineEdit.setObjectName("id_lineEdit")
        self.IDSearch = QtWidgets.QPushButton(self.widget_2)
        self.IDSearch.setGeometry(QtCore.QRect(250, 40, 131, 31))
        self.IDSearch.setObjectName("IDSearch")
        self.ScanButton = QtWidgets.QPushButton(self.widget_2)
        self.ScanButton.setGeometry(QtCore.QRect(250, 130, 131, 31))
        self.ScanButton.setObjectName("ScanButton")
        self.DeleteAll = QtWidgets.QPushButton(self.widget_2)
        self.DeleteAll.setGeometry(QtCore.QRect(10, 200, 141, 31))
        self.DeleteAll.setObjectName("DeleteAll")
        self.tabWidget.addTab(self.DataBase, "")
        self.Information = QtWidgets.QWidget()
        self.Information.setObjectName("Information")
        self.InformationtableWidget = QtWidgets.QTableWidget(self.Information)
        self.InformationtableWidget.setGeometry(QtCore.QRect(0, 340, 421, 271))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.InformationtableWidget.setFont(font)
        self.InformationtableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.InformationtableWidget.setObjectName("InformationtableWidget")
        self.InformationtableWidget.setColumnCount(2)
        self.InformationtableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.InformationtableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.InformationtableWidget.setHorizontalHeaderItem(1, item)
        self.InformationtableWidget.horizontalHeader().setDefaultSectionSize(105)
        self.InformationtableWidget.horizontalHeader().setMinimumSectionSize(50)
        self.InformationtableWidget.horizontalHeader().setStretchLastSection(True)
        self.InformationtableWidget.verticalHeader().setDefaultSectionSize(50)
        self.widget_3 = QtWidgets.QWidget(self.Information)
        self.widget_3.setGeometry(QtCore.QRect(0, 0, 551, 331))
        self.widget_3.setObjectName("widget_3")
        self.label_9 = QtWidgets.QLabel(self.widget_3)
        self.label_9.setGeometry(QtCore.QRect(130, 0, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.InformationtableView = QtWidgets.QTableView(self.widget_3)
        self.InformationtableView.setGeometry(QtCore.QRect(0, 30, 541, 291))
        self.InformationtableView.setObjectName("InformationtableView")
        self.InformationtableView.horizontalHeader().setDefaultSectionSize(200)
        self.widget_4 = QtWidgets.QWidget(self.Information)
        self.widget_4.setGeometry(QtCore.QRect(450, 340, 461, 261))
        self.widget_4.setObjectName("widget_4")
        self.AddButton_Infor = QtWidgets.QPushButton(self.widget_4)
        self.AddButton_Infor.setGeometry(QtCore.QRect(10, 130, 121, 31))
        self.AddButton_Infor.setObjectName("AddButton_Infor")
        self.DeleteButton_Infor = QtWidgets.QPushButton(self.widget_4)
        self.DeleteButton_Infor.setGeometry(QtCore.QRect(10, 170, 141, 31))
        self.DeleteButton_Infor.setObjectName("DeleteButton_Infor")
        self.OriginButton_Infor = QtWidgets.QPushButton(self.widget_4)
        self.OriginButton_Infor.setGeometry(QtCore.QRect(240, 100, 121, 31))
        self.OriginButton_Infor.setObjectName("OriginButton_Infor")
        self.NameSearch_Infor = QtWidgets.QPushButton(self.widget_4)
        self.NameSearch_Infor.setGeometry(QtCore.QRect(240, 10, 121, 31))
        self.NameSearch_Infor.setObjectName("NameSearch_Infor")
        self.label_10 = QtWidgets.QLabel(self.widget_4)
        self.label_10.setGeometry(QtCore.QRect(10, 20, 91, 21))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.widget_4)
        self.label_11.setGeometry(QtCore.QRect(10, 50, 71, 21))
        self.label_11.setObjectName("label_11")
        self.name_lineEdit_Infor = QtWidgets.QLineEdit(self.widget_4)
        self.name_lineEdit_Infor.setGeometry(QtCore.QRect(110, 20, 113, 20))
        self.name_lineEdit_Infor.setObjectName("name_lineEdit_Infor")
        self.id_lineEdit_Infor = QtWidgets.QLineEdit(self.widget_4)
        self.id_lineEdit_Infor.setGeometry(QtCore.QRect(110, 50, 113, 20))
        self.id_lineEdit_Infor.setObjectName("id_lineEdit_Infor")
        self.IDSearch_Infor = QtWidgets.QPushButton(self.widget_4)
        self.IDSearch_Infor.setGeometry(QtCore.QRect(240, 50, 121, 31))
        self.IDSearch_Infor.setObjectName("IDSearch_Infor")
        self.DeleteAll_Infor = QtWidgets.QPushButton(self.widget_4)
        self.DeleteAll_Infor.setGeometry(QtCore.QRect(10, 210, 141, 31))
        self.DeleteAll_Infor.setObjectName("DeleteAll_Infor")
        self.InformationImglabel = QtWidgets.QLabel(self.Information)
        self.InformationImglabel.setGeometry(QtCore.QRect(550, 30, 371, 291))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.InformationImglabel.setFont(font)
        self.InformationImglabel.setStyleSheet("border-width: 1px;border-style: solid;border-color: rgb(255, 170, 0);background-color: rgb(100, 100, 100);")
        self.InformationImglabel.setScaledContents(False)
        self.InformationImglabel.setAlignment(QtCore.Qt.AlignCenter)
        self.InformationImglabel.setObjectName("InformationImglabel")
        self.tabWidget.addTab(self.Information, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 938, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "??????????????????"))
        self.CS_label.setText(_translate("MainWindow", "??????"))
        self.Streamlabel.setText(_translate("MainWindow", "Stream"))
        self.IO_label.setText(_translate("MainWindow", "??????"))
        self.label_6.setText(_translate("MainWindow", "?????????"))
        self.OpenCamera.setText(_translate("MainWindow", "???????????????"))
        self.PhotoButton.setText(_translate("MainWindow", "??????"))
        self.ImportButton.setText(_translate("MainWindow", "???????????????face_db"))
        self.ImgRecoButton.setText(_translate("MainWindow", "????????????????????????"))
        self.OUTButton.setText(_translate("MainWindow", "??????"))
        self.INButton.setText(_translate("MainWindow", "??????"))
        self.CameratableWidget.setSortingEnabled(True)
        item = self.CameratableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "??????"))
        item = self.CameratableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "??????"))
        item = self.CameratableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "???"))
        self.label_2.setText(_translate("MainWindow", "????????????"))
        self.thresholdButton.setText(_translate("MainWindow", "ok"))
        self.Imglabel.setText(_translate("MainWindow", "ImgLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Camera), _translate("MainWindow", "Camera"))
        item = self.DataBasetableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "??????"))
        item = self.DataBasetableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "???"))
        self.label_3.setText(_translate("MainWindow", "DataBase"))
        self.dataImglabel.setText(_translate("MainWindow", "ImgLabel"))
        self.AddButton.setText(_translate("MainWindow", "??????"))
        self.DeleteButton.setText(_translate("MainWindow", "???????????????"))
        self.OriginButton.setText(_translate("MainWindow", "????????????"))
        self.NameSearch.setText(_translate("MainWindow", "Name ??????"))
        self.label_4.setText(_translate("MainWindow", "??????Name"))
        self.label_5.setText(_translate("MainWindow", "??????ID"))
        self.IDSearch.setText(_translate("MainWindow", "ID ??????"))
        self.ScanButton.setText(_translate("MainWindow", "????????????"))
        self.DeleteAll.setText(_translate("MainWindow", "???????????????"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.DataBase), _translate("MainWindow", "DataBase"))
        item = self.InformationtableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "??????"))
        item = self.InformationtableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "???"))
        self.label_9.setText(_translate("MainWindow", "Information"))
        self.AddButton_Infor.setText(_translate("MainWindow", "??????"))
        self.DeleteButton_Infor.setText(_translate("MainWindow", "???????????????"))
        self.OriginButton_Infor.setText(_translate("MainWindow", "????????????"))
        self.NameSearch_Infor.setText(_translate("MainWindow", "Name ??????"))
        self.label_10.setText(_translate("MainWindow", "??????Name"))
        self.label_11.setText(_translate("MainWindow", "??????ID"))
        self.IDSearch_Infor.setText(_translate("MainWindow", "ID ??????"))
        self.DeleteAll_Infor.setText(_translate("MainWindow", "???????????????"))
        self.InformationImglabel.setText(_translate("MainWindow", "ImgLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Information), _translate("MainWindow", "Information"))
