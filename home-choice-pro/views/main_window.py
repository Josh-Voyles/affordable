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
from models.affordability_calculator import AffordabilityCalculator as af
from views.main_window_ui import Ui_MainWindow
from views.pop_up_error_window import ErrorWindow

VALID_ENTRY = r"^[0-9]*\.?[0-9]+$"


class MainWindow(QMainWindow):
    """Builds main UI from auto-generated main_window_ui."""

    home_affordability: int
    total_loan_cost: int
    total_principal: int
    total_interest: int
    downpayment: int = 0

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.error = ErrorWindow()

        self.setWindowTitle("Home Choice Pro")

        self.edit_boxes = [
            self.ui.monthlyPaymentEdit,
            self.ui.dpEdit,
            self.ui.interestRateEdit,
        ]

        self.ui.calcPushButton.clicked.connect(self.calculate_house)
        self.ui.resetPushButton.clicked.connect(self.reset)

    def calculate_house(self):
        """
        Checks edit boxes are valid digits -> calculations are made.
        Invalid -> error message displays.
        """
        if self.verify_digits():
            calc = af(
                self.ui.monthlyPaymentEdit.text(),
                self.ui.dpEdit.text(),
                self.ui.interestRateEdit.text(),
                self.ui.termComboBox.currentText(),
            )
            self.load_calculations(calc)
            self.display_results()

        else:
            self.display_error()

    def load_calculations(self, calc):
        """Processes calculations from AffordabilityCalculator"""
        self.home_affordability = calc.calculate_home_affordability_price()
        self.total_loan_cost = calc.calculate_total_home_loan_price()
        self.total_principal = calc.calculate_loan_principal()
        self.total_interest = calc.calculate_loan_interest()
        if not self.ui.dpEdit.text() == "0":
            (float(self.ui.dpEdit.text()) / self.home_affordability * 100)
            self.downpayment = round(
                float(self.ui.dpEdit.text()) / self.home_affordability * 100
            )

    def display_results(self):
        """Display calculations in application header"""
        self.ui.homeAffordabilityLabelNumber.setText("$" + str(self.home_affordability))
        self.ui.totalCostLabelNumber.setText("$" + str(self.total_loan_cost))
        self.ui.principalLabelNumber.setText("$" + str(self.total_principal))
        self.ui.interestLabelNumber.setText("$" + str(self.total_interest))
        self.ui.downPaymentHeaderLabel.setText(
            f"Down Payment: {str(self.downpayment)}%"
        )

    def reset(self):
        """Resets all edit boxes to 0."""
        for edit in self.edit_boxes:
            edit.setText("0")
        self.ui.termComboBox.setCurrentIndex(0)
        self.ui.homeAffordabilityLabelNumber.setText("$0")
        self.ui.totalCostLabelNumber.setText("$0")
        self.ui.principalLabelNumber.setText("$0")
        self.ui.interestLabelNumber.setText("$0")
        self.ui.downPaymentHeaderLabel.setText("-")

    def verify_digits(self):
        """Checks edit boxes -> digits are decimal and not empty."""
        for edit in self.edit_boxes:
            if not re.match(VALID_ENTRY, edit.text()):
                return False
        return True

    def display_error(self):
        """shows an error window to inform user that the input is invalid."""
        self.error.show()
