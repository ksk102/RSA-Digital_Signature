import sys
from PySide2 import QtWidgets, QtCore
from gui import GuiDigitalSignature
from pki import Pki

class GuiMenu:
  def __init__(self, window):
    self.pki = Pki()

    window.guiSignal.emailReady.connect(self.DisplayKeys)
    window.guiSignal.emailReady.connect(self.AddKeyPairs)


  @QtCore.Slot(str)
  def DisplayKeys(self, email):
    # Get the keys from PKI
    publicKey, privateKey = self.pki.checkPair(email)

    # Set Text on the TextEdit fields
    window.privateKey.setText(privateKey)
    window.publicKey.setText(publicKey)

  @QtCore.Slot(str)
  def AddKeyPairs(self, email):
    None


if __name__ == "__main__":
  app = QtWidgets.QApplication([])

  window = GuiDigitalSignature()
  window.show()

  menu = GuiMenu(window)

  sys.exit(app.exec_())