"""
Home Choice Pro Morgtage Calculator

This application calculates 'how much house you can afford' based on monthly payment.

UMGC CMSC 495 6380
Class Project
Joey Garcia
Josh Voyles
Randy Shreeves
Zaria Gibbs

Main Window Test Cases Below

"""

import pytest
import os
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore
from views.main_window import MainWindow

PATH_TO_GUIDE = os.path.join(
    os.path.dirname(__file__), "..", "..", "docs", "user_guide.md"
)


# main window
@pytest.fixture
def main_window(qtbot):
    main_window = MainWindow()
    main_window.show()
    qtbot.addWidget(main_window)
    yield main_window


@pytest.fixture
def mock_qmessagebox(qtbot):
    """This fixture sinks the QMessageBox to prevent the pop up"""

    def mock_messagebox(*args, **kwargs):
        msgbox = QMessageBox()
        msgbox.setText("Mock Message Box")
        msgbox.setStandardButtons(QMessageBox.Ok)
        return msgbox

    QMessageBox.warning = mock_messagebox
    QMessageBox.information = mock_messagebox
    QMessageBox.critical = mock_messagebox


def test_main_window(main_window):
    assert isinstance(main_window, MainWindow)


# make sure we title our app
def test_window_title(main_window):
    assert main_window.windowTitle() == "Home Choice Pro"


# Side Panel
def test_logo(main_window):
    assert main_window.ui.Logo.isVisible()


# Calc button
def test_calculator_button(main_window):
    assert main_window.ui.calculatorButton.isChecked()


# verify starting values for each edit box
def test_empty_edit_boxes(main_window):
    assert main_window.ui.monthlyPaymentEdit.text() == "0"
    assert main_window.ui.dpEdit.text() == "0"
    assert main_window.ui.interestRateEdit.text() == "0"
    assert main_window.ui.HOAEdit.text() == "0"


def test_verify_digits(main_window):
    main_window.ui.monthlyPaymentEdit.setText("1")
    main_window.ui.dpEdit.setText("1")
    main_window.ui.interestRateEdit.setText("1")
    assert main_window.verify_digits() is True
    main_window.ui.monthlyPaymentEdit.setText("a")
    main_window.ui.dpEdit.setText("1")
    main_window.ui.interestRateEdit.setText("1")
    assert main_window.verify_digits() is False
    main_window.ui.monthlyPaymentEdit.setText("1")
    main_window.ui.dpEdit.setText("b")
    main_window.ui.interestRateEdit.setText("1")
    assert main_window.verify_digits() is False
    main_window.ui.monthlyPaymentEdit.setText("1")
    main_window.ui.dpEdit.setText("1")
    main_window.ui.interestRateEdit.setText("c")
    assert main_window.verify_digits() is False
    main_window.ui.monthlyPaymentEdit.setText("")
    main_window.ui.dpEdit.setText("1")
    main_window.ui.interestRateEdit.setText("1")
    assert main_window.verify_digits() is False
    main_window.ui.monthlyPaymentEdit.setText("1")
    main_window.ui.dpEdit.setText("1")
    main_window.ui.interestRateEdit.setText(" ")
    assert main_window.verify_digits() is False
    main_window.ui.monthlyPaymentEdit.setText("1")
    main_window.ui.dpEdit.setText("1")
    main_window.ui.interestRateEdit.setText("1")
    main_window.ui.HOAEdit.setText("1")
    assert main_window.verify_digits() is True
    main_window.ui.monthlyPaymentEdit.setText("1")
    main_window.ui.dpEdit.setText("1")
    main_window.ui.interestRateEdit.setText("1")
    main_window.ui.HOAEdit.setText("b")
    assert main_window.verify_digits() is False


def test_monthly_payment_edit(main_window, qtbot):
    main_window.ui.monthlyPaymentEdit.clear()
    qtbot.keyClicks(main_window.ui.monthlyPaymentEdit, "12345")
    assert main_window.ui.monthlyPaymentEdit.text() == "12345"


def test_dpEdit(main_window, qtbot):
    main_window.ui.dpEdit.clear()
    qtbot.keyClicks(main_window.ui.dpEdit, "12345")
    assert main_window.ui.dpEdit.text() == "12345"


def test_interest_rate_edit(main_window, qtbot):
    main_window.ui.interestRateEdit.clear()
    qtbot.keyClicks(main_window.ui.interestRateEdit, "12345")
    assert main_window.ui.interestRateEdit.text() == "12345"


