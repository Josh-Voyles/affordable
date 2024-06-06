
from PyQt5.QtWidgets import QMainWindow
from views.pop_up_error_window_ui import Ui_Form

class ErrorWindow(QMainWindow):
    def __init__(self):
        super(ErrorWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.setWindowTitle("Home Choice Pro")
