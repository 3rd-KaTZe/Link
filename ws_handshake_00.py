# Attention Python 3.4
# bytes/string spécifique à la version 3
# socket.send doit travailler sur des bytes
# Protocol de HandShake WebSocket
# R.Perrin ; 3rd Wing KaTZe ; Sept 2014

import re
from base64 import b64encode
from hashlib import sha1



def ws_handshake (hs_in):

    websocket_answer = (
        'HTTP/1.1 101 Switching Protocols',
        'Upgrade: websocket',
        'Connection: Upgrade',
        'Sec-WebSocket-Accept: {key}\r\n\r\n',
    )

    GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


    # Hand Shake Websocket

    handshake_in_str = hs_in.decode()
    #Debug
    #print("Handshake In : \n",handshake_in_str)

    #On recherche la clé dans le HandShake 
    key = (re.search('Sec-WebSocket-Key:\s+(.*?)[\n\r]+', handshake_in_str)
        .groups()[0]
        .strip())

    #Debug
    #print("key = ",key)
    #test "dGhlIHNhbXBsZSBub25jZQ==" doit donner "s3pPLMBiTxaQ9kYGzzhZRbK+xOo="
    #key = "dGhlIHNhbXBsZSBub25jZQ=="

    # La clé de réponse = clé de HS + GUID
    response_key_str = key + GUID
    #print (response_key_str)

    # On encode en byte avant encodage64bits de la clé
    response_key_byte = response_key_str.encode('utf-8')
    response_key_64 = b64encode(sha1(response_key_byte).digest())

    # Clé codée en Str
    response_key = response_key_64.decode()

    #Recomposition du message de Réponse Handshake (str)
    response_str = '\r\n'.join(websocket_answer).format(key=response_key)
    #print ("Réponse au HandShake :\n",response_str)

    # Encodage byte de la réponse ... quel bordel
    response_bytes = response_str.encode('utf-8')
    return response_bytes

    # fin du hand Shake
    ##
    ##
    ##


