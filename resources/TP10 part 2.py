from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from Crypto.Cipher import AES
from Crypto.Util import Padding
import binascii


NwkSkey = "026e26a58c4f234c3b9924f86dcad3a9"
AppSkey = "dd0a32bf8b4082bc4a0017e99c1517d6"

#la clé à utiliser est ici AppSKey, car FPort = 1


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
#print(binascii.hexlify(payload_decrypt))

payload_decrypt.hex()

#A1 = bytes.fromhex("01") + bytes.fromhex("00") * 4 + bytes.fromhex("00") + bin(DevAddr) +
