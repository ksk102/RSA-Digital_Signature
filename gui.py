from PySide2 import QtCore, QtWidgets, QtGui

# Signal and Slot function
class GuiSignal(QtCore.QObject):
  emailReady = QtCore.Signal(str)
  messageOnKeyPress = QtCore.Signal(str)


class GuiDigitalSignature(QtWidgets.QWidget):
  def __init__(self):
    super().__init__()

    self.windowClosing = False
    self.guiSignal = GuiSignal()

    self.InitGui()


  def closeEvent(self, event):
    self.windowClosing = True
    return super().closeEvent(event)


  def Alert(self, message):
    alert = QtWidgets.QMessageBox()
    alert.warning(self, "Error", message)


  def InitGui(self):
    self.InitTitleAndWindow() # Initialise Title and Window of the interface
    self.InitLayout() # Initialise the overall layout of the Window


  def InitTitleAndWindow(self):
    # Set Window Title
    title = "Digital Signature Implementation Demostration - RSA (PSS)"
    self.setWindowTitle(title)
    # Icons made by Icongeek26 "https://www.flaticon.com/authors/icongeek26"
    # from "https://www.flaticon.com/" 
    # is licensed by Creative Commons BY 3.0
    self.setWindowIcon(QtGui.QIcon('images/icon.png'))

    # Set Window Size
    windowSize = QtCore.QSize(800, 600) 

    # Put Window onto center of the device
    screen = QtGui.QGuiApplication.primaryScreen()
    screenGeometry = screen.geometry() # Get device's screen size
    self.setGeometry(QtWidgets.QStyle.alignedRect(QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter, windowSize, screenGeometry))

  
  def InitLayout(self):
    # Outermost Layout of the Window
    mainLayout = QtWidgets.QGridLayout() 
    
    # Set same width for both of the main content areas (Sender and Receiver)
    mainLayout.setColumnStretch(0, 1)
    mainLayout.setColumnStretch(2, 1)
    # Beautifying the vertical separate line between sender and receiver
    mainLayout.setColumnMinimumWidth(1, 30)
    # Beautifying the space between the upper and lower part (PKI)
    mainLayout.setRowMinimumHeight(1, 30)
    # Set the Height for PKI content area
    mainLayout.setRowMinimumHeight(2, 160)

    # Initialise the three main content areas
    senderLayout = self.SetSenderLayout()
    receiverLayout = self.SetReceiverLayout()
    PkiLayout = self.SetPkiLayout()

    # Put each main content area into the row and column accordingly
    mainLayout.addLayout(senderLayout, 0, 0)
    mainLayout.addLayout(receiverLayout, 0, 2)
    mainLayout.addLayout(PkiLayout, 2, 0, 1, 0)

    # Draw the vertical separate line
    vline = QtWidgets.QFrame()
    vline.setFrameShape(QtWidgets.QFrame.VLine)
    vline.setStyleSheet("color: grey")
    # Put the separate line to the space between sender and receiver
    mainLayout.addWidget(vline, 0, 1, QtCore.Qt.AlignHCenter)

    # Initialise the layout
    self.setLayout(mainLayout)


  def SetSenderLayout(self):
    # Email Edit Field validation
    def ValidateEmail(sender):
      if self.windowClosing is True:
        return

      rx = QtCore.QRegExp("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$")
      emailValidator = QtGui.QRegExpValidator(rx, self)

      if (emailValidator.validate(sender.text(), 0)[0] != QtGui.QValidator.State.Acceptable):
        self.Alert("Invalid Email!")
        sender.setStyleSheet('background-color: #ffcdd2; ')
        sender.setFocus()
      else:
        sender.setStyleSheet('background-color: white; ')
        messageEdit.setFocus()
        self.guiSignal.emailReady.emit(emailEdit.text())

    # Validate Message Edit field
    def ValidateMessage(sender):
      if self.windowClosing is True:
        return

      if sender.toPlainText().strip() == "":
        self.Alert("Message must not be empty")
        sender.setStyleSheet('background-color: #ffcdd2; ')
        sender.setFocus
      else:
        sender.setStyleSheet('background-color: white; ')

    
    def ValidateInput():
      ValidateEmail(emailEdit)
      ValidateMessage(messageEdit)

    def EmitMessageChangeSignal(sender):
      if sender.toPlainText().strip() == "":
        self.hash.setText("")
      else:
        self.guiSignal.messageOnKeyPress.emit(sender.toPlainText())

    # main layout for the Sender content area
    layout = QtWidgets.QVBoxLayout()

    # set the title for the Sender content area
    titleLabel = QtWidgets.QLabel("Sender")
    layout.addWidget(titleLabel)
    
    # Email Edit Field
    emailEdit = QtWidgets.QLineEdit()
    emailEdit.setPlaceholderText("Sender's Email")
    emailEdit.setToolTip("Sender's Email")
    emailEdit.editingFinished.connect(lambda: ValidateEmail(emailEdit)) # Email Edit onblur
    layout.addWidget(emailEdit)

    # Public and Private Keys label
    keysLabel = QtWidgets.QLabel("Keys")
    layout.addWidget(keysLabel)
    # Public and Private keys edit field
    publicEdit = QtWidgets.QTextEdit()
    publicEdit.setPlaceholderText("Public Key")
    publicEdit.setReadOnly(True)
    publicEdit.setToolTip("Public Key")
    privateEdit = QtWidgets.QTextEdit()
    privateEdit.setPlaceholderText("Private Key")
    privateEdit.setReadOnly(True)
    privateEdit.setToolTip("Private Key")
    # Layout for public and private keys
    keysLayout = QtWidgets.QHBoxLayout()
    keysLayout.addWidget(publicEdit)
    keysLayout.addWidget(privateEdit)
    layout.addLayout(keysLayout)
    # Export keys
    self.publicKey = publicEdit
    self.privateKey = privateEdit

    # Message label
    messageLabel = QtWidgets.QLabel("Message")
    layout.addWidget(messageLabel)
    # Message edit field
    messageEdit = QtWidgets.QTextEdit()
    messageEdit.textChanged.connect(lambda: EmitMessageChangeSignal(messageEdit)) # messageEdit onkeypress
    layout.addWidget(messageEdit)
    
    # Hash label
    hashLabel = QtWidgets.QLabel("Hash")
    layout.addWidget(hashLabel)
    # Hash edit field
    hashEdit = QtWidgets.QTextEdit()
    hashEdit.setReadOnly(True)
    layout.addWidget(hashEdit)
    # export hash edit field
    self.hash = hashEdit

    # Signature label
    signLabel = QtWidgets.QLabel("Signature")
    layout.addWidget(signLabel)
    # Signature edit field
    signEdit = QtWidgets.QTextEdit()
    signEdit.setReadOnly(True)
    layout.addWidget(signEdit)

    # Send Button
    sendButton = QtWidgets.QPushButton("Send")
    sendButton.clicked.connect(ValidateInput) # sendButton onclicked
    layout.addWidget(sendButton)

    return layout


  def SetReceiverLayout(self):
    # main layout for receiver's content area
    layout = QtWidgets.QVBoxLayout()
    # set title for the receiver's content area
    titleLabel = QtWidgets.QLabel("Receiver")
    layout.addWidget(titleLabel)

    # Signed Document edit Field
    signedEdit = QtWidgets.QTextEdit()
    signedEdit.setPlaceholderText("Retrieved Signed Document")
    signedEdit.setToolTip("Retrieved Signed Document")
    layout.addWidget(signedEdit)

    # Sender's Public Key label
    publicLabel = QtWidgets.QLabel("Sender's Public Key")
    layout.addWidget(publicLabel)
    # Sender's public key edit field
    publicEdit = QtWidgets.QTextEdit()
    publicEdit.setReadOnly(True)
    layout.addWidget(publicEdit)

    # Message and Signature label
    messageLabel = QtWidgets.QLabel("Message")
    signatureLabel = QtWidgets.QLabel("Signature")
    # Message and Signature edit field
    messageEdit = QtWidgets.QTextEdit()
    messageEdit.setReadOnly(True)
    signatureEdit = QtWidgets.QTextEdit()
    signatureEdit.setReadOnly(True)
    # wrapper layout for message and signature
    messageSignatureLayout = QtWidgets.QHBoxLayout()
    # message layout
    messageLayout = QtWidgets.QVBoxLayout()
    messageLayout.addWidget(messageLabel)
    messageLayout.addWidget(messageEdit)
    # signature layout
    signatureLayout = QtWidgets.QVBoxLayout()
    signatureLayout.addWidget(signatureLabel)
    signatureLayout.addWidget(signatureEdit)
    # bring both message and signature layout to the wrapper layout
    messageSignatureLayout.addLayout(messageLayout)
    messageSignatureLayout.addLayout(signatureLayout)
    # bring the wrapper layout to main layout
    layout.addLayout(messageSignatureLayout)

    # Generated Hash and Retrieved Hash label
    generateLabel = QtWidgets.QLabel("Generated Hash")
    retrieveLabel = QtWidgets.QLabel("Retrieved Hash")
    # Generated Hash and Retrieved Hash edit field
    generateEdit = QtWidgets.QTextEdit()
    generateEdit.setReadOnly(True)
    retrieveEdit = QtWidgets.QTextEdit()
    retrieveEdit.setReadOnly(True)
    # wrapper layout for both hashes
    hashLayout = QtWidgets.QHBoxLayout()
    # generated hash's layout
    generateLayout = QtWidgets.QVBoxLayout()
    generateLayout.addWidget(generateLabel)
    generateLayout.addWidget(generateEdit)
    # retrieved hash's layout
    retrieveLayout = QtWidgets.QVBoxLayout()
    retrieveLayout.addWidget(retrieveLabel)
    retrieveLayout.addWidget(retrieveEdit)
    # bring both hashes layout to wrapper layout
    hashLayout.addLayout(generateLayout)
    hashLayout.addLayout(retrieveLayout)
    # bring wrapper layout to main layout
    layout.addLayout(hashLayout)

    # Verified Indicator
    verifiedIndicate = QtWidgets.QLineEdit()
    verifiedIndicate.setReadOnly(True)
    verifiedIndicate.setAlignment(QtCore.Qt.AlignHCenter)
    layout.addWidget(verifiedIndicate)

    return layout


  def SetPkiLayout(self):
    # main layout for PKI part
    layout = QtWidgets.QVBoxLayout()
    # set title for the PKI part
    titleLabel = QtWidgets.QLabel("PKI")
    layout.addWidget(titleLabel)

    # make scrollable layout wrapper
    scrollLayout = QtWidgets.QVBoxLayout()

    # items for pki
    emailEdit = []
    keyEdit = []
    # layout for each item pair
    itemLayout = []    

    for x in range(10):
      # add email and key edit fields
      emailEdit.insert(x, QtWidgets.QLineEdit())
      emailEdit[x].setReadOnly(True)
      keyEdit.insert(x, QtWidgets.QLineEdit())
      keyEdit[x].setReadOnly(True)
      keyEdit[x].setMinimumWidth(500)
      # add each email and key edit field into respective wrapper layout
      itemLayout.insert(x, QtWidgets.QHBoxLayout()) 
      itemLayout[x].addWidget(emailEdit[x])
      itemLayout[x].addWidget(keyEdit[x])

      # add each item layout into scrollable wrapper layout
      scrollLayout.addLayout(itemLayout[x])

    # convert scrollable wrapper layout to a widget, as QScrollArea accept only widget
    widget = QtWidgets.QWidget()
    widget.setMinimumWidth(700)
    widget.setLayout(scrollLayout)

    # add the widget above into the scrollable area
    scrollArea = QtWidgets.QScrollArea()
    scrollArea.setWidget(widget)
    scrollArea.setAlignment(QtCore.Qt.AlignHCenter)

    # add the scrollable area into the outermost main layout for the PKI
    layout.addWidget(scrollArea)

    return layout