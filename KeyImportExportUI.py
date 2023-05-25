from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile, askopenfilename
import time
from KeyImportExportImplementation import importKey
from KeyGenImplementation import *
import os


#Pomocne Funkcije


def open_file_export(value):
    file_path = askopenfilename()
    print(file_path)
    with open(file_path,"wb") as file:
        file.write(value)
        file.close()

def uploadFiles():
    pb1 = Progressbar(keyImportWindow, orient=HORIZONTAL, length=300, mode='determinate')
    pb1.grid(row=4, columnspan=3, pady=20)

    for i in range(5):
        keyImportWindow.update_idletasks()
        pb1['value'] += 20
        time.sleep(1)
    pb1.destroy()
    Label(keyImportWindow, text='Key Imported Successfully!', foreground='green').grid(row=4, columnspan=3, pady=10)


#UI Logika
def KeyImportUI():
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
    buttonChoose = Button(keyImportWindow, text='Choose Key', command=lambda: open_file())
    buttonUpload = Button(keyImportWindow, text='Import Key', command=uploadFiles)

    labelName.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
    entryName.grid(row=1, column=0, columnspan=3, padx=20, pady=(5,25))

    labelEmail.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
    entryEmail.grid(row=3, column=0, columnspan=3, padx=20, pady=(5,25))

    labelPassword.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
    entryPassword.grid(row=5, column=0, columnspan=3, padx=20, pady=(5,25))

    labelUpload.grid(row=6, column=0, padx=20, pady=25)
    buttonChoose.grid(row=6, column=1, padx=20, pady=25)
    buttonUpload.grid(row=7, columnspan=3, pady=10)

    keyImportWindow.mainloop()



def CredentialsForExportWindow():

    #print(hashedPassphrase)
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

    buttonDone = Button(credentialsForExportWindow, text="Export",
                        command=lambda: ExportKyesWindow(entryName.get(), entryEmail.get()))


    # Pozicioniranje
    labelInfo.grid(row=0, column=0, columnspan=2, pady=10)

    labelName.grid(row=1, column=0, columnspan=2, pady=3)
    entryName.grid(row=2, column=0, columnspan=2, pady=10)

    labelEmail.grid(row=3, column=0, columnspan=2, pady=3)
    entryEmail.grid(row=4, column=0, columnspan=2, pady=10)

    buttonDone.grid(row=6, column=0, columnspan=2, pady=10)


def export_file_with_contents(contents, file_type, filename, export_path):
    try:
        file_path = os.path.join(export_path, f"{filename}.{file_type}")
        with open(file_path, "w") as file:
            file.write(contents)
        print(f"File '{filename}.{file_type}' successfully exported with contents.")
    except Exception as e:
        print(f"Error exporting file: {e}")
def get_first_column_value(row):
    value = table[row][0]
    global keyExportWindow
    keyExportWindow = Toplevel()
    keyExportWindow.title("Key Import Window")

    labelUpload = Label(keyExportWindow, text='Choose where you will export key')
    buttonChoose = Button(keyExportWindow, text='Choose file location', command=lambda: open_file_export(value))


    labelUpload.grid(row=0, column=0, padx=20, pady=25)
    buttonChoose.grid(row=0, column=1, padx=20, pady=25)




    print("Public key:", value)

def get_second_column_value(row):
    value = table[row][1]
    global keyExportWindow
    keyExportWindow = Toplevel()
    keyExportWindow.title("Key Import Window")

    labelUpload = Label(keyExportWindow, text='Choose where you will export key')
    buttonChoose = Button(keyExportWindow, text='Choose file location', command=lambda: open_file_export(value))


    labelUpload.grid(row=0, column=0, padx=20, pady=25)
    buttonChoose.grid(row=0, column=1, padx=20, pady=25)




    print("Private key:", value)



def create_table(keys):
    global table

    table=[]
    for el in keys:
        table.append([el.EcryptedPrivateKey, el.publicKey])
    #table = [
        #["Data 1A", "Data 1B"],
        #["Data 2A", "Data 2B"],
        #["Data 3A", "Data 3B"],
        #["Data 4A", "Data 4B"]
    #]

    for i, row in enumerate(table):
        for j, value in enumerate(row):
            label =Label(root, text=value[0:200])
            label.grid(row=i, column=j, padx=10, pady=5)

        first_button = Button(root, text="Export public key", command=lambda row=i: get_first_column_value(row))
        first_button.grid(row=i, column=len(row))

        second_button = Button(root, text="Export private key", command=lambda row=i: get_second_column_value(row))
        second_button.grid(row=i, column=len(row) + 1)
def ExportKyesWindow(name,email):
    credentialsForExportWindow.destroy()
    global root
    root = Tk()
    # Create the table

    keys = dictionaryOfPrivateKeyRings.get(email + name)
    create_table(keys)

    # Start the main event loop
    root.mainloop()