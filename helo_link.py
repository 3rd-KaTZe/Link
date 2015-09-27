# coding=utf-8
__author__ = 'etcher3rd'

import sys
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
from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket, QHostAddress, QUdpSocket
from custom_logging import mkLogger, logged
from queue import Queue
from logging import Handler, Formatter
from ui import main_ui
from json import dumps

com_errors = 0

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
        socket_sioc.stateChanged.connect(self.on_state_changed)
        socket_sioc.error.connect(self.on_error)
        socket_sioc.disconnected.connect(self.on_disconnected)
        socket_sioc.readyRead.connect(self.read_data)
        self.connect_to_sioc()

    @pyqtSlot()
    def connect_to_sioc(self):
        self.logger.info('tentative de connexion à l\'ami SIOC sur {}:{}'.format(sioc_hote, sioc_port))
        global pit_state
        pit_state = {}
        while not socket_sioc.state() == 3:
            socket_sioc.connectToHost(sioc_hote, sioc_port)
            if socket_sioc.waitForConnected(1000):
                self.logger.info('connexion établie')
                self.connected.emit()
                socket_sioc.setSocketOption(QAbstractSocket.KeepAliveOption, 1)
                socket_sioc.setSocketOption(QAbstractSocket.LowDelayOption, 1)
                self.write_data(self.data_import)
            else:
                self.disconnected.emit()

    @pyqtSlot()
    def on_state_changed(self):
        self.logger.debug('statut: {}'.format(STATE_DIC[socket_sioc.state()]))

    @pyqtSlot()
    def on_disconnected(self):
        self.logger.warning('connexion SIOC perdue')
        self.connect_to_sioc()

    @pyqtSlot()
    def on_error(self):
        if socket_sioc.error() in [1, 5]:
            self.logger.debug(ERROR_DIC[socket_sioc.error()])
            return
        self.logger.error(ERROR_DIC[socket_sioc.error()])

    @pyqtSlot()
    def read_data(self):
        # self.logger.debug('données disponibles en lecture')
        while not socket_sioc.atEnd():
            msg = socket_sioc.read(4096).decode().strip('\r\n')
            if msg in ['Arn.Vivo:']:
                # self.msg_from_sioc.emit('SIOC ALIVE')  # DEBUG
                break
            # self.logger.debug('message reçu: {}'.format(msg))
            self.msg_from_sioc.emit(msg)

    @pyqtSlot(str)
    def write_data(self, msg):
        if not socket_sioc.state() == 3:
            return
        socket_sioc.writeData(msg.encode())
        if not socket_sioc.waitForBytesWritten(1000):
            self.logger.error('erreur lors de l\'écriture sur le socket')


class WebSocketServer(QWebSocketServer):
    msg_from_pit = pyqtSignal(str)

    new_client_count = pyqtSignal()
    logger, local_clients, remote_clients = None, [], []

    @logged
    def __init__(self, *args, **kwargs):
        self.logger.debug('')
        QWebSocketServer.__init__(self, *args, **kwargs)

    def start_listening(self):
        self.logger.info('ouverture du socket WebServer pour le Katze Pit')
        if not self.listen(QHostAddress.Any, link_port):
            if self.error() == 1006:
                self.logger.error('impossible de lier le socket; est-ce qu\'une autre instance du Link tourne déjà ?')
            else:
                try:
                    self.logger.error(ERROR_DIC[self.error()])
                except KeyError:
                    self.logger.exception('erreur inconnue: {}'.format(self.error()))
        else:
            self.logger.info('socket ouvert, en attente de client')
            # noinspection PyUnresolvedReferences
            self.newConnection.connect(self.on_new_connection)

    @pyqtSlot()
    def on_new_connection(self):
        global pit_state
        self.logger.debug('')
        client = self.nextPendingConnection()
        client.address = client.peerAddress().toString()
        self.logger.info('connexion d\'un Katze Pit depuis l\'adresse: {}'.format(client.peerAddress().toString()))
        self.logger.debug(client)
        client.disconnected.connect(self.on_client_disconnect)
        client.textMessageReceived.connect(self.process_text_message)
        client.pong.connect(self.on_pong)
        client.error.connect(self.on_error)
        client.stateChanged.connect(self.on_client_state_changed)
        self.write_data(dumps(pit_state, client))
        if client.address in ['127.0.0.1'] + whitelist:
            self.local_clients.append(client)
        else:
            self.remote_clients.append(client)
        self.new_client_count.emit()

    @property
    def local_clients_count(self):
        return len(self.local_clients)

    @property
    def remote_clients_count(self):
        return len(self.remote_clients)

    @property
    def total_clients_count(self):
        return self.remote_clients_count + self.local_clients_count

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

    # noinspection PyBroadException
    @pyqtSlot()
    def on_client_disconnect(self):
        self.logger.debug('')
        client = self.sender()
        self.logger.info('déconnexion du Katze Pit: {}'.format(client.peerAddress().toString()))
        client.deleteLater()
        try:
            self.local_clients.remove(client)
        except:
            pass
        try:
            self.remote_clients.remove(client)
        except:
            pass
        self.new_client_count.emit()

    @pyqtSlot(QByteArray)
    def process_text_message(self, msg):
        client = self.sender()
        if permit_remote_commands is False and not client in self.local_clients:
            return
        self.msg_from_pit.emit(msg)

    @pyqtSlot(str)
    def write_data(self, msg, client=None):
        # self.logger.debug(msg)
        if client is not None:
            client.sendTextMessage(msg)
        else:
            for client in self.local_clients + self.remote_clients:
                client.sendTextMessage(msg)


