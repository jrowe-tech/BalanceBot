# Custom Override Functions For Standardized Frame Utilities
# Allows For MultiFrame Functionality Within One MainWindow Instance
from PyQt5 import QtCore, QtGui, QtWidgets
import json
from glob import glob
import mediapipe as mp
import os
import cv2


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
        print(component)

        if self.active:
            component.show()
        else:
            component.hide()

        self.components[name] = component

        # print(f"Component {component} Added With Name {name} \nComponent Active: {self.active}\n"
        #      f"Frame Components: {self.components}")

    def Show(self):
        print(f"Components Dictionary: {self.components}\n"
              f"Components Values: {self.components.values()}")

        for component in self.components.values():
            # print(f"Showing Component: {component}")
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
        self.graphicsView = QtWidgets.QGraphicsView(self)
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
        # self.pixmap.setPixmap(QtGui.QPixmap("pixmaps\\VideoDebug.jpg"))

    def changeImageCV2(self, image):
        print("CV2 Mat Image Change")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QtGui.QImage(image, image.shape[1], image.shape[0],
                             QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap(image).scaled(1380, 691,
                    QtCore.Qt.KeepAspectRatioByExpanding)
        self.pixmap.setPixmap(pixmap)

    def changeImageStatic(self, imgPath, scaled=False):
        print("Static Image Change")
        if scaled:
            pixmap = QtGui.QPixmap(imgPath).scaled(1380, 691,
                        QtCore.Qt.KeepAspectRatioByExpanding)
            self.pixmap.setPixmap(pixmap)
        else:
            self.pixmap.setPixmap(QtGui.QPixmap(imgPath))



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


def video2MP(capturePath, savePath, defaultPATH = "recorded_videos\\"):
    '''Video Processing Tool With Mediapipe, Use Extensions For capturePATH but not for
    savePath'''

    savePath = defaultPATH + savePath + ".mp4"
    capturePath = defaultPATH + capturePath

    # Video Capture From CAPTUREPATH
    cap = cv2.VideoCapture(capturePath)

    #Get Frames Per Second
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Setup Configuration Frame
    _, config_frame = cap.read()
    print(config_frame)
    video_writer = cv2.VideoWriter("recorded_videos\\" + savePath + ".mp4", 0x7634706d, fps,
                                   (config_frame.shape[1], config_frame.shape[0]))

    # Reset Active Frame To 0 And Reset Frame Counter
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    frame_counter = 0
    frame_cap = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    # Setup Pose Detection:
    # Static Image -> False
    # Model Complexity -> 0-2, Least To Most Accurate (and slow)
    # Enable Segmentation -> Improves Accuracy and Smoothes Location (recommended)
    with mp_pose.Pose(static_image_mode=False,
                      model_complexity=2,
                      enable_segmentation=True,
                      min_detection_confidence=0.8,
                      min_tracking_confidence=0.8) as pose:
        while True:
            # Count Frames
            frame_counter += 1

            # Read From Video
            active, frame = cap.read()

            if active:

                print(f"Processing Frame {frame_counter} of {frame_cap}")

                frame.flags.writeable = False

                # Mediapipe Processing
                results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_styles.get_default_pose_landmarks_style())

                # Break When Video Ends
                if frame_counter == frame_cap:
                    break

                # Write To Save Path
                video_writer.write(frame)

    # Release Video Writer For Low Latency
    video_writer.release()
    cap.release()


#print(getVideos("recorded_videos\\"))
#static_mediapipe_2d("test1.mp4", "test1_detected.mp4", defaultPath="recorded_videos\\")
#print("COMPLETED FUNCTIONS")
