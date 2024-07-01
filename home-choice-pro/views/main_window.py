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
import os
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from models.affordability_calculator import AffordabilityCalculator as af_calc
from views.main_window_ui import Ui_MainWindow

PATH_TO_GUIDE = os.path.join(os.path.dirname(__file__), "..", "docs", "user_guide.md")


class MainWindow(QMainWindow):
    """Builds main UI from auto-generated main_window_ui."""

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        # additional ui tweaks
        self.setWindowTitle("Home Choice Pro")
        self.guide = self.open_guide()
        self.ui.guideLabel.setText(self.guide)
        self.not_pmi_warned = True

        # variables to display to user
        self.home_affordability: int = 0
        self.total_loan_cost: int = 0
        self.total_principal: int = 0
        self.total_interest: int = 0
        self.display_dp: int = 0

        # variables to load to calc
        self.monthly_payment: float = 0.00
        self.down_payment: float = 0.00
        self.interest_rate: float = 0.00
        self.home_owners: float = 0.00
        self.property_tax: float = 0.00
        self.insurance: float = 0.00
        self.private_insurance: float = 0.00

        # list of float to pass to aff calc
        self.parameters = []

        # ui edit boxes
        self.edit_boxes = [
            self.ui.monthlyPaymentEdit,
            self.ui.dpEdit,
            self.ui.interestRateEdit,
            self.ui.HOAEdit,
            self.ui.propertyTaxEdit,
            self.ui.insuranceEdit,
            self.ui.PMIEdit,
        ]

        self.ui.calcPushButton.clicked.connect(self.calculate_house)
        self.ui.resetPushButton.clicked.connect(self.reset)
        self.ui.calculatorButton.clicked.connect(self.display_calculator_page)
        self.ui.guideButton.clicked.connect(self.display_user_guide)

    def calculate_house(self):
        """
        Checks edit boxes are valid digits -> calculations are made.
        Invalid -> error message displays.
        """
        if self.verify_digits():
            calc = af_calc()
            calc.process_affordability(*self.parameters)
            self.load_calculations(calc)
            self.display_results()

        else:
            self.display_error("Only numeric characters allowed!")

    def verify_digits(self):
        """Checks edit boxes -> digits are decimal and not empty."""
        self.parameters.clear()
        for edit in self.edit_boxes:
            try:
                self.parameters.append(
                    float(edit.text().replace(",", "").replace("$", "").strip())
                    if edit.text().strip() != ""
                    else 0.00
                )
            except ValueError:
                return False
        self.parameters.insert(3, float(self.ui.termComboBox.currentText()))
        return True

    def load_calculations(self, calc):
        """Processes calculations from AffordabilityCalculator"""
        self.home_affordability = calc.get_max_home_price()
        self.total_loan_cost = calc.get_total_loan_cost()
        self.total_principal = calc.get_total_loan_principal()
        self.total_interest = calc.get_total_loan_interest()
        if (
            self.ui.dpEdit.text() != "0"
            and self.ui.dpEdit.text() != ""
            and self.home_affordability > 0
        ):
            self.display_dp = round(
                float(self.ui.dpEdit.text()) / self.home_affordability * 100
            )
        else:
            self.display_dp = 0

    def display_results(self):
        """Display calculations in application header"""
        self.ui.homeAffordabilityLabelNumber.setText("$" + str(self.home_affordability))
        self.ui.totalCostLabelNumber.setText("$" + str(self.total_loan_cost))
        self.ui.principalLabelNumber.setText("$" + str(self.total_principal))
        self.ui.interestLabelNumber.setText("$" + str(self.total_interest))
        self.ui.downPaymentHeaderLabel.setText(f"Down Payment: {str(self.display_dp)}%")

        if int(self.display_dp) < 20:
            self.display_PMI_warning()

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

    def display_error(self, error_message="Error!"):
        """shows an error window to inform user that the input is invalid."""
        message = f"An error occurred: {error_message}"
        QMessageBox.critical(self.ui.centralwidget, "Error!", message)

    def open_guide(self):
        """returns user guide text or error for Github issue"""
        try:
            with open(PATH_TO_GUIDE, "r") as file:
                return file.read()
        except FileNotFoundError:
            return "File Not Found: Please open an issue -> https://github.com/Josh-Voyles/Home-Choice-Pro/issues"

    def display_calculator_page(self):
        """Set stacked widgeted index to show calculator"""
        self.ui.stackedWidget.setCurrentIndex(0)

    def display_user_guide(self):
        """Set stacked widgeted index to show user guide"""
        self.ui.stackedWidget.setCurrentIndex(3)

    def display_PMI_warning(self):
        # assumes PMI is the last parameter, should write a test for correct order
        if self.not_pmi_warned and self.parameters[-1] <= 0:
            print(self.parameters[-1])
            message = "Private Mortage Insurance typically required with down payments less than 20 percent"
            QMessageBox.warning(self, "PMI Error", message)
            self.not_pmi_warned = False
