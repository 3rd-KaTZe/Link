# coding=utf-8
__author__ = 'etcher3rd'
__version__ = '5009'


from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QTextCursor, QPixmap, QImage
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread, Qt, QObject
from PyQt5.QtWebSockets import QWebSocket
from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket
from custom_logging import mkLogger, logged
from queue import Queue
from logging import Handler, Formatter
from ui import main_ui
from time import sleep

from os import _exit


import os
import socket
import select
import sys
import threading
import time
import datetime
import json
import logging

import ws_protocol_00
import ws_handshake_00
import sbr_string
import sbr_data



KTZmain = sys.modules['__main__']
ordre = ""
msgSioc = ""
Sioc_Dico = {}
Trans_Dico = {}
AR_Dico = {'Ordre1': 0, 'Ordre2': 0, 'PingBack': 0}
Data_Dico = {}
Data_Config = {}
Com_Errors = 0

ini_lock = threading.Lock()
run_lock = threading.Lock()
Sioc_run = True
Sioc_alive = False
WS_run = True
WS_alive = False
pulse_ws = 100

def ws_server():
    time.sleep(2.0)
    ini_lock.acquire()
    print("WS_Server >> Start-up du serveur Web-Socket")
    logger.info("WS_Server >> Start-up du serveur Web-Socket")
    miaou = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    miaou.bind((link_hote, link_port))
    miaou.listen(1)
    print("WS-Server >> Ecoute sur le port {} \n".format(link_port))

    ini_lock.release()
    while KTZmain.WS_run:

        print("-- WS-Serveur >> en attente d'un client\n")
        connexion, adresse_client = miaou.accept()

        s = "WS_Server >> Connection Recu de : " + str(adresse_client)
        print(s)
        connexion.send(ws_handshake_00.ws_handshake(connexion.recv(1024)))

        # fin du hand Shake
        print("WS_Server >> Connection Etablie")
        KTZmain.WS_alive = True
        miaou_in = [connexion]
        miaou_out = [connexion]
        loopnb = 0

        ######################## Boucle secondaire de communication WS #####################################
        while KTZmain.WS_alive:

            run_lock.acquire()
            loopnb += 1
            ready_to_read, ready_to_write, in_error = select.select(miaou_in, miaou_out, miaou_in, 0.05)
            for _ in ready_to_read:
                try:
                    recv_msg = ws_protocol_00.readFrame(connexion.recv(1024))
                    KTZmain.ordre = recv_msg.strip('\u0000')
                    loopnb = 0
                except:
                    print("WS_Server >> erreur reception WebSocket")
            trans_msg = json.dumps(KTZmain.Trans_Dico)

            try:
                connexion.send(ws_protocol_00.createFrame(trans_msg))

            except:
                print("WS_Server >> erreur envoi WebSocket")
            KTZmain.Trans_Dico = {}
            if loopnb > KTZmain.pulse_ws:
                KTZmain.WS_alive = False
            if len(KTZmain.ordre) > 0:
                ar_msg = json.dumps(KTZmain.AR_Dico)
                try:
                    connexion.send(ws_protocol_00.createFrame(ar_msg))
                except:
                    print("WS_Server >> erreur envoi WebSocket")
            run_lock.release()
            time.sleep(0.1)
        print("WS_Server >> Liaison avec le KaTZ-Pit Interrompue")
        connexion.close()

