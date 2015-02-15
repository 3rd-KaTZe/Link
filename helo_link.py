# coding=utf-8
__author__ = 'etcher3rd'

import sys
import threading
import sbr_string
import sbr_data
import win32com.client
import wmi

from main import __version__
from os import _exit
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QTextCursor, QPixmap, QIntValidator, QIcon
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread, QObject, QByteArray, QTimer
from PyQt5.QtWebSockets import QWebSocketServer
from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket, QHostAddress
from custom_logging import mkLogger, logged
from queue import Queue
from logging import Handler, Formatter
from ui import main_ui
from json import dumps


ordre = ""
msgSioc = ""
Sioc_Dico = {}
Trans_Dico = {}
ack_dico = {'Ordre1': 0, 'Ordre2': 0, 'PingBack': 0}
com_errors = 0

ini_lock = threading.Lock()
run_lock = threading.Lock()
Sioc_run = True
Sioc_alive = False
WS_run = True
WS_alive = False
pulse_ws = 100

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


class SiocClient(QObject):
    connected = pyqtSignal()
    disconnected = pyqtSignal()
    msg_from_sioc = pyqtSignal(str)

    logger = None

    @logged
    def __init__(self):
        global data_dico
        self.logger.debug('')
        QObject.__init__(self)
        data_dico = sbr_data.read_data_dico()
        self.data_import = ''.join(["Arn.Inicio:"] + ['{}:'.format(x) for x in data_dico] + ['\n'])

    # noinspection PyUnresolvedReferences
    @pyqtSlot()
    def run(self):
        sioc_socket_v2.stateChanged.connect(self.on_state_changed)
        sioc_socket_v2.error.connect(self.on_error)
        sioc_socket_v2.disconnected.connect(self.on_disconnected)
        sioc_socket_v2.readyRead.connect(self.read_data)
        self.connect_to_sioc()

    @pyqtSlot()
    def connect_to_sioc(self):
        self.logger.info('connexion à l\'ami SIOC sur {}:{}'.format(sioc_hote, sioc_port))
        while not sioc_socket_v2.state() == 3:
            sioc_socket_v2.connectToHost(sioc_hote, sioc_port)
            if sioc_socket_v2.waitForConnected(1000):
                self.logger.info('connexion établie')
                self.connected.emit()
                sioc_socket_v2.setSocketOption(QAbstractSocket.KeepAliveOption, 1)
                sioc_socket_v2.setSocketOption(QAbstractSocket.LowDelayOption, 1)
                self.write_data(self.data_import)
            else:
                self.disconnected.emit()

    @pyqtSlot()
    def on_state_changed(self):
        self.logger.debug('statut: {}'.format(STATE_DIC[sioc_socket_v2.state()]))

    @pyqtSlot()
    def on_disconnected(self):
        self.logger.warning('connexion SIOC perdue')
        self.connect_to_sioc()

    @pyqtSlot()
    def on_error(self):
        if sioc_socket_v2.error() in [1]:
            return
        self.logger.error(ERROR_DIC[sioc_socket_v2.error()])

    @pyqtSlot()
    def read_data(self):
        # self.logger.debug('données disponibles en lecture')
        while not sioc_socket_v2.atEnd():
            msg = sioc_socket_v2.read(4096).decode().strip('\r\n')
            if msg in ['Arn.Vivo:']:
                # self.msg_from_sioc.emit('SIOC ALIVE')  # DEBUG
                break
            # self.logger.debug('message reçu: {}'.format(msg))
            self.msg_from_sioc.emit(msg)

    @pyqtSlot(str)
    def write_data(self, msg):
        sioc_socket_v2.writeData(msg.encode())
        if not sioc_socket_v2.waitForBytesWritten(1000):
            self.logger.error('erreur lors de l\'écriture sur le socket')


