from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QFormLayout, QFrame, QLineEdit, QVBoxLayout, \
    QPushButton


class ImagesSelectionForm(QWidget):
    finished = pyqtSignal()

    def __init__(self, dyssynchrony_configuration):
        super().__init__()
        self._dyssynchrony_configuration = dyssynchrony_configuration

        layout = QVBoxLayout()

        font = QFont()
        font.setPointSize(16)
        label = QLabel("Please complete the directory or the file you want to analyze, remember that the images need to be on .tif file format", self)
        label.setWordWrap(True)
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
        button.clicked.connect(self._form_submit)
        layout.addWidget(button)

        self.setLayout(layout)

    def _form_submit(self):
        self._validate_form()
        if self._is_form_valid():
            image_path = self._images_path_input.text()
            self._dyssynchrony_configuration.set_image_path(image_path)
            self.finished.emit()

    def _is_form_valid(self):
        return self._images_path_input.text() != ""

    def _validate_form(self):
        if self._images_path_input.text() == "":
            self._images_path_error.show()
        else:
            self._images_path_error.hide()

    def _set_up_form(self, widget):
        layout = QFormLayout(widget)

        images_path_label = QLabel("Path where the images are", widget)
        self._images_path_input = QLineEdit(widget)
        self._images_path_input.setText("/home/agusgs/Projects/CardiAP/DesktopApp/photos_examples/c1d000.tif")
        self._images_path_error = QLabel("This field is required")
        self._images_path_error.hide()

        layout.setWidget(0, QFormLayout.LabelRole, images_path_label)
        layout.setWidget(0, QFormLayout.FieldRole, self._images_path_input)
        layout.setWidget(1, QFormLayout.LabelRole, self._images_path_error)

        widget.setLayout(layout)