# noinspection PyBroadException
def sioc_client():
    ini_lock.acquire()
    print("Sioc-Thread >> Démarrage Sioc_Client et Cach3_Client" + "\n")
    KTZmain.Data_Dico = sbr_data.read_data_dico()
    data_import = "Arn.Inicio:"
    for d in KTZmain.Data_Dico:
        #print(d)
        data_import = data_import + str(d) + ":"
        #print(data_import)

    data_import += "\n"

    print("Cach3_Client : Creation de la connection TS3" + "\n")
    cach3_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while KTZmain.Sioc_run is True:

        retry_sioc = True

        while retry_sioc is True:

            try:
                print("Sioc_Client : Tentative de Connection")
                sioc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sioc_socket.connect((sioc_hote, sioc_port))
                sioc_socket.sendall(data_import.encode())
                _ = sioc_socket.recv(1024).decode()

                s = "Sioc_Client : Connection SIOC Etablie" + "\n"
                print(s)
                retry_sioc = False
                KTZmain.Sioc_alive = True

            except socket.error:
                print("Sioc_Client : Connection SIOC Echouée\n")
                print("Sioc_Client : SIOC est il bien démarré ?\n")
                print("Sioc_Client : Vérifier les paramêtres de connection à SIOC")
                print("Sioc_Client : IP = " + str(sioc_hote) + "   :   Port = " + str(sioc_port) + "\n")
                print("Sioc_Client : Nouvel Essai dans 15 secondes" + "\n")
                time.sleep(15.0)
        ini_lock.release()

        time.sleep(2.0)
        while KTZmain.Sioc_alive:
            run_lock.acquire()
            if len(KTZmain.ordre) > 0:
                chan = KTZmain.ordre.split("=")
                if int(chan[0]) == 4:
                    switch = chan[1]
                    cach3_socket.sendto(switch.encode(), (cach3_hote, cach3_port))
                if int(chan[0]) == 5:
                    KTZmain.Com_Errors += 1
                    KTZmain.ordre = "5=" + str(KTZmain.Com_Errors)
                msg_cmd = "Arn.Resp:" + KTZmain.ordre + ":\n"

                try:
                    sioc_socket.sendall(msg_cmd.encode())

                except:
                    print("SIOC Loop >> Erreur de transmission avec SIOC")
                    print("SIOC Loop >> Vérifier que SIOC est toujours en marche")
                    KTZmain.Sioc_alive = False
                print("Envoyé à SIOC >" + msg_cmd)
                KTZmain.ordre = ""
            _now = datetime.datetime.now()
            pulse = _now.hour * 3600 + _now.minute * 60 + _now.second
            pulse_msg = "Arn.Resp:9=" + str(pulse) + ":\n"
            try:
                sioc_socket.sendall(pulse_msg.encode())

            except:
                print("SIOC Loop >> Erreur de transmission avec SIOC")
                print("SIOC Loop >> Vérifier que SIOC est toujours en marche\n")
                KTZmain.Sioc_alive = False
            try:
                KTZmain.msgSioc = sioc_socket.recv(4096).decode()
            except:
                print("SIOC Loop >>  Erreur Reception Message\n")
                KTZmain.msgSioc = "5=1"
            KTZmain.Sioc_Dico = sbr_string.Sioc_Read(KTZmain.msgSioc)
            for cle in KTZmain.Sioc_Dico:
                KTZmain.Trans_Dico[KTZmain.Data_Dico[cle][0]] = round((KTZmain.Sioc_Dico[cle] * KTZmain.Data_Dico[cle][1]), 0)
            KTZmain.Sioc_Dico = {}
            run_lock.release()
            time.sleep(0.1)

        print("SIOC Loop >> Fin de communication avec SIOC")
        print("SIOC Loop >> Fermeture de la socket")
        sioc_socket.close()
        print("SIOC Loop >> Tentative de reconnection\n")
        ini_lock.acquire()


class SiocClient(QObject):

    connected = pyqtSignal()
    disconnected = pyqtSignal()
    msg_from_sioc = pyqtSignal(str)

    STATE_DIC = {
        0: 'déconnecté',
        1: 'résolution de l\'hôte',
        2: 'établissement de la connexion',
        3: 'connecté',
        4: 'server_side_only',
        5: 'internal_use_only',
        6: 'sur le point de fermer'
    }

    ERROR_DIC = {
        0: 'connexion refusée par le serveur',
        1: 'connexion terminée par le serveur',
        2: 'l\'adresse du serveur n\'a pas été trouvée',
        3: 'privilèges insuffisants',
        4: 'plus de ressources disponibles (trop de sockets ouverts)',
        5: 'time out de l\'opération',
        6: 'datagram trop grand pour l\'OS',
        7: 'erreur réseau',
        8: 'adresse exclusive réservée',  # UDP
        9: 'l\'adresse n\'appartient pas à cet hôte',  # UDP
        10: 'l\'opération demandée n\'est pas supportée par l\'OS',
        11: 'internal_use_only',
        12: 'le proxy requiert une autentification',
        13: 'échec de la connexion sécurisée',
        14: 'la connexion à ce serveur à été refusée par l\'OS',
        15: 'la connexion s\'est terminée de manière innatendue',
        16: 'le serveur n\' pas répondu lors de la phase d\'autentification',
        17: 'l\'adresse du proxy n\'a pas été trouvée',
        18: 'réponse innatendue de la part du serveur proxy'
    }

    logger = None
    @logged
    def __init__(self):
        self.logger.debug('')
        QObject.__init__(self)
        data_dico = sbr_data.read_data_dico()
        self.data_import = ''.join(["Arn.Inicio:"] + [str(x) for x in data_dico]+ ['\n'])


    @pyqtSlot()
    def run(self):
        sioc_socket.stateChanged.connect(self.on_state_changed)
        sioc_socket.error.connect(self.on_error)
        sioc_socket.disconnected.connect(self.connect_to_sioc)
        sioc_socket.readyRead.connect(self.read_data)
        self.connect_to_sioc()

    @pyqtSlot()
    def connect_to_sioc(self):
        self.logger.debug('connexion à l\'ami SIOC à l\'adresse {}:{}'.format(sioc_hote, sioc_port))
        while not sioc_socket.state() == 3:
            sioc_socket.connectToHost(sioc_hote, sioc_port)
            if sioc_socket.waitForConnected(1000):
                self.connected.emit()
                sioc_socket.setSocketOption(QAbstractSocket.KeepAliveOption, 1)
                self.write_data(self.data_import.encode())
            else:
                self.disconnected.emit()

    @pyqtSlot()
    def on_state_changed(self):
        self.logger.debug('statut: {}'.format(self.STATE_DIC[sioc_socket.state()]))

    @pyqtSlot()
    def on_error(self):
        self.logger.error(self.ERROR_DIC[sioc_socket.error()])

    @pyqtSlot()
    def read_data(self):
        self.logger.debug('données disponibles en lecture')
        while True:
            msg = sioc_socket.read(4096)
            print(msg)
            if msg == b'':
                break
            self.msg_from_sioc.emit(msg.decode())

    @pyqtSlot(str)
    def write_data(self, data):
        sioc_socket.write(data)


