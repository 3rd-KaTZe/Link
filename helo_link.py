# coding=utf-8
__author__ = 'KaTZe3rd'
__version__ = '5009'
# KaTZ-Link v0.005
# 3rd Wing 120th , KaTZe , Q4-2014

# Le système 0003 fonction pour l'export des données vers KaTZ-Pit
# Système 004, export des données offset vers KaTZ-Pit
# Système 005 envoi vers KaTZ-Pit des données renommées


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


# debugging = True
debugging = False
# ----------------------------------------------------------------------------------------------------------------------
# Données Globales            ############################################################################
#----------------------------------------------------------------------------------------------------------------------
KTZmain = sys.modules['__main__']
#exitFlag=0
ordre = ""
msgSioc = ""
# Dictionnaire des commandes SIOC
Sioc_Dico = {}
# Dictionnaire des commandes transmises
Trans_Dico = {}
# Dictionnaire d'accuse de reception >> KaTZ-Pit
AR_Dico = {'Ordre1': 0, 'Ordre2': 0, 'PingBack': 0}
# Dictionnaire de transcription SIOC <> KaTZ-Pit
Data_Dico = {}
# Dictionnaire des données de configuration
Data_Config = {}
# Erreur de transmission
Com_Errors = 0

ini_lock = threading.Lock()
run_lock = threading.Lock()

# Creation de "KTZmain.Sioc_run", variable flag de connexion SIOC
# Tant que Sioc_run = True, on essaye de se reconnecter ou reconnecter à SIOC
Sioc_run = True

# Creation de "KTZmain.Sioc_alive", variable flag de connexion SIOC active
# Sera utilisé pour relancer une connection SIOC si elle est perdue
Sioc_alive = False

# Creation de "KTZmain.WS_run", variable flag de fonctionnement du serveur WS
# Tant que WS_run = True, on est à l'écoute des connexions WS
WS_run = True

# Creation de "KTZmain.WS_alive", variable flag de connexion WS active
# Sera utilisé pour se replacer en écoute si la connection WS est perdue
WS_alive = False

# Le ping est envoyé au SIOC
# Il revient en rebond sur le Canal #8 toutes les 5 secondes
# Le KaTZ-Pit renvoi un Pong
# Rythme de test du pong (nb de boucles pour tester la réponse de la WS)
# Si pas d'activité après n boucles alors on considère qu'il y a eu deconnection
# Base 10 boucles par secondes, donne 50 boucles entre deux ping
pulse_ws = 100

#----------------------------------------------------------------------------------------------------------------------
#  Paramêtres d'Initialisation ############################################################################
#----------------------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------


# Demarrage de la Websocket
# Reception des ordres du KaTZ-Pit, avec la fonction Cmd, qui récupère le n° d'offset à envoyer à DCS
# Envoi des données récupérées depuis le client SIOC

#----------------------------------------------------------------------------------------------------------------------
#  Serveur Websocket pour les KaTZ-Pits  #################################################################
#----------------------------------------------------------------------------------------------------------------------

