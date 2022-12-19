from PyQt5.QtWidgets import *
from PyQt5 import Qt
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from glob import glob
from threading import Thread
import json
import sys
import cv2

class GridLayout(QWidget):
    def __init__(self, img_path, height, width):
        super().__init__()
        QWidget.__init__(self)
        grid_layout = QGridLayout()

        self.inputThread = Thread(target=self.declareVideo, daemon=True)
        self.inputThread.start()
        self.height = height
        self.width = width

        self.setLayout(grid_layout)
        self.show()

        # Grab MP4 / AVI Video Objects
        videos = self.getVideos("recorded_videos\\")
        self.currentIndex = None
        videoCount = len(videos)
        yLength = videoCount
        self.thumbnails = []

        self.currentVideo = None
        for x in range((videoCount // 3) + 1):
            for y in range(min(3, yLength)):
                video = videos[x*3 + y]
                thumbnail = Thumbnail(self, video, width//3, height//3,
                                      text="TEST", clicked=self.changeVideoSelection)
                self.thumbnails.append(thumbnail)
                grid_layout.addWidget(thumbnail, x, y)
            yLength -= 3

            grid_layout.setColumnStretch(x, x + 1)

        self.setWindowTitle('Basic Grid Layout')

    def getVideos(self, path):
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

    def changeVideoSelection(self):
        print("ACTIVATED FUNCTION")
        if self.currentIndex is not None:
            for i, thumbnail in enumerate(self.thumbnails):
                if thumbnail.active and i != self.currentIndex:
                    self.currentVideo = thumbnail.video[0]
                    print(f"Changing Video To: {self.currentVideo}")
                    self.thumbnails[self.currentIndex].active = False
                    print(f"Switching {self.thumbnails[self.currentIndex]} to deactivated")
                    self.currentIndex = i
                    print(f"New Index: {i}")
        else:
            for i, thumbnail in enumerate(self.thumbnails):
                if thumbnail.active:
                    self.currentVideo = thumbnail.video[0]
                    print(f"Initializing Video To: {self.currentVideo}")
                    self.currentIndex = i
                    print(f"New Index: {i}")
                    break


    def declareVideo(self):
        while True:
            input("HIT ENTER TO SEE CURRENT VIDEO")
            print(self.currentVideo)

class Thumbnail(QWidget):
    def __init__(self, parent, video, width, height, text=None, clicked=None):
        QWidget.__init__(self, parent=parent)
        self.video = video
        image = QPixmap(video[2]).scaled(width, height,
                                          Qt.KeepAspectRatioByExpanding)
        self.pixmap = QLabel()
        self.pixmap.setPixmap(image)
        self.clickFunction = None
        self.active = False
        currentVideo = 2

        self.label = QLabel()
        if text:
            self.label.setText(text)
        self.label.setAlignment(Qt.AlignCenter)

        lay = QVBoxLayout(self)

        lay.addWidget(self.pixmap)
        lay.addWidget(self.label)

        self.clicked = clicked

        self.videoCallback = currentVideo
        print(self.videoCallback == currentVideo)
        self.mousePressEvent = self.clickEvent

    def clickEvent(self, event):
        if self.clicked:
            self.active = True
            self.clicked()



def start():
    app = QApplication(sys.argv)
    app2 = GridLayout("OpenCVCalibrationChessboard.png",
                      500, 500)
    app.exec()

start()