def test_loan_term_box(main_window, qtbot):
    assert main_window.ui.termComboBox.currentText() == "30"
    qtbot.mouseClick(main_window.ui.termComboBox, QtCore.Qt.LeftButton)
    qtbot.keyClicks(main_window.ui.termComboBox, "15")
    assert main_window.ui.termComboBox.currentText() == "15"


def test_hoa_edit(main_window, qtbot):
    assert main_window.ui.HOAEdit.text() == "0"
    main_window.ui.HOAEdit.clear()
    qtbot.keyClicks(main_window.ui.HOAEdit, "12345")
    assert main_window.ui.HOAEdit.text() == "12345"


def test_property_tax_edit(main_window, qtbot):
    assert main_window.ui.propertyTaxEdit.text() == "0"
    main_window.ui.propertyTaxEdit.clear()
    qtbot.keyClicks(main_window.ui.propertyTaxEdit, "0.74")
    assert main_window.ui.propertyTaxEdit.text() == "0.74"


def test_insurance_edit(main_window, qtbot):
    assert main_window.ui.insuranceEdit.text() == "0"
    main_window.ui.propertyTaxEdit.clear()
    qtbot.keyClicks(main_window.ui.propertyTaxEdit, "0.5")
    assert main_window.ui.propertyTaxEdit.text() == "0.5"


def test_PMI_edit(main_window, qtbot):
    assert main_window.ui.PMIEdit.text() == "0"
    main_window.ui.PMIEdit.clear()
    qtbot.keyClicks(main_window.ui.PMIEdit, "0.34")
    assert main_window.ui.PMIEdit.text() == "0.34"


def test_calculate_house(main_window, mock_qmessagebox, qtbot):
    """Tests known values and validates the result"""
    # enter values in gui
    main_window.ui.monthlyPaymentEdit.clear()
    qtbot.keyClicks(main_window.ui.monthlyPaymentEdit, "1300")
    main_window.ui.dpEdit.clear()
    qtbot.keyClicks(main_window.ui.dpEdit, "1")
    main_window.ui.interestRateEdit.clear()
    main_window.ui.HOAEdit.clear()
    qtbot.keyClicks(main_window.ui.HOAEdit, "300")
    qtbot.keyClicks(main_window.ui.interestRateEdit, "1")
    qtbot.mouseClick(main_window.ui.calcPushButton, QtCore.Qt.LeftButton)
    assert main_window.ui.homeAffordabilityLabelNumber.text() == "$310908"
    assert main_window.ui.totalCostLabelNumber.text() == "$360000"
    assert main_window.ui.principalLabelNumber.text() == "$310907"
    assert main_window.ui.interestLabelNumber.text() == "$49093"
    assert main_window.ui.downPaymentHeaderLabel.text() == "Down Payment: 0%"


def test_calculate_house_2(main_window, mock_qmessagebox, qtbot):
    """Tests known values and validates the result"""
    # enter values in gui
    main_window.ui.monthlyPaymentEdit.clear()
    qtbot.keyClicks(main_window.ui.monthlyPaymentEdit, "2400")
    main_window.ui.dpEdit.clear()
    qtbot.keyClicks(main_window.ui.dpEdit, "50000")
    main_window.ui.interestRateEdit.clear()
    main_window.ui.HOAEdit.clear()
    qtbot.keyClicks(main_window.ui.HOAEdit, "350")
    qtbot.keyClicks(main_window.ui.interestRateEdit, "6.125")
    qtbot.mouseClick(main_window.ui.termComboBox, QtCore.Qt.LeftButton)
    qtbot.keyClicks(main_window.ui.termComboBox, "15")
    main_window.ui.propertyTaxEdit.clear()
    qtbot.keyClicks(main_window.ui.propertyTaxEdit, "0.74")
    qtbot.mouseClick(main_window.ui.calcPushButton, QtCore.Qt.LeftButton)
    assert main_window.ui.homeAffordabilityLabelNumber.text() == "$271329"
    assert main_window.ui.totalCostLabelNumber.text() == "$338882"
    assert main_window.ui.principalLabelNumber.text() == "$221329"
    assert main_window.ui.interestLabelNumber.text() == "$117553"
    assert main_window.ui.downPaymentHeaderLabel.text() == "Down Payment: 18%"


