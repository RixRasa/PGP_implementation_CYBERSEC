import hashlib
from Crypto.PublicKey import RSA
from Crypto.PublicKey import DSA
from Hashing_and_Truncating import *
from ElGamalImpl import *


class PrivateKeyRing:
    def __init__(self, email, name, password, algorithm, publicKey, privateKey):
        self.userId = email + name
        self.hashedPassphrade = password
        self.algorithm = algorithm
        self.EcryptedPrivateKey = privateKey
        self.publicKey = publicKey
        self.publicKeyId = publicKey[-8:]


    def export1(self, filename):
        print()

    def import1(self, filename):
        print()

#dictionaryOfPrivateKeyRings = {"ilija@gmail.comilija":[PrivateKeyRing("ilija@gmail.com","Ilija","be77e3d34969ee11d2789f625efac759","Rsa","123","***")
#                                       ,PrivateKeyRing("lizard123400@gmail.com","Ilija","be77e3d34969ee11d2789f625efac759","Rsa","456","***")]}
dictionaryOfPrivateKeyRings = {}
dictionaryOfPrublicKeyRings = {}

class PublicKeyRing:
    def __init__(self, userId, algorithm, publicKey):
        self.userId = userId
        self.algorithm = algorithm
        self.publicKey = publicKey
        self.publicKeyId = publicKey[-8:]



def GeneratingKey(name, email, password, algorithm):
    if(algorithm == 1):# RSA
        GenerateRsaKey(name, email, password)
    if(algorithm == 2):# ElGamal & DSA
        GenerateDsaKey(name, email, password)
        GenerateElGamalKey(name, email, password)



def GenerateRsaKey(name, email, password):
    key = RSA.generate(2048) #Dobijamo OBJEKAT RsaKey

    # Hashujemo passphrase sa SHA1
    hashedPassphrase = sha1_hash(password)

    #Pretvaramo kljuceve iz RsaKey objekta u bytes
    privateKey = key.export_key(format = 'PEM' ,passphrase=hashedPassphrase) #eksportujemo u byte string formata 'PEM'
    publicKey = key.public_key().export_key()
    print(privateKey); print(publicKey)

    #Pravimo objekat
    keyRing = PrivateKeyRing(email, name , hashedPassphrase, "Rsa", publicKey, privateKey)

    if not dictionaryOfPrivateKeyRings.__contains__(keyRing.userId):
        dictionaryOfPrivateKeyRings[keyRing.userId] = []
        dictionaryOfPrivateKeyRings[keyRing.userId].append(keyRing)
    else:
        dictionaryOfPrivateKeyRings[keyRing.userId].append(keyRing)



def GenerateElGamalKey(name, email, password):
    privateKey, publicKey = GeneratingPublicAndPrivateKeys()

    # Hashujemo passphrase sa SHA1
    hashedPassphrase = sha1_hash(password)

    privateKeyExport = privateKey.export_key(hashedPassphrase)#eksportujemo u byte string formata 'PEM'
    publicKeyExport = publicKey.export_key()
    print(privateKeyExport);print(publicKeyExport)

    # Pravimo objekat
    keyRing = PrivateKeyRing(email, name, hashedPassphrase, "ElGamal", publicKeyExport, privateKeyExport)

    if not dictionaryOfPrivateKeyRings.__contains__(keyRing.userId):
        dictionaryOfPrivateKeyRings[keyRing.userId] = []
        dictionaryOfPrivateKeyRings[keyRing.userId].append(keyRing)
    else:
        dictionaryOfPrivateKeyRings[keyRing.userId].append(keyRing)



def GenerateDsaKey(name, email, password):
    key = DSA.generate(2048)

    # Hashujemo passphrase sa SHA1
    hashedPassphrase = sha1_hash(password)

    # Pretvaramo kljuceve iz RsaKey objekta u bytes
    privateKey = key.export_key(format = 'PEM',passphrase=hashedPassphrase)
    publicKey = key.public_key().export_key()
    print(privateKey);print(publicKey)

    # Pravimo objekat
    keyRing = PrivateKeyRing(email, name, hashedPassphrase, "Dsa", publicKey, privateKey)

    if not dictionaryOfPrivateKeyRings.__contains__(keyRing.userId):
        dictionaryOfPrivateKeyRings[keyRing.userId] = []
        dictionaryOfPrivateKeyRings[keyRing.userId].append(keyRing)
    else:
        dictionaryOfPrivateKeyRings[keyRing.userId].append(keyRing)






