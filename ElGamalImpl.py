import random
from math import pow
import base64
from Crypto.Cipher import CAST
from Hashing_and_Truncating import *



#|||||||||||||||||||||||||||||||||||||||||||||||PUBLIC AND PRIVATE KEY CLASSES||||||||||||||||||||||||||||||||||||||||||||||
class PublicKey():
    def __init__(self, q, g, h):
        self.q = q
        self.g = g
        self.h = h

    def export_key(self):
        #print(self.q);print(self.g);print(self.h) #samo za testiranje

        string = str(self.q) + "/" + str(self.g) + "/" + str(self.h) #Formiranje stringa od atributa objekta kljuca

        stringBytes = string.encode('utf-8') #Prebacivanje iz stringa u bytes

        stringBytesEcode64 = b'-----BEGIN ELGAMAL PUBLIC KEY-----\n' +  base64.b64encode(stringBytes) + b'\n' + b'-----END ELGAMAL PUBLIC KEY-----' #Dodavanje zaglavlja i encodovanje u 'pem'

        return stringBytesEcode64

    def import_key(self, stringBytesEcode64):
        stringBytesEcode64 = stringBytesEcode64[35: -33] #Skidanje zaglavlja

        stringBytes = base64.b64decode(stringBytesEcode64) #Deckodovanje iz 'pem' formata

        string = stringBytes.decode('utf-8') #Prebacivanje iz bytes u string

        q,g,h = string.split('/') #Splitovanje stringa i ubacivanje vrednosti
        print(q); print(g); print(h)# samo za testiranje


class PrivateKey():
    def __init__(self, key, q):
        self.key = key
        self.q = q

    def export_key(self, passphrase):
        #print(self.key); print(self.q)#samo za testiranje

        string = str(self.key) + "/" + str(self.q) #Formiranje stringa od atributa objekta kljuca

        stringBytes = string.encode('utf-8') #Prebacivanje iz stringa u bytes

        hashedPassphrase = truncate_hash(sha1_hash(passphrase), 128) #Hashiramo sifru koju cemo koristiti kao kljuc za enkripciju privatnog kljuca

        cipher = CAST.new(hashedPassphrase, CAST.MODE_OPENPGP) #Enkriptujemo privatni kljuc('stringBytes') pomocu kljuca('hashedPassphrase')
        privateKeyEncripted = cipher.encrypt(stringBytes)

        stringBytesEcode64 =b'-----BEGIN ELGAMAL PRIVATE KEY-----\n' +  base64.b64encode(privateKeyEncripted) + b'\n' + b'-----END ELGAMAL PRIVATE KEY-----' #Dodajemo zaglavlje i encodujemo u 'pem'

        return stringBytesEcode64

    def import_key(self, passphrase, stringBytesEcode64):
        hashedPassphrase = truncate_hash(sha1_hash(passphrase), 128)#Hashirsamo sifru

        privateKeyEncripted = base64.b64decode(stringBytesEcode64[36:-34])#Skidamo zaglavlje i decodujemo iz 'pem-a'

        eiv = privateKeyEncripted[:CAST.block_size + 2]  #Desifrujemo i dobijamo ponovo privatni kljuc u formi 'bytes' ('stringBytes')
        ciphertext = privateKeyEncripted[CAST.block_size + 2:]
        cipher = CAST.new(hashedPassphrase, CAST.MODE_OPENPGP, eiv)
        stringBytes = cipher.decrypt(ciphertext)

        string = stringBytes.decode('utf-8') #Prebacivanje iz bytes u string

        key, q = string.split('/') #Splitovanje stringa i ubacivanje vrednosti

        print(key); print(q)# samo za testiranje



#||||||||||||||||||||||||||||||||||||||||||||||GENERATING KEYS||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
def GeneratingPublicAndPrivateKeys():
    q = random.randint(pow(10, 20), pow(10, 50))
    g = random.randint(2, q)

    key = gen_key(q)  # Private key for receiver
    h = power(g, key, q)

    publicKey = PublicKey(q, g, h)
    privateKey = PrivateKey(key, q)

    return privateKey, publicKey



#|||||||||||||||||||||||||||||||||||||||||HELPER FUNKCIONS FOR ELGAMAL|||||||||||||||||||||||||||||||||||||||||||||||||||||
def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b;
    else:
        return gcd(b, a % b)


# Generating large random numbers
def gen_key(q):
    key = random.randint(pow(10, 20), q)
    while gcd(q, key) != 1:
        key = random.randint(pow(10, 20), q)

    return key


# Modular exponentiation
def power(a, b, c):
    x = 1
    y = a

    while b > 0:
        if b % 2 != 0:
            x = (x * y) % c;
        y = (y * y) % c
        b = int(b / 2)

    return x % c



#||||||||||||||||||||||||||||||||||||||||||||ENKRIPCIJA I DEKRIPCIJA||||||||||||||||||||||||||||||||||||||||||||||||||||||||
def encrypt(msg, publicKey):
    h = publicKey.h; q = publicKey.q; g = publicKey.g

    en_msg = []

    k = gen_key(q)  # Private key for sender
    s = power(h, k, q)
    p = power(g, k, q)

    for i in range(0, len(msg)):
        en_msg.append(msg[i])

    for i in range(0, len(en_msg)):
        en_msg[i] = s * ord(en_msg[i])

    return en_msg, p


def decrypt(en_msg, p, privateKey):
    key = privateKey.key; q = privateKey.q

    dr_msg = []
    h = power(p, key, q)
    for i in range(0, len(en_msg)):
        dr_msg.append(chr(int(en_msg[i] / h)))

    return dr_msg


# Driver code
def main():
    msg = 'encryption'
    print("Original Message :", msg)

    private, public = GeneratingPublicAndPrivateKeys()

    public.import_key(public.export_key()); print(); print();print()
    private.import_key("Kurcina", private.export_key("Kurcina"))


    en_msg, p = encrypt(msg, public)
    dr_msg = decrypt(en_msg, p, private)
    dmsg = ''.join(dr_msg)
    print("Decrypted Message :", dmsg)