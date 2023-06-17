import datetime
import zlib
from Crypto.Hash import SHA1
from Crypto.PublicKey import RSA, DSA
from Crypto.Signature import pss, DSS
from Crypto.Cipher import CAST
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP
import base64
from tkinter import *
from KeyGenImplementation import dictionaryOfPrivateKeyRings, dictionaryOfPublicKeyRings
from ElGamalImpl import PrivateKey, PublicKey, encryptElGamal, decryptElGamal

################################################# SENDING A MESSAGE ########################################################
#Enkripcija Sesijskog kljuca
def EnctryptSestionKey(sestionKey, publicKey):

    if(publicKey.algorithm == "Rsa"):
        key = RSA.import_key(publicKey.publicKey)
        cipher = PKCS1_OAEP.new(key)
        ciphertext = cipher.encrypt(sestionKey)
        return ciphertext

    if(publicKey.algorithm == "ElGamal"):
        key = PublicKey.import_key(publicKey.publicKey)

        en_msg = encryptElGamal(repr(sestionKey), key)
        return en_msg


#Enkripcija Simetricnim algoritmom
def EncryptionSymm(symmAlgoritham, fullMessage):
    sestionKey = get_random_bytes(16)

    if(symmAlgoritham == 1):
        cipher = AES.new(sestionKey, AES.MODE_CFB)
        ciphertext = cipher.encrypt(fullMessage)
        return sestionKey, cipher.iv + b'BLOKIC' + ciphertext

    if(symmAlgoritham == 2):
        cipher = CAST.new(sestionKey, CAST.MODE_CFB)
        ciphertext = cipher.encrypt(fullMessage)
        return sestionKey, cipher.iv + b'BLOKIC' + ciphertext


#Kompresija
def Compression(fullMessage):
    return zlib.compress(fullMessage)


#Potpis
def Signature(privateKey, fullMessage):

    if privateKey.algorithm == "Rsa":
        hashedMessage = SHA1.new(fullMessage)
        key = RSA.import_key(privateKey.EcryptedPrivateKey, passphrase= privateKey.hashedPassphrade)
        signature = pss.new(key).sign(hashedMessage)
        return signature

    if privateKey.algorithm == "Dsa":
        hashedMessage = SHA1.new(fullMessage)
        key = DSA.import_key(privateKey.EcryptedPrivateKey, passphrase= privateKey.hashedPassphrade)
        signer = DSS.new(key, 'fips-186-3')
        signature = signer.sign(hashedMessage)
        return signature


def SendMessage(privateKey, publicKey, senderName, receiverName,symmAlgoritham, message, signature, security, compression, conversion, fileName):
    timestamp = str(datetime.datetime.now()).encode('utf-8')
    fileName = fileName.encode('utf-8')
    message = message.encode('utf-8')
    fullMessage = fileName + b'BLOKICPrvi' + timestamp + b'BLOKICPrvi' + message #prvi goli oblik poruke

    #Potpis
    if signature == 1:
        sign = Signature(privateKey, fullMessage)
        fullMessage = str(datetime.datetime.now()).encode('utf-8') + b'BLOKICDrugi' + privateKey.publicKeyId + b'BLOKICDrugi' + sign[0:2] + b'BLOKICDrugi' + sign + b'BLOKICDrugi' + fullMessage

    #Kompresija
    if compression == 1:
        fullMessage = Compression(fullMessage)

    #Enkripcija
    if security == 1:
        sesionKey, encryption = EncryptionSymm(symmAlgoritham, fullMessage)
        encryptSestionKey = EnctryptSestionKey(sesionKey, publicKey)
        fullMessage = publicKey.publicKeyId + b'BLOKICTreci' + encryptSestionKey + b'BLOKICTreci' + encryption# ovde se nalazi 'iv' + 'BLOKIC' + 'cipher'

    #Konverzija
    if conversion == 1:
        fullMessage = base64.b64encode(fullMessage)


    fullMessage = str(symmAlgoritham).encode('utf-8') + b'rasa21' + str(conversion).encode('utf-8') + b'rasa21' + str(security).encode('utf-8') + b'rasa21'\
                  + str(compression).encode('utf-8') + b'rasa21' + str(signature).encode('utf-8') + b'rasa21' + fullMessage

    with open(fileName,"wb") as file:
        file.write(fullMessage)