class WebSocketServer(QWebSocketServer):
    msg_from_pit = pyqtSignal(str)

    new_client_count = pyqtSignal(int)
    logger, clients = None, []

    @logged
    def __init__(self, *args, **kwargs):
        self.logger.debug('')
        QWebSocketServer.__init__(self, *args, **kwargs)

    def start_listening(self):
        self.logger.info('ouverture du socket WebServer pour le Katze Pit')
        if not self.listen(QHostAddress.Any, link_port):
            self.logger.error(ERROR_DIC[self.error()])
        else:
            self.logger.info('socket ouvert, en attente de client')
            # noinspection PyUnresolvedReferences
            self.newConnection.connect(self.on_new_connection)

    @pyqtSlot()
    def on_new_connection(self):
        self.logger.debug('')
        client = self.nextPendingConnection()
        self.logger.info('connexion d\'un Katze Pit depuis l\'adresse: {}'.format(client.peerAddress().toString()))
        self.logger.debug(client)
        client.disconnected.connect(self.on_client_disconnect)
        client.textMessageReceived.connect(self.process_text_message)
        client.pong.connect(self.on_pong)
        client.error.connect(self.on_error)
        client.stateChanged.connect(self.on_client_state_changed)
        self.clients.append(client)
        self.new_client_count.emit(self.clients_count)

    @property
    def clients_count(self):
        return len(self.clients)

    @pyqtSlot()
    def on_close(self):
        self.logger.debug('')
        self.ws_v2.newConnection.disconnect()

    @pyqtSlot(int, str)
    def on_pong(self, elapsed_time, _):
        self.logger.debug('ping reçu après {}ms'.format(elapsed_time))

    @pyqtSlot()
    def on_client_state_changed(self):
        client = self.sender()
        self.logger.debug(STATE_DIC[client.state()])

    @pyqtSlot()
    def on_error(self):
        client = self.sender()
        self.logger.error(ERROR_DIC[client.error()])

    @pyqtSlot()
    def on_client_disconnect(self):
        self.logger.debug('')
        client = self.sender()
        self.logger.info('déconnexion du Katze Pit: {}'.format(client.peerAddress().toString()))
        client.deleteLater()
        self.clients.remove(client)
        self.new_client_count.emit(self.clients_count)

    @pyqtSlot(QByteArray)
    def process_text_message(self, msg):
        # client = self.sender()
        # self.logger.debug(msg)
        self.msg_from_pit.emit(msg)

    @pyqtSlot(str)
    def write_data(self, msg):
        # self.logger.debug(msg)
        for client in self.clients:
            # self.logger.debug(client)
            client.sendTextMessage(msg)


class FocusDCS(QObject):
    logger = None

    @logged
    def __init__(self):
        self.logger.debug('')
        QObject.__init__(self)
        self.timer = QTimer()
        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(self.on_timeout)
        self.__is_running = False

    def start(self, interval):
        self.__is_running = True
        self.timer.start(interval)

    def stop(self):
        self.__is_running = False
        self.timer.stop()

    @pyqtSlot()
    def on_timeout(self):
        # self.logger.debug('')
        raise_dcs_window()

    @property
    def is_running(self):
        return self.__is_running