def test_calculate_house_3(main_window, mock_qmessagebox, qtbot):
    """Third calculation test adding PMI and insurance"""
    # enter values in gui
    main_window.ui.monthlyPaymentEdit.clear()
    qtbot.keyClicks(main_window.ui.monthlyPaymentEdit, "2400")
    main_window.ui.dpEdit.clear()
    qtbot.keyClicks(main_window.ui.dpEdit, "50000")
    main_window.ui.interestRateEdit.clear()
    main_window.ui.HOAEdit.clear()
    qtbot.keyClicks(main_window.ui.HOAEdit, "350")
    qtbot.keyClicks(main_window.ui.interestRateEdit, "6.125")
    qtbot.mouseClick(main_window.ui.termComboBox, QtCore.Qt.LeftButton)
    qtbot.keyClicks(main_window.ui.termComboBox, "30")
    main_window.ui.propertyTaxEdit.clear()
    qtbot.keyClicks(main_window.ui.propertyTaxEdit, "0.74")
    main_window.ui.PMIEdit.clear()
    qtbot.keyClicks(main_window.ui.PMIEdit, "0.5")
    main_window.ui.insuranceEdit.clear()
    qtbot.keyClicks(main_window.ui.insuranceEdit, "0.34")
    qtbot.mouseClick(main_window.ui.calcPushButton, QtCore.Qt.LeftButton)
    assert main_window.ui.homeAffordabilityLabelNumber.text() == "$321210"
    assert main_window.ui.totalCostLabelNumber.text() == "$593244"
    assert main_window.ui.principalLabelNumber.text() == "$271210"
    assert main_window.ui.interestLabelNumber.text() == "$322034"
    assert main_window.ui.downPaymentHeaderLabel.text() == "Down Payment: 16%"


def test_reset(main_window, qtbot):
    """
    Tests user's interaction with text edit boxes.
    Simulates entering values in all boxes.
    Resets all boxes to default including downpayment label
    """
    # test entering values
    main_window.ui.monthlyPaymentEdit.clear()
    qtbot.keyClicks(main_window.ui.monthlyPaymentEdit, "12345")
    main_window.ui.dpEdit.clear()
    qtbot.keyClicks(main_window.ui.dpEdit, "12345")
    main_window.ui.interestRateEdit.clear()
    qtbot.keyClicks(main_window.ui.interestRateEdit, "12345")
    main_window.ui.HOAEdit.clear()
    qtbot.keyClicks(main_window.ui.HOAEdit, "300")
    qtbot.mouseClick(main_window.ui.termComboBox, QtCore.Qt.LeftButton)
    qtbot.keyClicks(main_window.ui.termComboBox, "15")
    main_window.ui.propertyTaxEdit.clear()
    qtbot.keyClicks(main_window.ui.propertyTaxEdit, "0.74")
    main_window.ui.PMIEdit.clear()
    qtbot.keyClicks(main_window.ui.PMIEdit, "0.5")
    main_window.ui.insuranceEdit.clear()
    qtbot.keyClicks(main_window.ui.insuranceEdit, "0.34")
    # reset
    qtbot.mouseClick(main_window.ui.resetPushButton, QtCore.Qt.LeftButton)
    # validate cleared
    assert main_window.ui.monthlyPaymentEdit.text() == "0"
    assert main_window.ui.dpEdit.text() == "0"
    assert main_window.ui.interestRateEdit.text() == "0"
    assert main_window.ui.termComboBox.currentText() == "30"
    assert main_window.ui.HOAEdit.text() == "0"
    assert main_window.ui.propertyTaxEdit.text() == "0"
    assert main_window.ui.PMIEdit.text() == "0"
    assert main_window.ui.insuranceEdit.text() == "0"
    assert main_window.ui.homeAffordabilityLabelNumber.text() == "$0"
    assert main_window.ui.totalCostLabelNumber.text() == "$0"
    assert main_window.ui.principalLabelNumber.text() == "$0"
    assert main_window.ui.interestLabelNumber.text() == "$0"
    assert main_window.ui.downPaymentHeaderLabel.text() == "-"


def test_open_file(main_window):
    guide = main_window.ui.guideLabel.text()
    with open(PATH_TO_GUIDE, "r") as file:
        test_guide = file.read()
    assert guide == test_guide


def test_display_pages(main_window, qtbot):
    """Tests user interaction with side panel navigaton buttons"""
    assert main_window.ui.calculatorPage.isVisible()
    qtbot.mouseClick(main_window.ui.guideButton, QtCore.Qt.LeftButton)
    assert main_window.ui.guidePage.isVisible()
    qtbot.mouseClick(main_window.ui.calculatorButton, QtCore.Qt.LeftButton)
    assert main_window.ui.calculatorPage.isVisible()


# this should be the last thing
def test_quit(main_window, qtbot):
    """Tests user's ability to quit the application"""
    assert main_window.isVisible()
    qtbot.mouseClick(main_window.ui.quitButton, QtCore.Qt.LeftButton)
    assert not main_window.isVisible()
