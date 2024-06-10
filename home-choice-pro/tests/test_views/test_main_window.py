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
from PyQt5 import QtCore
from views.main_window import MainWindow 
from views.pop_up_error_window import ErrorWindow

# main window
@pytest.fixture
def main_window(qtbot):
    main_window = MainWindow()
    main_window.show()
    qtbot.addWidget(main_window)
    yield main_window

def test_main_window(main_window):
    assert isinstance(main_window, MainWindow)

# make sure we title our app
def test_window_title(main_window):
    assert main_window.windowTitle() == 'Home Choice Pro'

# Side Panel
def test_logo(main_window):
    assert main_window.ui.Logo.isVisible()

# Calc button
def test_calculator_button(main_window):
    assert main_window.ui.calculatorButton.isChecked()

# verify starting values for each edit box
def test_empty_edit_boxes(main_window):
    assert main_window.ui.monthlyPaymentEdit.text() == '0'
    assert main_window.ui.dpEdit.text() == '0'
    assert main_window.ui.interestRateEdit.text() == '0'


def test_verify_digits(main_window):
    main_window.ui.monthlyPaymentEdit.setText('1')
    main_window.ui.dpEdit.setText('1')
    main_window.ui.interestRateEdit.setText('1')
    assert main_window.verify_digits() == True
    main_window.ui.monthlyPaymentEdit.setText('a')
    main_window.ui.dpEdit.setText('1')
    main_window.ui.interestRateEdit.setText('1')
    assert main_window.verify_digits() == False
    main_window.ui.monthlyPaymentEdit.setText('1')
    main_window.ui.dpEdit.setText('b')
    main_window.ui.interestRateEdit.setText('1')
    assert main_window.verify_digits() == False
    main_window.ui.monthlyPaymentEdit.setText('1')
    main_window.ui.dpEdit.setText('1')
    main_window.ui.interestRateEdit.setText('c')
    assert main_window.verify_digits() == False
    main_window.ui.monthlyPaymentEdit.setText('')
    main_window.ui.dpEdit.setText('1')
    main_window.ui.interestRateEdit.setText('1')
    assert main_window.verify_digits() == False
    main_window.ui.monthlyPaymentEdit.setText('1')
    main_window.ui.dpEdit.setText('1')
    main_window.ui.interestRateEdit.setText(' ')
    assert main_window.verify_digits() == False

def test_display_error(main_window, qtbot):
    main_window.display_error()
    assert isinstance(main_window.error, ErrorWindow)
    assert main_window.error.isVisible()
    assert main_window.error.windowTitle() == 'Home Choice Pro'
    # had trouble with error window message, will come back since changing anway
    qtbot.mouseClick(main_window.error.ui.closeButton, QtCore.Qt.LeftButton)
    assert not main_window.error.isVisible()

    
def test_monthly_payment_edit(main_window, qtbot):
    main_window.ui.monthlyPaymentEdit.clear()
    qtbot.keyClicks(main_window.ui.monthlyPaymentEdit, '12345')
    assert main_window.ui.monthlyPaymentEdit.text() == '12345'

def test_dpEdit(main_window, qtbot):
    main_window.ui.dpEdit.clear()
    qtbot.keyClicks(main_window.ui.dpEdit, '12345')
    assert main_window.ui.dpEdit.text() == '12345'

def test_interest_rate_edit(main_window, qtbot):
    main_window.ui.interestRateEdit.clear()
    qtbot.keyClicks(main_window.ui.interestRateEdit, '12345')
    assert main_window.ui.interestRateEdit.text() == '12345'

def test_radial_buttons(main_window, qtbot):
    assert main_window.ui.radioButtonDollar.isChecked()
    qtbot.mouseClick(main_window.ui.radioButtonPercent, QtCore.Qt.LeftButton)
    assert main_window.ui.radioButtonPercent.isChecked()

def test_loan_term_box(main_window, qtbot):
    assert main_window.ui.termComboBox.currentText() == '30'
    qtbot.mouseClick(main_window.ui.termComboBox, QtCore.Qt.LeftButton)
    qtbot.keyClicks(main_window.ui.termComboBox, '15')
    assert main_window.ui.termComboBox.currentText() == '15'

def test_calculate_house(main_window, qtbot):
    main_window.ui.monthlyPaymentEdit.clear()
    qtbot.keyClicks(main_window.ui.monthlyPaymentEdit, '1000')
    main_window.ui.dpEdit.clear()
    qtbot.keyClicks(main_window.ui.dpEdit, '1')
    main_window.ui.interestRateEdit.clear()
    qtbot.keyClicks(main_window.ui.interestRateEdit, '1')
    qtbot.mouseClick(main_window.ui.calcPushButton, QtCore.Qt.LeftButton)
    assert main_window.ui.homeAffordabilityLabelNumber.text() == '$310908'
    assert main_window.ui.totalCostLabelNumber.text() == '$360000'
    assert main_window.ui.principalLabelNumber.text() == '$310907'
    assert main_window.ui.interestLabelNumber.text() == '$49093'


def test_reset(main_window, qtbot):
    main_window.ui.monthlyPaymentEdit.clear()
    qtbot.keyClicks(main_window.ui.monthlyPaymentEdit, '12345')
    main_window.ui.dpEdit.clear()
    qtbot.keyClicks(main_window.ui.dpEdit, '12345')
    main_window.ui.interestRateEdit.clear()
    qtbot.keyClicks(main_window.ui.interestRateEdit, '12345')
    qtbot.mouseClick(main_window.ui.radioButtonPercent, QtCore.Qt.LeftButton)
    qtbot.mouseClick(main_window.ui.termComboBox, QtCore.Qt.LeftButton)
    qtbot.keyClicks(main_window.ui.termComboBox, '15')
    qtbot.mouseClick(main_window.ui.resetPushButton, QtCore.Qt.LeftButton)
    assert main_window.ui.monthlyPaymentEdit.text() == '0'
    assert main_window.ui.dpEdit.text() == '0'
    assert main_window.ui.interestRateEdit.text() == '0'
    assert main_window.ui.termComboBox.currentText() == '30'
    assert main_window.ui.radioButtonDollar.isChecked()
    assert main_window.ui.homeAffordabilityLabelNumber.text() == '$0'
    assert main_window.ui.totalCostLabelNumber.text() == '$0'
    assert main_window.ui.principalLabelNumber.text() == '$0'
    assert main_window.ui.interestLabelNumber.text() == '$0'


# this should be the last thing
def test_quit(main_window, qtbot):
    assert main_window.isVisible()
    qtbot.mouseClick(main_window.ui.quitButton, QtCore.Qt.LeftButton)
    assert not main_window.isVisible()

