from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from KeyGenImplementation import *




def CredentialsForImportWindow():
    global keyImportWindow
    keyImportWindow = Toplevel()
    keyImportWindow.title("Key Import Window")

    labelName = Label(keyImportWindow, text="Enter name of user that is importing key: " )
    entryName = Entry(keyImportWindow, width=100)

    labelEmail = Label(keyImportWindow, text="Enter Email of user that is importing key ( Only if you are importing your private key! ): ")
    entryEmail = Entry(keyImportWindow, width=100)

    labelPassword1 = Label(keyImportWindow, text="If you are importing your private key please provide us your passphrase:")
    labelPassword2 = Label(keyImportWindow,text="If you are importing someone else's public key you dont need to enter password:")
    entryPassword = Entry(keyImportWindow, width=50)

    labelUpload = Label(keyImportWindow, text='Import Public or Private Key')
    buttonChoose = Button(keyImportWindow, text='Choose Key', command=lambda: open_file_import(entryName.get(), entryEmail.get(), entryPassword.get()))

    #Pozicioniranje
    labelName.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
    entryName.grid(row=1, column=0, columnspan=3, padx=20, pady=(5,25))

    labelEmail.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
    entryEmail.grid(row=3, column=0, columnspan=3, padx=20, pady=(5,25))

    labelPassword1.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
    labelPassword2.grid(row=5, column=0, columnspan=3, padx=5, pady = (0,5))
    entryPassword.grid(row=6, column=0, columnspan=3, padx=20, pady=(5,25))

    labelUpload.grid(row=7, column=0, padx=20, pady=25)
    buttonChoose.grid(row=7, column=1, padx=20, pady=25)


def open_file_import(name, email, password):
    file_path = askopenfilename()

    with open(file_path, "rb") as file:
        byteString = file.read()
        prORpb, algorithm, userId, key = byteString.split(b'*')

        #If its private key
        if(prORpb == b'private'):
            hashedPassphrase = sha1_hash(password)
            keyRing = ''

            if(algorithm == b'Rsa'):
                publicKey = RSA.import_key(key, passphrase=hashedPassphrase).public_key().export_key()
                keyRing = PrivateKeyRing(email, name, hashedPassphrase, "Rsa", publicKey, key)

            elif(algorithm == b'ElGamal'):
                publicKey = PrivateKey.import_key(hashedPassphrase, key).generatePublicKey().export_key()
                keyRing = PrivateKeyRing(email, name, hashedPassphrase, "ElGamal", publicKey, key)

            elif(algorithm == b'Dsa'):
                publicKey = DSA.import_key(key, passphrase=hashedPassphrase).public_key().export_key()
                keyRing = PrivateKeyRing(email, name, hashedPassphrase, "Dsa", publicKey, key)

            if not dictionaryOfPrivateKeyRings.__contains__(name):
                dictionaryOfPrivateKeyRings[name] = []
                dictionaryOfPrivateKeyRings[name].append(keyRing)
            else:
                dictionaryOfPrivateKeyRings[name].append(keyRing)


        #If its public key
        elif(prORpb == b'public'):
            keyRing = PublicKeyRing(userId.decode('utf-8'), algorithm.decode('utf-8'), key)

            if not dictionaryOfPublicKeyRings.__contains__(name):
                dictionaryOfPublicKeyRings[name] = []
                dictionaryOfPublicKeyRings[name].append(keyRing)
            else:
                dictionaryOfPublicKeyRings[name].append(keyRing)


        for key in dictionaryOfPrivateKeyRings:
            for value in dictionaryOfPrivateKeyRings[key]:
                print(value.__str__())

        for key in dictionaryOfPublicKeyRings:
            for value in dictionaryOfPublicKeyRings[key]:
                print(value.__str__())



#///////////////////////////////////////////////////////EXPORT/////////////////////////////////////////////////////////////
def CredentialsForExportWindow():
    # Novi window
    global credentialsForExportWindow
    credentialsForExportWindow = Toplevel()
    credentialsForExportWindow.title("Enter credentials")
    credentialsForExportWindow.resizable(False,False)

    # Generisanje widgeta
    labelInfo = Label(credentialsForExportWindow, text="Enter credentials")

    labelName = Label(credentialsForExportWindow, text="Enter name: ", relief="sunken")
    entryName = Entry(credentialsForExportWindow, width=100)

    buttonDone = Button(credentialsForExportWindow, text="Export", command=lambda: ExportKeysWindow(entryName.get()))

    # Pozicioniranje
    labelInfo.grid(row=0, column=0, columnspan=2, pady=10)

    labelName.grid(row=1, column=0, columnspan=2, pady=3)
    entryName.grid(row=2, column=0, columnspan=2, pady=10)

    buttonDone.grid(row=4, column=0, columnspan=2, pady=10)

def ExportKeysWindow(name):
    credentialsForExportWindow.destroy()

    global root
    root = Toplevel()
    # Create the table

    keys = dictionaryOfPrivateKeyRings.get(name)

    global table
    table = []
    for el in keys:
        table.append([el.EcryptedPrivateKey, el.publicKey, el.algorithm, el.userId])

    for i, row in enumerate(table):
        for j, value in enumerate(row):
            label = Label(root, text=value[0:200])
            label.grid(row=i, column=j, padx=10, pady=5)

        first_button = Button(root, text="Export private key", command= lambda id = i : open_file_export(id, b'private'))
        first_button.grid(row=i, column=len(row), padx=5)

        second_button = Button(root, text="Export public key", command=lambda id = i: open_file_export(id, b'public'))
        second_button.grid(row=i, column=len(row) + 1)

    # Start the main event loop

def open_file_export(i, prORpb):
    value = table[i][ 0 if prORpb == b'private' else 1]
    algorithm = table[i][2]
    userId = table[i][3]

    file_path = askopenfilename()
    with open(file_path,"wb") as file:
        file.write(prORpb + b'*' +algorithm.encode('utf-8') + b'*' + userId.encode('utf-8') + b'*' + value)
        file.close()


