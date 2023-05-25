import tkinter
from tkinter import *
from tkinter import ttk
from KeyGenImplementation import *
import re





def AllKeysWindow():
    #print(hashedPassphrase)
    # Novi window
    global allKyesWindow
    allKyesWindow = Toplevel()
    allKyesWindow.title("Enter credentials")
    allKyesWindow.resizable(False,False)

    # Generisanje widgeta
    labelInfo = Label(allKyesWindow, text="Enter credentials")

    labelName = Label(allKyesWindow, text="Enter name: ", bd=1, relief="sunken")
    entryName = Entry(allKyesWindow, width=100)

    labelEmail = Label(allKyesWindow, text="Enter Email: ", bd=1, relief="sunken")
    entryEmail = Entry(allKyesWindow, width=100)

    buttonDone = Button(allKyesWindow, text="Show",
                        command=lambda: showAllKeysWindow(entryName.get(), entryEmail.get()))


    # Pozicioniranje
    labelInfo.grid(row=0, column=0, columnspan=2, pady=10)

    labelName.grid(row=1, column=0, columnspan=2, pady=3)
    entryName.grid(row=2, column=0, columnspan=2, pady=10)

    labelEmail.grid(row=3, column=0, columnspan=2, pady=3)
    entryEmail.grid(row=4, column=0, columnspan=2, pady=10)

    buttonDone.grid(row=6, column=0, columnspan=2, pady=10)

def showAllKeysWindow(name,email):
    allKyesWindow.destroy()

    # Provera Regexa
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if name == "":
        AllKeysWindow()
    elif email == "" or (not re.fullmatch(regex, email)):
        AllKeysWindow()

    else:
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
            #print(el.hashedPassphrade)
            polje = [el.userId, el.algorithm, el.EcryptedPrivateKey, el.publicKey ]
            tv.insert('','end',values=polje)

        buttonShow = Button(showAllKeysWindow, text="Show my private keys",
                            command=lambda: passwordForPrivateKey(keys))
        buttonShow.pack(side=tkinter.LEFT,padx=10,pady=10)
#stojanovicrasa4@gmail.com

def passwordForPrivateKey(keys):




    # Novi window
    global showPrivateKeysPasswordWindow
    showPrivateKeysPasswordWindow = Toplevel()
    showPrivateKeysPasswordWindow.title("password")

    # Generisanje widgeta
    labelInfo = Label(showPrivateKeysPasswordWindow, text="Enter your password")
    entryPassword = Entry(showPrivateKeysPasswordWindow, width=50)


    buttonDone = Button(showPrivateKeysPasswordWindow, text="Done",
                        command=lambda: showPrivateKeysWindow(keys,sha1_hash(entryPassword.get())))

    # Pozicioniranje
    labelInfo.grid(row=0, column=0, columnspan=2, pady=3, padx=50)
    entryPassword.grid(row=1, column=0, columnspan=2, pady=20, padx=50)
    buttonDone.grid(row=2, column=0, columnspan=2, pady=20, padx=50)


def showPrivateKeysWindow(keys,sifra):

    print("Sifra sa kojom poredim polje keys:"+sifra)
    if sifra != keys[0].hashedPassphrade:
        print(keys[0].hashedPassphrade)
        print("NE POKLAPA SE")
    else:
        global showPrivateKeysWindow

        showPrivateKeysWindow = Tk()
        showPrivateKeysWindow.title("All your private keys")
        frm = Frame(showPrivateKeysWindow)
        frm.pack(side=tkinter.LEFT, padx=20)
        tv = ttk.Treeview(frm, columns=(1, 2), show="headings", height="5")
        tv.pack()


        tv.heading(1, text="Algorithm")
        tv.heading(2, text="Decrypted Private Key")




        for el in keys:
            privateKey = 0
            if(el.algorithm == "Rsa"):
                privateKey = str(RSA.import_key(el.EcryptedPrivateKey, passphrase= el.hashedPassphrade))
            elif(el.algorithm == "Dsa"):
                privateKey = str(DSA.import_key(el.hashedPassphrade, passphrase= el.hashedPassphrade))
            elif(el.algorithm == "ElGamal"):
                privateKey = "..."



            polje = [el.algorithm,privateKey]
            tv.insert('', 'end', values=polje)