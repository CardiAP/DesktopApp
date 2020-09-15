from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QFormLayout, QFrame, QLineEdit, QVBoxLayout, \
    QPushButton


class OutputForm(QWidget):
    def __init__(self, main_windown, results):
        super().__init__()
        self._results = results
        self._main_windown = main_windown

        layout = QVBoxLayout()

        font = QFont()
        font.setPointSize(12)
        label = QLabel("Please select the path to save the json result", self)
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

        button = QPushButton("Save", self)
        button.clicked.connect(self.form_submit)
        layout.addWidget(button)

        self.setLayout(layout)

    def form_submit(self):
        self._validate_form()
        if not self._form_valid():
            self._save_file()

    def _save_file(self):
        print("piolita")

    def _form_valid(self):
        form_inputs = [
            self._images_path_error.text(),
            self._min_dist_input.text(),
            self._calibration_input.text(),
            self._slice_width_input.text()
        ]
        return len([value for value in form_inputs if value == ""]) > 0

    def _validate_form(self):
        if self._output_path_input.text() == "":
            self._output_path_error.show()
        else:
            self._output_path_error.hide()

    def _set_up_form(self, widget):
        layout = QFormLayout(widget)

        output_path_label = QLabel("Path to save the json file", widget)
        self._output_path_input = QLineEdit(widget)
        self._output_path_error = QLabel("This field is required")
        self._output_path_error.hide()

        layout.setWidget(0, QFormLayout.LabelRole, output_path_label)
        layout.setWidget(0, QFormLayout.FieldRole, self._output_path_input)
        layout.setWidget(1, QFormLayout.LabelRole, self._output_path_error)

        widget.setLayout(layout)
