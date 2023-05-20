class PrivateKeyRing:
    def __init__(self, email, name, password, algorithm, publicKey, privateKey):
        self.userId = email + name
        self.algorithm = algorithm
        self.EcryptedPrivateKey = privateKey
        self.publicKey = publicKey



class PublicKeyRing:
    def __init__(self, email, name, password, algorithm, publicKey, privateKey):
        self.userId = email + name
        self.algorithm = algorithm
        self.EcryptedPrivateKey = privateKey
        self.publicKey = publicKey



def KeyGenerator():
    print("Not yet implemented")