# noinspection PyBroadException
def ws_server():
    time.sleep(2.0)
    ini_lock.acquire()
    #print("WS_Server >> ini_lock.acquire")

    # Démarrage du serveur Web-Socket
    print("WS_Server >> Start-up du serveur Web-Socket")
    logger.info("WS_Server >> Start-up du serveur Web-Socket")

    # ouverture de la socket d'écoute
    miaou = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    miaou.bind((link_hote, link_port))
    # 5 connections maxi en attente ... a modifier si plusieurs KaTZ-Pit
    miaou.listen(1)

    # Confirmation d'ouverture de la socket
    print("WS-Server >> Ecoute sur le port {} \n".format(link_port))
    if debugging:
        logger.info("WS-Server >> Ecoute sur le port {} \n".format(link_port))

    ini_lock.release()
    #print("WS_Server >> ini_lock.release\n\n")

    ########################### Boucle primaire d'écoute de connexion à la WS ####################################
    while KTZmain.WS_run:

        print("-- WS-Serveur >> en attente d'un client\n")  # Debug , Log
        # On accept un client
        connexion, adresse_client = miaou.accept()

        s = "WS_Server >> Connection Recu de : " + str(adresse_client)
        print(s)
        if debugging:
            logger.info(s)

        # Hand Shake Websocket
        connexion.send(ws_handshake_00.ws_handshake(connexion.recv(1024)))

        # fin du hand Shake
        print("WS_Server >> Connection Etablie")
        KTZmain.WS_alive = True

        #List des connexions actives pour la fonction select
        miaou_in = [connexion]
        miaou_out = [connexion]

        # Compteur de boucle d'Envoi/Reception, pour envoyer un ping au KaTZ-Pit
        # Si pas de réponse, on assume que la connexion est tombé et on se remet en écoute
        loopnb = 0

        ######################## Boucle secondaire de communication WS #####################################
        while KTZmain.WS_alive:

            run_lock.acquire()  # prise de lock

            # Système de ping-pong ------------------------------------------------------------------------------------
            # Le compteur de boucle est incrémenté
            loopnb += 1

            # Il sera remis à zero s'il y a un message du KaTZ-Pit
            # Si n boucles sans réponse du KaTZ-Pit, il est mort
            # alors on ferme la socket

            # Debug timing des thread in/out
            #top = time.perf_counter()
            #print(top,"-- WS-Serveur >> run_lock.acquire\n")        #Debug Log

            # Module de reception des ordre depuis le KaTZ-Pit ----------------------------------------------
            # On evalue s'il y a des ordre en attente d'être lus
            # Le timeout est fixé à 0.1 seconde
            ready_to_read, ready_to_write, in_error = select.select(miaou_in, miaou_out, miaou_in, 0.05)

            #print("socket ready to read = ", ready_to_read)
            #print("socket ready to write = ", ready_to_write)
            #print("socket in error = ", in_error)

            for _ in ready_to_read:
                #La socket s est prète à être lue
                # noinspection PyBroadException
                try:
                    recv_msg = ws_protocol_00.readFrame(connexion.recv(1024))
                    KTZmain.ordre = recv_msg.strip('\u0000')
                    #print('Ordre transcrit : ',json.dumps(KTZmain.ordre))
                    # La socket est active, on remet à zero le compteur de loop
                    loopnb = 0
                except:
                    print("WS_Server >> erreur reception WebSocket")

            #top = time.perf_counter()       #Debug , Lecture du timecode
            #print(top,"-- WS-Serveur >> fin de reception des ordres / debut transmission data \n")        #Debug Log

            # Module d'envoi des messages au KaTZ-Pit ---------------------------------------------------------

            # Fonctionnement séquentiel avec les lock
            # Si lock release par module Sioc alors il y a un message

            # Conversion Json du message
            trans_msg = json.dumps(KTZmain.Trans_Dico)

            try:
                # Envoi du Message au KaTZ-Pit
                connexion.send(ws_protocol_00.createFrame(trans_msg))

            except:
                print("WS_Server >> erreur envoi WebSocket")

            # Debug, lecture des messages envoyés
            #top = time.perf_counter()
            #print(KTZmain.Trans_Dico)
            #print(top, "WS_Server >> Envoyé au KaTZ-Pit >"+trans_msg,"\n")  #Debug Log

            #remise à zero de la chaine de message
            KTZmain.Trans_Dico = {}

            # print(loopnb)
            # Si nombre de loop sans réponse > pulse_ws, la socket est morte on sort de la boucle
            if loopnb > KTZmain.pulse_ws:
                KTZmain.WS_alive = False

            # Si on a recu un ordre du KaTZ-Pit on envoi un AR, avec remise à zero des chan de communication 1-2-7 ----
            if len(KTZmain.ordre) > 0:

                ar_msg = json.dumps(KTZmain.AR_Dico)

                try:
                    # Envoi de l'Accuse Reception au KaTZ-Pit
                    connexion.send(ws_protocol_00.createFrame(ar_msg))

                except:
                    print("WS_Server >> erreur envoi WebSocket")

            # Debug timing des thread in/out
            #top = time.perf_counter() #Debug , Lecture du timecode
            #print(top,"-- WS-Serveur >> run_lock.release\n\n") #Debug , Log
            run_lock.release()  # libération du lock

            time.sleep(0.1)  # mise en sommeil du thread pour libérer puissance machine au thread Sioc

            ######################## Fin de la boucle WS provoquée par la mort de la socket ###########################

        print("WS_Server >> Liaison avec le KaTZ-Pit Interrompue")
        #print("WS_Server >> Socket Fermée")
        connexion.close()
        # miaou.close()
        #print("WS_Server >> Fin de la boucle WS")


