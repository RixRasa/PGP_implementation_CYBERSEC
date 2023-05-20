import hashlib
import rsa
from Crypto.PublicKey import RSA
from Crypto.Cipher import CAST

dictionaryOfPrivateKeyRings = {}


class PrivateKeyRing:
    def __init__(self, email, name, password, algorithm, publicKey, privateKey):
        self.userId = email + name
        self.hashedPassphrade = password
        self.algorithm = algorithm
        self.EcryptedPrivateKey = privateKey
        self.publicKey = publicKey
        self.publicKeyId = publicKey[-8:]


    def export1(self):
        print()
    def import1(self):
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
        GenerateDsaElGamalKey(name, email, password)



def GenerateRsaKey(name, email, password):
    key = RSA.generate(2048)
    #Pretvaramo kljuceve iz RsaKey objekta u bytes
    privateKey = key.export_key()
    publicKey = key.public_key().export_key()

    #Hashujemo passphrase sa SHA1
    hashedPassphrase = truncate_hash(sha1_hash(password), 128)

    #Ovde sifrujemo privateKey , Cast128 algoritmom uz pomoc hashovanog Passphrase-a kao kljuca
    cipher = CAST.new(hashedPassphrase, CAST.MODE_OPENPGP)
    privateKeyEncripted = cipher.encrypt(privateKey)

    #Pravimo objekat
    keyRing = PrivateKeyRing(email, name , hashedPassphrase, "Rsa", privateKeyEncripted, publicKey, )

    if not dictionaryOfPrivateKeyRings.__contains__(keyRing.userId):
        dictionaryOfPrivateKeyRings[keyRing.userId] = []
        dictionaryOfPrivateKeyRings[keyRing.userId].append(keyRing)
    else:
        dictionaryOfPrivateKeyRings[keyRing.userId].append(keyRing)


    #Ovde desifrujemo privaeKeyEncripted samo radi provere
    '''eiv = privateKeyEncripted[:CAST.block_size + 2] #blok koji iz nekog razloga mora da postoji
    ciphertext = privateKeyEncripted[CAST.block_size + 2:] #nasa poruka koja ide iza 'eiv' bloka 
    cipher = CAST.new(hashedPassphrase, CAST.MODE_OPENPGP, eiv)
    privateKeyDecrypted = cipher.decrypt(ciphertext)'''




def GenerateDsaElGamalKey(name, email, passoword):
    print("nije jos implementirano")


def truncate_hash(hash_value, desired_length):
    # Convert the hash value to bytes
    hash_bytes = bytes.fromhex(hash_value)

    # Truncate the hash value to the desired length
    truncated_bytes = hash_bytes[:desired_length // 8]

    # Convert the truncated bytes back to a hexadecimal string
    return truncated_bytes


def sha1_hash(message):
    # Create a SHA-1 hash object
    sha1 = hashlib.sha1()

    # Convert the message to bytes and update the hash object
    sha1.update(message.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    hashed_message = sha1.hexdigest()

    return hashed_message


