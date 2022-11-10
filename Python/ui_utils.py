# Custom Override Functions For Standardized Frame Utilities
# Allows For MultiFrame Functionality Within One MainWindow Instance
from PyQt5 import QtCore


class Frame:
    def __init__(self, widget):
        self.components = dict()
        self.active = False
        self.cleanFrames = None
        self.setupFrames = None
        self._translate = QtCore.QCoreApplication.translate
        self.parent = widget

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
        if self.cleanFrames is None:
            return

        self.cleanFrames()

    def OnFrameOpen(self):
        if self.openFrames is not None:
            return

        self.openFrames()
