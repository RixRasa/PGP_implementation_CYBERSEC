import tkinter
from tkinter import *
from tkinter import ttk
from KeyGenImplementation import *
from ElGamalImpl import PrivateKey
from tkinter import Toplevel


#-------------------------------------------PREGLED PRIVATNIH KEY RINGOVA------------------------------------------------
def AllKeysPrivate():

    # Novi window
    global allKeysWindow
    allKeysWindow = Toplevel()
    allKeysWindow.title("All private key rings")
    allKeysWindow.resizable(False, False)

    # Generisanje widgeta

    labelName = Label(allKeysWindow, text="Enter name of user that wants to see their private key ring ", bd=1)
    entryName = Entry(allKeysWindow, width=100)

    buttonDone = Button(allKeysWindow, text="Show", command=lambda: ShowAllPrivateKeys(entryName.get()))


    # Pozicioniranje

    labelName.grid(row=1, column=0, columnspan=2, pady=3)
    entryName.grid(row=2, column=0, columnspan=2, pady=10)

    buttonDone.grid(row=4, column=0, columnspan=2, pady=10)

def ShowAllPrivateKeys(name):
    allKeysWindow.destroy()

    # Provera Regexa
    if name == "":
        AllKeysPrivate()


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

    buttonShow = Button(showAllKeysWindow, text="Delete a key", command=lambda: DeletePrivateKeyPair(name, keys))
    buttonShow.pack(side=tkinter.LEFT, padx=10)



#------------------------------------------PRIKAZ DEKRIPTOVANIH PRIVATNIH KLJUCEVA------------------------------------------
def PasswordForPrivateKey(keys):
    # Novi window
    global showPrivateKeysPasswordWindow
    showPrivateKeysPasswordWindow = Toplevel()
    showPrivateKeysPasswordWindow.title("password")

    # Generisanje widgeta
    labelInfo = Label(showPrivateKeysPasswordWindow, text="Enter your password")
    entryPassword = Entry(showPrivateKeysPasswordWindow, width=50)

    buttonDone = Button(showPrivateKeysPasswordWindow, text="Done", command=lambda: ShowPrivateKeys(keys, sha1_hash(entryPassword.get())))

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



#-------------------------------------------------- BRISANJE KLJUCEVA ------------------------------------------------------
def DeletePrivateKeyPair(name, keys):

    # Novi window
    global deleteKeyPairWindow
    deleteKeyPairWindow = Toplevel()
    deleteKeyPairWindow.title("Deleting a key")
    deleteKeyPairWindow.resizable(False, False)

    # Generisanje widgeta

    labelEmail = Label(deleteKeyPairWindow, text="Enter email of a key pair you want to delete: ")
    entryEmail = Entry(deleteKeyPairWindow, width=100)

    labelPass = Label(deleteKeyPairWindow, text="Enter password: ", bd=1, relief="sunken")
    entryPass = Entry(deleteKeyPairWindow, width=100)

    buttonDone = Button(deleteKeyPairWindow, text="Delete", command=lambda: deletePrivate(name, entryEmail.get(), entryPass.get(), keys))

    # Pozicioniranje

    labelEmail.grid(row=1, column=0, columnspan=2, pady=3)
    entryEmail.grid(row=2, column=0, columnspan=2, pady=10)

    labelPass.grid(row=3, column=0, columnspan=2, pady=3)
    entryPass.grid(row=4, column=0, columnspan=2, pady=10)

    buttonDone.grid(row=6, column=0, columnspan=2, pady=10)


def deletePrivate(name, email, password, keys):
    sifrahash = sha1_hash(password)

    string = "The key you wanted to delete was not found"

    for index,el in enumerate(keys):
        if el.userId == (email+name):
            if sifrahash == el.hashedPassphrade:
                keys.remove(el)
                deleteKeyPairWindow.destroy()
                print("Obrisali ste kljuc " + el.userId)
                return
            else:
                string = "You entered wrong password for the key you wanted to delete"

    global keyNotFoundWindow
    keyNotFoundWindow = Toplevel()
    keyNotFoundWindow.title("Key not found")

    labelInfo = Label(keyNotFoundWindow, text=string)
    buttonDone = Button(keyNotFoundWindow, text="Ok", command=lambda: helper1(keys))

    labelInfo.grid(row=0, column=0, columnspan=2, pady=10)
    buttonDone.grid(row=1, column=0, columnspan=2, pady=10)


def helper1(keys):
    keyNotFoundWindow.destroy()
    DeletePrivateKeyPair(keys)