class Gui():

    def __init__(self):
        pass

    class LoggingHandler(QObject, Handler):

        sig_send_text = pyqtSignal(str)

        def __init__(self):
            QObject.__init__(self)
            # Handler.__init__(self)
            self.q = Queue()

        def emit(self, record):
            self.q.put(record)

        @pyqtSlot()
        def run(self):
            while True:
                text = self.format(self.q.get())
                self.sig_send_text.emit(text)

    class Main(QMainWindow, main_ui.Ui_MainWindow):

        logger = None
        @logged
        def __init__(self):
            QMainWindow.__init__(self)
            self.setupUi(self)
            self.show()

            self.logger_thread = QThread(self)
            self.logger_handler = Gui.LoggingHandler()
            formatter = Formatter('%(levelname)s - %(name)s - %(funcName)s - %(message)s')
            self.logger_handler.setFormatter(formatter)
            self.logger_handler.moveToThread(self.logger_thread)
            self.logger_thread.started.connect(self.logger_handler.run)
            self.logger_handler.sig_send_text.connect(self.log)
            logger.addHandler(self.logger_handler)
            self.logger_thread.start()

            self.sioc_thread = QThread(self)
            self.sioc_client = SiocClient()
            sioc_socket.connected.connect(self.on_sioc_connect)
            sioc_socket.disconnected.connect(self.on_sioc_disconnect)
            self.sioc_client.msg_from_sioc.connect(self.log)
            self.sioc_client.moveToThread(self.sioc_thread)
            self.sioc_thread.started.connect(self.sioc_client.run)
            self.sioc_thread.start()


        @pyqtSlot(str)
        def log(self, text):
            self.log_window.moveCursor(QTextCursor.End)
            self.log_window.append(text)

        @pyqtSlot()
        def on_sioc_connect(self):
            self.sioc_state_pic.setPixmap(QPixmap(':/pics/green_light.png'))

        @pyqtSlot()
        def on_sioc_disconnect(self):
            self.sioc_state_pic.setPixmap(QPixmap(':/pics/red_light.png'))

# Main Programme
if __name__ == "__main__":
    logger = mkLogger('__main__')
    Data_Config = sbr_data.read_config()
    sioc_hote = Data_Config["sioc_hote"]
    sioc_port = int(Data_Config["sioc_port"])
    sioc_plage = int(Data_Config["sioc_plage"])
    cach3_hote = Data_Config["ts_hote"]
    cach3_port = int(Data_Config["ts_port"])
    link_hote = Data_Config["link_hote"]
    link_port = int(Data_Config["link_port"])
    
    
    sioc_socket = QTcpSocket()

    qt_app = QApplication(sys.argv)
    main_ui = Gui.Main()
    # main_ui.setWindowIcon(ekpi_icon)
    _exit(qt_app.exec())
    # main_ui.run()

    sioc_socket = SiocClient(sioc_hote, sioc_port)
    while 1:
        pass
    exit(0)


    msg = "Configuration du Helo-Link : \n\n" + "Sioc IP = " + str(sioc_hote) + " ;  Sioc Port = " + str(
        sioc_port) + " ;  Décalage des offsets = " + str(sioc_plage)
    print(msg)
    link_hote = Data_Config["link_hote"]
    link_port = int(Data_Config["link_port"])
    msg1 = "WS IP = " + str(link_hote) + " ;  WS Port = " + str(link_port)
    print(msg1)
    cach3_hote = Data_Config["ts_hote"]
    cach3_port = int(Data_Config["ts_port"])
    msg2 = "Cach3 IP = " + str(cach3_hote) + " ;  Cach3 Port = " + str(cach3_port) + "\n"
    print(msg2)
    KtzWs_1 = threading.Thread(None, ws_server, "WS_Server_Thread", (), {})
    KtzSioc_2 = threading.Thread(None, sioc_client, "Sioc_Server_Thread", (), {})
    KtzWs_1.start()
    KtzSioc_2.start()

    #TODO: bug à la fermture, peut-être voir avec thread.join()