# == == == == == == == == == == == == == == =SQL == == == == = Information == == == == == == == == == == == == == == == == == == == == == =
import cv2
import numpy as np
from PyQt5.QtWidgets import  QTableView
from PyQt5 import  QtGui, QtWidgets
from PyQt5.QtCore import Qt

import datetime

# SQL number 方便识别表头 STIO
st_ID, st_NAME, st_TIME, st_IOSTATE, st_ADDRESS = range(5)

global all_IDs
all_IDs = 0
global addclicked
addclicked = 0


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


def add_table_item_Information(tableWidget, operation, id):
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


def modltable_init(model, tableView):
    '''
    重新加载表‘modelTableName’，用于还原
    '''
    model.setTable('STIO')
    model.setHeaderData(st_ID, Qt.Horizontal, "ID")
    model.setHeaderData(st_NAME, Qt.Horizontal, "名称")
    model.setHeaderData(st_TIME, Qt.Horizontal, "时间")
    model.setHeaderData(st_IOSTATE, Qt.Horizontal, "出/入校")
    model.setHeaderData(st_ADDRESS, Qt.Horizontal, "ADDRESS")
    model.select()

    tableView.setColumnWidth(st_ID, 70)  # 设置 表头“st_ID”宽度
    tableView.setColumnWidth(st_NAME, 100)  # 设置 表头“st_NAME”宽度
    tableView.setColumnWidth(st_TIME, 180)  # 设置 表头“st_TIME”宽度
    tableView.setColumnWidth(st_IOSTATE, 100)  # 设置 表头“st_IOSTATE”宽度
    tableView.setColumnWidth(st_ADDRESS, 250)  # 设置 表头“st_ADDRESS”宽度
    tableView.setColumnHidden(st_ADDRESS, True)  # 隐藏st_ADDRESS列
    tableView.setSelectionMode(QTableView.SingleSelection)
    tableView.setSelectionBehavior(QTableView.SelectRows)


def table_init(tableView):
    '''
    初始化表头宽度，查询后要重新添加
    '''
    tableView.setColumnWidth(st_ID, 70)  # 设置 表头“st_ID”宽度
    tableView.setColumnWidth(st_NAME, 100)  # 设置 表头“st_NAME”宽度
    tableView.setColumnWidth(st_TIME, 180)  # 设置 表头“st_TIME”宽度
    tableView.setColumnWidth(st_IOSTATE, 100)  # 设置 表头“st_IOSTATE”宽度
    tableView.setColumnWidth(st_ADDRESS, 250)  # 设置 表头“st_ADDRESS”宽度
    tableView.setColumnHidden(st_ADDRESS, True)  # 隐藏st_ADDRESS列

    tableView.setSelectionMode(QTableView.SingleSelection)
    tableView.setSelectionBehavior(QTableView.SelectRows)
    tableView.scrollToBottom()


def deleteRecord(model, tableView, tableWidget):
    '''
    删除指定行
    '''
    while model.canFetchMore():
        model.fetchMore()
    index = tableView.currentIndex()
    if not index.isValid():
        return
    record = model.record(index.row())
    id = record.value(st_ID)
    name = record.value(st_NAME)
    result = id + '_' + name
    model.removeRow(index.row())
    model.select()
    add_table_item_Information(tableWidget, "删除指定行", result)


def deleteAllrows(model, tableView, tableWidget):
    '''
    删除指定行
    '''
    while model.canFetchMore():
        model.fetchMore()
    row = model.rowCount()
    for i in range(row):
        model.removeRow(i)
    model.select()
    add_table_item_Information(tableWidget, "删除所有行", 'allrows')


def addRecord(model, tableView, tableWidget):
    '''
    添加行，再次点击完成添加
    '''
    while model.canFetchMore():
        model.fetchMore()
    row = model.rowCount()
    model.insertRow(row)
    index = model.index(row, st_ID)
    tableView.setCurrentIndex(index)
    tableView.edit(index)

    global addclicked
    if addclicked == 0:
        addclicked = addclicked + 1
    else:
        addclicked = 0
        add_table_item_Information(tableWidget, '添加行', '--')


