from tkinter import *

def SendMessageOptions():
    global sendMessageOptionsWindow
    sendMessageOptionsWindow = Toplevel()
    sendMessageOptionsWindow.title("Sending message")

    #Generating Widgets for Sender
    labelInfoSender = Label(sendMessageOptionsWindow, text="Enter informations of SENDER:")

    labelNameSender = Label(sendMessageOptionsWindow, text="Enter name of sender: ", relief="sunken")
    entryNameSender = Entry(sendMessageOptionsWindow, width=100)

    labelEmailSender = Label(sendMessageOptionsWindow, text="Enter Email of sender: ", relief="sunken")
    entryEmailSender = Entry(sendMessageOptionsWindow, width=100)

    r = IntVar()
    chooseAlgorithhmRsa = Radiobutton(sendMessageOptionsWindow, text="Rsa", variable=r, value=1)
    chooseAlgorithhmDsa = Radiobutton(sendMessageOptionsWindow, text="DSA / ElGamal", variable=r, value=2)

    #Generating Widgets for Receiver
    labelInfoReceiver = Label(sendMessageOptionsWindow, text="Enter informations of RECIEVER:")

    labelNameReceiver = Label(sendMessageOptionsWindow, text="Enter name of sender: ", relief="sunken")
    entryNameReceiver = Entry(sendMessageOptionsWindow, width=100)

    labelEmailReceiver = Label(sendMessageOptionsWindow, text="Enter Email of sender: ", relief="sunken")
    entryEmailReceiver = Entry(sendMessageOptionsWindow, width=100)

    #Generating Widgets for Options
    labelInfoOptions = Label(sendMessageOptionsWindow, text="Check services you want to use:")
    security = IntVar()
    signature = IntVar()
    compression = IntVar()
    conversion = IntVar()
    securityCheck = Checkbutton(sendMessageOptionsWindow, text="security", variable=security)
    signatureCheck = Checkbutton(sendMessageOptionsWindow, text="signature", variable=signature)
    compressionCheck = Checkbutton(sendMessageOptionsWindow, text="compression", variable=compression)
    conversionCheck = Checkbutton(sendMessageOptionsWindow, text="conversion", variable=conversion)

    #Button done
    buttonDone = Button(sendMessageOptionsWindow, text="Export", command=lambda: ChooseKeys(entryNameSender.get(), entryEmailSender.get(), r.get()
                                                                                            , entryNameReceiver.get(), entryEmailReceiver.get()
                                                                                            , security.get(), signature.get(), compression.get(), conversion.get()))

    #Positioning widgets
    labelInfoSender.grid(row=0, column=0, columnspan=4, pady=10)

    labelNameSender.grid(row=1, column=0, columnspan=4, pady=3)
    entryNameSender.grid(row=2, column=0, columnspan=4, pady=10)

    labelEmailSender.grid(row=3, column=0, columnspan=4, pady=3)
    entryEmailSender.grid(row=4, column=0, columnspan=4, pady=10)

    chooseAlgorithhmRsa.grid(row = 5,column=0 ,columnspan=2, pady= (3,50))
    chooseAlgorithhmDsa.grid(row=5, column=2, columnspan=2, pady= (3,50))

    labelInfoReceiver.grid(row=6, column=0, columnspan=4, pady=10)

    labelNameReceiver.grid(row=7, column=0, columnspan=4, pady=3)
    entryNameReceiver.grid(row=8, column=0, columnspan=4, pady=10)

    labelEmailReceiver.grid(row=9, column=0, columnspan=4, pady=3)
    entryEmailReceiver.grid(row=10, column=0, columnspan=4, pady=(3,70))

    labelInfoOptions.grid(row = 11, column=0, columnspan=4, pady = (20,3))
    securityCheck.grid(row = 12 , column=0,pady = (3,20))
    signatureCheck.grid(row=12, column=1,pady = (3,20))
    compressionCheck.grid(row=12, column=2,pady = (3,20))
    conversionCheck.grid(row=12, column=3,pady = (3,20))

    buttonDone.grid(row = 13, columnspan=4, pady = 40)

def ChooseKeys(nameSender, emailSender, algorithm, nameReceiver, emailReceiver, security, signature, compression, conversion):
    print("kurcina")