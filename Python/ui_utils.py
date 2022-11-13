# Custom Override Functions For Standardized Frame Utilities
# Allows For MultiFrame Functionality Within One MainWindow Instance
from PyQt5 import QtCore, QtGui, QtWidgets


class Frame:
    def __init__(self, widget, ui):
        self.components = dict()
        self.active = False
        self.cleanFrames = None
        self.setupFrames = None
        self._translate = QtCore.QCoreApplication.translate
        self.parent = widget
        self.ui = ui

    def AddComponent(self, name, component):
        component.setObjectName(name)

        if self.active:
            component.show()
        else:
            component.hide()

        self.components[name] = component

        print(f"Component {component} Added With Name {name} \nComponent Active: {self.active}\n"
              f"Frame Components: {self.components}")

    def Show(self):
        for component in self.components.values():
            print(f"Showing Component: {component}")
            component.show()

    def ActivateComponent(self, name):
        if name not in self.components:
            print("Component Not Found")
            return

        self.components[name].show()
        return True

    def Hide(self):
        for component in self.components.values():
            component.hide()

    def OnFrameClose(self):
        print(f"Frame Override Cleanup Function: {self.cleanFrames}")
        if self.cleanFrames is None:
            return

        self.cleanFrames()

    def OnFrameOpen(self):
        print(f"Frame Override Startup Function: {self.setupFrames}")
        if self.setupFrames is None:
            return

        self.setupFrames()

    def CreateFont(self, size=20, font=None):
        base = QtGui.QFont()
        base.setPointSize(size)
        if font is not None:
            base.setFamily(font)

        return base

    def CreateLabel(self, location: [int], text, size, font=None, objText=None, wordWrap=False, center=False):
        temp = QtWidgets.QLabel(self.parent)
        temp.setGeometry(QtCore.QRect(location[0], location[1],
                                      location[2], location[3]))
        temp.setFont(self.CreateFont(size, font))
        temp.setWordWrap(wordWrap)
        temp.setText(text)

        if objText is None:
            self.AddComponent(text + "_Label", temp)
        else:
            self.AddComponent(objText, temp)

        if center:
            temp.setAlignment(QtCore.Qt.AlignCenter)

        return temp
