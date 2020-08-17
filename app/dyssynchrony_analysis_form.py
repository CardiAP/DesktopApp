from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtWidgets import QWidget, QLabel, QFormLayout, QFrame, QSpacerItem, QSizePolicy, QLineEdit, QVBoxLayout


class DyssynchronyAnalysisForm(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        font = QFont()
        font.setPointSize(12)
        label = QLabel("Complete the form to perform the analysis", self)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(font)
        layout.addWidget(label)

        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        form_widget = QWidget(self)
        self._set_up_form(form_widget)
        layout.addWidget(form_widget)

        self.setLayout(layout)

    def _set_up_form(self, widget):
        layout = QFormLayout(widget)

        images_path_label = QLabel("Path where the images are", self)
        images_path_input = QLineEdit(self)

        layout.setWidget(0, QFormLayout.LabelRole, images_path_label)
        layout.setWidget(0, QFormLayout.FieldRole, images_path_input)

        min_dist_label = QLabel("Minimum distance between peaks", self)
        min_dist_input = QLineEdit(self)
        min_dist_input.setMaxLength(4)
        min_dist_input.setValidator(QIntValidator(self))

        layout.setWidget(1, QFormLayout.LabelRole, min_dist_label)
        layout.setWidget(1, QFormLayout.FieldRole, min_dist_input)

        calibration_label = QLabel("Calibration", self)
        calibration_input = QLineEdit(self)
        calibration_input.setMaxLength(4)
        calibration_input.setValidator(QIntValidator(self))

        layout.setWidget(2, QFormLayout.LabelRole, calibration_label)
        layout.setWidget(2, QFormLayout.FieldRole, calibration_input)

        slice_width_label = QLabel("Calibration", self)
        slice_width_input = QLineEdit(self)
        slice_width_input.setMaxLength(4)
        slice_width_input.setValidator(QIntValidator(self))

        layout.setWidget(3, QFormLayout.LabelRole, slice_width_label)
        layout.setWidget(3, QFormLayout.FieldRole, slice_width_input)

        widget.setLayout(layout)
