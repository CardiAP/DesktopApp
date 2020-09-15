from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtWidgets import QWidget, QLabel, QFormLayout, QFrame, QLineEdit, QVBoxLayout, \
    QPushButton


class DyssynchronyAnalysisForm(QWidget):
    finished = pyqtSignal(dict)

    def __init__(self, dyssynchrony_configuration):
        super().__init__()

        self._dyssynchrony_configuration = dyssynchrony_configuration
        layout = QVBoxLayout()

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

        button = QPushButton("Continue", self)
        button.clicked.connect(self.form_submit)
        layout.addWidget(button)

        self.setLayout(layout)

    def form_submit(self):
        self._validate_form()
        if self._form_valid():
            form_data = {
                "slice_width": int(self._slice_width_input.text()),
                "min_dist_between_maxs": int(self._min_dist_input.text()),
                "calibration": float(self._calibration_input.text())
            }
            self.finished.emit(form_data)

    def _form_valid(self):
        form_inputs = [
            self._min_dist_input.text(),
            self._calibration_input.text(),
            self._slice_width_input.text()
        ]
        return len([value for value in form_inputs if value == ""]) == 0

    def _validate_form(self):
        if self._min_dist_input.text() == "":
            self._min_dist_error.show()
        else:
            self._min_dist_error.hide()

        if self._calibration_input.text() == "":
            self._calibration_error.show()
        else:
            self._calibration_error.hide()

        if self._slice_width_input.text() == "":
            self._slice_width_error.show()
        else:
            self._slice_width_error.hide()

    def _set_up_form(self, widget):
        layout = QFormLayout(widget)

        min_dist_label = QLabel("Minimum distance between peaks", widget)
        self._min_dist_input = QLineEdit(widget)
        self._min_dist_input.setMaxLength(4)
        self._min_dist_input.setValidator(QIntValidator(widget))
        self._min_dist_error = QLabel("This field is required")
        self._min_dist_error.hide()

        layout.setWidget(2, QFormLayout.LabelRole, min_dist_label)
        layout.setWidget(2, QFormLayout.FieldRole, self._min_dist_input)
        layout.setWidget(3, QFormLayout.LabelRole, self._min_dist_error)

        calibration_label = QLabel("Calibration", widget)
        self._calibration_input = QLineEdit(widget)
        self._calibration_input.setMaxLength(4)
        self._calibration_input.setValidator(QIntValidator(widget))
        self._calibration_error = QLabel("This field is required")
        self._calibration_error.hide()

        layout.setWidget(4, QFormLayout.LabelRole, calibration_label)
        layout.setWidget(4, QFormLayout.FieldRole, self._calibration_input)
        layout.setWidget(5, QFormLayout.LabelRole, self._calibration_error)

        slice_width_label = QLabel("The width (in pixels) of each slice", widget)
        self._slice_width_input = QLineEdit(widget)
        self._slice_width_input.setMaxLength(4)
        self._slice_width_input.setValidator(QIntValidator(widget))
        self._slice_width_input.setText("0")
        self._slice_width_error = QLabel("This field is required")
        self._slice_width_error.hide()

        layout.setWidget(6, QFormLayout.LabelRole, slice_width_label)
        layout.setWidget(6, QFormLayout.FieldRole, self._slice_width_input)
        layout.setWidget(7, QFormLayout.LabelRole, self._slice_width_error)

        widget.setLayout(layout)
