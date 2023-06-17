import hashlib
from Crypto.PublicKey import RSA
from Crypto.PublicKey import DSA
from Hashing_and_Truncating import *
from ElGamalImpl import *


#------------------------------------------- STRUKTURE POTREBNE ZA GENERISANJE KLJUCA -------------------------------------
class PrivateKeyRing:
    def __init__(self, email, name, password, algorithm, publicKey, privateKey):
        self.userId = email + name
        self.hashedPassphrade = password
        self.algorithm = algorithm
        self.EcryptedPrivateKey = privateKey
        self.publicKey = publicKey
        self.publicKeyId = publicKey[-33:-25] if algorithm == "Rsa" or algorithm == "Dsa" else publicKey[-41:-33]


    def __str__(self):
        print(self.userId + " - " + self.algorithm + " - " + self.hashedPassphrade)
        print(self.publicKey)
        print(self.EcryptedPrivateKey)


    #Ovo ipak ne treba
    def export1(self, filename):
        print()

    def import1(self, filename):
        print()


class PublicKeyRing:
    def __init__(self, userId, algorithm, publicKey):
        self.userId = userId
        self.algorithm = algorithm
        self.publicKey = publicKey
        self.publicKeyId = publicKey[-33:-25] if algorithm == "Rsa" or algorithm == "Dsa" else publicKey[-41:-33]


    def __str__(self):
        print(self.userId + " - " + self.algorithm)
        print(self.publicKey)


dictionaryOfPrivateKeyRings = {}
dictionaryOfPublicKeyRings = {}


#------------------------------------------- POTREBNE FUNKCIJE ZA GENERISANJE KLJUCA --------------------------------------
def GeneratingKey(name, email, password, algorithm):
    if(algorithm == 1):# RSA
        GenerateRsaKey(name, email, password)
    if(algorithm == 2):# DSA
        GenerateDsaKey(name, email, password)
    if(algorithm == 3):# ElGamal
        GenerateElGamalKey(name, email, password)



def GenerateRsaKey(name, email, password):
    key = RSA.generate(2048) #Dobijamo OBJEKAT RsaKey

    # Hashujemo passphrase sa SHA1
    hashedPassphrase = sha1_hash(password)

    #Pretvaramo kljuceve iz RsaKey objekta u bytes
    privateKey = key.export_key(format = 'PEM' ,passphrase=hashedPassphrase) #eksportujemo u byte string formata 'PEM'
    publicKey = key.public_key().export_key()

    #Pravimo objekat
    keyRing = PrivateKeyRing(email, name , hashedPassphrase, "Rsa", publicKey, privateKey)

    if not dictionaryOfPrivateKeyRings.__contains__(name):
        dictionaryOfPrivateKeyRings[name] = []
        dictionaryOfPrivateKeyRings[name].append(keyRing)
    else:
        dictionaryOfPrivateKeyRings[name].append(keyRing)

    #helpDictionaryUserID[keyRing.userId] = keyRing
    #helpDictionaryKeyID[keyRing.publicKeyId] = keyRing
    keyRing.__str__()


def GenerateElGamalKey(name, email, password):
    privateKey, publicKey = GeneratingPublicAndPrivateKeys()

    # Hashujemo passphrase sa SHA1
    hashedPassphrase = sha1_hash(password)

    privateKeyExport = privateKey.export_key(hashedPassphrase)#eksportujemo u byte string formata 'PEM'
    publicKeyExport = publicKey.export_key()

    # Pravimo objekat
    keyRing = PrivateKeyRing(email, name, hashedPassphrase, "ElGamal", publicKeyExport, privateKeyExport)

    if not dictionaryOfPrivateKeyRings.__contains__(name):
        dictionaryOfPrivateKeyRings[name] = []
        dictionaryOfPrivateKeyRings[name].append(keyRing)
    else:
        dictionaryOfPrivateKeyRings[name].append(keyRing)

    #helpDictionaryUserID[keyRing.userId] = keyRing
    #helpDictionaryKeyID[keyRing.publicKeyId] = keyRing
    keyRing.__str__()


def GenerateDsaKey(name, email, password):
    key = DSA.generate(2048)

    # Hashujemo passphrase sa SHA1
    hashedPassphrase = sha1_hash(password)

    # Pretvaramo kljuceve iz RsaKey objekta u bytes
    privateKey = key.export_key(format = 'PEM',passphrase=hashedPassphrase)
    publicKey = key.public_key().export_key()

    # Pravimo objekat
    keyRing = PrivateKeyRing(email, name, hashedPassphrase, "Dsa", publicKey, privateKey)

    if not dictionaryOfPrivateKeyRings.__contains__(name):
        dictionaryOfPrivateKeyRings[name] = []
        dictionaryOfPrivateKeyRings[name].append(keyRing)
    else:
        dictionaryOfPrivateKeyRings[name].append(keyRing)

    #helpDictionaryUserID[keyRing.userId] = keyRing
    #helpDictionaryKeyID[keyRing.publicKeyId] = keyRing
    keyRing.__str__()




