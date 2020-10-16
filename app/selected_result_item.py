from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QStyle


class SelectedResultItem(QWidget):
    remove_clicked = pyqtSignal(int)

    def __init__(self, parent, selected_result):
        super(SelectedResultItem, self).__init__(parent=parent)
        image_id, image_name = selected_result
        self.setLayout(QGridLayout())
        self._label = QLabel(image_name, parent=self)
        self._button = QPushButton(parent=self)
        self._button.setIcon(self.style().standardIcon(getattr(QStyle, "SP_DialogDiscardButton")))
        self._button.clicked.connect(lambda: self.remove_clicked.emit(image_id))
        self._button.setToolTip("Remove this image from the selected results")
        self.layout().addWidget(self._label, 0, 0)
        self.layout().addWidget(self._button, 0, 1)