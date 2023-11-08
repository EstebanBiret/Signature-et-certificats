import base64
import struct


phyPayload = "QCZLjgGC4woFAwHcYJuX0c/5zJVZCw6brV8="
binData = base64.b64decode(phyPayload)
# print(binData) # on a bien du binaire !

MHDR = binData[0]  # le premier octet
Mtype = MHDR >> 5  # les 3 premiers bits

MACPayload = binData[1:-4]  # tout sauf MIC et MHDR

# print(MACPayload.hex())

# FHDR_partial = MACPayload[:8]

# DevAddr, FCtrl, Fcnt, Fopts0 = struct.unpack("<IBHB", FHDR_partial)
# on change la convention I = 4 octets, B = 1 octet, H = 2 octets

DevAddr = int.from_bytes(MACPayload[:4], byteorder='little').to_bytes(4, byteorder='big').hex()
print("DevAddr : " + DevAddr)

FCtrl = bin(MACPayload[4])  # 2 est la longueur de Fopts
print("FCtrl : " + FCtrl[2:])

FCnt = int.from_bytes(MACPayload[5:7], byteorder='little').to_bytes(2, byteorder='big').hex()
print("FCnt : " + FCnt)

FOptsO = int.from_bytes(MACPayload[7:8], byteorder='little').to_bytes(1, byteorder='big').hex()
print("FOptsO : " + FOptsO)

FRMPayload = MACPayload[10:]
print("FRMPayload : " + FRMPayload.hex().upper())


from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from Crypto.Cipher import AES
from Crypto.Util import Padding
import binascii


NwkSkey = "026e26a58c4f234c3b9924f86dcad3a9"
AppSkey = "dd0a32bf8b4082bc4a0017e99c1517d6"

# la clé à utiliser est ici AppSKey, car FPort = 1


# Convertir la clé AppSkey de la chaîne de caractères à la forme binaire
key_bin = binascii.unhexlify(AppSkey)

if len(FRMPayload) % 2 == 1:
    FRMPayload = '0' + FRMPayload

# Convertir la payload de la chaîne de caractères à la forme binaire
payload_bin = binascii.unhexlify(FRMPayload)

# Définir le mode de chiffrement AES-128-CBC avec la clé AppSkey
cipher = AES.new(key_bin, AES.MODE_ECB, b"\x00" * 16)

payload_pad_bin = Padding.pad(payload_bin, 16)

# Déchiffrer la payload avec la clé AppSkey
payload_decrypt = cipher.decrypt(payload_pad_bin)

# Afficher la payload déchiffrée (en hexadécimal)
# print(binascii.hexlify(payload_decrypt))

payload_decrypt.hex()

# A1 = bytes.fromhex("01") + bytes.fromhex("00") * 4 + bytes.fromhex("00") + bin(DevAddr) +
