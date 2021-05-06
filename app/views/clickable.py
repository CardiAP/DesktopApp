from PySide6.QtCore import QEvent, Signal
from PySide6.QtWidgets import QWidget


class Clickable(QWidget):
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        is_for_me = obj == self
        is_a_click_event = event.type() == QEvent.MouseButtonRelease
        is_inside_me = is_a_click_event and obj.rect().contains(event.pos())

        if is_for_me and is_inside_me:
            self.clicked.emit()
            return True
        else:
            return False