class URClient(QObject):
    connected = pyqtSignal()
    disconnected = pyqtSignal()

    logger = None

    @logged
    def __init__(self):
        self.logger.debug('')
        QObject.__init__(self)

    # noinspection PyUnresolvedReferences
    @pyqtSlot()
    def run(self):
        socket_UR.connected.connect(self.on_connected)
        socket_UR.disconnected.connect(self.on_disconnected)
        socket_UR.stateChanged.connect(self.on_state_changed)
        socket_UR.error.connect(self.on_error)
        self.connect_to_UR()

    @pyqtSlot(str)
    def write_data(self, msg):
        self.logger.debug(msg)
        socket_UR.write(msg.encode())

    @pyqtSlot()
    def connect_to_UR(self):
        self.logger.info('tentative de connexion à UR sur {}:UR_port'.format(UR_hote))
        while not socket_UR.state() == 3:
            socket_UR.connectToHost(UR_hote, UR_port)
            if socket_UR.waitForConnected(1000):
                self.logger.info('connexion établie')
                self.connected.emit()
            else:
                self.disconnected.emit()

    @pyqtSlot()
    def on_state_changed(self):
        self.logger.debug('statut: {}'.format(STATE_DIC[socket_UR.state()]))

    @pyqtSlot()
    def on_connected(self):
        self.logger.debug('')

    @pyqtSlot()
    def on_disconnected(self):
        self.logger.debug('connexion UR perdue')
        self.connect_to_UR()

    @pyqtSlot()
    def on_error(self):
        if socket_sioc.error() in [1, 5]:
            self.logger.debug(ERROR_DIC[socket_UR.error()])
            return
        self.logger.error(ERROR_DIC[socket_UR.error()])


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
        UR_thread, UR_client = None, None
        server = None

        @logged
        def __init__(self):
            self.logger.debug('')
            QMainWindow.__init__(self)
            self.setupUi(self)
            self.setWindowTitle('Katze Link {}'.format(__version__))
            self.ensurePolished()
            self.show()
            self.start_logger_handler()
            self.start_sioc_client()
            self.start_ws_server()
            self.start_dcs_focus_timer()
            self.start_UR_client()
            # noinspection PyUnresolvedReferences
            self.dcs_focus_button.clicked.connect(self.on_dcs_focus_button_state_clicked)
            self.dcs_focus_timeout.setValidator(QIntValidator(50, 5000))
            self.sioc_address_label.setText("Adresse SIOC: {}:{}".format(sioc_hote, sioc_port))
            # noinspection PyUnresolvedReferences
            self.permit_remote_checkbox.clicked.connect(self.on_permit_remote_clicked)
            self.permit_remote_checkbox.setCheckState(2)
            self.listening_port_label.setText(str(link_port))
            self.UR_ip_label.setText('{}:{}'.format(str(UR_hote), str(UR_port)))

        @pyqtSlot()
        def on_permit_remote_clicked(self):
            global permit_remote_commands
            if self.permit_remote_checkbox.checkState() == 2:
                permit_remote_commands = True
            else:
                permit_remote_commands = False

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

        # noinspection PyUnresolvedReferences
        @pyqtSlot()
        def start_sioc_client(self):
            self.sioc_thread = QThread(self)
            self.sioc_client = SiocClient()
            self.sioc_client.connected.connect(self.on_sioc_connect)
            self.sioc_client.disconnected.connect(self.on_sioc_disconnect)
            self.sioc_client.msg_from_sioc.connect(self.on_sioc_msg)
            self.sioc_client.moveToThread(self.sioc_thread)
            self.sioc_thread.started.connect(self.sioc_client.run)
            self.sioc_thread.start()

        @pyqtSlot()
        def start_UR_client(self):
            self.UR_thread = QThread()
            self.UR_client = URClient()
            self.UR_client.connected.connect(self.on_UR_connect)
            self.UR_client.disconnected.connect(self.on_UR_disconnect)
            self.UR_client.moveToThread(self.UR_thread)
            # noinspection PyUnresolvedReferences
            self.UR_thread.started.connect(self.UR_client.run)
            self.UR_thread.start()

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
        def on_UR_connect(self):
            self.UR_state.setPixmap(QPixmap(':/pics/green_light.png'))

        @pyqtSlot()
        def on_UR_disconnect(self):
            self.UR_state.setPixmap(QPixmap(':/pics/red_light.png'))

        @pyqtSlot()
        def on_sioc_connect(self):
            self.sioc_state_pic.setPixmap(QPixmap(':/pics/green_light.png'))

        @pyqtSlot()
        def on_sioc_disconnect(self):
            self.sioc_state_pic.setPixmap(QPixmap(':/pics/red_light.png'))

        @pyqtSlot(str)
        def on_sioc_msg(self, msglist):
            # self.logger.debug('message SIOC brut: {}'.format(msglist))
            global pit_state
            for msg in msglist.split('\r\n'):
                # self.logger.debug('raw splitted message: {}'.format(msg))
                if msg in ['Arn.Vivo:'] or not msg:
                    continue
                # self.logger.debug('message SIOC: {}'.format(msg))
                formatted_msg = sbr_string.sioc_read(msg)
                dic = {}
                for k in formatted_msg.keys():
                    v = round(formatted_msg[k] * data_dico[k][1], 0)
                    k = data_dico[k][0]
                    dic[k], pit_state[k] = v, v
                self.server.write_data(dumps(dic))

        @pyqtSlot(str)
        def on_pit_msg(self, msg):
            msg = msg.strip('\u0000')
            # self.logger.debug('message Pit: {}'.format(msg))
            # send ACK
            # self.server.write_data(dumps(ack_dico))
            chan = int(msg.split('=')[0])
            if chan == 4:
                msg = msg.split('=')[1]
                self.logger.debug(msg)
                self.UR_client.write_data(msg)
                return
            if chan == 5:
                # self.logger.error('erreur Pit: {}'.format(msg))
                global com_errors
                com_errors += 1
                msg = '5={}'.format(com_errors)
            if chan == 7:
                if self.toggle_dcs_focus():
                    msg = '7=2'
                else:
                    msg = '7=0'
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

        @pyqtSlot()
        def on_client_count_change(self):
            self.local_clients_count.setText(str(self.server.local_clients_count))
            self.remote_clients_count.setText(str(self.server.remote_clients_count))
            if self.server.total_clients_count == 0:
                self.on_ws_listening()
            else:
                self.on_ws_connect()

        @pyqtSlot()
        def on_dcs_focus_button_state_clicked(self):
            self.toggle_dcs_focus()

        @pyqtSlot()
        def toggle_dcs_focus(self):
            if self.dcs_focus_timer.is_running:
                self.dcs_focus_timer.stop()
                self.dcs_focus_timeout.setEnabled(True)
                self.dcs_focus_button.setText('Activer')
                self.dcs_focus_state.setPixmap(QPixmap(':/pics/red_light.png'))
            else:
                if raise_dcs_window(refresh_pid=True):
                    self.dcs_focus_timeout.setEnabled(False)
                    interval = int(self.dcs_focus_timeout.text())
                    if interval < 100:
                        interval = 100
                    self.dcs_focus_button.setText('Désactiver')
                    self.dcs_focus_state.setPixmap(QPixmap(':/pics/green_light.png'))
                    self.dcs_focus_timer.start(interval)
                    return True


