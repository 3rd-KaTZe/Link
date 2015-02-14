# KaTZ-Link v0.0
# 3rd Wing 120th , KaTZe , Q4-2014
# Transcription des données SIOC en données KaTZ-Pit

# On va transformer la réponse de SIOC en un dictionnaire KP={}
# miaou
#
import json
# Module Operating System
import os
import csv

import math


def read_data_dico():

    # Recuperer le repertoire current avec so.getcwd()
    currentrep = os.getcwd()
    #print (currentrep)



    DD={}
    DicoFichier = open("z_Data_Dico.csv", "r")
    #print("sbr_data >> Chargement de DataDico\n")

    while 1:
        ligne = DicoFichier.readline()
        if not ligne:
            break

        dicodata = ligne.strip('"\n')
        #print(dicodata)

        elementS = dicodata.split(",")
        # Les Données sont lus sous forme, de trois éléments
        # La Première est l'Offset Sioc
        # La deuxième est l'étiquette utilisée par le KaTZ-Pit
        # La troisième est le gain (multiplicateur pour obtenir la vrai valeur

        #On renvoi un Dictionnaire comportant comme clé l'OffSet de SIOC
        # Les deux autres éléments (étiquette,Gain) sont envoyés comme tupple
        DD[int(elementS[0])]=(elementS[1],float(elementS[2]))

    print (DD)
    return DD

def read_config():
    ret = {}
    with open("config_Helo-Link.csv") as f:
        lines = f.readlines()
    for l in lines:
        x, y = l.strip('"\n').split(',')
        ret[x] = y
    return ret



    
    





    
    