#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------------------
#  Client SIOC #######################################################################################
#----------------------------------------------------------------------------------------------------------------------

# noinspection PyBroadException
def sioc_client():
    ini_lock.acquire()
    #print("Sioc-Thread >> ini_lock.acquire")

    #Création des process client pour Sioc et Cach3
    print("Sioc-Thread >> Démarrage Sioc_Client et Cach3_Client" + "\n")

    ######################## Initialisation  de la connection SIOC #####################################

    #Chargement du Dictionnaire SIOC >> KaTZ-Pit
    KTZmain.Data_Dico = sbr_data.Data_Dico()
    #print(KTZmain.Data_Dico)

    #Création de la Liste de Valeur à Importer de SIOC
    #Liste "data_import" créé à partir du Dictionnaire
    data_import = "Arn.Inicio:"
    for d in KTZmain.Data_Dico:
        #print(d)
        data_import = data_import + str(d) + ":"
        #print(data_import)

    data_import += "\n"
    #print(data_import)

    ########################### Creation de la socket Cach3 #########################################

    print("Cach3_Client : Creation de la connection TS3" + "\n")
    cach3_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    ########################### Boucle primaire de connection à SIOC ####################################

    while KTZmain.Sioc_run is True:

        retry_sioc = True

        # Essai de connection à Sioc , si erreur pause et nouvel essai
        # Modif v3020, la boucle est ignorée si une connection est active
        # Si la connection est perdue, on retente une conneciton
        # Puisque la socket a été fermée lors de la perte de connection

        ### Boucle de tentative de connection -------------------------------------------------------------------------

        while retry_sioc is True:

            try:
                print("Sioc_Client : Tentative de Connection")
                sioc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sioc_socket.connect((sioc_hote, sioc_port))

                # Initialisation des variables à importer
                # Envoi à SIOC de la liste des valeurs échangées
                sioc_socket.sendall(data_import.encode())
                # print ("Sioc-Thread >> Liste des Offset Sioc Ecoutés : \n", data_import)

                # Sioc répond par Arn.Vivo:
                _ = sioc_socket.recv(1024).decode()
                # print (_)

                s = "Sioc_Client : Connection SIOC Etablie" + "\n"
                print(s)
                if debugging:
                    logger.info(s)

                # Modificaion des flags de connection
                retry_sioc = False
                KTZmain.Sioc_alive = True

            except socket.error:
                print("Sioc_Client : Connection SIOC Echouée\n")
                print("Sioc_Client : SIOC est il bien démarré ?\n")
                print("Sioc_Client : Vérifier les paramêtres de connection à SIOC")
                print("Sioc_Client : IP = " + str(sioc_hote) + "   :   Port = " + str(sioc_port) + "\n")
                print("Sioc_Client : Nouvel Essai dans 15 secondes" + "\n")
                time.sleep(15.0)

                ### Fin de Boucle de tentative de connection ----------------------------------------------------------

        # Flag une connection SIOC est active
        # On passe la main à la WS
        ini_lock.release()

        time.sleep(2.0)  # Mise en sommeil, puissance libérée pour WS thread

        ######################## Boucle secondaire de communication avec SIOC ##############################

        while KTZmain.Sioc_alive:

            ###################### 1- Module d'envoi des messages  ------------------------------

            run_lock.acquire()

            # Debug timing des thread in/out
            # top = time.perf_counter()
            # print(top,"-- Sioc-Thread >> run_lock.acquire\n")

            if len(KTZmain.ordre) > 0:

                # Lecture du message pour choisir entre :
                # ordre vers SIOC
                # changement de chan TS

                # print(KTZmain.ordre)
                chan = KTZmain.ordre.split("=")

                # print(chan[0])
                # print(chan[1])

                # Si le chan de l'ordre = 4, c'est un ordre TS, on envoi la commande ) Cach3
                if int(chan[0]) == 4:
                    switch = chan[1]
                    cach3_socket.sendto(switch.encode(), (cach3_hote, cach3_port))
                # On envoie le chan TS sur SIOC canal 4

                # Rq , si erreur dans la fonction de lecture des ordres
                # le canal 6 recoit la valeur 1 , on incrémente un compteur d'erreur
                # et on l'envoi à SIOC
                if int(chan[0]) == 5:
                    KTZmain.Com_Errors += 1
                    KTZmain.ordre = "5=" + str(KTZmain.Com_Errors)

                #Envoi de données à SIOC
                # Type Arn.Resp:ID=Val:\n , exemple Arn.Resp:1=71:\n
                msg_cmd = "Arn.Resp:" + KTZmain.ordre + ":\n"

                try:
                    sioc_socket.sendall(msg_cmd.encode())

                except:
                    print("SIOC Loop >> Erreur de transmission avec SIOC")
                    if debugging:
                        logger.error("SIOC Loop >> Erreur de transmission avec SIOC")
                    print("SIOC Loop >> Vérifier que SIOC est toujours en marche")
                    KTZmain.Sioc_alive = False

                # Debug Print
                print("Envoyé à SIOC >" + msg_cmd)
                # logger.info("Envoyé à SIOC >"+msg_cmd)
                # print ("Retour de SIOC >"+reponse0)

                # Remise a zero de la chaine d'ordres
                KTZmain.ordre = ""

            # Debug timing des thread in/out
            # top = time.perf_counter()
            # print(top,"-- Sioc-Thread >> fin trans Sioc, début Réception \n")

            ###################### 2- Module de reception des messages SIOC ------------------------------

            # Stabilité connection : envoi d'un pulseur à la seconde
            _now = datetime.datetime.now()
            pulse = _now.hour * 3600 + _now.minute * 60 + _now.second
            pulse_msg = "Arn.Resp:9=" + str(pulse) + ":\n"

            # Le pulseur est envoyé sur le canal 9 à SIOC, et revient
            # Il est alors revoyé au KaTZ-Pit, comme ping sur le canal 8 (toutes les 5 secondes)
            # Le KaTZ-Pit répond par un pong sur le canal 7
            # Ca assure une activité montante depuis le KaTZ-Pit
            # Si pas d'activité de réception dans la boucle WS, alors on suppose que le KaTZ_Pit est deconnecté

            try:
                sioc_socket.sendall(pulse_msg.encode())

            except:
                # Erreur de communication avec SIOC
                # On averti, on sort de la bouble et on réunitialise la socket pour reconnection
                print("SIOC Loop >> Erreur de transmission avec SIOC")
                if debugging:
                    logger.error("SIOC Loop >> Erreur de transmission avec SIOC")
                print("SIOC Loop >> Vérifier que SIOC est toujours en marche\n")
                KTZmain.Sioc_alive = False

            # Message recu de SIOC
            try:
                KTZmain.msgSioc = sioc_socket.recv(4096).decode()
            except:
                # Erreur dans le message recu
                # Log du problème, incrémentation du canal d'erreur (8)
                # La boucle n'est pas interompue
                # top = time.perf_counter()
                print("SIOC Loop >>  Erreur Reception Message\n")
                if debugging:
                    logger.error("SIOC Loop >>  Erreur Reception Message\n")
                KTZmain.msgSioc = "5=1"

            # Debug Reception de SIOC
            if debugging:
                top = time.perf_counter()
                s = " -- Sioc-Thread >> Recu de Sioc : " + str(KTZmain.msgSioc)
                print(top, s)
                logger.info(s)

            # Transcription du message recu en dictionnaire n°=Valeur
            # A l'aide de la fonction SIOC_Read du module str_function
            try:
                KTZmain.Sioc_Dico = sbr_string.Sioc_Read(KTZmain.msgSioc)
            except IndexError:
                logger.error("fichier SSI périmé ?") # TODO: Katze regarde une fois
            # Donnée "Sioc_Dico" va être "traduite" et envoyée vers KaTZ-Pit
            # KTZmain.Trans_Dico = KTZmain.Sioc_Dico

            # Test de conversion direct
            for cle in KTZmain.Sioc_Dico:
                # Le message est modifié
                # La clé devient le label
                # La valeur est multipliée par le gain
                # KTZmain.Trans_Dico[KTZmain.Data_Dico[cle][0]]=int(KTZmain.Sioc_Dico[cle]*KTZmain.Data_Dico[cle][1])
                KTZmain.Trans_Dico[KTZmain.Data_Dico[cle][0]] = round(
                    (KTZmain.Sioc_Dico[cle] * KTZmain.Data_Dico[cle][1]), 0)

            #remise à zero de la chaine de message
            KTZmain.Sioc_Dico = {}

            # Fin de l'itération ecoute/envoi de SIOC
            # Debug timing des thread in/out
            #top = time.perf_counter()
            #print(top,"-- Sioc-Thread >> run_lock.release\n\n")
            run_lock.release()

            time.sleep(0.1)  # mise en sommeil du thread pour libérer puissance machine au thread WS

            ######################## Fin de la Boucle secondaire de communication avec SIOC ###########################

        print("SIOC Loop >> Fin de communication avec SIOC")
        print("SIOC Loop >> Fermeture de la socket")
        if debugging:
            logger.error("SIOC Loop >>  Fermeture de la socket\n")
        sioc_socket.close()

        #  KTZmain.Sioc_run est toujours à "True", pourra être modifié si besoin de stopper cette boucle
        print("SIOC Loop >> Tentative de reconnection\n")
        ini_lock.acquire()

