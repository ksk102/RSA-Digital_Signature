import sys
from PySide2 import QtWidgets, QtCore
from gui import GuiDigitalSignature
from pki import Pki
from RsaPssSignature import RsaPssSignature

class GuiMenu:
  def __init__(self, window):
    self.pki = Pki()
    self.rsa = RsaPssSignature()

    window.guiSignal.emailReady.connect(self.DisplayKeys)
    window.guiSignal.messageOnKeyPress.connect(self.GenerateHash)


  @QtCore.Slot(str)
  def DisplayKeys(self, email):
    # Get the keys from PKI
    publicKey, privateKey = self.pki.checkPair(email)

    # convert to string type
    publicKeyPEM = self.rsa.GetKeyInPEM(publicKey)
    privateKeyPEM = self.rsa.GetKeyInPEM(privateKey)

    # Set Text on the TextEdit fields
    window.privateKey.setText(privateKeyPEM)
    window.publicKey.setText(publicKeyPEM)


  @QtCore.Slot(str)
  def GenerateHash(self, message):
    if self.rsa.SetMessage(message):
      self.rsa.HashMessage()

      window.hash.setText(self.rsa.GetHashedMessage())


if __name__ == "__main__":
  app = QtWidgets.QApplication([])

  window = GuiDigitalSignature()
  window.show()

  menu = GuiMenu(window)

  sys.exit(app.exec_())