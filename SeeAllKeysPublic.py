import tkinter
from tkinter import *
from KeyGenImplementation import dictionaryOfPublicKeyRings
from tkinter import ttk


#----------------------------------------------PREGLED SVIH PUBLIC KEY RINGOVA---------------------------------------------
def AllKeysPublic():
    global allKeysPublicWindow
    allKeysPublicWindow = Toplevel()
    allKeysPublicWindow.title("All public key rings ")
    allKeysPublicWindow.resizable(False, False)

    # Generisanje widgeta

    labelName = Label(allKeysPublicWindow, text="Enter name of user that wants to see their public key rings: ")
    entryName = Entry(allKeysPublicWindow, width=100)

    buttonDone = Button(allKeysPublicWindow, text="Show", command=lambda: ShowAllPublicKeys(entryName.get()))

    # Pozicioniranje

    labelName.grid(row=1, column=0, columnspan=2, pady=3)
    entryName.grid(row=2, column=0, columnspan=2, pady=10)

    buttonDone.grid(row=4, column=0, columnspan=2, pady=10)


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


#-------------------------------------------------- BRISANJE KLJUCEVA ------------------------------------------------------
def DeleteKeyPairPublic(keys):
    global deletePublicKeyPairWindow
    deletePublicKeyPairWindow = Toplevel()
    deletePublicKeyPairWindow.title("Enter credentials")
    deletePublicKeyPairWindow.resizable(False, False)

    # Generisanje widgeta

    labelEmail = Label(deletePublicKeyPairWindow, text="Enter UserID of a key pair you want to delete: ")
    entryEmail = Entry(deletePublicKeyPairWindow, width=100)

    buttonDone = Button(deletePublicKeyPairWindow, text="Delete", command=lambda: deletePublic(entryEmail.get(), keys))

    # Pozicioniranje

    labelEmail.grid(row=1, column=0, columnspan=2, pady=3)
    entryEmail.grid(row=2, column=0, columnspan=2, pady=10)

    buttonDone.grid(row=3, column=0, columnspan=2, pady=10)


def deletePublic(userid, keys):

    for index, el in enumerate(keys):
        if el.userId == userid:
            keys.remove(el)
            deletePublicKeyPairWindow.destroy()
            print("Kljuc " + el.userId + " obrisan!")
            return

    #mejl ne postoji
    global keyNotFoundWindow
    keyNotFoundWindow = Toplevel()
    keyNotFoundWindow.title("Key not found")

    labelInfo = Label(keyNotFoundWindow, text="The key you wanted to delete was not found")
    buttonDone = Button(keyNotFoundWindow, text="Ok", command=lambda: helper1(keys))

    labelInfo.grid(row=0, column=0, columnspan=2, pady=10)
    buttonDone.grid(row=1, column=0, columnspan=2, pady=10)

def helper1(keys):
    keyNotFoundWindow.destroy()
    DeleteKeyPairPublic(keys)

