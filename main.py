from tkinter import *
from KeyGenUI import KeyGeneratorWindow
from SeeAllKeysUI import *

from KeyImportExportUI import KeyImportUI,CredentialsForExportWindow
#Funkcije buttona (Odvajacemo logiku od izgleda)
def KeyGen():
    KeyGeneratorWindow()

def ListKeys():
    AllKeysWindow()
    print("List of Keys -  not yet implemented")

def SendMsg():
    print("Sending a Message  - not yet implemented")

def KeyImport():
    KeyImportUI()

def KeyExport():
    #print("kita")
    CredentialsForExportWindow()


global root
root = Tk()
root.eval('tk::PlaceWindow . center')
root.title('Cyber Security PGP Project')

#Ovde pravimo widgete i dajemo im atribute
main_label = Label(root, text = "Choose what do you want to do?", padx = 100 , bd = 1 ,relief="sunken")
buttonKeyGen = Button(root, text = "Generate new pair of keys" , command=KeyGen)
buttonImportKey = Button(root, text = "Import Keys" , command=KeyImport)
buttonExportKey = Button(root, text = "Export Keys" , command=KeyExport)
buttonListOfKeys = Button(root, text = "See all keys.", command = ListKeys)
buttonSendAMsg = Button(root, text = "Send a Message.", command = SendMsg)

#Ovde postavljamo widgete na ekran i biramo gde ce da se nalaze
main_label.grid(row = 0, column = 0, pady = 10)
buttonKeyGen.grid(row = 1, column = 0, pady = 10)
buttonImportKey.grid(row = 2, column = 0, pady = 10)
buttonExportKey.grid(row = 3, column = 0, pady = 10)
buttonListOfKeys.grid(row = 4, column = 0, pady = 10)
buttonSendAMsg.grid(row = 5, column = 0, pady = 10)

#Ovaj main loop je potreban kako bi konstantno mogao da se runnuje gui
root.mainloop()



'''from Crypto.PublicKey import RSA

def export_private_key(private_key, filename):
    with open(filename, "wb") as file:
        file.write(private_key.exportKey('PEM', 'MyPassphrase'))

def export_public_key(public_key, filename):
    with open(filename,"wb") as file:
        file.write(public_key.exportKey('PEM'))
        file.close()

keypair = RSA.generate(1024)
public_key = keypair.public_key()


export_public_key(keypair, 'private_key.pem')
export_public_key(public_key, 'public_key.pem')

string = "kurac"'''




