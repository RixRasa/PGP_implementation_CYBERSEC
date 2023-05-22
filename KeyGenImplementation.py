import hashlib
from Crypto.PublicKey import RSA
from Crypto.PublicKey import DSA
from Hashing_and_Truncating import *
from ElGamalImpl import *

dictionaryOfPrivateKeyRings = {}


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

'''class PublicKeyRing:
    def __init__(self, email, name, password, algorithm, publicKey, privateKey):
        self.userId = email + name
        self.algorithm = algorithm
        self.EcryptedPrivateKey = privateKey
        self.publicKey = publicKey'''



def GeneratingKey(name, email, password, algorithm):
    if(algorithm == 1):
        GenerateRsaKey(name, email, password)
    if(algorithm == 2):
        GenerateDsaKey(name, email, password)
        GenerateElGamalKey(name, email, password)


def GenerateRsaKey(name, email, password):
    key = RSA.generate(2048)

    # Hashujemo passphrase sa SHA1
    hashedPassphrase = sha1_hash(password)

    #Pretvaramo kljuceve iz RsaKey objekta u bytes
    privateKey = key.export_key(passphrase=hashedPassphrase)
    publicKey = key.public_key().export_key()

    #Pravimo objekat
    keyRing = PrivateKeyRing(email, name , hashedPassphrase, "Rsa", privateKey, publicKey)

    if not dictionaryOfPrivateKeyRings.__contains__(keyRing.userId):
        dictionaryOfPrivateKeyRings[keyRing.userId] = []
        dictionaryOfPrivateKeyRings[keyRing.userId].append(keyRing)
    else:
        dictionaryOfPrivateKeyRings[keyRing.userId].append(keyRing)


def GenerateElGamalKey(name, email, password):
    privateKey, publicKey = GeneratingPublicAndPrivateKeys()

    # Hashujemo passphrase sa SHA1
    hashedPassphrase = sha1_hash(password)

    privateKeyExport = privateKey.exportKey(hashedPassphrase)
    publicKeyExport = publicKey.exportKey()

    # Pravimo objekat
    keyRing = PrivateKeyRing(email, name, hashedPassphrase, "ElGamal", privateKeyExport, publicKeyExport)

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
    privateKey = key.export_key(passphrase=hashedPassphrase)
    publicKey = key.public_key().export_key()

    # Pravimo objekat
    keyRing = PrivateKeyRing(email, name, hashedPassphrase, "Dsa", privateKey, publicKey)

    if not dictionaryOfPrivateKeyRings.__contains__(keyRing.userId):
        dictionaryOfPrivateKeyRings[keyRing.userId] = []
        dictionaryOfPrivateKeyRings[keyRing.userId].append(keyRing)
    else:
        dictionaryOfPrivateKeyRings[keyRing.userId].append(keyRing)






