

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(358, 259)
        MainWindow.setMinimumSize(QtCore.QSize(358, 259))
        MainWindow.setMaximumSize(QtCore.QSize(358, 259))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 341, 241))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.sioc_state_pic = QtWidgets.QLabel(self.gridLayoutWidget)
        self.sioc_state_pic.setMinimumSize(QtCore.QSize(32, 32))
        self.sioc_state_pic.setMaximumSize(QtCore.QSize(32, 32))
        self.sioc_state_pic.setText("")
        self.sioc_state_pic.setPixmap(QtGui.QPixmap(":/pics/red_light.png"))
        self.sioc_state_pic.setObjectName("sioc_state_pic")
        self.gridLayout_3.addWidget(self.sioc_state_pic, 0, 1, 1, 1)
        self.ws_state_pic = QtWidgets.QLabel(self.gridLayoutWidget)
        self.ws_state_pic.setMinimumSize(QtCore.QSize(32, 32))
        self.ws_state_pic.setMaximumSize(QtCore.QSize(32, 32))
        self.ws_state_pic.setText("")
        self.ws_state_pic.setPixmap(QtGui.QPixmap(":/pics/red_light.png"))
        self.ws_state_pic.setObjectName("ws_state_pic")
        self.gridLayout_3.addWidget(self.ws_state_pic, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setMaximumSize(QtCore.QSize(99999, 16777215))
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        self.clients_count = QtWidgets.QLabel(self.gridLayoutWidget)
        self.clients_count.setMaximumSize(QtCore.QSize(99999, 16777215))
        self.clients_count.setObjectName("clients_count")
        self.horizontalLayout_5.addWidget(self.clients_count)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.gridLayout_3.addLayout(self.horizontalLayout_5, 1, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 2, 0, 1, 1)
        self.dcs_focus_state = QtWidgets.QLabel(self.gridLayoutWidget)
        self.dcs_focus_state.setMinimumSize(QtCore.QSize(32, 32))
        self.dcs_focus_state.setMaximumSize(QtCore.QSize(32, 32))
        self.dcs_focus_state.setText("")
        self.dcs_focus_state.setPixmap(QtGui.QPixmap(":/pics/red_light.png"))
        self.dcs_focus_state.setObjectName("dcs_focus_state")
        self.gridLayout_3.addWidget(self.dcs_focus_state, 2, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.dcs_focus_timeout = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.dcs_focus_timeout.setEnabled(True)
        self.dcs_focus_timeout.setMaximumSize(QtCore.QSize(70, 16777215))
        self.dcs_focus_timeout.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.dcs_focus_timeout.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.dcs_focus_timeout.setObjectName("dcs_focus_timeout")
        self.horizontalLayout.addWidget(self.dcs_focus_timeout)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout.addWidget(self.label_7)
        self.dcs_focus_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.dcs_focus_button.setObjectName("dcs_focus_button")
        self.horizontalLayout.addWidget(self.dcs_focus_button)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout_3.addLayout(self.horizontalLayout, 2, 2, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.sioc_address_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.sioc_address_label.setText("")
        self.sioc_address_label.setObjectName("sioc_address_label")
        self.horizontalLayout_2.addWidget(self.sioc_address_label)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 0, 2, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.log_window = QtWidgets.QTextBrowser(self.gridLayoutWidget)
        self.log_window.setEnabled(True)
        self.log_window.setObjectName("log_window")
        self.verticalLayout.addWidget(self.log_window)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.permit_remote_checkbox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.permit_remote_checkbox.setObjectName("permit_remote_checkbox")
        self.horizontalLayout_6.addWidget(self.permit_remote_checkbox)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.sioc_state_pic.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ff0000;\">client SIOC déconnecté</span></p><p><span style=\" color:#00aa00;\">client SIOC connecté</span></p></body></html>"))
        self.ws_state_pic.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ff0000;\">Serveur WebSocket inactif</span></p><p><span style=\" color:#ff5500;\">Serveur WebSocket en attente d\'un client</span></p><p><span style=\" color:#00aa00;\">Au moins un client est connecté</span></p></body></html>"))
        self.label_2.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; text-decoration: underline;\">Katze Pit:</span></p><p>Serveur WebSocket.</p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "Katze Pit"))
        self.label.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; text-decoration: underline;\">SIOC:</span></p><p>Connexion cliente au serveur SIOC. Si la connexion ne s\'établit pas, vérifiez que SIOC est lancé, et, dans la fenêtre principale de SIOC, que l\'adresse ainsi que le port correspondent bien à ceux que vous aurez renseignés dans EKPI.</p></body></html>"))
        self.label.setText(_translate("MainWindow", "SIOC"))
        self.label_3.setText(_translate("MainWindow", "Nombre de pits connectés:"))
        self.clients_count.setText(_translate("MainWindow", "0"))
        self.label_4.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; text-decoration: underline;\">Focus DCS:</span></p><p>Active une fonction qui rend le focus à la fenêtre de DCS après chaque clic dans le KatzePit, ce qui évite de perdre le contrôle de l\'appareil. A réactiver si vous quittez/relancez DCS.</p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "Focus DCS"))
        self.dcs_focus_state.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ff0000;\">Focus DCS inactif</span></p><p><span style=\" color:#00aa00;\">Focus DCS actif</span></p></body></html>"))
        self.label_6.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; text-decoration: underline;\">Intervalle Focus DCS:</span></p><p>Temps, en millisecondes, entre les vérifications. A chaque vérification, si la fenêtre de DCS n\'est pas la fenêtre active, elle sera ramenée au premier plan.</p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "Intervalle"))
        self.dcs_focus_timeout.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; text-decoration: underline;\">Intervalle Focus DCS:</span></p><p><br/></p><p>Temps, en millisecondes, entre les vérifications. A chaque vérification, si la fenêtre de DCS n\'est pas la fenêtre active, elle sera ramenée au premier plan.</p></body></html>"))
        self.dcs_focus_timeout.setText(_translate("MainWindow", "100"))
        self.label_7.setText(_translate("MainWindow", "ms"))
        self.dcs_focus_button.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; text-decoration: underline;\">Activer Focus DCS:</span></p><p><br/></p><p>Activer/désactiver le Focus DCS</p></body></html>"))
        self.dcs_focus_button.setText(_translate("MainWindow", "Activer"))
        self.log_window.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p></body></html>"))
        self.permit_remote_checkbox.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; text-decoration: underline;\">Commands distantes:</span></p><p><br/></p><p>Si cette case est cochée, les connexionx distantes (autre que 127.0.0.1) ne seront pas autorisées à envoyer des commandes à DCS. Utiles pour empêcher les petits blagueurs de vous éjecter en plein vol. Moins utile dans le cas de l\'instruction.</p></body></html>"))
        self.permit_remote_checkbox.setText(_translate("MainWindow", "Autoriser les pits distants à envoyer des commandes"))

import resources_rc
