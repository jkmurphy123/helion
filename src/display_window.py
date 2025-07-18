# src/display_window.py

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class ConversationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Conversation Display")
        self.setStyleSheet("background-color: black; color: white;")
        self.setFont(QFont("Courier", 16))
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.label = QLabel("Starting up...")
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.showFullScreen()

    def update_text(self, text):
        self.label.setText(text)