#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------


class DummyLogger():
    def __init__(self):
        pass
        self.info = self.debug
        self.warning = self.debug
        self.error = self.debug

    def debug(self, *args):
        pass


# Main Programme
if __name__ == "__main__":
    if debugging:
        #--------------------------------------------------------------------------------------------------------------
        # Creation du Logger          #############################################################################
        #--------------------------------------------------------------------------------------------------------------

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Recuperer le repertoire current avec so.getcwd()
        currentrep = os.getcwd()
        # On change de répertoire, en passant sur le sous répertoire log
        if not os.path.exists('log'):
            os.mkdir('log')
        os.chdir("log")
        #Format fichier log avec date+heure du jour
        now = datetime.datetime.now()
        logfilenom = now.strftime("Helo-Link_%Y%m%d-%H%M%S_log.log")
        fh = logging.FileHandler(logfilenom)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        # Retour au répertoire du KaTZ-Link
        os.chdir(currentrep)
    else:
        logger = DummyLogger()

    # Donnees de connection SIOC
    Data_Config = sbr_data.Data_Config()

    #Donnée "localhost" ou "192.168.0.10"
    # Les données sont lues dans le fichier "config_Helo-Link.csv" par la subroutine "sbr_data.py"
    # Données IP et Port
    sioc_hote = Data_Config["sioc_hote"]
    sioc_port = int(Data_Config["sioc_port"])

    # Décalage de la plage des valeurs SIOC
    # Defaut = 0 , mais les peuvent être décalées, dans siocConfig.lua
    # Faire correspondre la valeur du décalage.
    sioc_plage = int(Data_Config["sioc_plage"])

    msg = "Configuration du Helo-Link : \n\n" + "Sioc IP = " + str(sioc_hote) + " ;  Sioc Port = " + str(
        sioc_port) + " ;  Décalage des offsets = " + str(sioc_plage)
    print(msg)
    if debugging:
        logger.info(msg)

    # IP et Port du serveur Python
    link_hote = Data_Config["link_hote"]
    link_port = int(Data_Config["link_port"])
    msg1 = "WS IP = " + str(link_hote) + " ;  WS Port = " + str(link_port)
    print(msg1)
    if debugging:
        logger.info(msg1)

    # IP et Port du serveur UDP Plugin Cach3 sur TS
    cach3_hote = Data_Config["ts_hote"]
    cach3_port = int(Data_Config["ts_port"])
    msg2 = "Cach3 IP = " + str(cach3_hote) + " ;  Cach3 Port = " + str(cach3_port) + "\n"
    print(msg2)
    if debugging:
        logger.info(msg2)

    KtzWs_1 = threading.Thread(None, ws_server, "WS_Server_Thread", (), {})
    KtzSioc_2 = threading.Thread(None, sioc_client, "Sioc_Server_Thread", (), {})
    #KtzData_3 = threading.Thread(None, Data_Process, "Thread3", (), {})

    KtzWs_1.start()
    KtzSioc_2.start()
    #KtzData_3.start()

    #TODO: bug à la fermture, peut-être voir avec thread.join()