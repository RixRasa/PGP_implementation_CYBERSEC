import tkinter
from tkinter import *
from tkinter import ttk
from KeyGenImplementation import *
from ElGamalImpl import PrivateKey
import re
from tkinter import Toplevel





def AllKeys():

    # Novi window
    global allKeysWindow
    allKeysWindow = Toplevel()
    allKeysWindow.title("Enter credentials")
    allKeysWindow.resizable(False, False)

    # Generisanje widgeta
    labelInfo = Label(allKeysWindow, text="Enter credentials")

    labelName = Label(allKeysWindow, text="Enter name: ", bd=1, relief="sunken")
    entryName = Entry(allKeysWindow, width=100)

    labelEmail = Label(allKeysWindow, text="Enter Email: ", bd=1, relief="sunken")
    entryEmail = Entry(allKeysWindow, width=100)

    buttonDone = Button(allKeysWindow, text="Show", command=lambda: ShowAllKeys(entryName.get(), entryEmail.get()))


    # Pozicioniranje
    labelInfo.grid(row=0, column=0, columnspan=2, pady=10)

    labelName.grid(row=1, column=0, columnspan=2, pady=3)
    entryName.grid(row=2, column=0, columnspan=2, pady=10)

    labelEmail.grid(row=3, column=0, columnspan=2, pady=3)
    entryEmail.grid(row=4, column=0, columnspan=2, pady=10)

    buttonDone.grid(row=6, column=0, columnspan=2, pady=10)

def ShowAllKeys(name,email):
    allKeysWindow.destroy()

    # Provera Regexa
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if name == "":
        AllKeys()
    elif email == "" or (not re.fullmatch(regex, email)):
        AllKeys()

    global showAllKeysWindow
    showAllKeysWindow=Toplevel()
    showAllKeysWindow.title("All your keys")

    frm=Frame(showAllKeysWindow)
    frm.pack(side=tkinter.LEFT,padx=20)

    tv=ttk.Treeview(frm,columns=(1,2,3,4),show="headings",height="5")
    tv.pack()
    tv.heading(1, text="User ID")
    tv.heading(2, text="Algorithm")
    tv.heading(3, text="Ecrypted Private Key")
    tv.heading(4, text="Public Key")

    keys=dictionaryOfPrivateKeyRings.get(email+name)

    for el in keys:
        polje = [el.userId, el.algorithm, el.EcryptedPrivateKey, el.publicKey ]
        tv.insert('','end',values=polje)

    buttonShow = Button(showAllKeysWindow, text="Show my private keys", command=lambda: PasswordForPrivateKey(keys))
    buttonShow.pack(side=tkinter.LEFT,padx=10,pady=10)


def PasswordForPrivateKey(keys):

    # Novi window
    global showPrivateKeysPasswordWindow
    showPrivateKeysPasswordWindow = Toplevel()
    showPrivateKeysPasswordWindow.title("password")

    # Generisanje widgeta
    labelInfo = Label(showPrivateKeysPasswordWindow, text="Enter your password")
    entryPassword = Entry(showPrivateKeysPasswordWindow, width=50)

    buttonDone = Button(showPrivateKeysPasswordWindow, text="Done", command=lambda: ShowPrivateKeys(keys,sha1_hash(entryPassword.get())))

    # Pozicioniranje
    labelInfo.grid(row=0, column=0, columnspan=2, pady=3, padx=50)
    entryPassword.grid(row=1, column=0, columnspan=2, pady=20, padx=50)
    buttonDone.grid(row=2, column=0, columnspan=2, pady=20, padx=50)


def ShowPrivateKeys(keys,sifra):
    showPrivateKeysPasswordWindow.destroy()


    global showPrivateKeysWindow
    showPrivateKeysWindow = Toplevel()
    showPrivateKeysWindow.title("All your private keys")

    frm = Frame(showPrivateKeysWindow)
    frm.pack(side=tkinter.LEFT, padx=20)

    tv = ttk.Treeview(frm, columns=(1, 2), show="headings", height="5")
    tv.pack()
    tv.heading(1, text="Algorithm")
    tv.heading(2, text="Decrypted Private Key")

    for key in keys:
        string = ""
        if(key.hashedPassphrade == sifra):

            if(key.algorithm == "Rsa"):
                privateKey = RSA.import_key(key.EcryptedPrivateKey, passphrase=sifra)
                privateKey.public_key()
                string = str(privateKey.d) + " - " + str(privateKey.n)
                print(string)

            elif(key.algorithm == "Dsa"):
                privateKey = DSA.import_key(key.EcryptedPrivateKey, passphrase=sifra)
                string = privateKey
                print(string)

            elif(key.algorithm == "ElGamal"):
                privateKey = PrivateKey.import_key(sifra, key.EcryptedPrivateKey)
                string =str(privateKey.key) + " - " + str(privateKey.q)
                print(string)

            polje = [key.algorithm, string]
            tv.insert('', 'end', values=polje)