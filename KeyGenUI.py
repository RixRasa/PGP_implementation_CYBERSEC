from tkinter import *
from KeyGenImplementation import *
import re



def KeyGeneratorWindow():

    #Novi window
    global keyGeneratorInputWindow
    keyGeneratorInputWindow = Toplevel()
    keyGeneratorInputWindow.title("Key Gen")

    #Generisanje widgeta
    labelInfo = Label(keyGeneratorInputWindow, text ="Enter credentials:")

    labelName = Label(keyGeneratorInputWindow, text ="Enter name: ", bd = 1, relief="sunken")
    entryName = Entry(keyGeneratorInputWindow, width = 100 )

    labelEmail = Label(keyGeneratorInputWindow, text="Enter Email: ", bd = 1, relief="sunken")
    entryEmail = Entry(keyGeneratorInputWindow, width = 100)

    r = IntVar()
    chooseAlgorithhmRsa = Radiobutton(keyGeneratorInputWindow, text ="Rsa", variable=r, value = 1)
    chooseAlgorithhmDsa = Radiobutton(keyGeneratorInputWindow, text="DSA", variable=r, value=2)
    chooseAlgorithhmElGamal = Radiobutton(keyGeneratorInputWindow, text="ElGamal", variable=r, value=3)

    buttonDone = Button(keyGeneratorInputWindow, text ="Generate", command = lambda: PasswordWindow(entryName.get(), entryEmail.get(), r.get()))


    #Pozicioniranje
    labelInfo.grid(row = 0, column=0, columnspan=3, pady = 10)

    labelName.grid(row = 1, column=0, columnspan=3, pady = 3)
    entryName.grid(row = 2, column= 0, columnspan=3, pady = 10, padx = 10)

    labelEmail.grid(row=3, column=0, columnspan=3, pady=3)
    entryEmail.grid(row = 4, column= 0, columnspan=3, pady = 10)

    chooseAlgorithhmRsa.grid(row = 5, column= 0 , padx = 10, pady = 10)
    chooseAlgorithhmDsa.grid(row = 5, column= 1, pady = 10)
    chooseAlgorithhmElGamal.grid(row = 5, column= 2, pady = 10)

    buttonDone.grid(row = 6, column= 0, columnspan=3, pady = 10)


def PasswordWindow(name, email, algorithm):
    keyGeneratorInputWindow.destroy()

    #Provera Regexa
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if name == "":
        KeyGeneratorWindow()
    elif email == "" or (not re.fullmatch(regex, email)):
        KeyGeneratorWindow()

    # Novi window
    global keyGeneratorPasswordWindow
    keyGeneratorPasswordWindow = Toplevel()
    keyGeneratorPasswordWindow.title("password")

    # Generisanje widgeta
    labelInfo = Label(keyGeneratorPasswordWindow, text="Enter your password")
    entryPassword = Entry(keyGeneratorPasswordWindow, width = 50)

    buttonDone = Button(keyGeneratorPasswordWindow, text ="Done", command = lambda: GenerateKey(name, email, entryPassword.get(), algorithm))

    # Pozicioniranje
    labelInfo.grid(row=0, column=0, columnspan=2, pady=3, padx = 50)
    entryPassword.grid(row=1, column=0, columnspan=2, pady=20, padx = 50)
    buttonDone.grid(row=2, column=0, columnspan=2, pady = 20, padx = 50)

def GenerateKey(name, email, password, algorithm):
    keyGeneratorPasswordWindow.destroy()
    if password == "":
        PasswordWindow(name, email, algorithm)
    else:
        GeneratingKey(name, email, password, algorithm)

