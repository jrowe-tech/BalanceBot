from PyQt5 import QtCore, QtGui, QtWidgets
from ui_utils import Frame
import sys


class UI:
    def __init__(self):
        # Instantiate Window Reference
        self.window = QtWidgets.QMainWindow()
        self.translate = QtCore.QCoreApplication.translate
        self.window.setObjectName("Window")
        self.centralWidget = QtWidgets.QWidget(self.window)
        self.window.setCentralWidget(self.centralWidget)

        # Set Fixed Variables
        self.window.setWindowTitle(self.translate("Window", "AIGS BalanceBot"))
        self.window.resize(500, 360)
        self.menu = self.MainMenu(self.centralWidget)
        self.menu.active = True
        self.menu.Show()

        # Open Window
        self.window.show()

    class MainMenu(Frame):
        def __init__(self, widget):
            # Get Frame Functions
            super().__init__(widget)
            self.label = QtWidgets.QLabel(self.parent)
            self.label.setGeometry(QtCore.QRect(20, 340, 47, 16))
            self.AddComponent("Test Label", self.label)
            self.label.setText(self._translate("Window", "I would recommend giving up"))



    def changeFrame(self, frameIn, frameOut):
        frameIn.active = False
        frameIn.OnFrameClose()
        frameIn.hide()

        frameOut.active = True
        frameOut.OnFrameOpen()
        frameOut.show()


def StartApp():
    app = QtWidgets.QApplication(sys.argv)
    ui = UI()
    app.exec()


StartApp()
