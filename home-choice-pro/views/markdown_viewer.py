import os
from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea
from PyQt5.QtGui import QTextCursor



class MarkdownViewer(QWidget):
    def __init__(self, file_path=None, go_back_callback=None):
        super().__init__()
        self.go_back_callback = go_back_callback
        self.initUI()
        if file_path:
            self.loadMarkdownFile(file_path)

    def initUI(self):
        self.layout = QVBoxLayout(self)

        # Create a Go Back button
        self.go_back_button = QPushButton("Go Back", self)
        self.go_back_button.clicked.connect(self.go_back)

        # Create a QTextEdit widget that will display the markdown content
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        # Create a QScrollArea and set its properties
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.text_edit)

        # Create a layout for the top bar with the Go Back button
        top_bar_layout = QHBoxLayout()
        top_bar_layout.addWidget(self.go_back_button)

        # Add the top bar and scroll area to the main layout
        self.layout.addLayout(top_bar_layout)
        self.layout.addWidget(scroll_area)

        # Load CSS style from file
        css_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'github-markdown.css')
        try:
            with open(css_path, 'r') as css_file:
                github_css = css_file.read()
            # Apply CSS style to the QTextEdit widget
            self.text_edit.setStyleSheet(github_css)
        except Exception as e:
            print(f"Error loading CSS file: {e}")

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

    def go_back(self):
        if self.go_back_callback:
            self.go_back_callback()

