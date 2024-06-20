import sys
import os
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QFileDialog, QAction, QScrollArea
from PyQt5.QtGui import QTextCursor



class MarkdownViewer(QMainWindow):
    def __init__(self, file_path=None):
        super().__init__()
        self.initUI()
        if file_path:
            self.loadMarkdownFile(file_path)

    def initUI(self):
        self.setWindowTitle("Markdown Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.text_edit)

        self.setCentralWidget(scroll_area)

        openFile = QAction('Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        # Load CSS style from file
        css_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'github-markdown.css')
        with open(css_path, 'r') as css_file:
            github_css = css_file.read()

        # Apply CSS style to the QTextEdit widget
        self.text_edit.setStyleSheet(github_css)

    def showDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Markdown File", "", "Markdown Files (*.md);;All Files (*)", options=options)
        if fileName:
            self.loadMarkdownFile(fileName)

    def loadMarkdownFile(self, fileName):
        try:
            with open(fileName, 'r', encoding='utf-8') as file:
                markdown_content = file.read()
                self.displayMarkdown(markdown_content)
        except Exception as e:
            print(f"Error reading file: {e}")

    def displayMarkdown(self, content):
        self.text_edit.clear()
        self.text_edit.setMarkdown(content)
        self.text_edit.moveCursor(QTextCursor.Start)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = None
