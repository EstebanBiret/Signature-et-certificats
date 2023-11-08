import base64
import struct


phyPayload = "QCZLjgGC4woFAwHcYJuX0c/5zJVZCw6brV8="
binData = base64.b64decode(phyPayload)
#print(binData) # on a bien du binaire !

MHDR = binData[0] #le premier octet
Mtype = MHDR >> 5 #les 3 premiers bits

MACPayload = binData[1:-4] #tout sauf MIC et MHDR

#print(MACPayload.hex())

#FHDR_partial = MACPayload[:8]

#DevAddr, FCtrl, Fcnt, Fopts0 = struct.unpack("<IBHB", FHDR_partial) #on change la convention I = 4 octets, B = 1 octet, H = 2 octets

DevAddr = int.from_bytes(MACPayload[:4], byteorder='little').to_bytes(4, byteorder='big').hex()
print("DevAddr : " + DevAddr)

FCtrl = bin(MACPayload[4]) # 2 est la longueur de Fopts
print("FCtrl : " + FCtrl[2:])

FCnt = int.from_bytes(MACPayload[5:7], byteorder='little').to_bytes(2, byteorder='big').hex()
print("FCnt : " + FCnt)

FOptsO = int.from_bytes(MACPayload[7:8], byteorder='little').to_bytes(1, byteorder='big').hex()
print("FOptsO : " + FOptsO)

FRMPayload = MACPayload[10:]
print ("FRMPayload : " + FRMPayload.hex().upper()