class Gui():
    def __init__(self):
        pass

    class LoggingHandler(QObject, Handler):

        sig_send_text = pyqtSignal(str)

        def __init__(self):
            QObject.__init__(self)
            self.q = Queue()

        def emit(self, record):
            if record.levelno > 10:
                self.q.put(record)

        @pyqtSlot()
        def run(self):
            while True:
                text = self.format(self.q.get())
                self.sig_send_text.emit(text)

    class Main(QMainWindow, main_ui.Ui_MainWindow):

        logger = None
        sioc_thread, sioc_client = None, None
        logger_thread, logger_handler = None, None
        dcs_focus_timer, dcs_focus_timer_thread = None, None
        server = None

        @logged
        def __init__(self):
            self.logger.debug('')
            QMainWindow.__init__(self)
            self.setupUi(self)
            self.setWindowTitle('Katze Link {}'.format(__version__))
            self.show()
            self.start_logger_handler()
            self.start_sioc_client()
            self.start_ws_server()
            self.start_dcs_focus_timer()
            # noinspection PyUnresolvedReferences
            self.dcs_focus_button.clicked.connect(self.on_dcs_focus_button_state_clicked)
            self.dcs_focus_timeout.setValidator(QIntValidator(50, 5000))

        @pyqtSlot()
        def start_logger_handler(self):
            self.logger_thread = QThread(self)
            self.logger_handler = Gui.LoggingHandler()
            formatter = Formatter('%(levelname)s - %(name)s - %(funcName)s - %(message)s')
            self.logger_handler.setFormatter(formatter)
            self.logger_handler.moveToThread(self.logger_thread)
            # noinspection PyUnresolvedReferences
            self.logger_thread.started.connect(self.logger_handler.run)
            self.logger_handler.sig_send_text.connect(self.log)
            logger.addHandler(self.logger_handler)
            self.logger_thread.start()

        @pyqtSlot()
        def start_sioc_client(self):
            self.sioc_thread = QThread(self)
            self.sioc_client = SiocClient()
            # noinspection PyUnresolvedReferences
            sioc_socket_v2.connected.connect(self.on_sioc_connect)
            # noinspection PyUnresolvedReferences
            sioc_socket_v2.disconnected.connect(self.on_sioc_disconnect)
            self.sioc_client.msg_from_sioc.connect(self.on_sioc_msg)
            self.sioc_client.moveToThread(self.sioc_thread)
            # noinspection PyUnresolvedReferences
            self.sioc_thread.started.connect(self.sioc_client.run)
            self.sioc_thread.start()

        @pyqtSlot()
        def start_ws_server(self):
            self.logger.debug('')
            self.server = WebSocketServer('', QWebSocketServer.NonSecureMode)
            self.server.start_listening()
            if self.server.isListening():
                self.server.new_client_count.connect(self.on_client_count_change)
                self.server.msg_from_pit.connect(self.on_pit_msg)
                self.on_ws_listening()

        @pyqtSlot()
        def start_dcs_focus_timer(self):
            self.dcs_focus_timer_thread = QThread(self)
            self.dcs_focus_timer = FocusDCS()
            self.dcs_focus_timer.moveToThread(self.dcs_focus_timer_thread)
            self.dcs_focus_timer_thread.start()

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

        @pyqtSlot(str)
        def on_sioc_msg(self, msglist):
            # self.logger.debug('message SIOC brut: {}'.format(msglist))
            for msg in msglist.split('\r\n'):
                # self.logger.debug('raw splitted message: {}'.format(msg))
                if msg in ['Arn.Vivo:'] or not msg:
                    continue
                # self.logger.debug('message SIOC: {}'.format(msg))
                formatted_msg = sbr_string.sioc_read(msg)
                dic = {}
                for k in formatted_msg.keys():
                    dic[data_dico[k][0]] = round(formatted_msg[k] * data_dico[k][1], 0)
                self.server.write_data(dumps(dic))

        @pyqtSlot(str)
        def on_pit_msg(self, msg):
            msg = msg.strip('\u0000')
            # self.logger.debug('message Pit: {}'.format(msg))
            # send ACK
            # self.server.write_data(dumps(ack_dico))
            chan = int(msg.split('=')[0])
            if chan == 4:
                # TODO: CACH3
                pass
            if chan == 5:
                # self.logger.error('erreur Pit: {}'.format(msg))
                global com_errors
                com_errors += 1
                msg = '5={}'.format(com_errors)
            msg = 'Arn.Resp:{}:\n'.format(msg)
            # self.logger.debug('envoi du message à SIOC: {}'.format(msg))
            self.sioc_client.write_data(msg)

        @pyqtSlot()
        def on_ws_listening(self):
            self.ws_state_pic.setPixmap(QPixmap(':/pics/orange_light.png'))

        @pyqtSlot()
        def on_ws_disconnect(self):
            self.ws_state_pic.setPixmap(QPixmap(':/pics/red_light.png'))

        @pyqtSlot()
        def on_ws_connect(self):
            self.ws_state_pic.setPixmap(QPixmap(':/pics/green_light.png'))

        @pyqtSlot(str)
        def on_ws_msg(self, msg):
            self.logger.debug('message ws: {}'.format(msg))

        @pyqtSlot(int)
        def on_client_count_change(self, i):
            self.logger.debug(i)
            self.clients_count.setText(str(i))
            if i == 0:
                self.on_ws_listening()
            else:
                self.on_ws_connect()

        @pyqtSlot()
        def on_dcs_focus_button_state_clicked(self):
            if self.dcs_focus_timer.is_running:
                self.dcs_focus_timer.stop()
                self.dcs_focus_button.setText('Activer')
                self.dcs_focus_state.setPixmap(QPixmap(':/pics/red_light.png'))
            else:
                if raise_dcs_window(refresh_pid=True):
                    interval = int(self.dcs_focus_timeout.text())
                    if interval < 100:
                        interval = 100
                    self.dcs_focus_button.setText('Désactiver')
                    self.dcs_focus_state.setPixmap(QPixmap(':/pics/green_light.png'))
                    self.dcs_focus_timer.start(interval)


def raise_dcs_window(refresh_pid=False):
    global dcs_pid
    if dcs_pid is None or refresh_pid:
        c = wmi.WMI()
        dcs_pid = None
        for process in c.Win32_Process(name='dcs.exe'):
            dcs_pid = process.ProcessId
        if dcs_pid is None:
            logger.warning('le processus DCS.exe n\'a pas été trouvé')
            logger.info('notez que "DCS.exe" n\'existe QUE si vous êtes cockpit ou sur l\'interface multijoueur.')
            logger.ingo('l\'interface principale de DCS (avec les options, l\'éditeur de mission etc...) ne '
                        'compte pas')
            return
    shell.AppActivate(dcs_pid)
    shell.SendKeys('')
    return True

dcs_pid = None
shell = win32com.client.Dispatch("WScript.Shell")
logger = mkLogger('__main__')
data_config = sbr_data.read_config()
data_dico = sbr_data.read_data_dico()
sioc_hote = data_config["sioc_hote"]
sioc_port = int(data_config["sioc_port"])
sioc_plage = int(data_config["sioc_plage"])
cach3_hote = data_config["ts_hote"]
cach3_port = int(data_config["ts_port"])
link_hote = data_config["link_hote"]
link_port = int(data_config["link_port"])

sioc_socket_v2 = QTcpSocket()

qt_app = QApplication(sys.argv)
link_icon = QIcon(':/ico/link.ico')
ui_main = Gui.Main()
ui_main.setWindowIcon(link_icon)
_exit(qt_app.exec())