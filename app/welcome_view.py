from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class WelcomeView(QWidget):
    def __init__(self):
        super().__init__()
        font = QFont()
        font.setPointSize(20)

        label = QLabel("Welcome to CardiAP please select an action of the menu")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(font)

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)