from PyQt5.QtWidgets import QApplication, QMessageBox
import sys

class ErrorHandler:
    def __init__(self):
        self.app = QApplication(sys.argv)

    def show_error(self, title, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle(title)
        error_box.setText(message)
        error_box.setStandardButtons(QMessageBox.Ok)
        error_box.exec_()
        self.app.quit()  # Ensure QApplication is properly closed