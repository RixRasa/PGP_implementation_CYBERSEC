from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile, askopenfilename
import time


#Pomocne Funkcije
def open_file():
    file_path = askopenfilename()
    print(file_path)
    if file_path is not None:
        pass

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



def KeyExportUI():
    global keyExportWindow
    keyExportWindow = Toplevel()
    keyExportWindow.title("Key Import Window")

    labelUpload = Label(keyExportWindow, text='Choose where you will export key')
    buttonChoose = Button(keyExportWindow, text='Choose file location', command=lambda: open_file())
    buttonUpload = Button(keyExportWindow, text='Export Key', command=uploadFiles)