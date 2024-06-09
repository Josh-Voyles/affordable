"""
Home Choice Pro Morgtage Calculator

This application calculates 'how much house you can afford' based on monthly payment.

UMGC CMSC 495 6380
Class Project
Joey Garcia
Josh Voyles
Randy Shreeves
Zaria Gibbs

"""
from PyQt5.QtWidgets import QMainWindow
from views.pop_up_error_window_ui import Ui_Form

class ErrorWindow(QMainWindow):
    def __init__(self):
        super(ErrorWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.ui.closeButton = self.ui.errorCloseButton

        self.setWindowTitle("Home Choice Pro")