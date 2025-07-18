from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QTimer

class DisplayWindow(QWidget):
    def __init__(self, image_path, dialog_x, dialog_y, dialog_width, dialog_height):
        super().__init__()
        self.setWindowTitle("AI Conversation")
        self.setStyleSheet("background-color: black;")
        self.image_path = image_path
        self.pixmap = QPixmap(image_path)

        # Set up dialog label
        self.dialog_label = QLabel(self)
        self.dialog_label.setWordWrap(True)
        self.dialog_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.dialog_label.setStyleSheet("""
            color: white;
            background-color: rgba(0, 0, 0, 180);
            border-radius: 12px;
            padding: 15px;
            font-size: 24px;
            font-family: 'Arial';
        """)

        # Position and size from config
        self.dialog_label.setGeometry(dialog_x, dialog_y, dialog_width, dialog_height)

        # Timer to auto-clear text (optional)
        self.clear_timer = QTimer()
        self.clear_timer.setSingleShot(True)
        self.clear_timer.timeout.connect(self.clear_text)

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self.pixmap.isNull():
            painter.drawPixmap(self.rect(), self.pixmap)

    def display_text(self, text, display_ms=15000):
        self.dialog_label.setText(text)
        self.clear_timer.start(display_ms)

    def clear_text(self):
        self.dialog_label.setText("")
