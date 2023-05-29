from KeyGenUI import KeyGeneratorWindow
from SeeAllKeysUI import *
from KeyImportExportUI import CredentialsForImportWindow,CredentialsForExportWindow
from SendMessageUI import SendMessageOptions
#Funkcije buttona (Odvajacemo logiku od izgleda)
def KeyGen():
    KeyGeneratorWindow()

def ListKeys():
    AllKeys()

def KeyImport():
    CredentialsForImportWindow()

def KeyExport():
    #print("kita")
    CredentialsForExportWindow()

def SendMsg():
    SendMessageOptions()

def ReceiveMsg():
    print("Recive a Message - not yet implemented")


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
buttonReceiveAMsg = Button(root, text = "Receive a Message.", command = ReceiveMsg)

#Ovde postavljamo widgete na ekran i biramo gde ce da se nalaze
main_label.grid(row = 0, column = 0, pady = 10)
buttonKeyGen.grid(row = 1, column = 0, pady = 10)
buttonImportKey.grid(row = 2, column = 0, pady = 10)
buttonExportKey.grid(row = 3, column = 0, pady = 10)
buttonListOfKeys.grid(row = 4, column = 0, pady = 10)
buttonSendAMsg.grid(row = 5, column = 0, pady = 10)
buttonReceiveAMsg.grid(row = 6, column = 0, pady = 10)

#Ovaj main loop je potreban kako bi konstantno mogao da se runnuje gui
root.mainloop()







