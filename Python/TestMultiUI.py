import threading
from PyQt5 import QtCore, QtGui, QtWidgets
import ui_utils as utils
from ui_utils import Frame, VideoPlayer
import sys
import cv2
from time import sleep

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

        # Instantiate SubClass Frames
        self.menu = self.MainMenu(self.centralWidget, self)
        self.menu.active = True
        self.videoMenu = self.VideoMenu(self.centralWidget, self)
        self.videoMenu.active = False
        self.trainingMenu = self.TrainingMenu(self.centralWidget, self)
        self.trainingMenu.active = False
        self.videoPlayer = self.VideoPlayer(self.centralWidget, self)
        self.videoPlayer.active = False

        # Connect Frames
        self.menu.ConnectButtons(self)
        self.videoMenu.ConnectButtons(self)
        self.trainingMenu.ConnectButtons(self)

        # Show Main Menu On Start
        self.menu.Show()

        # Open Window
        self.window.showFullScreen()

    class MainMenu(Frame):
        def __init__(self, widget, ui):
            # Get Frame Functions
            super().__init__(widget, ui)

            # Create Version Number Label -> Adapt As Updates Roll Out
            self.version_label = self.CreateLabel(
                [10, 730, 200, 31], "Version 0.0.1", 20, objText="Version_Label")

            # Create Header Label Of Project
            self.project_label = self.CreateLabel(
                [0, 0, 581, 151], "BalanceBot", 85, objText="Project_Label"
            )

            # Create Descriptor Label Of Main Menu
            self.company_label = self.CreateLabel(
                [580, 0, 801, 151], "Artificial Intelligence Gymnastics Solutions",
                31, objText="Company_Label"
            )

            # Add Interactable Menu Buttons
            self.competition_button = QtWidgets.QPushButton(self.parent)
            self.competition_button.setGeometry(QtCore.QRect(740, 200, 500, 500))
            self.AddComponent("Competition_Button", self.competition_button)
            self.competition_button.setIcon(
                QtGui.QIcon('pixmaps/competitionIcon.png'))
            self.competition_button.setIconSize(QtCore.QSize(
                500, 500))

            self.training_button = QtWidgets.QPushButton(self.parent)
            self.training_button.setGeometry(QtCore.QRect(120, 200, 500, 500))
            self.AddComponent("Training_Button", self.training_button)
            self.training_button.setIcon(
                QtGui.QIcon('pixmaps/trainingIcon.png'))
            self.training_button.setIconSize(QtCore.QSize(
                400, 500))

            # Create Menu Button Labels
            self.trainingButton_label = self.CreateLabel(
                [240, 660, 231, 41], "Training", 23, center=True
            )

            self.competitionButton_label = self.CreateLabel(
                [820, 650, 321, 51], "Competition", 23, center=True
            )

            # Add Settings Button
            self.settings_button = QtWidgets.QPushButton(self.parent)
            self.settings_button.setGeometry(1260, 722, 101, 41)
            self.settings_button.setFont(self.CreateFont(20))
            self.settings_button.setText("Settings")
            self.AddComponent("Settings_Button", self.settings_button)

            # Create Dividing Line
            self.line = QtWidgets.QFrame(self.parent)
            self.line.setGeometry(QtCore.QRect(0, 150, 1381, 16))
            self.line.setFrameShadow(QtWidgets.QFrame.Raised)
            self.line.setLineWidth(4)
            self.line.setFrameShape(QtWidgets.QFrame.HLine)
            self.AddComponent("MainMenu_Line", self.line)

        def ConnectButtons(self, ui):
            self.ui = ui

            # Add Button Functions
            self.competition_button.clicked.connect(lambda:
                                                    self.ui.changeFrame(self, self.ui.videoPlayer))

            self.training_button.clicked.connect(lambda:
                                                 self.ui.changeFrame(self, self.ui.trainingMenu))

    class VideoMenu(Frame):
        def __init__(self, widget, ui):
            # Get Frame Functions
            super().__init__(widget, ui)

            # Selected Video
            self.selectedVideo = None

            # Create Title Label
            self.title_label = self.CreateLabel(
                [180, 0, 701, 91], "Recorded Videos",
                68, objText="VideoMenuTitle_Label"
            )

            # Create Descriptor Label
            self.description_label = self.CreateLabel(
                [880, 10, 491, 91],
                "Watch, Export, And Create New Videos",
                20, objText="VideoMenuDescription_Label"
            )

            # Create Back Button
            self.back_button = QtWidgets.QPushButton(self.parent)
            self.back_button.setGeometry(0, 0, 121, 61)
            self.back_button.setFont(self.CreateFont(23))
            self.back_button.setText("Back")
            self.AddComponent("VideoBack_Button", self.back_button)

            # Create Video Editing Buttons
            self.save_button = QtWidgets.QPushButton(self.parent)
            self.save_button.setGeometry(850, 690, 191, 41)
            self.save_button.setFont(self.CreateFont(15, bold=True))
            self.save_button.setText("Save")
            self.AddComponent("VideoSave_Button", self.save_button)

            self.view_button = QtWidgets.QPushButton(self.parent)
            self.view_button.setGeometry(30, 690, 181, 41)
            self.view_button.setFont(self.CreateFont(15, bold=True))
            self.view_button.setText("View")
            self.AddComponent("VideoView_Button", self.view_button)

            self.record_button = QtWidgets.QPushButton(self.parent)
            self.record_button.setGeometry(270, 690, 301, 41)
            self.record_button.setFont(self.CreateFont(15, bold=True))
            self.record_button.setText("Record Video")
            self.AddComponent("VideoRecord_Button", self.record_button)

            # Create Checkmark For Saving Videos
            self.save_checkBox = QtWidgets.QCheckBox(self.parent)
            self.save_checkBox.setGeometry(QtCore.QRect(1050, 690, 301, 41))
            self.save_checkBox.setFont(self.CreateFont(15))
            self.save_checkBox.setText("Save With Pose Detection")
            self.save_checkBox.setIconSize(QtCore.QSize(16, 16))
            self.AddComponent("Save_CheckBox", self.save_checkBox)

            # Create Horizontal Aesthetic Line
            self.line = QtWidgets.QFrame(self.parent)
            self.line.setGeometry(QtCore.QRect(0, 90, 1381, 21))
            self.line.setFrameShadow(QtWidgets.QFrame.Raised)
            self.line.setLineWidth(5)
            self.line.setFrameShape(QtWidgets.QFrame.HLine)
            self.AddComponent("VideoView_Line", self.line)

            # Create Frame For Scrolling Widget
            self.frame = QtWidgets.QFrame(self.parent)
            self.frame.setGeometry(QtCore.QRect(30, 130, 1310, 551))
            self.frame.setFrameShape(QtWidgets.QFrame.Box)
            self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.frame.setLineWidth(3)
            self.AddComponent("VideoMenu_Frame", self.frame)

            # Make Video Menu Scrollable -> Work On AFTER GRID
            self.scroll = QtWidgets.QScrollArea(self.frame)
            self.scroll.setGeometry(QtCore.QRect(10, 10, 1291, 531))
            self.scroll.setWidgetResizable(True)
            self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.AddComponent("Video_ScrollArea", self.scroll)

            # Create Grid Widget
            self.grid = QtWidgets.QGridLayout()
            self.gridWidget = QtWidgets.QWidget(self.parent)
            self.gridWidget.setGeometry(QtCore.QRect(0, 0, 1289, 529))
            self.scroll.setWidget(self.gridWidget)
            self.gridWidget.setLayout(self.grid)
            for video in utils.getVideos('recorded_videos\\'):
                thumb = utils.Thumbnail(video)
                thumb.clickFunction = lambda: self.changeActiveThumbnail(video[0])

        def changeActiveThumbnail(self, target):
            self.selectedVideo = target

        def ConnectButtons(self, ui):
            self.ui = ui

            # Connect Button Functionalities
            self.back_button.clicked.connect(lambda:
                                             ui.changeFrame(self, ui.menu))

    class TrainingMenu(Frame):
        def __init__(self, widget, ui):
            super().__init__(widget, ui)

            # Create Page Title Label
            self.title_label = self.CreateLabel(
                [180, 0, 671, 111], "Training Exercises",
                62, objText="TrainingTitle_Label"
            )

            # Create Training Descriptor Label
            self.training_description = self.CreateLabel(
                [880, 20, 671, 81], "Select Exercise To Begin",
                28, objText="TrainingDescription_Label", center=False
            )

            # Create Back Button
            self.back_button = QtWidgets.QPushButton(self.parent)
            self.back_button.setGeometry(0, 0, 121, 61)
            self.back_button.setFont(self.CreateFont(23))
            self.back_button.setText("Back")
            self.AddComponent("TrainingBack_Button", self.back_button)

            # Create Training Buttons 1-4
            # Training Button 1
            self.training1_button = QtWidgets.QPushButton(self.parent)
            self.training1_button.setGeometry(100, 170, 561, 241)
            self.training1_button.setFont(self.CreateFont(23))
            self.training1_button.setText("Training One")
            self.AddComponent("TrainingOne_Button", self.training1_button)

            # Training Button 2
            self.training2_button = QtWidgets.QPushButton(self.parent)
            self.training2_button.setGeometry(730, 170, 551, 241)
            self.training2_button.setFont(self.CreateFont(23))
            self.training2_button.setText("Training Two")
            self.AddComponent("TrainingTwo_Button", self.training2_button)

            # Training Button 3
            self.training3_button = QtWidgets.QPushButton(self.parent)
            self.training3_button.setGeometry(100, 470, 561, 241)
            self.training3_button.setFont(self.CreateFont(23))
            self.training3_button.setText("Training Three")
            self.AddComponent("TrainingThree_Button", self.training3_button)

            # Training Button 4
            self.training4_button = QtWidgets.QPushButton(self.parent)
            self.training4_button.setGeometry(730, 470, 551, 241)
            self.training4_button.setFont(self.CreateFont(23))
            self.training4_button.setText("Training Four")
            self.AddComponent("TrainingFour_Button", self.training4_button)

            # Add Line For AESTHETIC
            self.line = QtWidgets.QFrame(self.parent)
            self.line.setGeometry(QtCore.QRect(0, 110, 1381, 16))
            self.line.setFrameShadow(QtWidgets.QFrame.Raised)
            self.line.setLineWidth(4)
            self.line.setFrameShape(QtWidgets.QFrame.HLine)
            self.AddComponent("Training_Line", self.line)

        def ConnectButtons(self, ui):
            self.ui = ui

            # Set Button Functionalities
            self.back_button.clicked.connect(lambda:
                                             ui.changeFrame(self, ui.menu))

    class VideoPlayer(Frame):
        def __init__(self, widget, ui):
            super().__init__(widget, ui)

            # Create VideoPlayer Widget
            self.player = VideoPlayer((0, 0, 1380, 691), self.parent)
            #self.AddComponent("VideoPlayer", self.player)

            # Initialize VideoPlayer Parameters
            self.frameCap = None
            self.normalVideo = None
            self.poseVideo = None
            self.video = None
            self.playThread = None
            self.playing = False
            self.frame = 0
            self.playbackSpeed = 1.0

            # Show Default Image
            #self.player.changeImage(QtGui.QPixmap("pixmaps\\VideoDebug.jpg").scaled(
            #    1380, 691, QtCore.Qt.KeepAspectRatio))

            # Create Button Panel
            self.panel = QtWidgets.QFrame(self.parent)
            self.panel.setGeometry(QtCore.QRect(0, 690, 1381, 81))
            self.panel.setFrameShape(QtWidgets.QFrame.Panel)
            self.panel.setFrameShadow(QtWidgets.QFrame.Raised)
            self.panel.setLineWidth(7)
            self.AddComponent("VideoPlayer_Panel", self.panel)

            # Create Overlay Button
            self.overlay_button = QtWidgets.QPushButton(self.panel)
            self.overlay_button.setGeometry(QtCore.QRect(1260, 10, 111, 61))
            self.buttonFont = self.CreateFont(20)
            self.overlay_button.setText("Overlay")
            self.overlay_button.setFont(self.buttonFont)
            self.overlay_button.clicked.connect(lambda: self.overlayToggle())
            self.AddComponent("VideoPlayerOverlay_Button", self.overlay_button)

            # Create Play / Pause Button
            self.play_button = QtWidgets.QPushButton(self.panel)
            self.play_button.setGeometry(QtCore.QRect(600, 10, 161, 61))
            self.play_button.setFont(self.buttonFont)
            self.play_button.setText("Play")
            self.play_button.clicked.connect(lambda: self.play())
            self.AddComponent("VideoPlayerPlay_Button", self.play_button)

            # Create Next Frame Button
            self.nextFrame_button = QtWidgets.QPushButton(self.panel)
            self.nextFrame_button.setGeometry(QtCore.QRect(790, 10, 161, 61))
            self.nextFrame_button.setFont(self.buttonFont)
            self.nextFrame_button.setText("Next Frame")
            self.nextFrame_button.clicked.connect(lambda: self.nextFrame())
            self.AddComponent("VideoPlayerNextFrame_Button", self.nextFrame_button)

            # Create Previous Frame Button
            self.lastFrame_button = QtWidgets.QPushButton(self.panel)
            self.lastFrame_button.setGeometry(QtCore.QRect(410, 10, 161, 61))
            self.lastFrame_button.setFont(self.buttonFont)
            self.lastFrame_button.setText("Last Frame")
            self.lastFrame_button.clicked.connect(lambda: self.lastFrame())
            self.AddComponent("VideoPlayerLastFrame_Button", self.lastFrame_button)

            # Create Replay Button
            self.replay_button = QtWidgets.QPushButton(self.panel)
            self.replay_button.setGeometry(QtCore.QRect(10, 10, 141, 61))
            self.replay_button.setFont(self.buttonFont)
            self.replay_button.setText("Replay")
            self.replay_button.clicked.connect(lambda: self.replay())
            self.AddComponent("VideoPlayeReplay_Button", self.replay_button)

            # Attach Camera Stream On Frame Open (WORK ON LATER):
            # self.setupFrames = lambda: self.startDebugCameraStream()

        def replay(self):
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.frame = 0

            #Update Frame

        def nextFrame(self):
            if self.frame < self.frameCap:
                # Read Active Frame Data And Process
                _, data = self.video.read()
                data = cv2.cvtColor(data, cv2.BGR2RGB)
                image = QtGui.QImage(data, data.shape[1], data.shape[0],
                                     QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap(image).scaled(1380, 691,
                                                     QtCore.Qt.KeepAspectRatioByExpanding)
                #self.player.changeImage(pixmap)

                # Change Frames
                self.frame += 1

        def previousFrame(self):
            if self.frame > 1:
                # Change Current Video Frame To Previous Frame
                self.video.set(cv2.CAP_PROP_POS_FRAMES, self.video.get(
                    cv2.CAP_PROP_POS_FRAMES) - 2)

                # Read Active Frame Data And Process
                _, data = self.video.read()
                data = cv2.cvtColor(data, cv2.BGR2RGB)
                image = QtGui.QImage(data, data.shape[1], data.shape[0],
                                     QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap(image).scaled(1380, 691,
                                                     QtCore.Qt.KeepAspectRatioByExpanding)
                #self.player.changeImage(pixmap)

                self.frame -= 1


        def play(self):
            # Toggle Active Button Functions
            if self.active:
                self.play_button.setText("Play")
            else:
                self.play_button.setText("Pause")

                # Start Daemon Thread
                self.playThread = threading.Thread(target=self.startStream)
                self.playThread.setDaemon(True)
                self.playThread.start()

            self.active = not self.active
            self.nextFrame_button.blockSignals(self.active)
            self.lastFrame_button.blockSignals(self.active)



        def startStream(self):

            tick = 1 / self.video.get(cv2.CAP_PROP_FPS)

            # Start Video Stream Until Final Frame Reached OR Stopped
            while self.frame < self.frameCap and not self.active:

                # Read Active Frame Data And Process
                _, data = self.video.read()
                data = cv2.cvtColor(data, cv2.BGR2RGB)
                image = QtGui.QImage(data, data.shape[1], data.shape[0],
                                     QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap(image).scaled(1380, 691,
                                                     QtCore.Qt.KeepAspectRatioByExpanding)
                #self.player.changeImage(pixmap)

                # Go To Next Frame
                self.frame += 1

                # Fix Frame Rate Issues
                sleep(tick)


        def overlayToggle(self):
            if self.video == self.normalVideo:
                self.video = self.poseVideo
            else:
                self.video = self.normalVideo

        def debugCameraStream(self):
            # Create Buttons For Overlay Functions
            cam = cv2.VideoCapture(0)
            for i in range(500):
                active, frame = cam.read()
                if active:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image = QtGui.QImage(frame, frame.shape[1], frame.shape[0],
                                         QtGui.QImage.Format_RGB888)
                    pixmap = QtGui.QPixmap(image).scaled(1380, 691, QtCore.Qt.KeepAspectRatioByExpanding)
                    #self.player.changeImage(pixmap)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break

    def changeFrame(self, frameIn, frameOut):
        frameIn.active = False
        frameIn.OnFrameClose()
        frameIn.Hide()

        frameOut.active = True
        frameOut.OnFrameOpen()
        frameOut.Show()


def StartApp():
    app = QtWidgets.QApplication(sys.argv)
    ui = UI()
    app.exec()


StartApp()