def raise_dcs_window(refresh_pid=False):
    global dcs_pid
    if dcs_pid is None or refresh_pid:
        c = wmi.WMI()
        dcs_pid = None
        for process in c.Win32_Process(name='dcs.exe'):
            dcs_pid = process.ProcessId
        if dcs_pid is None:
            logger.warning('le processus DCS.exe n\'a pas été trouvé. Notez que "DCS.exe" n\'existe QUE si vous êtes '
                           'cockpit ou sur l\'interface multijoueur. L\'interface principale de DCS (avec les options, '
                           'l\'éditeur de mission etc...) ne compte pas')
            return
    shell.AppActivate(dcs_pid)
    shell.SendKeys('')
    return True


dcs_pid = None
shell = win32com.client.Dispatch("WScript.Shell")
logger = mkLogger('__main__')
pit_state = {}
whitelist = []
permit_remote_commands = True
data_config = sbr_data.read_config()
data_dico = sbr_data.read_data_dico()
try:
    sioc_hote = data_config["sioc_hote"]
    sioc_port = int(data_config["sioc_port"])
    sioc_plage = int(data_config["sioc_plage"])
    try:
        UR_hote = data_config["ur_hote"]
        UR_port = int(data_config["ur_port"])
    except KeyError:
        UR_hote = data_config["ts_hote"]
        UR_port = int(data_config["ts_port"])
    link_hote = data_config["link_hote"]
    link_port = int(data_config["link_port"])
except KeyError:
    logger.exception('Fichier de \'config_Helo-Link.csv\' corrompu')
    _exit(1)


socket_sioc = QTcpSocket()
socket_UR = QUdpSocket()

qt_app = QApplication(sys.argv)
link_icon = QIcon(':/ico/link.ico')
ui_main = Gui.Main()
ui_main.setWindowIcon(link_icon)
_exit(qt_app.exec())