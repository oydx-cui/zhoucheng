import ctypes
import re
from datetime import datetime

import matplotlib
import mplcyberpunk
from matplotlib.patches import Rectangle
from scipy.interpolate import make_interp_spline

import link_mysql
from lstm_model import rul

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
import image_label
import groupbox_show
from PIL import Image, ImageDraw
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDateTime, QTimer, Qt, QDir, QSize, QRect
from PyQt5.QtWidgets import QFileSystemModel, QPushButton, QVBoxLayout, \
    QMessageBox, QDesktopWidget, QTableWidgetItem, QTableWidget
from anomaly_detection import Detection
from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')

myFont = QtGui.QFont()
myFont2 = QtGui.QFont()
myFont3 = QtGui.QFont()
myFont4 = QtGui.QFont()
myFont.setFamily("SimHei")
myFont.setPointSize(13)
myFont2.setFamily("SimHei")
myFont2.setPointSize(11)
myFont3.setFamily("SimHei")
myFont3.setPointSize(12)
myFont4.setFamily("SimHei")
myFont4.setPointSize(8)
machine_pattern = re.compile(r'machine-(\d+)')
bearing_pattern = re.compile(r'bearing-(\d+)')


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1731, 923)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet(
            "QFrame#frame{background-color: qlineargradient(x0:0, y0:1, x1:1, y1:1,stop:0.4  rgb(1,102,230), stop:1 rgb(79,171,254));\n"
            "border:0px solid red;\n"
            "border-radius:30px\n"
            "}")
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(1171, 748))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_1 = QtWidgets.QFrame(self.frame)
        self.frame_1.setMinimumSize(QtCore.QSize(69, 736))
        self.frame_1.setStyleSheet("QFrame{\n"
                                   "    background-color: rgba(255, 255, 255,0);\n"
                                   "border:0px solid red;\n"
                                   "border-radius:30px\n"
                                   "}")
        self.frame_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_1.setObjectName("frame_1")
        self.listWidget = QtWidgets.QListWidget(self.frame_1)
        self.listWidget.setGeometry(QtCore.QRect(0, 80, 101, 241))
        self.listWidget.setSizeIncrement(QtCore.QSize(0, 0))
        self.listWidget.setStyleSheet("QListView {\n"
                                      "outline: -1px;\n"
                                      "}\n"
                                      "QListView::item{\n"
                                      "background-color: transparent;\n"
                                      "color: rgba(255, 255, 255, 199);\n"
                                      "padding:12px;\n"
                                      "padding-left:18px;\n"
                                      "outline: -1px;\n"
                                      "}\n"
                                      "QListView::item:hover {\n"
                                      "background-color: rgba(3,135,254, 59);\n"
                                      "outline: -1px;\n"
                                      "}\n"
                                      "QListView::item:selected {\n"
                                      "color: rgb(255, 255, 255);\n"
                                      "border-left:5px solid rgb(1,102,230);\n"
                                      "outline: -1px;\n"
                                      "}")
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        item.setIcon(QtGui.QIcon('./configuration-pic/detect_icon.png'))
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setIcon(QtGui.QIcon('./configuration-pic/rul_icon.png'))
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setIcon(QtGui.QIcon('./configuration-pic/history_icon.png'))
        self.listWidget.addItem(item)
        self.listWidget.setIconSize(QtCore.QSize(32, 32))
        self.horizontalLayout_3.addWidget(self.frame_1)
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setFixedSize(1613, 879)
        self.frame_2.setStyleSheet("QFrame{\n"
                                   "    background-color: rgb(245, 249, 254);\n"
                                   "border:0px solid red;\n"
                                   "border-radius:30px\n"
                                   "}")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.stackedWidget = QtWidgets.QStackedWidget(self.frame_2)
        self.stackedWidget.setGeometry(QtCore.QRect(10, -5, 1580, 871))  #
        self.stackedWidget.setObjectName("stackedWidget")
        self.timer = QTimer()
        self.timer.timeout.connect(self.showtime)  # 刷新时间
        self.timer.start(1000)

        # --------------------------------------------------------------------------------------------------------------------
        self.page_0 = QtWidgets.QWidget()  # 故障检测界面
        self.page_0.setObjectName("page_0")
        self.stackedWidget.addWidget(self.page_0)
        self.label_2 = QtWidgets.QLabel(self.page_0)
        self.label_2.setGeometry(QtCore.QRect(796, 345, 261, 41))
        self.label_2.setObjectName("label_2")
        self.label_2.setFont(myFont)
        self.label_time = QtWidgets.QLabel(self.page_0)
        self.label_time.setGeometry(QtCore.QRect(1236, 345, 291, 41))
        self.label_time.setObjectName("label_time")
        self.label_time.setFont(myFont)
        self.groupBox_wave = QtWidgets.QGroupBox(self.page_0)
        self.groupBox_wave.setGeometry(QtCore.QRect(300, 416, 1250, 415))
        self.groupBox_wave.setObjectName("groupBox_3")
        self.groupBox_wave.setFont(myFont2)
        self.wave_widget = WaveForm()
        layout = QVBoxLayout()
        layout.addWidget(self.wave_widget)
        self.groupBox_wave.setLayout(layout)
        self.wave_widget.setGeometry(70, 100, 1171, 391)
        self.wave_widget.setVisible(False)
        self.groupBox = QtWidgets.QGroupBox(self.page_0)
        self.groupBox.setGeometry(QtCore.QRect(696, 80, 871, 221))
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setFont(myFont2)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(10, 40, 72, 21))
        self.label_6.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.label_6.setFont(myFont)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(10, 100, 72, 21))
        self.label_7.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.label_7.setFont(myFont)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 160, 72, 21))
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.label.setFont(myFont)
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(100, 40, 102, 21))
        self.label_8.setObjectName("label_8")
        self.label_8.setFont(myFont)
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setGeometry(QtCore.QRect(100, 100, 102, 21))
        self.label_9.setObjectName("label_9")
        self.label_9.setFont(myFont)
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setGeometry(QtCore.QRect(100, 160, 102, 21))
        self.label_10.setObjectName("label_10")
        self.label_10.setFont(myFont)
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.groupBox)
        self.textBrowser_2.setGeometry(QtCore.QRect(210, 30, 200, 41))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.groupBox)
        self.textBrowser_3.setGeometry(QtCore.QRect(210, 90, 200, 41))
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.textBrowser_4 = QtWidgets.QTextBrowser(self.groupBox)
        self.textBrowser_4.setGeometry(QtCore.QRect(210, 150, 200, 41))
        self.textBrowser_4.setObjectName("textBrowser_4")
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        self.label_12.setGeometry(QtCore.QRect(430, 100, 101, 21))
        self.label_12.setObjectName("label_12")
        self.label_12.setFont(myFont)
        self.label_13 = QtWidgets.QLabel(self.groupBox)
        self.label_13.setGeometry(QtCore.QRect(430, 40, 101, 21))
        self.label_13.setObjectName("label_13")
        self.label_13.setFont(myFont)
        self.label_17 = QtWidgets.QLabel(self.groupBox)
        self.label_17.setGeometry(QtCore.QRect(430, 160, 101, 21))
        self.label_17.setObjectName("label_17")
        self.label_17.setFont(myFont)
        self.textBrowser_5 = QtWidgets.QTextBrowser(self.groupBox)
        self.textBrowser_5.setGeometry(QtCore.QRect(543, 30, 111, 41))
        self.textBrowser_5.setObjectName("textBrowser_5")
        self.textBrowser_6 = QtWidgets.QTextBrowser(self.groupBox)
        self.textBrowser_6.setGeometry(QtCore.QRect(543, 90, 111, 41))
        self.textBrowser_6.setObjectName("textBrowser_6")
        self.textBrowser_7 = QtWidgets.QTextBrowser(self.groupBox)
        self.textBrowser_7.setGeometry(QtCore.QRect(543, 150, 111, 41))
        self.textBrowser_7.setObjectName("textBrowser_7")
        self.label_14 = QtWidgets.QLabel(self.groupBox)
        self.label_14.setGeometry(QtCore.QRect(670, 40, 51, 21))
        self.label_14.setObjectName("label_14")
        self.label_14.setFont(myFont)
        self.label_15 = QtWidgets.QLabel(self.groupBox)
        self.label_15.setGeometry(QtCore.QRect(670, 100, 51, 21))
        self.label_15.setObjectName("label_15")
        self.label_15.setFont(myFont)
        self.label_16 = QtWidgets.QLabel(self.groupBox)
        self.label_16.setGeometry(QtCore.QRect(670, 160, 51, 21))
        self.label_16.setObjectName("label_16")
        self.label_16.setFont(myFont)
        self.textBrowser_8 = QtWidgets.QTextBrowser(self.groupBox)
        self.textBrowser_8.setGeometry(QtCore.QRect(740, 30, 101, 41))
        self.textBrowser_8.setObjectName("textBrowser_8")
        self.textBrowser_9 = QtWidgets.QTextBrowser(self.groupBox)
        self.textBrowser_9.setGeometry(QtCore.QRect(740, 90, 101, 41))
        self.textBrowser_9.setObjectName("textBrowser_9")
        self.textBrowser_10 = QtWidgets.QTextBrowser(self.groupBox)
        self.textBrowser_10.setGeometry(QtCore.QRect(740, 150, 101, 41))
        self.textBrowser_10.setObjectName("textBrowser_10")
        self.textBrowser_2.setFontPointSize(14)
        self.textBrowser_3.setFontPointSize(14)
        self.textBrowser_4.setFontPointSize(14)
        self.textBrowser_5.setFontPointSize(16)
        self.textBrowser_6.setFontPointSize(16)
        self.textBrowser_7.setFontPointSize(16)
        self.textBrowser_8.setFontPointSize(16)
        self.textBrowser_9.setFontPointSize(16)
        self.textBrowser_10.setFontPointSize(16)
        self.groupBox_2 = QtWidgets.QGroupBox(self.page_0)
        self.groupBox_2.setGeometry(QtCore.QRect(300, 80, 366, 306))
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_2.setFont(myFont2)

        self.scrollArea = QtWidgets.QScrollArea(self.page_0)
        self.scrollArea.setGeometry(QtCore.QRect(10, 60, 251, 805))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 231, 845))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        filedir1 = "test_example/"  # m1 到 m5
        machines = os.listdir(filedir1)
        for i in range(0, len(machines)):
            bearingdir1 = filedir1 + machines[i] + "/"
            bearings = os.listdir(bearingdir1)
            for j in range(0, len(bearings)):
                bearingdir2 = bearingdir1 + bearings[j] + "/"
                widget = QWidget()
                widget.setMinimumSize(QSize(228, 50))
                widget.setStyleSheet("background-color: rgb(255, 255, 255); border-radius: 12px;")
                button = QPushButton(widget)
                button.setGeometry(QRect(0, 0, 228, 50))
                machine_match = machine_pattern.search(bearingdir2)
                bearing_match = bearing_pattern.search(bearingdir2)
                machine_number = machine_match.group(1)
                bearing_number = bearing_match.group(1)
                button.setText("machine-" + str(machine_number) + " " + "bearing-" + str(bearing_number))
                button.setFont(myFont2)

                def create_lambda00(): return lambda: self.wave_widget.setVisible(True)

                def create_lambda(path): return lambda: self.generate_1(path)

                def create_lambda2(path): return lambda: self.wave_widget.plotfig(path)

                if str(machine_number) == '1' and str(bearing_number) == '01':
                    button.clicked.connect(create_lambda00())
                    button.clicked.connect(self.on_button_clicked)
                else:
                    button.clicked.connect(create_lambda2(bearingdir2 + (os.listdir(bearingdir2)[0])))
                    button.clicked.connect(create_lambda(bearingdir2 + (os.listdir(bearingdir2)[0])))

                button.setStyleSheet("""  
                               QPushButton:hover {  
                                   background-color: rgb(0, 206, 209);}  
                               QPushButton:pressed {  
                                   background-color: rgb(200, 200, 200);}  
                       """)
                self.verticalLayout.addWidget(widget)
        # --------------------------------------------------------------------------------------------------------------------------
        self.page_1 = QtWidgets.QWidget()  # RUL预测界面
        self.page_1.setObjectName("page_1")
        self.stackedWidget.addWidget(self.page_1)
        self.label_2_rul = QtWidgets.QLabel(self.page_1)
        self.label_2_rul.setGeometry(QtCore.QRect(300, 290, 261, 41))
        self.label_2_rul.setObjectName("label_2_rul")
        self.label_2_rul.setFont(myFont)
        self.label_time_rul = QtWidgets.QLabel(self.page_1)
        self.label_time_rul.setGeometry(QtCore.QRect(300, 360, 291, 41))
        self.label_time_rul.setObjectName("label_time_rul")
        self.label_time_rul.setFont(myFont)
        self.groupBox_wave_rul = QtWidgets.QGroupBox(self.page_1)
        self.groupBox_wave_rul.setGeometry(QtCore.QRect(300, 436, 1250, 415))
        self.groupBox_wave_rul.setObjectName("groupBox_3")
        self.groupBox_wave_rul.setFont(myFont2)
        self.wave_widget_rul = WaveForm()
        layout2 = QVBoxLayout()
        layout2.addWidget(self.wave_widget_rul)
        self.groupBox_wave_rul.setLayout(layout2)
        self.wave_widget_rul.setGeometry(70, 100, 1171, 391)
        self.wave_widget_rul.setVisible(False)
        self.groupBox_rul = QtWidgets.QGroupBox(self.page_1)
        self.groupBox_rul.setGeometry(QtCore.QRect(300, 65, 541, 195))
        self.groupBox_rul.setObjectName("groupBox_rul")
        self.groupBox_rul.setFont(myFont2)
        self.label_r1 = QtWidgets.QLabel(self.groupBox_rul)
        self.label_r1.setGeometry(QtCore.QRect(5, 50, 150, 21))
        self.label_r1.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_r1.setObjectName("label_r1")
        self.label_r1.setFont(myFont)
        self.label_r2 = QtWidgets.QLabel(self.groupBox_rul)
        self.label_r2.setGeometry(QtCore.QRect(5, 125, 260, 21))
        self.label_r2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_r2.setObjectName("label_r2")
        self.label_r2.setFont(myFont)
        self.textBrowser_r1 = QtWidgets.QTextBrowser(self.groupBox_rul)
        self.textBrowser_r1.setGeometry(QtCore.QRect(170, 45, 280, 41))
        self.textBrowser_r1.setObjectName("textBrowser_r1")
        self.textBrowser_r2 = QtWidgets.QTextBrowser(self.groupBox_rul)
        self.textBrowser_r2.setGeometry(QtCore.QRect(250, 115, 200, 41))
        self.textBrowser_r2.setObjectName("textBrowser_r2")
        self.textBrowser_r1.setFontPointSize(14)
        self.textBrowser_r2.setFontPointSize(14)

        self.groupBox_history_rul = QtWidgets.QGroupBox(self.page_1)  # 检测结果曲线图
        self.groupBox_history_rul.setGeometry(QtCore.QRect(880, 65, 670, 361))
        self.groupBox_history_rul.setObjectName("groupBox_history_rul")
        self.groupBox_history_rul.setFont(myFont2)
        self.wave_widget_2_rul = WaveForm()
        layout2_ = QVBoxLayout()
        layout2_.addWidget(self.wave_widget_2_rul)
        self.groupBox_history_rul.setLayout(layout2_)
        self.wave_widget_2_rul.setVisible(False)

        self.scrollArea2 = QtWidgets.QScrollArea(self.page_1)
        self.scrollArea2.setGeometry(QtCore.QRect(10, 60, 251, 805))
        self.scrollArea2.setWidgetResizable(True)
        self.scrollArea2.setObjectName("scrollArea")
        self.scrollArea2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollAreaWidgetContents2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents2.setGeometry(QtCore.QRect(0, 0, 231, 845))
        self.scrollAreaWidgetContents2.setObjectName("scrollAreaWidgetContents2")
        self.scrollArea2.setWidget(self.scrollAreaWidgetContents2)
        self.verticalLayout2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents2)
        self.verticalLayout2.setObjectName("verticalLayout2")
        filedir_rul = "life_vib_example/"  # m1 到 m5
        machines_rul = os.listdir(filedir_rul)
        for i in range(0, len(machines_rul)):
            bearingdir_rul = filedir_rul + machines_rul[i] + "/"
            bearings_rul = os.listdir(bearingdir_rul)
            for j in range(0, len(bearings_rul)):
                bearingdir2_rul = bearingdir_rul + bearings_rul[j] + "/"
                widget = QWidget()
                widget.setMinimumSize(QSize(228, 50))
                widget.setStyleSheet("background-color: rgb(255, 255, 255); border-radius: 12px;")
                button = QPushButton(widget)
                button.setGeometry(QRect(0, 0, 228, 50))
                machine_match = machine_pattern.search(bearingdir2_rul)
                bearing_match = bearing_pattern.search(bearingdir2_rul)
                machine_number2 = machine_match.group(1)
                bearing_number2 = bearing_match.group(1)
                button.setText("machine-" + str(machine_number2) + " " + "bearing-" + str(bearing_number2))
                button.setFont(myFont2)

                def create_lambda_rul(path):
                    return lambda: (self.generate_rul(path))

                def create_lambda_rul2(path):
                    return lambda: (self.generate_rul_2(path))

                def create_lambda00():
                    return lambda: self.wave_widget_rul.setVisible(True)

                if str(machine_number2) == '1' and str(bearing_number2) == '01':
                    button.clicked.connect(create_lambda00())
                    button.clicked.connect(self.on_button_clicked_rul)
                else:
                    button.clicked.connect(create_lambda_rul(bearingdir2_rul + (os.listdir(bearingdir2_rul)[0])))
                    button.clicked.connect(create_lambda_rul2(bearingdir2_rul + (os.listdir(bearingdir2_rul)[0])))
                button.setStyleSheet("""  
                                       QPushButton:hover {  
                                           background-color: rgb(0, 206, 209);}  
                                       QPushButton:pressed {  
                                           background-color: rgb(200, 200, 200);}  
                               """)
                self.verticalLayout2.addWidget(widget)
        # -------------------------------------------------------------------------------------------------------------------------
        self.page_2 = QtWidgets.QWidget()  # 历史记录界面
        self.page_2.setObjectName("page_2")
        self.stackedWidget.addWidget(self.page_2)
        self.scrollArea3 = QtWidgets.QScrollArea(self.page_2)
        self.scrollArea3.setGeometry(QtCore.QRect(10, 60, 251, 805))
        self.scrollArea3.setWidgetResizable(True)
        self.scrollArea3.setObjectName("scrollArea_3")
        self.scrollArea3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollAreaWidgetContents3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents3.setGeometry(QtCore.QRect(0, 0, 231, 845))
        self.scrollAreaWidgetContents3.setObjectName("scrollAreaWidgetContents3")
        self.scrollArea3.setWidget(self.scrollAreaWidgetContents3)
        self.verticalLayout3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents3)
        self.verticalLayout3.setObjectName("verticalLayout3")
        filedir_rul_his = "life_vib_example/"  # m1 到 m5
        machines_rul_h = os.listdir(filedir_rul_his)
        for i in range(0, len(machines_rul_h)):
            bearingdir_rul_h = filedir_rul_his + machines_rul_h[i] + "/"
            bearings_rul_h = os.listdir(bearingdir_rul_h)
            for j in range(0, len(bearings_rul_h)):
                bearingdir2_rul_h = bearingdir_rul_h + bearings_rul_h[j] + "/"
                widget = QWidget()
                widget.setMinimumSize(QSize(228, 50))
                widget.setStyleSheet("background-color: rgb(255, 255, 255); border-radius: 12px;")
                button = QPushButton(widget)
                button.setGeometry(QRect(0, 0, 228, 50))
                machine_match = machine_pattern.search(bearingdir2_rul_h)
                bearing_match = bearing_pattern.search(bearingdir2_rul_h)
                machine_number2 = machine_match.group(1)
                bearing_number2 = bearing_match.group(1)
                button.setText("machine-" + str(machine_number2) + " " + "bearing-" + str(bearing_number2))
                button.setFont(myFont2)

                def create_lambda_his(path):
                    return lambda: (self.generate_his(path))

                button.clicked.connect(create_lambda_his(bearingdir2_rul_h + (os.listdir(bearingdir2_rul_h)[0])))
                button.setStyleSheet("""  
                                                      QPushButton:hover {  
                                                          background-color: rgb(0, 206, 209);}  
                                                      QPushButton:pressed {  
                                                          background-color: rgb(200, 200, 200);}  
                                              """)
                self.verticalLayout3.addWidget(widget)

        self.groupBox_history = QtWidgets.QGroupBox(self.page_2)  # 检测结果曲线图
        self.groupBox_history.setGeometry(QtCore.QRect(770, 475, 780, 381))
        self.groupBox_history.setObjectName("groupBox_history")
        self.groupBox_history.setFont(myFont2)
        self.wave_widget_2 = WaveForm()
        layout2 = QVBoxLayout()
        layout2.addWidget(self.wave_widget_2)
        self.groupBox_history.setLayout(layout2)
        self.wave_widget_2.setVisible(False)
        self.groupBox_h_pic = QtWidgets.QGroupBox(self.page_2)  # 历史记录界面轴承故障标注
        self.groupBox_h_pic.setGeometry(QtCore.QRect(1140, 80, 410, 381))
        self.groupBox_h_pic.setObjectName("groupBox_3")
        self.groupBox_h_pic.setFont(myFont2)

        self.scroll_table = QtWidgets.QGroupBox(self.page_2)  # 故障检测历史
        self.scroll_table.setGeometry(QtCore.QRect(285, 80, 820, 360))
        self.scroll_table.setObjectName("groupBox_4")
        self.scroll_table.setFont(myFont4)
        self.scroll_widget = AutoScroll()
        layout3 = QVBoxLayout()
        layout3.addWidget(self.scroll_widget)
        self.scroll_table.setLayout(layout3)
        self.scroll_widget.setVisible(True)

        self.scroll_table2 = QtWidgets.QGroupBox(self.page_2)  # 寿命预测历史
        self.scroll_table2.setGeometry(QtCore.QRect(285, 475, 450, 381))
        self.scroll_table2.setObjectName("groupBox_4")
        self.scroll_table2.setFont(myFont4)
        self.scroll_widget2 = AutoScroll_rul()
        layout4 = QVBoxLayout()
        layout4.addWidget(self.scroll_widget2)
        self.scroll_table2.setLayout(layout4)
        self.scroll_widget2.setVisible(True)
        # -------------------------------------------------------------------------------------------------------------------------
        self.widget_title = QtWidgets.QWidget(self.stackedWidget)
        self.widget_title.setGeometry(QtCore.QRect(30, 20, 200, 30))
        self.widget_title.setMinimumSize(QtCore.QSize(200, 30))
        self.widget_title.setMaximumSize(QtCore.QSize(200, 30))
        self.widget_title.setObjectName("widget_title")
        self.label_title = QtWidgets.QLabel(self.widget_title)
        self.label_title.setGeometry(QtCore.QRect(0, 0, 200, 30))
        self.label_title.setObjectName("label_title")
        self.horizontalLayout_3.addWidget(self.frame_2)
        self.horizontalLayout_2.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.close_button = QPushButton('', self.frame)
        self.close_button.clicked.connect(self.close)
        self.close_button.setGeometry(30, 828, 30, 30)
        self.close_button.setStyleSheet('''  
                QPushButton {  
                    border: none;
                    background-color: transparent;
                    border-image:url(./configuration-pic/close.png);
                }  
                 QPushButton:pressed {  
                    background-color: rgb(200, 200, 200);}
                ''')
        self.minimize_button = QPushButton('', self)
        self.minimize_button.clicked.connect(self.showMinimized)
        self.minimize_button.setGeometry(40, 780, 30, 30)
        self.minimize_button.setStyleSheet('''  
                        QPushButton {  
                            border: none;
                            background-color: transparent;
                            border-image:url(./configuration-pic/minimize.png);
                        }  
                         QPushButton:pressed {  
                            background-color: rgb(200, 200, 200);}
                        ''')

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(1)
        self.listWidget.currentRowChanged['int'].connect(self.stackedWidget.setCurrentIndex)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.label_title.setText("轴  承  选  择")
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setText(_translate("MainWindow", "轴承信息：--------"))
        self.label_time.setText(_translate("MainWindow", "当前时间"))
        self.label_2_rul.setText(_translate("MainWindow", "轴承信息：--------"))
        self.label_time_rul.setText(_translate("MainWindow", "当前时间"))
        self.groupBox.setTitle(_translate("MainWindow", "故障检测信息"))
        self.groupBox.setStyleSheet("""
                                         QGroupBox {
                                             border: 2px solid grey; 
                                             border-radius: 5px;    
                                             margin-top: 1ex;
                                             background-image: url(./configuration-pic/bg_wave.jpg);}""")
        self.groupBox_rul.setTitle(_translate("MainWindow", "轴承健康信息"))
        self.groupBox_rul.setStyleSheet("""
                                                 QGroupBox {
                                                     border: 2px solid grey; 
                                                     border-radius: 5px;    
                                                     margin-top: 1ex;
                                                     background-image: url(./configuration-pic/bg_wave.jpg);}""")
        self.groupBox_wave.setTitle(_translate("MainWindow", "传感器时域信号"))
        self.groupBox_wave.setStyleSheet("""
                                            QGroupBox {
                                                border: 2px solid grey;
                                                border-radius: 5px;
                                                margin-top: 1ex;
                                                background-image: url(./configuration-pic/bg_wave.jpg);}""")
        self.groupBox_wave_rul.setTitle(_translate("MainWindow", "RUL传感器时域信号"))
        self.groupBox_wave_rul.setStyleSheet("""
                                                    QGroupBox {
                                                        border: 2px solid grey;
                                                        border-radius: 5px;
                                                        margin-top: 1ex;
                                                        background-image: url(./configuration-pic/bg_wave.jpg);}""")
        self.groupBox_2.setTitle("故障位置及大小示意图")
        self.groupBox_2.setStyleSheet("""
                                  QGroupBox {
                                      border: 2px solid grey; 
                                      border-radius: 5px;    
                                      margin-top: 1ex;       
                                      background-image: url(./configuration-pic/groupbox2_bg.jpg);}""")

        self.label_6.setText(_translate("MainWindow", "结果一"))
        self.label_7.setText(_translate("MainWindow", "结果二"))
        self.label_r1.setText(_translate("MainWindow", "健康状态："))
        self.label_r2.setText(_translate("MainWindow", "预期剩余寿命（天）："))
        self.label.setText(_translate("MainWindow", "结果三"))
        self.label_8.setText(_translate("MainWindow", "故障位置："))
        self.label_9.setText(_translate("MainWindow", "故障位置："))
        self.label_10.setText(_translate("MainWindow", "故障位置："))
        self.label_6.setStyleSheet("background-image: url(./configuration-pic/bg_wave_1.jpg);")
        self.label_7.setStyleSheet("background-image: url(./configuration-pic/bg_wave_1.jpg);")
        self.label_r1.setStyleSheet("background-image: url(./configuration-pic/bg_wave_1.jpg);")
        self.label_r2.setStyleSheet("background-image: url(./configuration-pic/bg_wave_1.jpg);")
        self.label.setStyleSheet("background-image: url(./configuration-pic/bg_wave_1.jpg);")
        self.label_8.setStyleSheet("background-image: url(./configuration-pic/bg_wave_1.jpg);")
        self.label_9.setStyleSheet("background-image: url(./configuration-pic/bg_wave_1.jpg);")
        self.label_10.setStyleSheet("background-image: url(./configuration-pic/bg_wave_1.jpg);")
        self.label_12.setText(_translate("MainWindow", "故障大小："))
        self.label_13.setText(_translate("MainWindow", "故障大小："))
        self.label_17.setText(_translate("MainWindow", "故障大小："))
        self.label_12.setStyleSheet("background-image: url(./configuration-pic/bg_wave_2.jpg);")
        self.label_13.setStyleSheet("background-image: url(./configuration-pic/bg_wave_2.jpg);")
        self.label_17.setStyleSheet("background-image: url(./configuration-pic/bg_wave_2.jpg);")
        self.label_14.setText(_translate("MainWindow", "得分："))
        self.label_15.setText(_translate("MainWindow", "得分："))
        self.label_16.setText(_translate("MainWindow", "得分："))
        self.label_14.setStyleSheet("background-image: url(./configuration-pic/bg_wave_3.jpg);")
        self.label_15.setStyleSheet("background-image: url(./configuration-pic/bg_wave_3.jpg);")
        self.label_16.setStyleSheet("background-image: url(./configuration-pic/bg_wave_3.jpg);")
        self.groupBox_history.setTitle(_translate("MainWindow", "历史检测记录"))
        self.groupBox_history.setStyleSheet("""
                                                        QGroupBox {
                                                            border: 2px solid grey;
                                                            border-radius: 5px;
                                                            margin-top: 1ex;}""")
        self.groupBox_history_rul.setTitle(_translate("MainWindow", "寿命预测结果历史记录"))
        self.groupBox_history_rul.setStyleSheet("""
                                                                QGroupBox {
                                                                    border: 2px solid grey;
                                                                    border-radius: 5px;
                                                                    margin-top: 1ex;}""")
        self.groupBox_h_pic.setTitle("最近检测结果示意图")
        self.groupBox_h_pic.setStyleSheet("""
                                                 QGroupBox {
                                                     border: 2px solid grey;
                                                     border-radius: 5px;
                                                     margin-top: 1ex;}""")
        self.scroll_table.setTitle("故障检测历史数据")
        self.scroll_table.setStyleSheet("""
                                              QGroupBox {
                                                  border: 2px solid grey;
                                                  border-radius: 5px;
                                                  margin-top: 1ex;}""")
        self.scroll_table2.setTitle("寿命预测历史数据")
        self.scroll_table2.setStyleSheet("""
                                                     QGroupBox {
                                                         border: 2px solid grey;
                                                         border-radius: 5px;
                                                         margin-top: 1ex;}""")
        self.widget_title.setStyleSheet("background-color: rgb(79,171,254);\n"
                                        "border-radius:12px")
        self.label_title.setStyleSheet("font: 75 10pt \"微软雅黑\";\n"
                                       "color:rgb(255, 255, 255);")

    def generate_1(self, dir_):  # 实时监测界面 生成波形图、故障位置信息以及示意图
        if dir_ != '':
            file_name = dir_
            file_name = repr(file_name)[1:-1]
            output_num = 3
            det = Detection()
            res = det.detect(file_name=file_name, output_num=output_num)
            if res != (None, None):
                print(res)
                img_path = './configuration-pic/label-pic.jpg'
                img = Image.open(img_path)
                a = ImageDraw.ImageDraw(img)
                self.textBrowser_2.clear()
                self.textBrowser_3.clear()
                self.textBrowser_4.clear()
                self.textBrowser_5.clear()
                self.textBrowser_6.clear()
                self.textBrowser_7.clear()
                self.textBrowser_8.clear()
                self.textBrowser_9.clear()
                self.textBrowser_10.clear()
                self.textBrowser_2.setTextColor(groupbox_show.show_color(res[0][0][1]))
                self.textBrowser_5.setTextColor(groupbox_show.show_color(res[0][0][1]))
                self.textBrowser_8.setTextColor(groupbox_show.show_color(res[0][0][1]))
                self.textBrowser_3.setTextColor(groupbox_show.show_color(res[0][1][1]))
                self.textBrowser_6.setTextColor(groupbox_show.show_color(res[0][1][1]))
                self.textBrowser_9.setTextColor(groupbox_show.show_color(res[0][1][1]))
                self.textBrowser_4.setTextColor(groupbox_show.show_color(res[0][2][1]))
                self.textBrowser_7.setTextColor(groupbox_show.show_color(res[0][2][1]))
                self.textBrowser_10.setTextColor(groupbox_show.show_color(res[0][2][1]))
                self.textBrowser_5.setText(groupbox_show.show_size(res[0][0][0]))
                self.textBrowser_6.setText(groupbox_show.show_size(res[0][1][0]))
                self.textBrowser_7.setText(groupbox_show.show_size(res[0][2][0]))
                if self.textBrowser_5.toPlainText() != '':
                    self.textBrowser_2.setText(groupbox_show.translate_pos(res[0][0][1]))
                    self.textBrowser_8.setText(str(format(res[1][0], '.3f')))
                if self.textBrowser_6.toPlainText() != '':
                    self.textBrowser_3.setText(groupbox_show.translate_pos(res[0][1][1]))
                    self.textBrowser_9.setText(str(format(res[1][1], '.3f')))
                if self.textBrowser_7.toPlainText() != '':
                    self.textBrowser_4.setText(groupbox_show.translate_pos(res[0][2][1]))
                    self.textBrowser_10.setText(str(format(res[1][2], '.3f')))
                times = np.array([0, 0, 0, 0, 0])
                for i in range(0, 3):
                    if res[0][i][0] != 0:
                        image_label.labelling(a, res[0][i][1], res[0][i][0], str(format(res[1][i], '.2f')), times)
                img.save('temp.jpg')
                newstyle = """  
                QGroupBox {  
                    border-image: url(./temp.jpg);  
                } 
                """
                newstyle_ = self.groupBox_2.styleSheet() + newstyle
                self.groupBox_2.setStyleSheet(newstyle_)
                self.textBrowser_2.setAlignment(Qt.AlignCenter)
                self.textBrowser_3.setAlignment(Qt.AlignCenter)
                self.textBrowser_4.setAlignment(Qt.AlignCenter)
                self.textBrowser_5.setAlignment(Qt.AlignCenter)
                self.textBrowser_6.setAlignment(Qt.AlignCenter)
                self.textBrowser_7.setAlignment(Qt.AlignCenter)
                self.textBrowser_8.setAlignment(Qt.AlignCenter)
                self.textBrowser_9.setAlignment(Qt.AlignCenter)
                self.textBrowser_10.setAlignment(Qt.AlignCenter)
                machine_match = machine_pattern.search(file_name)
                bearing_match = bearing_pattern.search(file_name)
                machine_number = machine_match.group(1)
                bearing_number = bearing_match.group(1)
                m_number = int(machine_number)
                b_number = int(bearing_number)
                # link_mysql.to_mysql(res, m_number, b_number)
                self.label_2.setText("Machine-"+machine_number + "  "+"Bearing-" + bearing_number)
                self.wave_widget.setVisible(True)
            else:
                dir_ = ''
                reply = QMessageBox.warning(self.page_0, "Warning",
                                             f"输入格式错误 ！！", QMessageBox.Ok)
                if reply == QMessageBox.Ok:
                    return

    def showtime(self):  # 显示当前时间
        time = QDateTime.currentDateTime()
        timedisplay = time.toString("yyyy-MM-dd hh:mm:ss dddd")
        self.label_time.setText(timedisplay)
        self.label_time_rul.setText(timedisplay)

    def on_button_clicked(self):
        QTimer.singleShot(4000, self.delayed_function)

    def delayed_function(self):
        if os.path.isfile('./acceleration_data.csv'):
            df = pd.read_csv('acceleration_data.csv')
            sn = pd.Series(range(1, 101), name='sn')
            det_dir = './test_example/machine-1/bearing-01'
            column_det = {'X': 'de', 'Y': 'fe'}
            df_det_re = df.rename(columns=column_det)
            df_det = df_det_re.head(100)
            df_det.insert(0, 'sn', sn)
            xlsx_path = os.path.join(det_dir, 'signal_0.xlsx')
            df_det.to_excel(xlsx_path, index=False)
            file_name = "test_example/machine-1/bearing-01/signal_0.xlsx"
            file_name = repr(file_name)[1:-1]
            output_num = 3
            det = Detection()
            res = det.detect(file_name=file_name, output_num=output_num)
            if res != (None, None):
                print(res)
                img_path = './configuration-pic/label-pic.jpg'
                img = Image.open(img_path)
                a = ImageDraw.ImageDraw(img)
                self.textBrowser_2.clear()
                self.textBrowser_3.clear()
                self.textBrowser_4.clear()
                self.textBrowser_5.clear()
                self.textBrowser_6.clear()
                self.textBrowser_7.clear()
                self.textBrowser_8.clear()
                self.textBrowser_9.clear()
                self.textBrowser_10.clear()
                self.textBrowser_2.setTextColor(groupbox_show.show_color(res[0][0][1]))
                self.textBrowser_5.setTextColor(groupbox_show.show_color(res[0][0][1]))
                self.textBrowser_8.setTextColor(groupbox_show.show_color(res[0][0][1]))
                self.textBrowser_3.setTextColor(groupbox_show.show_color(res[0][1][1]))
                self.textBrowser_6.setTextColor(groupbox_show.show_color(res[0][1][1]))
                self.textBrowser_9.setTextColor(groupbox_show.show_color(res[0][1][1]))
                self.textBrowser_4.setTextColor(groupbox_show.show_color(res[0][2][1]))
                self.textBrowser_7.setTextColor(groupbox_show.show_color(res[0][2][1]))
                self.textBrowser_10.setTextColor(groupbox_show.show_color(res[0][2][1]))
                self.textBrowser_5.setText(groupbox_show.show_size(res[0][0][0]))
                self.textBrowser_6.setText(groupbox_show.show_size(res[0][1][0]))
                self.textBrowser_7.setText(groupbox_show.show_size(res[0][2][0]))
                if self.textBrowser_5.toPlainText() != '':
                    self.textBrowser_2.setText(groupbox_show.translate_pos(res[0][0][1]))
                    self.textBrowser_8.setText(str(format(res[1][0], '.3f')))
                if self.textBrowser_6.toPlainText() != '':
                    self.textBrowser_3.setText(groupbox_show.translate_pos(res[0][1][1]))
                    self.textBrowser_9.setText(str(format(res[1][1], '.3f')))
                if self.textBrowser_7.toPlainText() != '':
                    self.textBrowser_4.setText(groupbox_show.translate_pos(res[0][2][1]))
                    self.textBrowser_10.setText(str(format(res[1][2], '.3f')))
                times = np.array([0, 0, 0, 0, 0])
                for i in range(0, 3):
                    if res[0][i][0] != 0:
                        image_label.labelling(a, res[0][i][1], res[0][i][0], str(format(res[1][i], '.2f')), times)
                img.save('temp.jpg')
                newstyle = """
                        QGroupBox {
                            border-image: url(./temp.jpg);
                        }
                        """
                newstyle_ = self.groupBox_2.styleSheet() + newstyle
                self.groupBox_2.setStyleSheet(newstyle_)
                self.textBrowser_2.setAlignment(Qt.AlignCenter)
                self.textBrowser_3.setAlignment(Qt.AlignCenter)
                self.textBrowser_4.setAlignment(Qt.AlignCenter)
                self.textBrowser_5.setAlignment(Qt.AlignCenter)
                self.textBrowser_6.setAlignment(Qt.AlignCenter)
                self.textBrowser_7.setAlignment(Qt.AlignCenter)
                self.textBrowser_8.setAlignment(Qt.AlignCenter)
                self.textBrowser_9.setAlignment(Qt.AlignCenter)
                self.textBrowser_10.setAlignment(Qt.AlignCenter)
                machine_match = machine_pattern.search(file_name)
                bearing_match = bearing_pattern.search(file_name)
                machine_number = machine_match.group(1)
                bearing_number = bearing_match.group(1)
                self.label_2.setText("Machine-" + machine_number + "  " + "Bearing-" + bearing_number)
                self.wave_widget.setVisible(True)
            else:
                dir_ = ''
                reply = QMessageBox.warning(self.page_0, "Warning",
                                            f"输入格式错误 ！！", QMessageBox.Ok)
                if reply == QMessageBox.Ok:
                    return

    def on_button_clicked_rul(self):
        QTimer.singleShot(4000, self.delayed_function_rul)

    def delayed_function_rul(self):
        if os.path.isfile('acceleration_data.csv'):
            df = pd.read_csv('acceleration_data.csv')
            rul_dir = './life_vib_example/machine-1/bearing-01'
            column_rul = {'X': 'Horizontal_vibration_signals', 'Y': 'Vertical_vibration_signals', 'Z': 'useless'}
            df_rul_re = df.rename(columns=column_rul)
            df_rul = df_rul_re.head(32713)
            csv_path = os.path.join(rul_dir, '1.csv')
            df_rul.to_csv(csv_path, index=False)
            dir_ = "life_vib_example/machine-1/bearing-01/1.csv"
            self.wave_widget_2_rul.plotfig_rul_his(dir_)
            self.wave_widget_2_rul.setVisible(True)
            self.label_2_rul.setText("Machine-1" + " Bearing-01")
            self.textBrowser_r1.clear()
            res = rul(1, 1)
            self.textBrowser_r1.setTextColor(groupbox_show.show_color_rul(res))
            self.textBrowser_r1.setText(groupbox_show.show_color_rul_text(res))
            self.textBrowser_r1.setAlignment(Qt.AlignCenter)
            self.textBrowser_r2.clear()
            self.textBrowser_r2.setTextColor(groupbox_show.show_color_rul(res))
            self.textBrowser_r2.setText(str(format(res, '.3f')))
            self.textBrowser_r2.setAlignment(Qt.AlignCenter)

    def generate_his(self, dir_):  # 历史记录界面生成数据、曲线
        self.wave_widget_2.setVisible(True)
        self.wave_widget_2.plotfig_rul_his(dir_)
        img_path = './configuration-pic/label-pic.jpg'
        img = Image.open(img_path)
        a = ImageDraw.ImageDraw(img)
        machine_match = machine_pattern.search(dir_)
        bearing_match = bearing_pattern.search(dir_)
        machine_number = machine_match.group(1)
        bearing_number = bearing_match.group(1)
        m = int(machine_number)
        b = int(bearing_number)
        res = link_mysql.to_mysql_h_2(m, b)
        self.scroll_widget.initUI_2(m, b)
        self.scroll_widget2.initUI_2(m,b)
        times = np.array([0, 0, 0, 0, 0])
        image_label.labelling(a, res[1], res[0], str(format(res[2], '.2f')), times)
        image_label.labelling(a, res[4], res[3], str(format(res[5], '.2f')), times)
        image_label.labelling(a, res[7], res[6], str(format(res[8], '.2f')), times)
        img.save('temp_h.jpg')
        newstyle = """
                        QGroupBox {
                            border-image: url(./temp_h.jpg);
                        }
                        """
        newstyle_ = self.groupBox_h_pic.styleSheet() + newstyle
        self.groupBox_h_pic.setStyleSheet(newstyle_)

    def generate_rul(self, dir_):  # 寿命预测界面生成曲线
        self.wave_widget_2_rul.plotfig_rul_his(dir_)
        self.wave_widget_rul.plotfig_rul(dir_)
        self.wave_widget_rul.setVisible(True)
        self.wave_widget_2_rul.setVisible(True)

    def generate_rul_2(self, dir_):  # 寿命预测界面生成结果
        machine_match = machine_pattern.search(dir_)
        bearing_match = bearing_pattern.search(dir_)
        machine_number = machine_match.group(1)
        bearing_number = bearing_match.group(1)
        m_number = int(machine_number)
        b_number = int(bearing_number)
        self.label_2_rul.setText("Machine-" + machine_number + "  " + "Bearing-" + bearing_number)
        self.textBrowser_r1.clear()
        res = rul(m_number, b_number)
        self.textBrowser_r1.setTextColor(groupbox_show.show_color_rul(res))
        self.textBrowser_r1.setText(groupbox_show.show_color_rul_text(res))
        self.textBrowser_r1.setAlignment(Qt.AlignCenter)
        self.textBrowser_r2.clear()
        self.textBrowser_r2.setTextColor(groupbox_show.show_color_rul(res))
        self.textBrowser_r2.setText(str(format(res, '.3f')))
        self.textBrowser_r2.setAlignment(Qt.AlignCenter)


