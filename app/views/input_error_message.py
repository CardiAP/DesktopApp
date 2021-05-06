from PySide6.QtWidgets import QLabel


class InputErrorMessage(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("color: red; font-size: 12px;")