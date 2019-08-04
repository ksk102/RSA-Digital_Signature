import sys
import random
from PySide2 import QtCore, QtWidgets, QtGui


class GuiDigitalSignature(QtWidgets.QWidget):
  def __init__(self):
    super().__init__()
    self.InitGui()


  def InitGui(self):
    self.InitTitleAndWindow() # Initialise Title and Window of the interface
    self.InitLayout() # Initialise the overall layout of the Window


  def InitTitleAndWindow(self):
    # Set Window Title
    title = "Digital Signature Implementation Demostration - RSA (PSS)"
    self.setWindowTitle(title)

    # Set Window Size
    windowSize = QtCore.QSize(800, 600) 

    # Put Window onto cetner of the device
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
    mainLayout.setRowMinimumHeight(2, 200)

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
    layout = QtWidgets.QVBoxLayout()

    titleLabel = QtWidgets.QLabel("Sender")
    layout.addWidget(titleLabel)
    
    # Email Edit Field
    emailEdit = QtWidgets.QLineEdit()
    emailEdit.setPlaceholderText("Sender's Email")

    rx = QtCore.QRegExp("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$")
    emailEdit.setValidator(QtGui.QRegExpValidator(rx, self))
    layout.addWidget(emailEdit)

    # Public and Private Keys Field
    keysLabel = QtWidgets.QLabel("Keys")
    layout.addWidget(keysLabel)

    publicEdit = QtWidgets.QLineEdit()
    publicEdit.setPlaceholderText("Public Key")
    privateEdit = QtWidgets.QLineEdit()
    privateEdit.setPlaceholderText("Private Key")

    keysLayout = QtWidgets.QHBoxLayout()
    keysLayout.addWidget(publicEdit)
    keysLayout.addWidget(privateEdit)
    
    layout.addLayout(keysLayout)

    # Message Field
    messageLabel = QtWidgets.QLabel("Message")
    layout.addWidget(messageLabel)

    messageEdit = QtWidgets.QTextEdit()
    layout.addWidget(messageEdit)

    # Hash Field
    hashLabel = QtWidgets.QLabel("Hash")
    layout.addWidget(hashLabel)

    hashEdit = QtWidgets.QTextEdit()
    layout.addWidget(hashEdit)

    # Signature Field
    signLabel = QtWidgets.QLabel("Signature")
    layout.addWidget(signLabel)

    signEdit = QtWidgets.QTextEdit()
    layout.addWidget(signEdit)

    return layout


  def SetReceiverLayout(self):
    layout = QtWidgets.QVBoxLayout()

    titleLabel = QtWidgets.QLabel("Receiver")
    layout.addWidget(titleLabel)

    # Signed Document Field
    signedEdit = QtWidgets.QTextEdit()
    signedEdit.setPlaceholderText("Retrieved Signed Document")
    layout.addWidget(signedEdit)

    # Sender's Public Key Field
    publicLabel = QtWidgets.QLabel("Sender's Public Key")
    layout.addWidget(publicLabel)

    publicEdit = QtWidgets.QLineEdit()
    layout.addWidget(publicEdit)

    # Message and Signature Field
    messageLabel = QtWidgets.QLabel("Message")
    signatureLabel = QtWidgets.QLabel("Signature")

    messageEdit = QtWidgets.QTextEdit()
    signatureEdit = QtWidgets.QTextEdit()

    messageSignatureLayout = QtWidgets.QHBoxLayout()

    messageLayout = QtWidgets.QVBoxLayout()
    messageLayout.addWidget(messageLabel)
    messageLayout.addWidget(messageEdit)

    signatureLayout = QtWidgets.QVBoxLayout()
    signatureLayout.addWidget(signatureLabel)
    signatureLayout.addWidget(signatureEdit)

    messageSignatureLayout.addLayout(messageLayout)
    messageSignatureLayout.addLayout(signatureLayout)

    layout.addLayout(messageSignatureLayout)

    # Generated Hash and Retrieved Hash Field
    generateLabel = QtWidgets.QLabel("Generated Hash")
    retrieveLabel = QtWidgets.QLabel("Retrieved Hash")

    generateEdit = QtWidgets.QTextEdit()
    retrieveEdit = QtWidgets.QTextEdit()

    hashLayout = QtWidgets.QHBoxLayout()

    generateLayout = QtWidgets.QVBoxLayout()
    generateLayout.addWidget(generateLabel)
    generateLayout.addWidget(generateEdit)

    retrieveLayout = QtWidgets.QVBoxLayout()
    retrieveLayout.addWidget(retrieveLabel)
    retrieveLayout.addWidget(retrieveEdit)

    hashLayout.addLayout(generateLayout)
    hashLayout.addLayout(retrieveLayout)

    layout.addLayout(hashLayout)

    # Verified Indicator
    verifiedIndicate = QtWidgets.QLineEdit()
    layout.addWidget(verifiedIndicate)

    return layout


  def SetPkiLayout(self):
    layout = QtWidgets.QVBoxLayout()
    titleLabel = QtWidgets.QLabel("PKI")
    layout.addWidget(titleLabel)

    scrollLayout = QtWidgets.QVBoxLayout()

    emailEdit = []
    keyEdit = []
    itemLayout = []    

    for x in range(10):
      emailEdit.insert(x, QtWidgets.QLineEdit())
      keyEdit.insert(x, QtWidgets.QLineEdit())
      itemLayout.insert(x, QtWidgets.QHBoxLayout()) 
      itemLayout[x].addWidget(emailEdit[x])
      itemLayout[x].addWidget(keyEdit[x])

      scrollLayout.addLayout(itemLayout[x])

    widget = QtWidgets.QWidget()
    widget.setLayout(scrollLayout)

    scrollArea = QtWidgets.QScrollArea()
    scrollArea.setWidget(widget)

    layout.addWidget(scrollArea)

    return layout


if __name__ == "__main__":
  app = QtWidgets.QApplication([])

  window = GuiDigitalSignature()
  window.show()

  sys.exit(app.exec_())