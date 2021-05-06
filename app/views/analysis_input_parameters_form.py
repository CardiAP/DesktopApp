from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit

from app.models.input_parameters import InputParameters
from app.views.input_error_message import InputErrorMessage


class AnalysisInputParametersForm(QWidget):
    def __init__(self, input_parameters):
        super().__init__()
        self._setup_form(input_parameters)

    def _setup_form(self, input_parameters):
        layout = QGridLayout()

        min_dist_label = QLabel("Minimum distance between peaks", self)
        layout.addWidget(min_dist_label, 0, 0, 1, 2)

        bigger_than_zero_validator = QIntValidator(self)
        bigger_than_zero_validator.setBottom(1)

        self._min_dist_error = InputErrorMessage(
            "You need to provide a number bigger than zero")
        self._min_dist_error.hide()
        layout.addWidget(self._min_dist_error, 1, 0, 1, 2)

        self._min_dist_input = QLineEdit(self)
        self._min_dist_input.setMaxLength(4)
        self._min_dist_input.setValidator(bigger_than_zero_validator)
        self._min_dist_input.setText(str(input_parameters.min_dist or ''))
        layout.addWidget(self._min_dist_input, 2, 0, 1, 2)

        calibration_label = QLabel("Calibration", self)
        layout.addWidget(calibration_label, 3, 0, 1, 2)

        self._calibration_error = InputErrorMessage(
            "You need to provide a number bigger than zero")
        self._calibration_error.hide()
        layout.addWidget(self._calibration_error, 4, 0, 1, 2)

        self._calibration_input = QLineEdit(self)
        self._calibration_input.setMaxLength(4)
        self._calibration_input.setValidator(bigger_than_zero_validator)
        self._calibration_input.setText(
            str(input_parameters.calibration or ''))
        layout.addWidget(self._calibration_input, 5, 0, 1, 2)

        slice_width_label = QLabel("The width (in pixels) of each slice",
                                   self)
        layout.addWidget(slice_width_label, 6, 0, 1, 2)

        self._slice_width_error = InputErrorMessage(
            "You need to provide a number bigger or equal to zero")
        self._slice_width_error.hide()
        layout.addWidget(self._slice_width_error, 7, 0, 1, 2)

        slice_with_validator = QIntValidator(self)
        slice_with_validator.setBottom(0)
        self._slice_width_input = QLineEdit(self)
        self._slice_width_input.setMaxLength(4)
        self._slice_width_input.setValidator(slice_with_validator)
        self._slice_width_input.setText(str(input_parameters.slice_width))
        layout.addWidget(self._slice_width_input, 8, 0, 1, 2)

        self.setLayout(layout)

    def _from_string_to_int_or_none(self, value):
        if value is not None and value != '':
            return int(value)
        else:
            return None

    def parametrization(self):
        min_dist = self._from_string_to_int_or_none(
            self._min_dist_input.text())
        calibration = self._from_string_to_int_or_none(
            self._calibration_input.text())
        slice_width = self._from_string_to_int_or_none(
            self._slice_width_input.text())
        return InputParameters(min_dist, calibration, slice_width)

    def handle_errors(self, errors):
        self._clear_errors()
        errors.send_details_to(self)

    def _clear_errors(self):
        self._min_dist_error.hide()
        self._slice_width_error.hide()
        self._calibration_error.hide()

    def error_in_slice_width(self):
        self._slice_width_error.show()

    def error_in_calibration(self):
        self._calibration_error.show()

    def error_in_min_dist(self):
        self._min_dist_error.show()
