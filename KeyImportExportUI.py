from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile, askopenfilename
from KeyImportExportImplementation import importKey
from KeyGenImplementation import *





def open_file_import():
    file_path = askopenfilename()
    print(file_path)



#UI Logika
def CredentialsForImportWindow():
    global keyImportWindow
    keyImportWindow = Toplevel()
    keyImportWindow.title("Key Import Window")

    labelName = Label(keyImportWindow, text="Enter name: " )
    entryName = Entry(keyImportWindow, width=100)

    labelEmail = Label(keyImportWindow, text="Enter Email: ")
    entryEmail = Entry(keyImportWindow, width=100)

    labelPassword = Label(keyImportWindow, text="If you are importing private key please provide us your passphrase:")
    entryPassword = Entry(keyImportWindow, width=50)

    labelUpload = Label(keyImportWindow, text='Import Public or Private Key')
    buttonChoose = Button(keyImportWindow, text='Choose Key', command=lambda: open_file_import())

    #Pozicioniranje
    labelName.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
    entryName.grid(row=1, column=0, columnspan=3, padx=20, pady=(5,25))

    labelEmail.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
    entryEmail.grid(row=3, column=0, columnspan=3, padx=20, pady=(5,25))

    labelPassword.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
    entryPassword.grid(row=5, column=0, columnspan=3, padx=20, pady=(5,25))

    labelUpload.grid(row=6, column=0, padx=20, pady=25)
    buttonChoose.grid(row=6, column=1, padx=20, pady=25)

    keyImportWindow.mainloop()



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

    labelEmail = Label(credentialsForExportWindow, text="Enter Email: ", relief="sunken")
    entryEmail = Entry(credentialsForExportWindow, width=100)

    buttonDone = Button(credentialsForExportWindow, text="Export", command=lambda: ExportKeysWindow(entryName.get(), entryEmail.get()))

    # Pozicioniranje
    labelInfo.grid(row=0, column=0, columnspan=2, pady=10)

    labelName.grid(row=1, column=0, columnspan=2, pady=3)
    entryName.grid(row=2, column=0, columnspan=2, pady=10)

    labelEmail.grid(row=3, column=0, columnspan=2, pady=3)
    entryEmail.grid(row=4, column=0, columnspan=2, pady=10)

    buttonDone.grid(row=6, column=0, columnspan=2, pady=10)

def ExportKeysWindow(name,email):
    credentialsForExportWindow.destroy()

    global root
    root = Toplevel()
    # Create the table

    keys = dictionaryOfPrivateKeyRings.get(email + name)

    table = []
    for el in keys:
        table.append([el.EcryptedPrivateKey, el.publicKey, el.algorithm, el.userId])

    for i, row in enumerate(table):
        for j, value in enumerate(row):
            label = Label(root, text=value[0:200])
            label.grid(row=i, column=j, padx=10, pady=5)

        first_button = Button(root, text="Export private key", command= lambda : open_file_export(row[0], row[2], row[3], b'private'))
        first_button.grid(row=i, column=len(row), padx=5)

        second_button = Button(root, text="Export public key", command=lambda : open_file_export(row[1], row[2], row[3], b'public'))
        second_button.grid(row=i, column=len(row) + 1)

    # Start the main event loop

def open_file_export(value, algorithm, userId, prORpb):
    file_path = askopenfilename()
    with open(file_path,"wb") as file:
        file.write(prORpb + b'*' +algorithm.encode('utf-8') + b'*' + userId.encode('utf-8') + b'*' + value)
        file.close()
'''def get_first_column_value(row):
    value = table[row][0]
    global keyExportWindow
    keyExportWindow = Toplevel()
    keyExportWindow.title("Key Import Window")

    labelUpload = Label(keyExportWindow, text='Choose where you will export key')
    buttonChoose = Button(keyExportWindow, text='Choose file location', command=lambda: open_file_export(value))


    labelUpload.grid(row=0, column=0, padx=20, pady=25)
    buttonChoose.grid(row=0, column=1, padx=20, pady=25)

    print("Public key:", value)'''

