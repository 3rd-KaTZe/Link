# KaTZ-Link v0.0
# 3rd Wing 120th , KaTZe , Q4-2014
# Nettoyage des lignes de données ex-SIOC

# On va transformer la réponse de SIOC en un dictionnaire ST={}
# En fonction du volume d'information la syntaxe peut varier.
# On utilise json, pour identifier les caractères invisible \r, \n
#
# message test =  "Arn.Resp:23=2470:\r\nArn.Resp:26=112:\r\nArn.Resp:10=66:\r\n"
# message test = "Arn.Resp:23=2470:26=112:10=66:\r\n"
# message test = "Arn.Resp:23=2470:\r\n"
#message test = "Arn.Resp:420=10800:206=0:211=0:1000=728620:1002=607643:1004=258202:1005=102332:\r\nArn.Resp:1005=958676:\r\nArn.Resp:1000=505491:\r\n"
# meow
#
import json


def Sioc_Read(Sioc_Data):
    #print ("Sioc_Read_function : Recu de Main > ",json.dumps(Sioc_Data),"\n")

    #Test si message tronqué, alors envoi erreur canal 5
    if len(Sioc_Data)<3:
        Sioc_Data="Arn.Resp:5=1:\r\n"

    ST={}

    # Extraction des commandes individuelles
    # On enlève le Arn.Resp présent dans tous les formats
    data_ssArn = Sioc_Data.replace("Arn.Resp","")
    # On enlève les retours ligne r et n , et le : initial
    data_ssrn = data_ssArn.replace(":\r\n","").lstrip(":")
    #print("Sans ArnResp > ",data_ssArn)
    #print("Sans ret r et n > ",data_ssrn)

    #decoupage , en une liste de commande "canal:valeur"
    dataS1 = data_ssrn.split(":")
    #print("dataS1 = ",dataS1)

    #stockage dans le dictionnaire
    for elmt in dataS1:
        elementS = elmt.split("=")
        ST[int(elementS[0])]=int(elementS[1])

    #print(ST)

    # La fonction renvoie le dictionnaire
    return ST

    


# Debug de fonction avec les différentes formes d'input
#Sioc_Data = "Arn.Resp:23=2470:\r\nArn.Resp:26=112:\r\nArn.Resp:10=66:\r\n"        
#Sioc_Data = "Arn.Resp:23=2470:26=112:10=66:\r\n"        
#Sioc_Data = "Arn.Resp:23=2470:\r\n"
#Sioc_Data = "Arn.Resp:420=10800:206=0:211=0:1000=728620:1002=607643:1004=258202:1005=102332:\r\nArn.Resp:1005=958676:\r\nArn.Resp:1000=505491:\r\n"
#print(Sioc_Read(Sioc_Data))
#print(json.dumps(Sioc_Read(Sioc_Data)))
