# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Sat Feb 14 17:19:03 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(120, 30, 47, 13))
        self.label.setObjectName("label")
        self.log_window = QtWidgets.QTextBrowser(self.centralwidget)
        self.log_window.setGeometry(QtCore.QRect(10, 350, 781, 192))
        self.log_window.setObjectName("log_window")
        self.sioc_state_pic = QtWidgets.QLabel(self.centralwidget)
        self.sioc_state_pic.setGeometry(QtCore.QRect(190, 20, 32, 32))
        self.sioc_state_pic.setMinimumSize(QtCore.QSize(32, 32))
        self.sioc_state_pic.setMaximumSize(QtCore.QSize(32, 32))
        self.sioc_state_pic.setText("")
        self.sioc_state_pic.setPixmap(QtGui.QPixmap(":/pics/red_light.png"))
        self.sioc_state_pic.setObjectName("sioc_state_pic")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(100, 90, 46, 13))
        self.label_2.setObjectName("label_2")
        self.ws_state_pic = QtWidgets.QLabel(self.centralwidget)
        self.ws_state_pic.setGeometry(QtCore.QRect(190, 70, 32, 32))
        self.ws_state_pic.setMinimumSize(QtCore.QSize(32, 32))
        self.ws_state_pic.setMaximumSize(QtCore.QSize(32, 32))
        self.ws_state_pic.setText("")
        self.ws_state_pic.setPixmap(QtGui.QPixmap(":/pics/red_light.png"))
        self.ws_state_pic.setObjectName("ws_state_pic")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "SIOC"))
        self.label_2.setText(_translate("MainWindow", "KatzePit"))

import resources_rc
