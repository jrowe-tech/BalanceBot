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
        self.menu = self.MainMenu(self.centralWidget, self)
        self.menu.active = True
        self.videoMenu = self.VideoMenu(self.centralWidget, self)
        self.videoMenu.active = False
        self.videoMenu.Show()

        # Open Window
        self.window.showFullScreen()

    class MainMenu(Frame):
        def __init__(self, widget, ui):
            # Get Frame Functions
            super().__init__(widget)

            #Create Version Number Label -> Adapt As Updates Roll Out
            self.version_label = self.CreateLabel(
                [10, 730, 91, 31], "Version 0.0.1", 20, objText="Version_Label")

            #Create Header Label Of Project
            self.project_label = self.CreateLabel(
                [0, 0, 581, 151], "BalanceBot", 85, objText="Project_Label"
            )

            #Create Descriptor Label Of Main Menu
            self.company_label = self.CreateLabel(
                [580, 0, 801, 151], "Artificial Intelligence Gymnastics Solutions",
                31, objText="Company_Label"
            )

            #Create Menu Button Labels
            self.trainingButton_label = self.CreateLabel(
                [240, 660, 231, 41], "Training", 23
            )

            self.competitionButton_label = self.CreateLabel(
                [820, 650, 321, 51], "Competition", 23
            )

            #Create Menu Buttons (And Add Functions)
            self.competition_button = self.CreateButton(
                [1270, 722, 101, 41],
            )

        def trainingButton(self):
            self.appFunctions.changeFrame(self, self.appFunctions.videoMenu)

    class VideoMenu(Frame):
        def __init__(self, widget, ui):
            # Get Frame Functions
            super().__init__(widget)
            self.pushButton = QtWidgets.QPushButton(self.parent)
            self.pushButton.setGeometry(QtCore.QRect(20, 90, 221, 221))
            self.AddComponent("Practice Button", self.pushButton)
            self.pushButton.setText("You Are Dog")
            self.pushButton.clicked.connect(self.backButton)
            self.appFunctions = ui

        def backButton(self):
            self.appFunctions.changeFrame(self, self.appFunctions.menu)

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
