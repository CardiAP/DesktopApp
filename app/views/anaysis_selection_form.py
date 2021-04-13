from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QFormLayout, QFrame, QLineEdit, \
    QVBoxLayout, \
    QPushButton, QGridLayout, QFileDialog


class AnalysisSelectionForm(QWidget):
    form_submitted = pyqtSignal(str)
    ALTERNATION_DISCORDANCE = 'ALTERNATION_DISCORDANCE'
    WAVES = 'WAVES'
    SPARKS = 'SPARKS'
    AVAILABLE_ANALYSIS = [ALTERNATION_DISCORDANCE, WAVES, SPARKS]

    def __init__(self, path):
        super().__init__()
        self._filenames = None
        self._analysis_type = None
        self.layout = QGridLayout()

        font = QFont()
        font.setPointSize(16)
        select_images_button = QPushButton("Select the images you want to analyze", self)
        select_images_button.setWordWrap(True)
        select_images_button.setFont(font)
        select_images_button.clicked.connect(self._open_file_selector)

        self.layout.addWidget(select_images_button, 0, 1)

        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(line)

        button = QPushButton("Continue", self)
        button.clicked.connect(self._form_submit)
        self.layout.addWidget(button, 1, 0, 1, 2)

        self.setLayout(self.layout)

    def _form_submit(self):
        self._validate_form()
        if self._is_form_valid():
            self.form_submitted.emit(self._images_path_input.text())

    def _is_form_valid(self):
        return self._images_path_input.text() != ""

    def _validate_form(self):
        if self._images_path_input.text() == "":
            self._images_path_error.show()
        else:
            self._images_path_error.hide()

    def _open_file_selector(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setFilter("Image files (*.tif)")

        if dlg.exec_():
            self._filenames = dlg.selectedFiles()
