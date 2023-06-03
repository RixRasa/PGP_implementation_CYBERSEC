from tkinter import *
from tkinter.filedialog import askopenfilename
from SendReceiveMessageImpl import SendMessage,ReceiveMessage
from KeyGenImplementation import dictionaryOfPrivateKeyRings, dictionaryOfPublicKeyRings



################################################## RECEIVE - UI ##########################################################
def ReceiveUI():
    global receiveWindow
    receiveWindow = Toplevel()
    receiveWindow.title("Receive message")

    #Generating Wigdets
    labelNameReceiver = Label(receiveWindow, text="Who is Receiving message:")
    entryNameReceiver = Entry(receiveWindow, width=100)

    fileLabel = Label(receiveWindow, text="Choose file where message is:")
    fileButton = Button(receiveWindow, text="ChooseLocation", command=lambda: ChooseFile())

    receiveButton = Button(receiveWindow, text="Receive", command=lambda: ReceiveMessageUI(entryNameReceiver.get(), fileName))

    #Positioning
    labelNameReceiver.grid(row=1, column=0, columnspan=4, pady=3)
    entryNameReceiver.grid(row=2, column=0, columnspan=4, pady=10)

    fileLabel.grid(row=3, column=0, columnspan=4, pady=3)
    fileButton.grid(row=4, column=0, columnspan=4, pady=3)

    receiveButton.grid(row=5, column=0, columnspan=4, pady=3)


def ReceiveMessageUI(name, filename):
    ReceiveMessage(name, filename)


################################################## SEND - UI ##########################################################
def SendUI():
    global sendMessageOptionsWindow
    sendMessageOptionsWindow = Toplevel()
    sendMessageOptionsWindow.title("Sending message")

    #Generating Widgets for Sender
    labelInfoSender = Label(sendMessageOptionsWindow, text="Enter informations of SENDER:")

    labelNameSender = Label(sendMessageOptionsWindow, text="Enter name of sender: ", relief="sunken")
    entryNameSender = Entry(sendMessageOptionsWindow, width=100)

    rAsymm = IntVar()
    chooseAlgorithhmRsa = Radiobutton(sendMessageOptionsWindow, text="Rsa", variable=rAsymm, value=1)
    chooseAlgorithhmDsa = Radiobutton(sendMessageOptionsWindow, text="DSA / ElGamal", variable=rAsymm, value=2)

    rSymm = IntVar()
    chooseAlgorithhmAes = Radiobutton(sendMessageOptionsWindow, text="Aes", variable=rSymm, value=1)
    chooseAlgorithhmCast = Radiobutton(sendMessageOptionsWindow, text="Cast", variable=rSymm, value=2)

    #Message
    # Text Widget
    messageLabel = Label(sendMessageOptionsWindow, text="Enter the message to the reciever:")
    message = Text(sendMessageOptionsWindow, width=100, height=5)

    fileLabel = Label(sendMessageOptionsWindow, text="Choose file where you will send a message:")
    fileButton = Button(sendMessageOptionsWindow, text = "ChooseLocation", command=lambda : ChooseFile())

    #Generating Widgets for Receiver
    labelInfoReceiver = Label(sendMessageOptionsWindow, text="Enter informations of RECIEVER:")

    labelNameReceiver = Label(sendMessageOptionsWindow, text="Enter name of sender: ", relief="sunken")
    entryNameReceiver = Entry(sendMessageOptionsWindow, width=100)


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
    buttonDone = Button(sendMessageOptionsWindow, text="Send", command=lambda: ChooseKeys(entryNameSender.get(), entryNameReceiver.get(), rSymm.get(), rAsymm.get(), message.get('1.0', 'end'),
                                                                                           signature.get(), security.get(), compression.get(), conversion.get()))

    #Positioning widgets
    #Sender
    labelInfoSender.grid(row=0, column=0, columnspan=4, pady=10)

    labelNameSender.grid(row=1, column=0, columnspan=4, pady=3)
    entryNameSender.grid(row=2, column=0, columnspan=4, pady=10)

    chooseAlgorithhmRsa.grid(row = 3,column=0 ,columnspan=2, pady= (3,20))
    chooseAlgorithhmDsa.grid(row=3, column=2, columnspan=2, pady= (3,20))

    chooseAlgorithhmAes.grid(row=4, column=0, columnspan=2, pady=(3, 20))
    chooseAlgorithhmCast.grid(row=4, column=2, columnspan=2, pady=(3, 20))


    #Message
    messageLabel.grid(row=5, column=0, columnspan=4, pady=(40, 5))
    message.grid(row=6, column=0, columnspan=4, pady=(5, 10))

    fileLabel.grid(row=7, column=0, columnspan=4, pady=(5, 5))
    fileButton.grid(row=8, column=0, columnspan=4, pady=(5, 40))

    #Receiver
    labelInfoReceiver.grid(row=9, column=0, columnspan=4, pady=10)

    labelNameReceiver.grid(row=10, column=0, columnspan=4, pady=3)
    entryNameReceiver.grid(row=11, column=0, columnspan=4, pady=10)

    labelInfoOptions.grid(row = 12, column=0, columnspan=4, pady = (20,3))
    securityCheck.grid(row = 13 , column=0,pady = (3,20))
    signatureCheck.grid(row=13, column=1,pady = (3,20))
    compressionCheck.grid(row=13, column=2,pady = (3,20))
    conversionCheck.grid(row=13, column=3,pady = (3,20))


    buttonDone.grid(row = 14, columnspan=4, pady = 40)


