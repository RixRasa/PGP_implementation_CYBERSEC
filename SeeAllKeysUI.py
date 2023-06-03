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


    buttonDone = Button(allKeysWindow, text="Show", command=lambda: ShowAllKeys(entryName.get()))


    # Pozicioniranje
    labelInfo.grid(row=0, column=0, columnspan=2, pady=10)

    labelName.grid(row=1, column=0, columnspan=2, pady=3)
    entryName.grid(row=2, column=0, columnspan=2, pady=10)

    buttonDone.grid(row=4, column=0, columnspan=2, pady=10)

def AllKeysPublic():
    global allKeysPublicWindow
    allKeysPublicWindow = Toplevel()
    allKeysPublicWindow.title("Enter credentials")
    allKeysPublicWindow.resizable(False, False)

    # Generisanje widgeta
    labelInfo = Label(allKeysPublicWindow, text="Enter credentials")

    labelName = Label(allKeysPublicWindow, text="Enter name: ", bd=1, relief="sunken")
    entryName = Entry(allKeysPublicWindow, width=100)

    buttonDone = Button(allKeysPublicWindow, text="Show", command=lambda: ShowAllPublicKeys(entryName.get()))

    # Pozicioniranje
    labelInfo.grid(row=0, column=0, columnspan=2, pady=10)

    labelName.grid(row=1, column=0, columnspan=2, pady=3)
    entryName.grid(row=2, column=0, columnspan=2, pady=10)

    buttonDone.grid(row=4, column=0, columnspan=2, pady=10)
def ShowAllKeys(name):
    allKeysWindow.destroy()

    # Provera Regexa
    if name == "":
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

    keys=dictionaryOfPrivateKeyRings.get(name)

    for el in keys:
        polje = [el.userId, el.algorithm, el.EcryptedPrivateKey, el.publicKey ]
        tv.insert('','end',values=polje)

    buttonShow = Button(showAllKeysWindow, text="Show my private keys", command=lambda: PasswordForPrivateKey(keys))
    buttonShow.pack(side=tkinter.LEFT,padx=10,pady=10)

    buttonShow = Button(showAllKeysWindow, text="Delete a key", command=lambda: DeleteKeyPair(keys))
    buttonShow.pack(side=tkinter.LEFT, padx=10)

def ShowAllPublicKeys(name):
    allKeysPublicWindow.destroy()

    # Provera Regexa
    if name == "":
        AllKeysPublic()

    global showAllPublicKeysWindow
    showAllPublicKeysWindow = Toplevel()
    showAllPublicKeysWindow.title("All your keys")

    frm = Frame(showAllPublicKeysWindow)
    frm.pack(side=tkinter.LEFT, padx=20)

    tv = ttk.Treeview(frm, columns=(1, 2, 3), show="headings", height="5")
    tv.pack()
    tv.heading(1, text="User ID")
    tv.heading(2, text="Algorithm")
    tv.heading(3, text="Public key")


    keys = dictionaryOfPublicKeyRings.get(name)

    for el in keys:
        polje = [el.userId, el.algorithm, el.publicKey]
        tv.insert('', 'end', values=polje)


    buttonShow = Button(showAllPublicKeysWindow, text="Delete a key", command=lambda: DeleteKeyPairPublic(keys))
    buttonShow.pack(side=tkinter.LEFT, padx=10)
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

def DeleteKeyPair(keys):

    # Novi window
    global deleteKeyPairWindow
    deleteKeyPairWindow = Toplevel()
    deleteKeyPairWindow.title("Enter credentials")
    deleteKeyPairWindow.resizable(False, False)

    # Generisanje widgeta
    labelInfo = Label(deleteKeyPairWindow, text="Enter credentials")

    labelEmail = Label(deleteKeyPairWindow, text="Enter email of a key pair you want to delete: ", bd=1, relief="sunken")
    entryEmail = Entry(deleteKeyPairWindow, width=100)

    labelPass = Label(deleteKeyPairWindow, text="Enter password: ", bd=1, relief="sunken")
    entryPass = Entry(deleteKeyPairWindow, width=100)

    buttonDone = Button(deleteKeyPairWindow, text="Delete", command=lambda: delete(entryEmail.get(), entryPass.get(),keys))

    # Pozicioniranje
    labelInfo.grid(row=0, column=0, columnspan=2, pady=10)

    labelEmail.grid(row=1, column=0, columnspan=2, pady=3)
    entryEmail.grid(row=2, column=0, columnspan=2, pady=10)

    labelPass.grid(row=3, column=0, columnspan=2, pady=3)
    entryPass.grid(row=4, column=0, columnspan=2, pady=10)

    buttonDone.grid(row=6, column=0, columnspan=2, pady=10)

