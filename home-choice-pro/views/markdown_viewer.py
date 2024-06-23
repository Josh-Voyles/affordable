"""
Home Choice Pro Morgtage Calculator

This application calculates 'how much house you can afford' based on monthly payment.

UMGC CMSC 495 6380
Class Project
Joey Garcia
Josh Voyles
Randy Shreeves
Zaria Gibbs

Calls UserGuide from the Main Window using a github css and markdown file 

"""

import os
from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea
from PyQt5.QtGui import QTextCursor



class MarkdownViewer(QWidget):
    def __init__(self, file_path=None, go_back_callback=None):
        super().__init__()
        self.go_back_callback = go_back_callback
        self.init_ui()
        if file_path:
            self.load_markdown_file(file_path)

    def init_ui(self):
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

        # Set CSS sheet
        self.set_stylesheet()

    def set_stylesheet(self):
        """ Load GitHub CSS stylesheet from resources directory """
        css_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'github-markdown.css')
        try:
            with open(css_path, 'r') as css_file:
                github_css = css_file.read()
            # Apply CSS style to the QTextEdit widget
            self.text_edit.setStyleSheet(github_css)
        except Exception as e:
            print(f"Error loading CSS file: {e}")

    def load_markdown_file(self, file_name):
        """ Loads Markdown File at Constructor Parameter Argument """
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                markdown_content = file.read()
                self.display_markdown(markdown_content)
        except Exception as e:
            print(f"Error reading file: {e}")

    def display_markdown(self, content):
        """ Sets & displays Markdown File """
        self.text_edit.clear()
        self.text_edit.setMarkdown(content)
        self.text_edit.moveCursor(QTextCursor.Start)

    def go_back(self):
        """ 'Go Back' Button defined behavior"""
        if self.go_back_callback:
            self.go_back_callback()

