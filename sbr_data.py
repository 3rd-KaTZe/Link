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



    ret={}
    with open("z_Data_Dico.csv") as f:
        lines = f.readlines()
    for l in lines:
        x = l.strip('"\n').split(',')
        ret[int(x[0])] = (x[1], float(x[2]))
    return ret
    #print("sbr_data >> Chargement de DataDico\n")

    # while 1:
    #     line = DicoFichier.readline()
    #     if not line:
    #         break
    #     dicodata = line.strip('"\n')
    #     e = dicodata.split(",")
    #     data_dico[int(e[0])]=(e[1],float(e[2]))
    #
    # # print (DD)
    # return data_dico

def read_config():
    ret = {}
    with open("config_Helo-Link.csv") as f:
        lines = f.readlines()
    for l in lines:
        x, y = l.strip('"\n').split(',')
        ret[x] = y
    return ret



    
    





    
    


