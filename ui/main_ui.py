# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Sun Feb 15 02:49:23 2015
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
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(275, 70, 181, 20))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.clients_count = QtWidgets.QLabel(self.centralwidget)
        self.clients_count.setGeometry(QtCore.QRect(470, 70, 16, 16))
        self.clients_count.setObjectName("clients_count")
        self.dcs_focus_state = QtWidgets.QLabel(self.centralwidget)
        self.dcs_focus_state.setGeometry(QtCore.QRect(190, 130, 32, 32))
        self.dcs_focus_state.setMinimumSize(QtCore.QSize(32, 32))
        self.dcs_focus_state.setMaximumSize(QtCore.QSize(32, 32))
        self.dcs_focus_state.setText("")
        self.dcs_focus_state.setPixmap(QtGui.QPixmap(":/pics/red_light.png"))
        self.dcs_focus_state.setObjectName("dcs_focus_state")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(75, 140, 71, 20))
        self.label_4.setObjectName("label_4")
        self.dcs_focus_button = QtWidgets.QPushButton(self.centralwidget)
        self.dcs_focus_button.setGeometry(QtCore.QRect(160, 190, 75, 23))
        self.dcs_focus_button.setObjectName("dcs_focus_button")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(150, 230, 101, 61))
        self.label_5.setScaledContents(False)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.dcs_focus_timeout = QtWidgets.QLineEdit(self.centralwidget)
        self.dcs_focus_timeout.setGeometry(QtCore.QRect(370, 250, 113, 20))
        self.dcs_focus_timeout.setObjectName("dcs_focus_timeout")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(285, 250, 61, 20))
        self.label_6.setObjectName("label_6")
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
        self.label_3.setText(_translate("MainWindow", "Nombre de pits connectés:"))
        self.clients_count.setText(_translate("MainWindow", "0"))
        self.label_4.setText(_translate("MainWindow", "Focus DCS"))
        self.dcs_focus_button.setText(_translate("MainWindow", "Activer"))
        self.label_5.setText(_translate("MainWindow", "A réactiver si vous quittez/relancez DCS"))
        self.dcs_focus_timeout.setText(_translate("MainWindow", "100"))
        self.label_6.setText(_translate("MainWindow", "Intervalle"))

import resources_rc
