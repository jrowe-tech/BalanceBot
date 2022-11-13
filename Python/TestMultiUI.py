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

        # Instantiate SubClass Frames
        self.menu = self.MainMenu(self.centralWidget, self)
        self.menu.active = True
        self.videoMenu = self.VideoMenu(self.centralWidget, self)
        self.videoMenu.active = False
        self.trainingMenu = self.TrainingMenu(self.centralWidget, self)
        self.trainingMenu.active = False

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
            self.settings_button.setGeometry(1270, 722, 101, 41)
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
                                                    self.ui.changeFrame(self, self.ui.videoMenu))

            self.training_button.clicked.connect(lambda:
                                                 self.ui.changeFrame(self, self.ui.trainingMenu))

    class VideoMenu(Frame):
        def __init__(self, widget, ui):
            # Get Frame Functions
            super().__init__(widget, ui)

        def ConnectButtons(self, ui):
            self.ui = ui

    class TrainingMenu(Frame):
        def __init__(self, widget, ui):
            super().__init__(widget, ui)
            self.CreateLabel(
                [240, 660, 231, 41], "Training", 23
            )

        def ConnectButtons(self, ui):
            self.ui = ui

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