def addpreRecord(model, tableView, tableWidget, longname, add_io_num):
    '''
            添加行，再次点击完成添加
            model.setdata(index,值)
            st_ID, st_NAME, st_TIME, st_IOSTATE, st_ADDRESS
            '''

    '''
    获取时间
    '''
    date = datetime.datetime.today()
    strDate = date.strftime("%Y-%m-%d %H:%M:%S")
    add_id = longname.split('_')[0]
    add_name = longname.split('_')[-1]
    add_path = 'face_db/' + longname + '.jpg'
    if add_io_num:
        add_io = '出校'
    else:
        add_io = '入校'
    print('part1 over')
    model.setFilter("st_IOSTATE ='%s'" % add_io)  # io过滤
    model.setFilter("st_ID ='%s'" % add_id)  # id过滤
    model.setFilter("st_NAME ='%s'" % add_name)  # name过滤
    model.select()
    print('part2 over')
    while model.canFetchMore():
        model.fetchMore()
    print('row got')
    recordRow = model.rowCount()
    if recordRow == 0:
        while model.canFetchMore():
            model.fetchMore()
        row = model.rowCount()
        model.insertRow(row)
        model.setData(model.index(row, st_ID), add_id)
        model.setData(model.index(row, st_NAME), add_name)
        model.setData(model.index(row, st_TIME), strDate)
        model.setData(model.index(row, st_IOSTATE), add_io)
        model.setData(model.index(row, st_ADDRESS), add_path)
        index = model.index(row, st_ID)
        tableView.setCurrentIndex(index)
        tableView.edit(index)
        modltable_init(model, tableView)
        add_table_item_Information(tableWidget, '添加行', '--')
        return
    time = model.record(model.rowCount() - 1).value(st_TIME)  # 取最后一个时间
    print(time)
    time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    diff = date - time  # 同为datetime类型才能相减比较
    print(diff)
    if diff.seconds >= 60:
        while model.canFetchMore():
            model.fetchMore()
        row = model.rowCount()
        model.insertRow(row)
        model.setData(model.index(row, st_ID), add_id)
        model.setData(model.index(row, st_NAME), add_name)
        model.setData(model.index(row, st_TIME), strDate)
        model.setData(model.index(row, st_IOSTATE), add_io)
        model.setData(model.index(row, st_ADDRESS), add_path)
        index = model.index(row, st_ID)
        tableView.setCurrentIndex(index)
        tableView.edit(index)
        modltable_init(model, tableView)
        add_table_item_Information(tableWidget, '添加行', '--')

    else:
        modltable_init(model, tableView)
        return


def id_searchRecord(model, tableView, tableWidget, id_lineEdit):
    '''
    按id查询
    '''
    while model.canFetchMore():
        model.fetchMore()
    id_text = id_lineEdit.text()
    model.setFilter("st_ID ='%s'" % id_text)  # 过滤
    tableView.setModel(model)
    model.select()
    table_init(tableView)
    add_table_item_Information(tableWidget, '按id查询', id_text)
    id_lineEdit.setText('')


def name_searchRecord(model, tableView, tableWidget, name_lineEdit):
    '''
    按name查询
    '''
    while model.canFetchMore():
        model.fetchMore()
    name_text = name_lineEdit.text()
    print(name_text)
    model.setFilter("st_NAME ='%s'" % name_text)  # 过滤
    tableView.setModel(model)
    model.select()
    table_init(tableView)
    name_lineEdit.setText('')
    add_table_item_Information(tableWidget, '按name查询', name_text)


def origindata(model, tableView, tableWidget):
    '''
    读取表ImgT
    '''
    while model.canFetchMore():
        model.fetchMore()
    model.setTable('STIO')
    modltable_init(model, tableView)
    add_table_item_Information(tableWidget, '返回全表', 'STIO')


def tableview_clicked(model, tableView, tableWidget, label):
    '''
    表格单击事件
    '''
    while model.canFetchMore():
        model.fetchMore()
    label.clear()
    index = tableView.currentIndex()
    if not index.isValid():
        return
    record = model.record(index.row())
    id = record.value(st_ID)
    name = record.value(st_NAME)
    address = record.value(st_ADDRESS)
    print(address)
    try:
        # 显示到table
        add_table_item_Information(tableWidget, '显示图片', address)
        # 显示在 Imglabel上
        img_path = cv2.imdecode(np.fromfile(address, dtype=np.uint8), -1)  # 路径含有中文 需要用imdecode

        img = cv2.cvtColor(img_path, cv2.COLOR_BGR2RGB)
        img = img_resize(img)
        showimg = QtGui.QImage(img.data, img.shape[1], img.shape[0],img.shape[1]*3, QtGui.QImage.Format_RGB888)
        label.setPixmap(QtGui.QPixmap.fromImage(showimg))
    except:
        print('error')

# == == == == == == == == == == == == == == =SQL == == == == = Information == == == == == == == == == == == == == == == == == == == == == =
