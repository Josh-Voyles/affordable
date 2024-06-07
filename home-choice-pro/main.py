"""
Home Choice Pro Morgtage Calculator

This application calculates 'how much house you can afford' based on monthly payment.

UMGC CMSC 495 6380
Class Project
Joey Garcia
Josh Voyles
Randy Shreeves
Zaria Gibbs

This file will serve as the main entry point to the program.
"""

import sys

from PyQt5.QtWidgets import QApplication
from views.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