################################################# RECEIVE A MESSAGE ########################################################
#Dekripcija sesijskog kljuca
def DecryptSessionKey(privateKey, encryptSessionKey):

    if privateKey.algorithm == "Rsa":
        key = RSA.import_key(privateKey.EcryptedPrivateKey, passphrase=privateKey.hashedPassphrade)
        cipher = PKCS1_OAEP.new(key)
        sestionKey = cipher.decrypt(encryptSessionKey)
        return sestionKey

    if privateKey.algorithm == "ElGamal":
        key = PrivateKey.import_key(privateKey.hashedPassphrade, privateKey.EcryptedPrivateKey)
        sesionKey = decryptElGamal(encryptSessionKey, key)
        return eval(sesionKey)


#Dekripcija simetricnim algoritmom
def DecryptionSymm(symmAlgoritham, cipher, iv ,sessionKey):
    if symmAlgoritham == b'1':
        decipher = AES.new(sessionKey, AES.MODE_CFB, iv=iv)
        decrypted_text = decipher.decrypt(cipher)
        return decrypted_text

    if symmAlgoritham == b'2':
        decipher = CAST.new(sessionKey, CAST.MODE_CFB, iv=iv)
        decrypted_text = decipher.decrypt(cipher)
        return decrypted_text


#Dekompresija
def Decompression(fullMessage):
    return zlib.decompress(fullMessage)


#Verify potpisa
def Verify(fullMessage, sign, publicKey):

    if publicKey.algorithm == "Rsa":
        hashedMessage = SHA1.new(fullMessage)
        key = RSA.import_key(publicKey.publicKey)
        verifier = pss.new(key)
        try:
            verifier.verify(hashedMessage, sign)
            print("The signature is authentic.")
            return 1

        except (ValueError, TypeError):
            print("The signature is not authentic.")
            return 0

    if publicKey.algorithm == "Dsa":
        hashedMessage = SHA1.new(fullMessage)
        key = DSA.import_key(publicKey.publicKey)
        verifier = DSS.new(key, 'fips-186-3')
        try:
            verifier.verify(hashedMessage, sign)
            print("The message is authentic.")
            return 1
        except ValueError:
            print("The message is not authentic.")
            return 0


def ReceiveMessage(name, fileName):
    global receiveWindow
    receiveWindow = Toplevel()
    receiveWindow.title("Receive message")

    with open(fileName,"rb") as file:
        fullMessage = file.read()

    symmAlgoritham, conversion, security, compression, signature, fullMessage = fullMessage.split(b'rasa21')


    if conversion == b'1':
        fullMessage = base64.b64decode(fullMessage)


    if security == b'1':
        publickeyId, encryptSessionKey, encryption = fullMessage.split(b'BLOKICTreci')

        iv,cipher = encryption.split(b'BLOKIC')

        privateKey = b''
        for keyRing in dictionaryOfPrivateKeyRings[name]:
            if keyRing.publicKeyId == publickeyId:
                privateKey = keyRing
                privateKey.__str__()

        if(privateKey == b''):
            Greska("Private key not found")
            return

        try:
            sessionKey = DecryptSessionKey(privateKey, encryptSessionKey)
            fullMessage = DecryptionSymm(symmAlgoritham, cipher, iv, sessionKey)
        except (ValueError):
            Greska("Decryption is not successful")
            return


    if compression == b'1':
        try:
            fullMessage = Decompression(fullMessage)
        except(zlib.error):
            Greska("Compress is not valid")
            return


    if signature == b'1':
        timestamp, publickeyId, octets, sign, fullMessage = fullMessage.split(b'BLOKICDrugi')

        publicKey = b''
        for keyRing in dictionaryOfPublicKeyRings[name]:
            if keyRing.publicKeyId == publickeyId:
                publicKey = keyRing

        if (publicKey == b''):
            Greska("Public key not found")
            return

        if Verify(fullMessage, sign, publicKey):
            labelVerify = Label(receiveWindow, text="The signature is authentic.", padx = 40, pady = 15)
            labelVerify.grid(row=0, column=0, padx=(20, 20))
        else:
            labelVerify = Label(receiveWindow, text="The signature is not - authentic.", padx=40, pady=15)
            labelVerify.grid(row=0, column=0, padx=(20, 20))

    filename, timestamp, message = fullMessage.split(b'BLOKICPrvi')

    labelMessage = Label(receiveWindow, text="Message: " + message.decode('utf-8'), padx = 80, pady = 15)
    labelMessage.grid(row=1, column=0, padx=(20, 20))


def Greska(string):
    receiveWindow.destroy()

    errorWindow = Toplevel()
    errorWindow.title("Receive message")

    labelMessage = Label(errorWindow, text=string, padx=80, pady=15)
    labelMessage.grid(row=1, column=0, padx=(20, 20))