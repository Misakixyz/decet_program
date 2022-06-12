import shutil

from pyui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QFileDialog ,QTableView
import sys, os
import cv2
from threading import *
import numpy as np
import infer_camera
import time
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
import Infor_sqltools
from qt_material import apply_stylesheet

# SQL number 方便识别表头 ImgT
ID, NAME, ADDRESS = range(3)
# SQL number 方便识别表头 STIO
st_ID, st_NAME, st_TIME, st_IOSTATE, st_ADDRESS = range(5)

# IO_flag = 1 出校，= 0 入校
global IO_flag
IO_flag = 1

# sql添加
global addclicked
addclicked = 0
# 拍照姓名关键字
global PhotoName
PhotoName = "六六"
# 能否拍照关键字
global PhotoName_OK
PhotoName_OK = 0
# 预处理变量
global ShowPredictor

ShowPredictor = infer_camera.Predictor(infer_camera.args.mtcnn_model_path,
                                       infer_camera.args.mobilefacenet_model_path,
                                       infer_camera.args.face_db_path,
                                       threshold=infer_camera.args.threshold)
# 入校关键字
global INclicked
INclicked = 0
# 出校关键字
global OUTclicked
OUTclicked = 1
global photoimg

# 以此方法改变参数
# infer_camera.parser.set_defaults(threshold=0.9)
# infer_camera.args = infer_camera.parser.parse_args()
# print(infer_camera.args.threshold)
# 遍历文件夹下所有文件
def scanDir():
    files = os.listdir('face_db/')
    for file in files:
        file_d = os.path.join('face_db/', file)
        if os.path.isdir(file_d):  # 如果是文件夹则递归调用 scanDir() 函数
            scanDir(file_d)
        else:
            print("scan file" + file_d)


def mycopyfile(srcfile, dstpath):  # 复制函数
    '''
    srcfile 需要复制、移动的文件
    dstpath 目的地址
    '''
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)  # 创建路径
        shutil.copy(srcfile, dstpath + fname)  # 复制文件
        print("copy %s -> %s" % (srcfile, dstpath + fname))


def reShowPredictor():
    '''
    重新装载 ShowPredictor
    '''
    global ShowPredictor
    ShowPredictor = infer_camera.Predictor(infer_camera.args.mtcnn_model_path,
                                           infer_camera.args.mobilefacenet_model_path,
                                           infer_camera.args.face_db_path,
                                           threshold=infer_camera.args.threshold)


def add_table_item_Camera(tableWidget, name, operation, value):
    '''
    在tableWidget中加一行，并将坐标移动到表尾行
    '''
    try:
        row_cnt = tableWidget.rowCount()  # 返回当前行数（尾部）
        tableWidget.insertRow(row_cnt)  # 尾部插入一行新行表格
        tableWidget.setItem(row_cnt, 0, QtWidgets.QTableWidgetItem(str(name)))  # 0 名称
        tableWidget.setItem(row_cnt, 1, QtWidgets.QTableWidgetItem(str(operation)))  # 1 操作
        tableWidget.setItem(row_cnt, 2, QtWidgets.QTableWidgetItem(str(value)))  # 2 值
        tableWidget.scrollToBottom()
    except:
        print('error')


def add_table_item_DataBase(tableWidget, operation, id):
    '''
    在tableWidget中加一行，并将坐标移动到表尾行
    '''
    try:
        row_cnt = tableWidget.rowCount()  # 返回当前行数（尾部）
        tableWidget.insertRow(row_cnt)  # 尾部插入一行新行表格
        tableWidget.setItem(row_cnt, 0, QtWidgets.QTableWidgetItem(str(operation)))
        tableWidget.setItem(row_cnt, 1, QtWidgets.QTableWidgetItem(str(id)))
        tableWidget.scrollToBottom()
    except:
        print('error')


def img_resize(image):
    '''
    图片按比例缩放，用于在Qlabel中显示
    '''
    height, width = image.shape[0], image.shape[1]
    # 设置新的图片分辨率框架
    width_new = 320
    height_new = 240
    # 判断图片的长宽比率
    if width / height >= width_new / height_new:
        img_new = cv2.resize(image, (width_new, int(height * width_new / width)))
    else:
        img_new = cv2.resize(image, (int(width * height_new / height), height_new))
    return img_new


