from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class ConversationWindow(QWidget):
    def __init__(self, background_image, dialog_x, dialog_y, dialog_width, dialog_height):
        super().__init__()
        self.setWindowTitle("AI Conversation")
        self.showFullScreen()

        # Set background image
        self.background_label = QLabel(self)
        pixmap = QPixmap(background_image)
        self.background_label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        self.background_label.setGeometry(0, 0, self.width(), self.height())

        # Set dialog box
        self.text_area = QTextEdit(self)
        self.text_area.setGeometry(dialog_x, dialog_y, dialog_width, dialog_height)
        self.text_area.setStyleSheet("background-color: rgba(255, 255, 255, 180); color: black; font-size: 18px;")
        self.text_area.setReadOnly(True)

    def update_text(self, text):
        self.text_area.setPlainText(text)