def DeleteKeyPairPublic(keys):
    global deletePublicKeyPairWindow
    deletePublicKeyPairWindow = Toplevel()
    deletePublicKeyPairWindow.title("Enter credentials")
    deletePublicKeyPairWindow.resizable(False, False)

    # Generisanje widgeta
    labelInfo = Label(deletePublicKeyPairWindow, text="Enter credentials")

    labelEmail = Label(deletePublicKeyPairWindow, text="Enter UserID of a key pair you want to delete: ", bd=1,
                       relief="sunken")
    entryEmail = Entry(deletePublicKeyPairWindow, width=100)


    buttonDone = Button(deletePublicKeyPairWindow, text="Delete",
                        command=lambda: deletePublic(entryEmail.get(), keys))

    # Pozicioniranje
    labelInfo.grid(row=0, column=0, columnspan=2, pady=10)

    labelEmail.grid(row=1, column=0, columnspan=2, pady=3)
    entryEmail.grid(row=2, column=0, columnspan=2, pady=10)



    buttonDone.grid(row=6, column=0, columnspan=2, pady=10)
def delete(email,password,keys):
    # provera passworda
    sifrahash = sha1_hash(password)


    for index,el in enumerate(keys):
        if el.email == email:
            if sifrahash!=el.hashedPassphrade:
                deleteKeyPairWindow.destroy()
                wrongpassWindow(keys, 1)
                return
            keys.remove(el)
            deleteKeyPairWindow.destroy()
            wrongpassWindow(keys, 0)
            print("a")
            return

    #mejl postoji
    deleteKeyPairWindow.destroy()
    wrongpassWindow(keys, 2)

def deletePublic(userid,keys):


    for index, el in enumerate(keys):
        if el.userId == userid:
            keys.remove(el)
            deletePublicKeyPairWindow.destroy()
            keyNotFound(keys, 0)
            print("a")
            return

    # mejl postoji
    deletePublicKeyPairWindow.destroy()
    keyNotFound(keys, 2)
def wrongpassWindow(keys,flag):

    global WrongpassWindow

    def helper(keys):
        WrongpassWindow.destroy()
        DeleteKeyPair(keys)

    def helper1(keys):
        WrongpassWindow.destroy()
        DeleteKeyPair(keys)
    WrongpassWindow = Toplevel()
    if flag==1:
        WrongpassWindow.title("Wrong password")
        labelInfo = Label(WrongpassWindow, text="You entered wrong password")
        buttonDone = Button(WrongpassWindow, text="Ok",
                            command=lambda: helper(keys))
    elif flag==0:
        WrongpassWindow.title("Success")
        labelInfo = Label(WrongpassWindow, text="You have deleted a key pair successfuly")
        buttonDone = Button(WrongpassWindow, text="Ok",
                            command=lambda: helper1(keys))
    elif flag==2:
        WrongpassWindow.title("Key not found")
        labelInfo = Label(WrongpassWindow, text="The key you wanted to delete was not found")
        buttonDone = Button(WrongpassWindow, text="Ok",
                            command=lambda: helper1(keys))
    WrongpassWindow.resizable(False, False)

    # Generisanje widgeta




    #buttonDone = Button(WrongpassWindow, text="Ok",
                        #command=lambda: helper(keys))

    # Pozicioniranje
    labelInfo.grid(row=0, column=0, columnspan=2, pady=10)



    buttonDone.grid(row=6, column=0, columnspan=2, pady=10)

def keyNotFound(keys,flag):
    global keyNotFoundWindow

    keyNotFoundWindow=Toplevel()

    def helper1(keys):
        keyNotFoundWindow.destroy()
        DeleteKeyPairPublic(keys)

    if flag == 0:
        keyNotFoundWindow.title("Success")
        labelInfo = Label(keyNotFoundWindow, text="You have deleted a key pair successfuly")
        buttonDone = Button(keyNotFoundWindow, text="Ok",
                            command=lambda: helper1(keys))
    elif flag == 2:
        keyNotFoundWindow.title("Key not found")
        labelInfo = Label(keyNotFoundWindow, text="The key you wanted to delete was not found")
        buttonDone = Button(keyNotFoundWindow, text="Ok",
                            command=lambda: helper1(keys))
    keyNotFoundWindow.resizable(False, False)

    labelInfo.grid(row=0, column=0, columnspan=2, pady=10)

    buttonDone.grid(row=6, column=0, columnspan=2, pady=10)