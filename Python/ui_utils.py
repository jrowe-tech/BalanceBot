# Custom Override Functions For Standardized Frame Utilities
# Allows For MultiFrame Functionality Within One MainWindow Instance
from PyQt5 import QtCore, QtGui, QtWidgets
import json
from glob import glob
import os


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

    def CreateFont(self, size=20, font=None, bold=False, italic=False):
        base = QtGui.QFont()
        base.setPointSize(size)
        if font is not None:
            base.setFamily(font)

        base.setBold(bold)
        base.setItalic(italic)

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


class Thumbnail(QtWidgets.QWidget):
    def __init__(self, paths):
        super().__init__()
        QtWidgets.QWidget.__init__(self)
        self.image_data = paths
        self.thumbnail = QtGui.QPixmap(paths[2])
        self.image_label = QtWidgets.QLabel()
        self.image_label.setPixmap(self.thumbnail)
        self.containerWidget = QtWidgets.QWidget()
        self.image_label.mousePressEvent = self.onMousePress
        self.clickFunction = None

    def onMousePress(self, event):
        if self.clickFunction is not None:
            self.clickFunction()


class VideoPlayer(QtWidgets.QWidget):
    def __init__(self, size, parent):
        super().__init__()
        QtWidgets.QWidget.__init__(self)
        self.setParent(parent)
        self.graphicsView = QtWidgets.QGraphicsView(parent)
        self.graphicsView.setGeometry(QtCore.QRect(size[0], size[1],
                                                   size[2], size[3]))
        self.scene = QtWidgets.QGraphicsScene()
        self.pixmap = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOn)
        self.pixmap.setPixmap(QtGui.QPixmap("pixmaps\\VideoDebug.jpg"))

    def changeImage(self, image):
        self.pixmap.setPixmap(image)


# Check Saved JSON Log For Videos -> Return DATA
def getVideos(path):
    files = glob(path + '*.mp4') + glob(path + '*.avi')
    videoObjects = []
    with open("recorded_videos/data.json", mode='r') as log:
        data = json.load(log)
        for file in data:
            if path + file['name'] in files:
                videoObjects.append((file['name'], file['date'], "thumbnails\\" + file['thumbnail']))
            else:
                raise FileNotFoundError

    return sorted(videoObjects, key=lambda x: x[1])


print(getVideos("recorded_videos\\"))
