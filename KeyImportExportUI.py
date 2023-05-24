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
    keyImportWindow.title("Key Gen")

    labelUpload = Label(keyImportWindow, text='Import Public or Private Key')
    labelUpload.grid(row=0, column=0, padx=20, pady = 30)

    buttonChoose = Button(keyImportWindow, text='Choose Key', command=lambda: open_file())
    buttonChoose.grid(row=0, column=1 , padx=20 ,pady = 30)

    buttonUpload = Button(keyImportWindow, text='Import Key', command=uploadFiles)
    buttonUpload.grid(row=3, columnspan=3, pady=20)

    keyImportWindow.mainloop()



def KeyExportUI():
    print("Kurac")