# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Sun Feb 15 12:14:33 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(835, 358)
        MainWindow.setMinimumSize(QtCore.QSize(835, 358))
        MainWindow.setMaximumSize(QtCore.QSize(835, 358))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.log_window = QtWidgets.QTextBrowser(self.centralwidget)
        self.log_window.setGeometry(QtCore.QRect(10, 150, 821, 201))
        self.log_window.setObjectName("log_window")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 821, 129))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.ws_state_pic = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.ws_state_pic.setMinimumSize(QtCore.QSize(32, 32))
        self.ws_state_pic.setMaximumSize(QtCore.QSize(32, 32))
        self.ws_state_pic.setText("")
        self.ws_state_pic.setPixmap(QtGui.QPixmap(":/pics/red_light.png"))
        self.ws_state_pic.setObjectName("ws_state_pic")
        self.gridLayout_3.addWidget(self.ws_state_pic, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.sioc_state_pic = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.sioc_state_pic.setMinimumSize(QtCore.QSize(32, 32))
        self.sioc_state_pic.setMaximumSize(QtCore.QSize(32, 32))
        self.sioc_state_pic.setText("")
        self.sioc_state_pic.setPixmap(QtGui.QPixmap(":/pics/red_light.png"))
        self.sioc_state_pic.setObjectName("sioc_state_pic")
        self.gridLayout_3.addWidget(self.sioc_state_pic, 0, 1, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_3.setMaximumSize(QtCore.QSize(99999, 16777215))
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        self.clients_count = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.clients_count.setMaximumSize(QtCore.QSize(99999, 16777215))
        self.clients_count.setObjectName("clients_count")
        self.horizontalLayout_5.addWidget(self.clients_count)
        self.gridLayout_3.addLayout(self.horizontalLayout_5, 1, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 2, 0, 1, 1)
        self.dcs_focus_state = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.dcs_focus_state.setMinimumSize(QtCore.QSize(32, 32))
        self.dcs_focus_state.setMaximumSize(QtCore.QSize(32, 32))
        self.dcs_focus_state.setText("")
        self.dcs_focus_state.setPixmap(QtGui.QPixmap(":/pics/red_light.png"))
        self.dcs_focus_state.setObjectName("dcs_focus_state")
        self.gridLayout_3.addWidget(self.dcs_focus_state, 2, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_6 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.dcs_focus_timeout = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.dcs_focus_timeout.setObjectName("dcs_focus_timeout")
        self.horizontalLayout.addWidget(self.dcs_focus_timeout)
        self.label_7 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout.addWidget(self.label_7)
        self.dcs_focus_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.dcs_focus_button.setObjectName("dcs_focus_button")
        self.horizontalLayout.addWidget(self.dcs_focus_button)
        self.gridLayout_3.addLayout(self.horizontalLayout, 2, 2, 1, 1)
        self.horizontalLayout_3.addLayout(self.gridLayout_3)
        self.textBrowser = QtWidgets.QTextBrowser(self.horizontalLayoutWidget)
        self.textBrowser.setEnabled(False)
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout_3.addWidget(self.textBrowser)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Katze Pit"))
        self.label.setText(_translate("MainWindow", "SIOC"))
        self.label_3.setText(_translate("MainWindow", "Nombre de pits connectés:"))
        self.clients_count.setText(_translate("MainWindow", "0"))
        self.label_4.setText(_translate("MainWindow", "Focus DCS"))
        self.label_6.setText(_translate("MainWindow", "Intervalle"))
        self.dcs_focus_timeout.setText(_translate("MainWindow", "100"))
        self.label_7.setText(_translate("MainWindow", "ms"))
        self.dcs_focus_button.setText(_translate("MainWindow", "Activer"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; text-decoration: underline;\">Focus DCS:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Active une fonction qui rend le focus à la fenêtre de DCS après chaque clic dans le KatzePit. Cela évite de perdre le contrôle de l\'appareil à chaque clic dans la fenêtre du Katze Pit. A réactiver si vous quittez/relancez DCS.</span></p></body></html>"))

import resources_rc
