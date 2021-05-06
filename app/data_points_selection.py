from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QFormLayout, QPushButton, QDialog, QDialogButtonBox, \
    QVBoxLayout


class DataPointsSelection(QWidget):
    finished = Signal()

    def __init__(self):
        super().__init__()

        self.setLayout(QGridLayout())
        self.setStyleSheet("QWidget#data_points_selection { border: 1px solid black; }")

        label = QLabel("Here you need to select the data you want to extract from the analysis.")
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(label, 0, 0, 1, 2, Qt.AlignHCenter)

        self._image_data_selection = QWidget()
        self.layout().addWidget(self._image_data_selection, 1, 0, 5, 1)

        self._slices_data_selection = QWidget()
        self.layout().addWidget(self._slices_data_selection, 1, 1, 5, 1)

        self.continue_button = QPushButton("Continue")
        self.layout().addWidget(self.continue_button, 6, 0, 1, 2)

    def set_image_data_points_selection_form(self, widget):
        widget.setObjectName("data_points_selection")
        self.layout().replaceWidget(self._image_data_selection, widget)
        self._image_data_selection.deleteLater()
        self._image_data_selection = widget

    def set_slices_data_points_selection_form(self, widget):
        widget.setObjectName("data_points_selection")
        self.layout().replaceWidget(self._slices_data_selection, widget)
        self._slices_data_selection.deleteLater()
        self._slices_data_selection = widget

    def show_need_to_check_modal(self):
        NeedToSelectDataPoint().exec()


class NeedToSelectDataPoint(QDialog):

    def __init__(self):
        super(self.__class__, self).__init__()

        self.setWindowTitle("CardiAP")

        label = QLabel(
            'You need to select the data points you want for the image and the slices')
        label.setWordWrap(True)
        button = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(button)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        self.layout.addWidget(label)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)