def HSVAlgorithm(rgb_img, value=0.5, basedOnCurrentValue=True):
    hsv_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2HSV)
    img = hsv_img * 1.0
    img_out = img

    # 基于当前亮度进行调整（V*alpha）
    if basedOnCurrentValue:
        # 增量大于0，指数调整
        if value >= 0:
            alpha = 1 - value
            alpha = 1 / alpha

        # 增量小于0，线性调整
        else:
            alpha = value + 1
        img_out[:, :, 2] = img[:, :, 2] * alpha

    else:
        alpha = value
        img_out[:, :, 2] = img[:, :, 2] + 255.0 * alpha

    # HSV亮度上下限处理(小于0取0，大于1取1)
    img_out = img_out / 255.0
    mask_1 = img_out < 0
    mask_2 = img_out > 1
    img_out = img_out * (1 - mask_1)
    img_out = img_out * (1 - mask_2) + mask_2
    img_out = img_out * 255.0

    # HSV转RGB
    img_out = np.round(img_out).astype(np.uint8)
    img_out = cv2.cvtColor(img_out, cv2.COLOR_HSV2BGR)
    img_out = img_out / 255.0

    return img_out


# 继承UI界面
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        self.setupUi(self)

        self.setWindowTitle("人脸识别") # 设置窗口名称
        self.setWindowIcon(QtGui.QIcon("Camera.png")) # 设置程序图标

        # ==============SQL========↓↓↓↓↓↓↓↓↓↓↓↓↓↓========ImgT=======================
        self.createConnection()  # 链接数据库
        self.model = QSqlTableModel(self)
        self.model.setTable("ImgT")
        # 添加表头ID、NAME、ADDRESS
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "NAME")
        self.model.setHeaderData(2, Qt.Horizontal, "ADDRESS")
        self.model.select()
        self.DataBasetableView.setModel(self.model)
        self.table_init()
        self.SQL_tools_init()  # 初始化SQL界面的功能按钮
        # ================SQL===↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑=======================================
        # ================Information=================
        self.Informodel = QSqlTableModel(self)
        self.Informodel.setTable('STIO')
        self.Informodel.setHeaderData(0, Qt.Horizontal, "ID")
        self.Informodel.setHeaderData(1, Qt.Horizontal, "名称")
        self.Informodel.setHeaderData(2, Qt.Horizontal, "时间")
        self.Informodel.setHeaderData(3, Qt.Horizontal, "出/入校")
        self.Informodel.setHeaderData(4, Qt.Horizontal, "ADDRESS")
        self.Informodel.select()
        self.InformationtableView.setModel(self.Informodel)
        Infor_sqltools.table_init(self.InformationtableView)  # 初始化
        self.InforButton_init()
        # ===============Information===================
        # 初始化：摄像头：定时器、摄像头、编号
        self.timer_camera = QTimer()  # 初始化定时器
        self.cap = cv2.VideoCapture()  # 初始化摄像头
        self.CAM_NUM = 0

        # 初始化：阈值，显示在editline上
        self.thresholdlineEdit.setText(str(infer_camera.args.threshold))

        self.tabwidget_init()  # Tab初始化
        self.camera_init()  # 摄像头初始化
        self.PhotoandImport_init()  # 照片导入初始化
        self.Threshold_init()  # 阈值改变初始化
        self.ImgReco_init()  # 照片识别初始化
        self.IOButton_init()  # 出入校按钮初始化

        self.ScanButton.clicked.connect(lambda: self.scanAll_DataBase())  # 扫描face_db

    # 槽函数初始化：SQL工具
    def SQL_tools_init(self):
        self.AddButton.clicked.connect(lambda: self.addRecord())  # 添加行
        self.DeleteButton.clicked.connect(lambda: self.deleteRecord())  # 删除指定行
        self.IDSearch.clicked.connect(lambda: self.id_searchRecord())  # 按ID查询
        self.NameSearch.clicked.connect(lambda: self.name_searchRecord())  # 按NAME查询
        self.OriginButton.clicked.connect(lambda: self.origindata())  # 加载整个ImgT表
        self.DataBasetableView.clicked.connect(lambda: self.tableview_clicked())
        self.DeleteAll.clicked.connect(lambda: self.deleteAll())

    # 槽函数初始化：Tab
    def tabwidget_init(self):
        self.tabWidget.currentChanged.connect(lambda: self.changeTab())  # 切换标签页

    # 槽函数初始化：摄像头
    def camera_init(self):
        self.OpenCamera.clicked.connect(lambda: self.open_camera())  # 摄像头开启和关闭
        self.timer_camera.timeout.connect(lambda: self.show_camera())  # 摄像头定时器

    # 槽函数初始化：拍照、导入照片
    def PhotoandImport_init(self):
        self.PhotoButton.clicked.connect(lambda: self.getPhotoName())
        self.ImportButton.clicked.connect(lambda: self.msg())

    # 槽函数初始化：阈值
    def Threshold_init(self):
        self.thresholdButton.clicked.connect(lambda: self.Threshold_setting())

    # 槽函数初始化：图片识别
    def ImgReco_init(self):
        self.ImgRecoButton.clicked.connect(lambda: self.Imginfer())

    # Tab切换事件
    def changeTab(self):
        if self.tabWidget.currentIndex() == 1 or self.tabWidget.currentIndex() == 2:
            # 关闭摄像头
            self.timer_camera.stop()
            self.cap.release()
            self.Streamlabel.clear()
            self.OpenCamera.setText('打开摄像头')
            self.CS_label.setText('关闭')

    # 出/入校初始化
    def IOButton_init(self):
        self.INButton.clicked.connect(lambda: self.in_school())
        self.OUTButton.clicked.connect(lambda: self.out_school())

    # STIO表sqltools初始化
    def InforButton_init(self):
        self.DeleteButton_Infor.clicked.connect(
            lambda: Infor_sqltools.deleteRecord(self.Informodel, self.InformationtableView,
                                                self.InformationtableWidget))  # 删除初始化
        self.InformationtableView.clicked.connect(
            lambda: Infor_sqltools.tableview_clicked(self.Informodel, self.InformationtableView,
                                                     self.InformationtableWidget, self.InformationImglabel))
        self.NameSearch_Infor.clicked.connect(
            lambda: Infor_sqltools.name_searchRecord(self.Informodel, self.InformationtableView,
                                                     self.InformationtableWidget, self.name_lineEdit_Infor))
        self.IDSearch_Infor.clicked.connect(
            lambda: Infor_sqltools.id_searchRecord(self.Informodel, self.InformationtableView,
                                                   self.InformationtableWidget, self.id_lineEdit_Infor))
        self.OriginButton_Infor.clicked.connect(
            lambda: Infor_sqltools.origindata(self.Informodel, self.InformationtableView,
                                              self.InformationtableWidget))
        self.DeleteAll_Infor.clicked.connect(
            lambda: Infor_sqltools.deleteAllrows(self.Informodel, self.InformationtableView,
                                                 self.InformationtableWidget))
        self.AddButton_Infor.clicked.connect(
            lambda: Infor_sqltools.addRecord(self.Informodel,self.InformationtableView,
                                             self.InformationtableWidget))

    # 出校
    def out_school(self):
        self.IO_label.setText('出校')
        global IO_flag
        IO_flag = 1
        add_table_item_DataBase(self.CameratableWidget, '出/入校', '出校')

    # 入校
    def in_school(self):
        self.IO_label.setText('入校')
        global IO_flag
        IO_flag = 0
        add_table_item_DataBase(self.CameratableWidget, '出/入校', '入校')

    # 消息窗口-输入姓名
    def getPhotoName(self):
        '''
        拍摄照片
        '''
        global photoimg
        global PhotoName
        global PhotoName_OK
        PhotoName_OK = 1
        text, ok = QInputDialog.getText(self, 'PhotoName', '输入姓名：\nID_姓名')
        if ok and text:
            PhotoName = str(text)
            imagepath = 'face_db/' + PhotoName + '.jpg'
            add_table_item_Camera(self.CameratableWidget, PhotoName, '拍摄照片', imagepath)
            print(imagepath)
            cv2.imencode('.jpg', photoimg)[1].tofile(imagepath)
            PhotoName = "溜溜"
            p = Thread(target=reShowPredictor)
            p.start()
            print(PhotoName)

    # 路径选择框
    def msg(self):
        '''
        导入人脸到face_db
        '''
        global ShowPredictor
        # path = 'D:/WIN/Ana-VSCode/qt/face_db'
        directory = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, "选取文件", "./",
                                                          "jpg Files (*.jpg);;Text Files (*.txt)")
        if directory[1]:
            print(directory[0])
            p2 = Thread(target=mycopyfile, args=(directory[0], 'face_db/'))
            p2.start()
            # 刷新face_db
            p = Thread(target=reShowPredictor)
            p.start()
            # 显示到table
            add_table_item_Camera(self.CameratableWidget, '.jpg', '添加照片到face_db', directory[0])
            # 显示在 Imglabel上
            img = cv2.cv2.imdecode(np.fromfile(directory[0], dtype=np.uint8), -1)  # 路径含有中文 需要用imdecode
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            showimg = QtGui.QImage(img.data, img.shape[1], img.shape[0],img.shape[1]*3, QtGui.QImage.Format_RGB888)
            self.Imglabel.setPixmap(QtGui.QPixmap.fromImage(showimg))
        else:
            return

    # 打开摄像头
    def open_camera(self):
        if not self.timer_camera.isActive():
            flag = self.cap.open(self.CAM_NUM, cv2.CAP_DSHOW)
            self.cap.set(6, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))  # 读入mjpg
            self.cap.set(5, 30)  # 帧率
            self.cap.set(3, 1280)  # 帧宽
            self.cap.set(4, 720)  # 帧高
            if not flag:
                pass
            else:
                self.timer_camera.start(30)
                add_table_item_Camera(self.CameratableWidget, 'master', '打开摄像头', -1)
                self.OpenCamera.setText('关闭摄像头')
                self.CS_label.setText('开启')
        else:
            # 关闭摄像头
            self.timer_camera.stop()
            self.cap.release()
            self.cap.release()
            self.Streamlabel.clear()
            self.OpenCamera.setText('打开摄像头')
            add_table_item_Camera(self.CameratableWidget, 'master', '关闭摄像头', -2)
            self.CS_label.setText('关闭')
    def take_Photo(self):
        pass
    # 调用摄像头
    def show_camera(self):
        global PhotoName
        global PhotoName_OK
        global ShowPredictor
        global photoimg
        flag, image = self.cap.read()
        img = cv2.resize(image, (500, 300))
        # img = HSVAlgorithm(img, 0.5, True)
        # 检测人脸
        '''
        拍照
        '''
        if PhotoName_OK == 1:
            '''
            拍摄人脸并存储于face_db
            '''
            photoimg = img
            PhotoName_OK = 0
            print(PhotoName)
            # cv2.imwrite('face_db/' + PhotoName + '.jpg', img) #使用imwrite输入中文会乱码
            # imagepath = 'face_db/' + PhotoName + '.jpg'
            # add_table_item_Camera(self.CameratableWidget, PhotoName, '拍摄照片', imagepath)
            # print(imagepath)
            # cv2.imencode('.jpg', img)[1].tofile(imagepath)
            # PhotoName = "溜溜"
            # p = Thread(target=reShowPredictor)
            # p.start()
            # img = cv2.imdecode(np.fromfile(imagepath, dtype=np.uint8), -1)  # 路径含有中文 需要用imdecode
            phtotimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            '''
            将拍下的人脸显示在lable中
            '''
            phtotimg = img_resize(phtotimg)
            phtotshowimg = QtGui.QImage(phtotimg.data, phtotimg.shape[1], phtotimg.shape[0],phtotimg.shape[1]*3, QtGui.QImage.Format_RGB888)
            self.Imglabel.setPixmap(QtGui.QPixmap.fromImage(phtotshowimg))
            # return
        '''
        视频识别
        '''
        start = time.time()
        boxes, NPresults = ShowPredictor.recognition(img)
        if boxes is not None and NPresults is not None:  # 如果识别到人脸
            names = []
            probs = []
            for NPs in NPresults:
                '''
                分离 NPresults 中的 name 和 prob
                 生成 names 和 probs
                '''
                np_result = NPs
                names.append(np_result[0])
                probs.append(np_result[1])
            print(names)
            print(probs)
            img = ShowPredictor.draw_face(img, boxes, names)  # 在识别到的人脸画上框
            print('draw success')
            lasttime = '视频识别:' + str(int((time.time() - start) * 1000)) + 'ms'
            for NPs in NPresults:
                '''
                分离 NPresults 中的 name 和 prob
                    生成单独的name 和 prob
                    用于添加历史操作表
                '''
                np_result = NPs
                name = np_result[0]
                prob = np_result[1]
                print("add item")
                if IO_flag:
                    Infor_sqltools.addpreRecord(self.Informodel, self.InformationtableView, self.InformationtableWidget,
                                                name, 1)  # 写入到Information表
                else:
                    Infor_sqltools.addpreRecord(self.Informodel, self.InformationtableView, self.InformationtableWidget,
                                                name, 0)  # 写入到Information表
                add_table_item_Camera(self.CameratableWidget, name, lasttime, round(prob, 4))
            print('预测的人脸位置：', boxes.astype('int32').tolist())
            print('识别的人脸名称：', names)
            print('总识别时间：%dms' % int((time.time() - start) * 1000))
        # img = img_resize(img)
        # opencv格式不能直接显示，需要用下面代码转换一下
        # img = img_resize(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        showImage = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGBA8888)
        self.Streamlabel.setPixmap(QtGui.QPixmap.fromImage(showImage))
        return

    # 阈值设定
    def Threshold_setting(self):
        text = self.thresholdlineEdit.text()
        infer_camera.parser.set_defaults(threshold=float(text))
        infer_camera.args = infer_camera.parser.parse_args()
        reShowPredictor()
        add_table_item_Camera(self.CameratableWidget, text, '修改阈值', -3)

    # 外部照片识别
    def Imginfer(self):
        global IO_flag
        if not self.timer_camera.isActive():
            # 文件路径
            directory, ok = QFileDialog.getOpenFileName(self.centralwidget, "选取文件", "./",
                                                        "图像文件 Files (*.jpg)")
            print(directory)
            print(ok)
            if ok:
                img = cv2.imdecode(np.fromfile(directory, dtype=np.uint8), -1)  # 路径含有中文 需要用imdecode
                img = img_resize(img)
                start = time.time()
                boxes, NPresults = ShowPredictor.recognition(img)
                if boxes is not None and NPresults is not None:  # 如果识别到人脸
                    names = []
                    probs = []
                    for NPs in NPresults:
                        '''
                        分离 NPresults 中的 name 和 prob
                         生成 names 和 probs
                        '''
                        np_result = NPs
                        names.append(np_result[0])
                        probs.append(np_result[1])
                    print(names)
                    print(probs)
                    img = ShowPredictor.draw_face(img, boxes, names)  # 在识别到的人脸画上框
                    print('draw success')
                    lasttime = '视频识别:' + str(int((time.time() - start) * 1000)) + 'ms'
                    for NPs in NPresults:
                        '''
                        分离 NPresults 中的 name 和 prob
                            生成单独的name 和 prob
                            用于添加历史操作表
                        '''
                        np_result = NPs
                        name = np_result[0]
                        prob = np_result[1]
                        print("add item")
                        Infor_sqltools.addpreRecord(self.Informodel, self.InformationtableView,
                                                    self.InformationtableWidget,
                                                    name, IO_flag)  # 写入到Information表
                        add_table_item_Camera(self.CameratableWidget, name, lasttime, round(prob, 4))
                    print('预测的人脸位置：', boxes.astype('int32').tolist())
                    print('识别的人脸名称：', names)
                    print('总识别时间：%dms' % int((time.time() - start) * 1000))
                # opencv格式不能直接显示，需要用下面代码转换一下
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
                showImage = QtGui.QImage(img.data, img.shape[1], img.shape[0],img.shape[1]*3, QtGui.QImage.Format_RGBA8888)
                self.Streamlabel.setPixmap(QtGui.QPixmap.fromImage(showImage))
            else:
                return
        else:
            print('camera error')
            if (QMessageBox.question(self, "提示信息",
                                     ("摄像头未开启"),
                                     QMessageBox.Yes) == QMessageBox.Yes):
                return

    # ======================SQL================DataBase=============================================
    def createConnection(self):
        '''
        连接数据库，建表ImgT,建表
        '''
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('qsql.db')
        if not self.db.open():
            QMessageBox.critical(None, '不能打开数据库',
                                 '不能建立数据库连接, 这个例子需要SQLit支持\n'
                                 '要获取如何建立数据库连接，请参考Qt SQL技术文档\n\n'
                                 '点击Cancel按钮退出',
                                 QMessageBox.Cancel)
            return False

        query = QSqlQuery()
        sql_code = u'create table ImgT(ID varchar(50) primary key, NAME varchar(50), ADDRESS varchar(50))'
        if query.exec_(sql_code):
            print('create ImgT')
        else:
            print('ImgT has created')
        query2 = QSqlQuery()
        sql_code2 = u'create table STIO(st_ID varchar(50), st_NAME varchar(50), st_TIME varchar(50), st_IOSTATE varchar(50), st_ADDRESS varchar(50)) '
        if query2.exec_(sql_code2):
            print('create STIO')
        else:
            print('STIO has created')
        return True

    def table_init(self):
        '''
        初始化表头宽度，查询后要重新添加
        '''
        self.DataBasetableView.setColumnWidth(ID, 70)  # 设置 表头“id”宽度
        self.DataBasetableView.setColumnWidth(NAME, 120)  # 设置 表头“NAME”宽度
        self.DataBasetableView.setColumnWidth(ADDRESS, 220)  # 设置 表头“ADDRESS”宽度
        self.DataBasetableView.setSelectionMode(QTableView.SingleSelection)
        self.DataBasetableView.setSelectionBehavior(QTableView.SelectRows)
        self.DataBasetableView.scrollToBottom()

    def modltable_init(self):
        '''
        重新加载表‘ImgT’，用于还原
        '''
        self.model = QSqlTableModel(self)
        self.model.setTable("ImgT")
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "NAME")
        self.model.setHeaderData(2, Qt.Horizontal, "ADDRESS")
        self.model.select()

        self.DataBasetableView.setModel(self.model)
        self.DataBasetableView.setColumnWidth(ID, 70)  # 设置 表头“id”宽度
        self.DataBasetableView.setColumnWidth(NAME, 120)  # 设置 表头“NAME”宽度
        self.DataBasetableView.setColumnWidth(ADDRESS, 220)  # 设置 表头“ADDRESS”宽度
        self.DataBasetableView.setSelectionMode(QTableView.SingleSelection)
        self.DataBasetableView.setSelectionBehavior(QTableView.SelectRows)

    def closeEvent(self, event):
        '''
        触发关闭事件，关闭数据库
        '''
        self.db.close()

    def deleteRecord(self):
        '''
        删除指定行
        '''
        while self.model.canFetchMore():
            self.model.fetchMore()
        index = self.DataBasetableView.currentIndex()
        if not index.isValid():
            return
        record = self.model.record(index.row())
        id = record.value(ID)
        name = record.value(NAME)
        if (QMessageBox.question(self, "提示信息",
                                 ("Delete {0} from ID DataBase?"
                                         .format(id)),
                                 QMessageBox.Yes | QMessageBox.No) ==
                QMessageBox.No):
            return
        self.model.removeRow(index.row())
        self.model.submitAll()
        self.model.select()
        add_table_item_DataBase(self.DataBasetableWidget, '删除行', id)

    def deleteAll(self):
        while self.model.canFetchMore():
            self.model.fetchMore()
        row = self.model.rowCount()
        for i in range(row):
            self.model.removeRow(i)
        self.model.select()
        add_table_item_DataBase(self.DataBasetableWidget, '删除所有行', 'allrows')

    def addRecord(self):
        '''
        添加行，再次点击完成添加
        '''
        while self.model.canFetchMore():
            self.model.fetchMore()
        row = self.model.rowCount()
        self.model.insertRow(row)
        index = self.model.index(row, ID)
        self.DataBasetableView.setCurrentIndex(index)
        self.DataBasetableView.edit(index)

        global addclicked
        if addclicked == 0:
            addclicked = addclicked + 1
        else:
            addclicked = 0
            add_table_item_DataBase(self.DataBasetableWidget, '添加行', '--')

    def addpreRecord(self, add_id, add_name, add_path):
        '''
                添加行，再次点击完成添加
                model.setdata(index,值)
                '''
        while self.model.canFetchMore():
            self.model.fetchMore()
        row = self.model.rowCount()
        self.model.insertRow(row)
        index = self.model.index(row, ID)
        self.DataBasetableView.setCurrentIndex(index)
        self.DataBasetableView.edit(index)

        self.model.setData(self.model.index(row, 0), add_id)
        self.model.setData(self.model.index(row, 1), add_name)
        self.model.setData(self.model.index(row, 2), add_path)

        global addclicked
        if addclicked == 0:
            addclicked = addclicked + 1
        else:
            addclicked = 0
            add_table_item_DataBase(self.DataBasetableWidget, '添加行', '--')

    def id_searchRecord(self):
        '''
        按id查询
        '''
        while self.model.canFetchMore():
            self.model.fetchMore()
        id_text = self.id_lineEdit.text()
        print(id_text)
        # self.model.setTable('ImgT')
        self.model.setFilter("ID ='%s'" % id_text)  # 过滤
        self.DataBasetableView.setModel(self.model)
        self.model.select()
        self.table_init()
        add_table_item_DataBase(self.DataBasetableWidget, '按id查询', id_text)
        self.id_lineEdit.setText('')

    def name_searchRecord(self):
        '''
        按name查询
        '''
        while self.model.canFetchMore():
            self.model.fetchMore()
        name_text = self.name_lineEdit.text()
        print(name_text)
        # self.model.setTable('ImgT')
        self.model.setFilter("NAME ='%s'" % name_text)  # 过滤
        self.DataBasetableView.setModel(self.model)
        self.model.select()
        self.table_init()
        add_table_item_DataBase(self.DataBasetableWidget, '按name查询', name_text)
        self.name_lineEdit.setText('')

    def origindata(self):
        '''
        读取表ImgT
        '''
        while self.model.canFetchMore():
            self.model.fetchMore()
        self.model.setTable('ImgT')
        self.modltable_init()
        add_table_item_DataBase(self.DataBasetableWidget, '返回全表', 'ImgT')

    def tableview_clicked(self):
        '''
        表格单s击事件
        '''
        while self.model.canFetchMore():
            self.model.fetchMore()
        self.dataImglabel.clear()
        index = self.DataBasetableView.currentIndex()
        if not index.isValid():
            return
        record = self.model.record(index.row())
        id = record.value(ID)
        name = record.value(NAME)
        address = record.value(ADDRESS)
        print(address)
        try:
            # 显示到table
            add_table_item_DataBase(self.DataBasetableWidget, '显示图片', address)
            # 显示在 Imglabel上
            img_path = cv2.imdecode(np.fromfile(address, dtype=np.uint8), -1)  # 路径含有中文 需要用imdecode

            img = cv2.cvtColor(img_path, cv2.COLOR_BGR2RGB)
            img = img_resize(img)
            showimg = QtGui.QImage(img.data, img.shape[1], img.shape[0],img.shape[1]*3, QtGui.QImage.Format_RGB888)
            self.dataImglabel.setPixmap(QtGui.QPixmap.fromImage(showimg))
        except:
            print('error')

    def scanAll_DataBase(self):
        files = os.listdir('face_db')
        self.deleteAll()
        while self.model.canFetchMore():
            self.model.fetchMore()
        for file in files:
            if '_' not in file:
                continue
            id = file.split('.')[0].split('_')[0]
            name = file.split('.')[0].split('_')[-1]
            file_d = os.path.join('face_db/', file)  # 路径+文件名

            # self.model.setFilter("ID ='%s'" % id)  # id过滤
            # self.model.select()
            # recordRow = self.model.rowCount()
            # if recordRow == 0:
            row = self.model.rowCount()
            self.model.insertRow(row)
            self.model.setData(self.model.index(row, 0), id)
            self.model.setData(self.model.index(row, 1), name)
            self.model.setData(self.model.index(row, 2), file_d)
            index = self.model.index(row, ID)
            self.DataBasetableView.setCurrentIndex(index)
            self.modltable_init()
        add_table_item_DataBase(self.DataBasetableWidget, '扫描全表', '--')

    # =============================SQL=========DataBase===========================================


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)  # 适配2k屏幕
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MyApp()

    apply_stylesheet(app, theme='dark_teal.xml') # 使用样式

    mainWindow.show()  # 显示mainWindow
    sys.exit(app.exec_())  # 关闭窗口
