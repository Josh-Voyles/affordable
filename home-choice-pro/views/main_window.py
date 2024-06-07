"""
Home Choice Pro Morgtage Calculator

This application calculates 'how much house you can afford' based on monthly payment.

UMGC CMSC 495 6380
Class Project
Joey Garcia
Josh Voyles
Randy Shreeves
Zaria Gibbs

Calls MainWindow from auto-generated QT Designer Files

"""
from PyQt5.QtWidgets import QMainWindow
from views.main_window_ui import Ui_MainWindow
from views.pop_up_error_window import ErrorWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.setWindowTitle("Home Choice Pro")

        self.editBoxes = [
                self.ui.monthlyPaymentEdit,
                self.ui.dpEdit,
                self.ui.interestRateEdit,
                ]

        self.ui.calcPushButton.clicked.connect(self.calculate_house)
        self.ui.resetPushButton.clicked.connect(self.reset)

    def calculate_house(self):
        if self.verify_digits():
            # call calculations
            pass
        else:
            self.display_error()

    def reset(self):
        for edit in self.editBoxes:
            edit.setText('0')
        self.ui.radioButtonDollar.setChecked(True)
        self.ui.termComboBox.setCurrentIndex(0)


    def verify_digits(self):
        for edit in self.editBoxes:
            if not edit.text().isdigit():
                return False
        return True

    def display_error(self):
        self.error = ErrorWindow()
        self.error.show()

        
