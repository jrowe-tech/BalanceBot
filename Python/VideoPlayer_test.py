from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import cv2
import numpy as np
from time import sleep as s

class VideoPlayer(QWidget):
    def __init__(self, size, parent):
        super().__init__()
        QWidget.__init__(self)
        self.label = QLabel(parent)
        self.label.setGeometry(QRect(size[0], size[1],
                                     size[2], size[3]))
        self.image = None
        self.graphicsView = QGraphicsView(parent)
        self.graphicsView.setGeometry(QRect(size[0], size[1],
                                            size[2], size[3]))
        self.scene = QGraphicsScene()
        self.pixmap = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

    def changeImage(self, image):
        #self.label.setPixmap(image)
        self.pixmap.setPixmap(image)

class App:
    def __init__(self):
        self.window = QMainWindow()
        self.window.setObjectName("Window")
        self.centralWidget = QWidget(self.window)
        self.window.setCentralWidget(self.centralWidget)
        self.player = VideoPlayer((0, 0, 1380, 691), self.centralWidget)
        self.pixmap = QPixmap().scaled(1380, 691, Qt.KeepAspectRatioByExpanding)
        self.player.changeImage(self.pixmap)
        self.window.showFullScreen()
        self.pixmap = QPixmap("pixmaps\\VideoDebug.jpg").scaled(1380, 691, Qt.KeepAspectRatioByExpanding)
        self.camera = cv2.VideoCapture(0)#"recorded_videos\\Jake.mp4")
        while True:
            active, frame = self.camera.read()
            if active:
                cv2.imshow("FRAME", frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.image = QImage(frame, frame.shape[1], frame.shape[0]
                                    , QImage.Format_RGB888)
                self.pixmap = QPixmap(self.image).scaled(1380, 691, Qt.KeepAspectRatioByExpanding)
                self.player.changeImage(self.pixmap)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        cv2.destroyAllWindows()


def start():
    app = QApplication(sys.argv)
    app2 = App()
    app.exec()

start()