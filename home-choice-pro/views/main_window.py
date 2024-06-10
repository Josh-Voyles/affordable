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
import re
from PyQt5.QtWidgets import QMainWindow
from views.main_window_ui import Ui_MainWindow
from views.pop_up_error_window import ErrorWindow
from models.affordability_calculator import AffordabilityCalculator as af

VALID_ENTRY = r'^[0-9]+\.?[0-9]*$'

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
            calc = af(
                    self.ui.monthlyPaymentEdit.text(),
                    self.ui.dpEdit.text(),
                    self.ui.interestRateEdit.text(),
                    self.ui.termComboBox.currentText()
                    )
            self.display_results(calc)

        else:
            self.display_error()

    def display_results(self, calc):
        self.ui.homeAffordabilityLabelNumber.setText('$' + calc.calculate_home_affordability_price())
        self.ui.totalCostLabelNumber.setText('$' + calc.calculate_total_home_loan_price())
        self.ui.principalLabelNumber.setText('$' + calc.calculate_loan_principal())
        self.ui.interestLabelNumber.setText('$' + calc.calculate_loan_interest())

    def reset(self):
        for edit in self.editBoxes:
            edit.setText('0')
        self.ui.radioButtonDollar.setChecked(True)
        self.ui.termComboBox.setCurrentIndex(0)
        self.ui.homeAffordabilityLabelNumber.setText('$0')
        self.ui.totalCostLabelNumber.setText('$0')
        self.ui.principalLabelNumber.setText('$0')
        self.ui.interestLabelNumber.setText('$0')


    def verify_digits(self):
        for edit in self.editBoxes:
            if not re.match(VALID_ENTRY, edit.text()):
                return False
        return True

    def display_error(self):
        self.error = ErrorWindow()
        self.error.show()

        
