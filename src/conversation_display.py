import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConversationWindow()

    # Example: Simulate text updates
    messages = [
        "Talker: Let's talk about dreams.",
        "Listener: Oh, dreams are rather intriguing, aren't they!",
        "Talker: Well, aren't we just a regular Edgar Allan Poe?",
        "Listener: Guess we're not so different after all, huh?"
    ]

    index = 0

    def update():
        nonlocal index
        if index < len(messages):
            window.update_text("\n".join(messages[:index+1]))
            index += 1
        else:
            timer.stop()

    timer = QTimer()
    timer.timeout.connect(update)
    timer.start(3000)  # update every 3 seconds

    sys.exit(app.exec_())