def SendMessageUI(senderName, receiverName, symmAlgoritham, asymmAlgorihtm, message, signature, security, compression,
                  conversion):
    privateKey = keysPrivateRing[idPrivateKey]
    publicKey = keysPublicRing[idPublicKey]

    SendMessage(privateKey, publicKey, senderName, receiverName, symmAlgoritham, message, signature, security,
                compression, conversion, fileName)



################################################## CHOOSE ##########################################################
idPrivateKey = -1
idPublicKey = -1
fileName = "randomfile.pem"

def ChooseKeys(senderName, receiverName, symmAlgoritham, asymmAlgorihtm, message, signature, security, compression, conversion):
    sendMessageOptionsWindow.destroy()

    global root
    root = Toplevel()

    global keysPrivateRing; global keysPublicRing
    keysPrivateRing = dictionaryOfPrivateKeyRings.get(senderName)
    keysPublicRing = dictionaryOfPublicKeyRings.get(senderName)

    global table1
    table1 = []
    for el in keysPrivateRing:
            table1.append([el.EcryptedPrivateKey, el.publicKey, el.algorithm, el.userId])

    global table2
    table2 = []
    for el in keysPublicRing:
            table2.append([el.publicKey, el.algorithm, el.userId])


    for i, row in enumerate(table1):
        if row[2] == ("Rsa" if asymmAlgorihtm == 1 else "Dsa"):
            for j, value in enumerate(row):
                label = Label(root, text=value[0:200])
                label.grid(row=i, column=j, padx=10, pady=5)

            first_button = Button(root, text="Choose this private key", command= lambda id = i : ChoosePrivate(id))
            first_button.grid(row=i, column=len(row), padx=5)

    for i, row in enumerate(table2):
        if row[1] == ("Rsa" if asymmAlgorihtm == 1 else "ElGamal"):
            print("Ovde")
            for j, value in enumerate(row):
                label = Label(root, text=value[0:200])
                label.grid(row=i + len(table1), column=j, padx=10, pady=5)

            first_button = Button(root, text="Choose this public key", command= lambda id = i : ChoosePublic(id))
            first_button.grid(row=i + len(table1), column=len(row), padx=5)


    buttonSend = Button(root, text = "Send", command = lambda : SendMessageUI(senderName, receiverName, symmAlgoritham, asymmAlgorihtm, message, signature, security, compression, conversion))
    buttonSend.grid(row = len(table1) + len(table2) + 1, column = 0, columnspan= 3, pady = (20,20))

def ChooseFile():
    global fileName
    fileName = askopenfilename()

def ChoosePrivate(id):
    global idPrivateKey
    idPrivateKey = id
    print(id)

def ChoosePublic(id):
    global idPublicKey
    idPublicKey = id
    print(id)
