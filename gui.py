import sys
import random
from PySide2 import QtCore, QtWidgets, QtGui


class GuiDigitalSignature(QtWidgets.QWidget):
  def __init__(self):
    super().__init__()

    self.InitGUI()


  def InitGui():
    self.SetTitleAndWindow()


  def SetTitleAndWindow(self):
    title = "Digital Signature Implementation Demostration - RSA (PSS)"
    self.setWindowTitle(title)

    windowSize = QtCore.QSize(800, 600)
    screen = QtGui.QGuiApplication.primaryScreen()
    screenGeometry = screen.geometry()

    self.setGeometry(QtWidgets.QStyle.alignedRect(QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter, windowSize, screenGeometry))


if __name__ == "__main__":
  app = QtWidgets.QApplication([])

  window = GuiDigitalSignature()
  window.show()

  sys.exit(app.exec_())