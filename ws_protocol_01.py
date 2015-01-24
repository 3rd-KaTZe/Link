# Attention Python 3.4
# bytes/string spécifique à la version 3
# socket.send doit travailler sur des bytes
# Protocole d'échange WebSocket, suivant norme RFC 6455
# R.Perrin ; 3rd Wing KaTZe ; Sept 2014

"""
Parses a WebSocket frame.
"""
class Frame:
    _payloadLen = 0
    _payloadStart = 2
    _maskStart = 2
    _maskData = []

    fin = False
    continues = False
    utf8 = False
    binary = False
    terminate = False
    ping = False
    pong = False
    mask = False


    def parse (self, data):
        self.parseFirstByte(data[0])
        self.parseSecondByte(data[1])

        if self._payloadLen == 126: #16 bit int length
            self._payloadLen = (data[2] << 8) + data[3]    
            self._maskStart += 2
            self._payloadStart += 2

        if self._payloadLen == 127: #64 bit int length
            self._payloadLen = (data[2] << 56) + (data[3] << 48) + (data[4] <<40) + (data[5] << 32) + (data[6] << 24) + (data[7] << 16) + (data[8] << 8) + data[9]
            self._maskStart += 8
            self._payloadStart += 8

        if True == self.mask:
            self._maskData = [
                data[self._maskStart], 
                data[self._maskStart + 1], 
                data[self._maskStart + 2], 
                data[self._maskStart + 3]
            ]

    def parseFirstByte (self, byte):
        self.fin = byte >= 128
        opcode = byte
        if True == self.fin:
            opcode -= 128
        
        self.continues = opcode == 0
        self.utf8 = opcode == 1
        self.binary = opcode == 2
        self.terminate = opcode == 8
        self.ping = opcode == 9
        self.pong = opcode == 10   

    def parseSecondByte (self, byte):
        self.mask = byte >= 128
        self._payloadLen = byte
            
        if True == self.mask:
            self._payloadStart += 4
            self._payloadLen -= 128

    def getPayload (self, data):
        if True == self.mask:
            res = bytearray(self._payloadLen)
            i = 0
            for char in data[self._payloadStart:]:
                res.append(char^self._maskData[i%4])
                i += 1

            return res

        return data[self._payloadStart:]

    def __str__ (self):
        lenthsFrm = " maskStart: {}\n payloadStart: {}\n payloadLen: {}\n" 
        lenths = lenthsFrm.format(self._maskStart, self._payloadStart, self._payloadLen)

        flagsFrm = " fin: {}\n continues: {}\n utf8: {}\n binary: {}\n terminate: {}\n ping: {}\n pong: {}\n mask: {}\n" 
        flags = flagsFrm.format(self.fin, self.continues, self.utf8, self.binary, self.terminate, self.ping, self.pong, self.mask)

        return "Frame:\n" + lenths + flags
    
         
"""
Unmaks a websocket frame using Frame.
"""
def readFrame (data):
    print(data)
    frame = Frame()
    frame.parse(data)

    
    try:
        return frame.getPayload(data).decode("utf-8")
    except :
        print(data)
        print("erreur decoding, envoi message 5=1")
        com_error = "5=1"
        return com_error


"""
Should create a frame containing the given text msg.

"""
def createFrame (text):

    # Le bit 0 est toujours à 129 ou 0x81

    # payload < 126
    if (len(text) <= 125):

        # print("Message Court")
        ret = bytearray(2)
        ret[0] = 129
        ret[1] = len(text)
        
        for byte in text.encode("utf-8"):
            ret.append(byte)


    # 16 bits payload
    elif (len(text) > 125 and len(text) <= 65535):

        #print("7+16 Bit Payload")
        ret = bytearray(2)
        ret[0] = 129
        ret[1] = 126
        ret.append((len(text) >> 8) & 255)
        ret.append((len(text)) & 255)
        
        for byte in text.encode("utf-8"):
            ret.append(byte)    

    # 64 bits payload
    else:

        #print("7+64 Bit Payload")
        ret = bytearray(2)
        ret[0] = 129
        ret[1] = 127
        ret.append((len(text) >> 56) & 255)
        ret.append((len(text) >> 48) & 255)
        ret.append((len(text) >> 40) & 255)
        ret.append((len(text) >> 32) & 255)
        ret.append((len(text) >> 24) & 255)
        ret.append((len(text) >> 16) & 255)
        ret.append((len(text) >> 8) & 255)
        ret.append((len(text)) & 255)
        
        for byte in text.encode("utf-8"):
            ret.append(byte)    
       
     
    #print("Module CreateFrame : ret ",ret)

    return ret

    