class WaveForm(QWidget):  # 嵌套窗体 用于显示canvas画布界面
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.fig = plt.figure()
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.figtoolbar = NavigationToolbar(self.canvas, self)
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.canvas)
        vlayout.addWidget(self.figtoolbar)
        self.setLayout(vlayout)

    def plotfig(self, path):  # 实时检测界面 传感器时域信号曲线图
        if path != '':
            self.fig.clf()
            df = pd.read_excel(path)
            accr_1 = df['de']
            accr_2 = df['fe']
            axes = self.fig.subplots(2, 1)
            axes[0].plot(accr_1, label='Drive End Signal')
            axes[0].legend(loc='upper left')
            axes[0].grid(True)
            axes[1].plot(accr_2, label='Fan End Signal', color='orange')
            axes[1].legend(loc='upper left')
            axes[1].grid(True)
            mplcyberpunk.add_glow_effects(axes[0], gradient_fill=True)
            mplcyberpunk.add_glow_effects(axes[1], gradient_fill=True)
            self.canvas.draw()
            self.repaint()

    def plotfig_rul(self, path):  # 寿命预测界面 横向纵向传感器信号
        if path != '':
            self.fig.clf()
            df = pd.read_csv(path)
            axes = self.fig.subplots(2, 1)
            downsample_rate = 30
            accr_1 = df['Horizontal_vibration_signals'][::downsample_rate]
            accr_2 = df['Vertical_vibration_signals'][::downsample_rate]
            axes[0].plot(accr_1, label='Horizontal vibration signals', linewidth=0.5)
            axes[0].legend(loc='upper left')
            axes[0].grid(True)
            axes[1].plot(accr_2, label='Vertical vibration signals', color='orange', linewidth=0.5)
            axes[1].legend(loc='upper left')
            axes[1].grid(True)
            mplcyberpunk.add_glow_effects(axes[0], gradient_fill=True)
            mplcyberpunk.add_glow_effects(axes[1], gradient_fill=True)
            self.canvas.draw()
            self.repaint()

    def plotfig_rul_his(self, dir_):  # 寿命预测界面 历史检测结果曲线图
        self.fig.clf()  # 解决重叠问题
        machine_match = machine_pattern.search(dir_)
        bearing_match = bearing_pattern.search(dir_)
        machine_number = machine_match.group(1)
        bearing_number = bearing_match.group(1)
        m_number = int(machine_number)
        b_number = int(bearing_number)
        rul_data = []
        link_mysql.to_my_sql_rul(m_number, b_number, rul_data)
        smooth = make_interp_spline(range(1, len(rul_data) + 1), rul_data)  # 平滑处理
        x_ = np.linspace(1, len(rul_data), 200)
        y = smooth(x_)
        ax = self.fig.subplots(1, 1)
        ax.plot(x_, y, label='RUL', c='#1E90FF', linewidth=2.25)
        ax.legend(loc='upper left')
        ax.grid(True)
        ax.axhline(y=50, color='gray', linestyle='--', linewidth=2)
        ax.axhline(y=100, color='gray', linestyle='--', linewidth=2)
        y_max = max(rul_data) + 10
        ax.set_ylim(0, y_max)
        ax.set_xlim(0, len(rul_data)+10)
        rect_red = Rectangle((0, 0), len(rul_data)+10, 50, fill=True, color='#FF9999', alpha=0.5, zorder=0)
        rect_yellow = Rectangle((0, 50), len(rul_data) + 10, 50, fill=True, color='#FFFFCC', alpha=0.5, zorder=0)
        rect_green = Rectangle((0, 100), len(rul_data) + 10, 120, fill=True, color='#99FF99', alpha=0.5, zorder=0)
        ax.add_patch(rect_red)
        ax.add_patch(rect_yellow)
        ax.add_patch(rect_green)
        ax.set_xlabel('历史检测', fontproperties={'family': 'Microsoft YaHei', 'size': 11})
        ax.set_ylabel('剩余寿命/days', fontproperties={'family': 'Microsoft YaHei', 'size': 11})
        ax.set_title("轴承" + machine_number + "-" + bearing_number + "寿命预测历史记录",
        fontproperties={'family': 'Microsoft YaHei', 'size': 11})
        self.canvas.draw()
        self.repaint()


