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
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from models.affordability_calculator import AffordabilityCalculator as af_calc
from views.main_window_ui import Ui_MainWindow

PATH_TO_GUIDE = os.path.join(os.path.dirname(__file__), "..", "docs", "user_guide.md")

DEFAULT_MONTLY = 3000
DEFAULT_DOWN_PAYMENT = 80000
DEFAULT_INTEREST_RATE = 6.125
DEFAULT_HOA = 350
DEFAULT_PROPERTY_TAX = 0.74
DEFAULT_HOME_INSURANCE = 0.74
DEFAULT_PMI = 1.01
RECCOMENDED_DP_PERCENTAGE = 20

CALCULATOR_WINDOW = 0
USER_GUIDE_WINDOW = 3

THIRTY_INDEX = 0
FIFTEEN_INDEX = 1

class MainWindow(QMainWindow):
    """Builds main UI from auto-generated main_window_ui."""

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        # regex input validator
        regex = QRegExp(r"^(\d+)?(\.\d+)?$")
        validator = QRegExpValidator(regex)
        self.ui.monthlyPaymentEdit.setValidator(validator)
        self.ui.dpEdit.setValidator(validator)
        self.ui.interestRateEdit.setValidator(validator)
        self.ui.HOAEdit.setValidator(validator)
        self.ui.propertyTaxEdit.setValidator(validator)
        self.ui.insuranceEdit.setValidator(validator)
        self.ui.PMIEdit.setValidator(validator)
        # additional ui tweaks

        self.setWindowTitle("Home Choice Pro")
        self.guide = self.open_guide()
        self.ui.guideLabel.setText(self.guide)
        self.is_pmi_warned = False

        # variables to display to user
        self.home_affordability: int = 0
        self.total_loan_cost: int = 0
        self.total_principal: int = 0
        self.total_interest: int = 0
        self.display_dp: int = 0

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
        
        # gui displays placeholder default values
        self.default_values = [
            DEFAULT_MONTLY,
            DEFAULT_DOWN_PAYMENT,
            DEFAULT_INTEREST_RATE,
            DEFAULT_HOA,
            DEFAULT_PROPERTY_TAX,
            DEFAULT_HOME_INSURANCE,
            DEFAULT_PMI,
        ]

        self.ui.calcPushButton.clicked.connect(self.calculate_house)
        self.ui.resetPushButton.clicked.connect(self.reset)
        self.ui.calculatorButton.clicked.connect(self.display_calculator_page)
        self.ui.guideButton.clicked.connect(self.display_user_guide)

    def calculate_house(self) -> None:
        """
        Checks edit boxes are valid digits -> calculations are made.
        Invalid -> error message displays.
        """
        self.check_digits()
        calc = af_calc()
        calc.process_affordability(*self.parameters)
        self.load_calculations(calc)
        self.display_results()

    def check_digits(self) -> None:
        """Checks edit boxes -> either default values or entry"""
        self.parameters.clear()
        for index, edit in enumerate(self.edit_boxes):
            self.parameters.append(
                float(edit.text())
                if edit.text() != ""
                else self.default_values[index]
                )
        self.parameters.insert(3, float(self.ui.termComboBox.currentText()))

    def load_calculations(self, calc) -> None:
        """Processes calculations from AffordabilityCalculator"""
        self.home_affordability = calc.get_max_home_price()
        self.total_loan_cost = calc.get_total_loan_cost()
        self.total_principal = calc.get_total_loan_principal()
        self.total_interest = calc.get_total_loan_interest()
        if self.ui.dpEdit.text() != "" and self.home_affordability > 0:
            self.display_dp = round(
                float(self.ui.dpEdit.text()) / self.home_affordability * 100
            )
        else:
            self.display_dp = round(DEFAULT_DOWN_PAYMENT / self.home_affordability * 100)

    def display_results(self) -> None:
        """Display calculations in application header"""
        self.ui.homeAffordabilityLabelNumber.setText("$" + str(self.home_affordability))
        self.ui.totalCostLabelNumber.setText("$" + str(self.total_loan_cost))
        self.ui.principalLabelNumber.setText("$" + str(self.total_principal))
        self.ui.interestLabelNumber.setText("$" + str(self.total_interest))
        self.ui.downPaymentHeaderLabel.setText(f"Down Payment: {str(self.display_dp)}%")

        if int(self.display_dp) < RECCOMENDED_DP_PERCENTAGE:
            self.display_PMI_warning()

    def reset(self) -> None:
        """Resets all edit boxes to empty"""
        for edit in self.edit_boxes:
            edit.setText("")
        self.ui.termComboBox.setCurrentIndex(THIRTY_INDEX)
        self.ui.homeAffordabilityLabelNumber.setText("$0")
        self.ui.totalCostLabelNumber.setText("$0")
        self.ui.principalLabelNumber.setText("$0")
        self.ui.interestLabelNumber.setText("$0")
        self.ui.downPaymentHeaderLabel.setText("-")

    def open_guide(self) -> None:
        """returns user guide text or error for Github issue"""
        try:
            with open(PATH_TO_GUIDE, "r") as file:
                return file.read()
        except FileNotFoundError:
            return "File Not Found: Please open an issue -> https://github.com/Josh-Voyles/Home-Choice-Pro/issues"

    def display_calculator_page(self) -> None:
        """Set stacked widgeted index to show calculator"""
        self.ui.stackedWidget.setCurrentIndex(CALCULATOR_WINDOW)

    def display_user_guide(self) -> None:
        """Set stacked widgeted index to show user guide"""
        self.ui.stackedWidget.setCurrentIndex(USER_GUIDE_WINDOW)

    def display_PMI_warning(self) -> None:
        # assumes PMI is the last parameter, should write a test for correct order
        if not self.is_pmi_warned and self.parameters[-1] <= 0:
            print(self.parameters[-1])
            message = "Private Mortage Insurance typically required with down payments less than 20 percent"
            QMessageBox.warning(self, "PMI Error", message)
            self.is_pmi_warned = True
