import sys
from PySide2 import QtWidgets, QtCore
from gui import GuiDigitalSignature
from pki import Pki
from RsaPssSignature import RsaPssSignature

class GuiMenu:
  def __init__(self, window):
    self.pki = Pki()
    self.rsa = RsaPssSignature()
    self.rsaReceiver = RsaPssSignature()

    self.email = ""
    self.emailChanged = False
    self.hashedMessage = ""
    self.hashChanged = False

    window.guiSignal.emailReady.connect(self.DisplayKeys)
    window.guiSignal.emailReady.connect(self.GenerateSignature)
    window.guiSignal.messageOnKeyPress.connect(self.GenerateHash)
    window.guiSignal.messageOnKeyPress.connect(self.GenerateSignature)

    window.guiSignal.sendOnClicked.connect(self.ReceiveSignatureDocument)
    window.guiSignal.sendOnClicked.connect(self.GetSenderPublicKey)
    window.guiSignal.signedDocumentChanged.connect(self.ShowMessageSignature)
    window.guiSignal.signedDocumentChanged.connect(self.GenerateReceiveHash)


  @QtCore.Slot(str)
  def DisplayKeys(self, email):
    # To check whether user changed the email
    # Used to prevent system from regenerate the signature when user click Send
    # It is because emailReady Signal will be triggered everytime the Send button is clicked
    if self.email != email:
      self.email = email
      self.emailChanged = True
    else:
      self.emailChanged = False
      return

    # To check whether the email entered is a new email
    newEmail = False
    if not self.pki.CheckEntryExists(email):
      newEmail = True

    # Get the keys from PKI
    publicKey, self.privateKey = self.pki.CheckPair(email)

    # convert to string type
    publicKeyPEM = self.rsa.GetKeyInPEM(publicKey)
    privateKeyPEM = self.rsa.GetKeyInPEM(self.privateKey)

    # Set Text on the TextEdit fields
    window.privateKey.setText(privateKeyPEM)
    window.publicKey.setText(publicKeyPEM)

    # if it is a new email, add an entry on PKI content area
    if newEmail:
      window.AddPkiEntry(email, publicKeyPEM)


  @QtCore.Slot(str)
  def GenerateHash(self, message):
    if self.rsa.SetMessage(message):
      # Hash the message
      self.rsa.HashMessage()
      # Set the plaintext hash on the edit field
      hashedMessage = self.rsa.GetHashedMessage()
      window.hash.setText(hashedMessage)


  # Generate signature based on hash
  def GenerateSignature(self, email):
    # check if message hash exists, if yes, then proceed, else return
    # use to generate a new signature after user change the email
    try:
      hashedMessage = self.rsa.GetHashedMessage()
    except AttributeError:
      return

    # To check whether user have changed the message
    # Generate the signature when the message is changed
    if self.hashedMessage != hashedMessage:
        self.hashedMessage = hashedMessage
        self.hashChanged = True
    else:
      self.hashChanged = False
    # Used to prevent system from regenerate the signature when user click Send
    # It is because emailReady Signal will be triggered everytime the Send button is clicked
    # If hashChanged check is not exists, signature will not be regenerate as emailChanged is evaluate as False
    # Here it generate the signature when hash is changed
    if (self.emailChanged is False) and (self.hashChanged is False):
      return

    # sign the hash using private key
    self.rsa.SignSignature(key = self.privateKey)
    # set the plaintext signature on edit field
    window.signature.setText(self.rsa.GetSignature())

  @QtCore.Slot()
  def ReceiveSignatureDocument(self):
    window.signedDocument.setText(self.rsa.GetSignedDocument())

  
  @QtCore.Slot()
  def GetSenderPublicKey(self):
    senderPublicKey = self.pki.GetPublicKey(self.email)
    senderPublicKeyPEM = self.rsaReceiver.GetKeyInPEM(senderPublicKey)

    window.senderPublic.setText(senderPublicKeyPEM)

  
  @QtCore.Slot(str)
  def ShowMessageSignature(self, signedDoc):
    # trim the message out from the signature document
    message = self.rsaReceiver.GetMessageFromSignedDoc(signedDoc)

    # check the format of the signature
    if message:
      window.signedDocument.setStyleSheet('background-color: white; ')
      window.receiverMessage.setText(message)
      self.rsaReceiver.SetMessage(message)
    else:
      window.signedDocument.setStyleSheet('background-color: #ffcdd2; ')
      window.signedDocument.setFocus()
      window.receiverMessage.setText("")
      window.receiveSignature.setText("")
      window.generatedHash.setText("")
      window.retrievedHash.setText("")
      window.Alert("Incorrect Signature Document Format")


  @QtCore.Slot(str)
  def GenerateReceiveHash(self, signedDoc):
    # Get the hashAlgo from "Hash: " section of the signed document
    hashAlgo = self.rsaReceiver.GetHashAlgoFromSignedDoc(signedDoc)

    # Check whether it is the supported hash function
    if self.rsaReceiver.SetHashAlgo(hashAlgo):
      window.signedDocument.setStyleSheet('background-color: white; ')
    else:
      window.signedDocument.setStyleSheet('background-color: #ffcdd2; ')
      window.generatedHash.setText("")
      window.Alert("Supported Hashing Function: \nSHA256, SHA384, SHA512, SHA1, MD5")

    # Generate the hash value using the hashing function given
    self.rsaReceiver.HashMessage()
    # Set the plaintext hash on the edit field
    hashedMessage = self.rsaReceiver.GetHashedMessage()
    window.generatedHash.setText(hashedMessage)


if __name__ == "__main__":
  app = QtWidgets.QApplication([])

  window = GuiDigitalSignature()
  window.showMaximized()

  menu = GuiMenu(window)

  sys.exit(app.exec_())