class AutoScroll(QTableWidget):  # 历史记录界面 带滚动条的列表
    def __init__(self, parent=None):
        super(AutoScroll, self).__init__(parent)
        self.setStyleSheet("QTableWidget { border: 0px; }")
        self.initUI()

    def initUI(self):  # 列表初始显示全部轴承数据
        self.setColumnCount(12)
        res = link_mysql.to_mysql_h_3()
        self.setRowCount(len(res))
        self.setColumnWidth(0, 105)
        for i in range(1, 13):
            self.setColumnWidth(i, 80)
        header = ['检测时间', '机器编号', '轴承编号', '故障深度1', '故障位置1',
                   '故障得分1', '故障深度2', '故障位置2', '故障得分2', '故障深度3',
                   '故障位置3', '故障得分3']
        self.setHorizontalHeaderLabels(header)
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                if type(res[i][j]) == datetime:
                    time_str = res[i][j].strftime('%m-%d %H:%M:%S')
                    item = QTableWidgetItem(time_str)
                else:
                    item = QTableWidgetItem(str(res[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(i, j, item)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def initUI_2(self, m, b):  # 选择轴承后，列表显示单一轴承数据
        self.clear()
        self.setColumnCount(12)
        res = link_mysql.to_mysql_h_4(m, b)
        self.setRowCount(len(res))
        self.setColumnWidth(0, 105)
        for i in range(1, 13):
            self.setColumnWidth(i, 80)
        header = ['检测时间', '机器编号', '轴承编号', '故障深度1', '故障位置1',
                   '故障得分1', '故障深度2', '故障位置2', '故障得分2', '故障深度3',
                   '故障位置3', '故障得分3']
        self.setHorizontalHeaderLabels(header)
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                if type(res[i][j]) == datetime:
                    time_str = res[i][j].strftime('%m-%d %H:%M:%S')
                    item = QTableWidgetItem(time_str)
                else:
                    item = QTableWidgetItem(str(res[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(i, j, item)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)


class AutoScroll_rul(QTableWidget):  # 历史记录界面 带滚动条的列表
    def __init__(self, parent=None):
        super(AutoScroll_rul, self).__init__(parent)
        self.setStyleSheet("QTableWidget { border: 0px; }")
        self.initUI()

    def initUI(self):  # 列表初始显示全部轴承数据
        self.setColumnCount(4)
        res = link_mysql.to_mysql_h_3_rul()
        self.setRowCount(len(res))
        self.setColumnWidth(0, 115)
        for i in range(1, 5):
            self.setColumnWidth(i, 80)
        header = ['检测时间', '机器编号', '轴承编号', '预测结果']
        self.setHorizontalHeaderLabels(header)
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                if type(res[i][j]) == datetime:
                    time_str = res[i][j].strftime('%m-%d %H:%M:%S')
                    item = QTableWidgetItem(time_str)
                else:
                    item = QTableWidgetItem(str(res[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(i, j, item)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def initUI_2(self, m, b):  # 选择轴承后，列表显示单一轴承数据
        self.clear()
        self.setColumnCount(4)
        res = link_mysql.to_mysql_h_4_rul(m, b)
        self.setRowCount(len(res))
        self.setColumnWidth(0, 115)
        for i in range(1, 5):
            self.setColumnWidth(i, 80)
        header = ['检测时间', '机器编号', '轴承编号', '预测结果']
        self.setHorizontalHeaderLabels(header)
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                if type(res[i][j]) == datetime:
                    time_str = res[i][j].strftime('%m-%d %H:%M:%S')
                    item = QTableWidgetItem(time_str)
                else:
                    item = QTableWidgetItem(str(res[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(i, j, item)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)


