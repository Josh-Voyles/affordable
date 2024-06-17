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
import os

from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets, QtCore, QtGui
from views.main_window import MainWindow

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
