from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QPushButton, QGridLayout, QDialog, QLabel, \
    QDialogButtonBox


class AnalysisResultsRefinement(QWidget):
    finished = pyqtSignal()

    def __init__(self):
        super(AnalysisResultsRefinement, self).__init__()
        self.setLayout(QVBoxLayout())

        self._content_section = QWidget()
        self.layout().addWidget(self._content_section)
        self._content_section.setLayout(QGridLayout())

        self._analysis_results_overview = QTabWidget(self)
        self._content_section.layout().addWidget(self._analysis_results_overview, 0, 0)
        self._selected_results = QWidget(self)
        self._content_section.layout().addWidget(self._selected_results, 0, 1)

        self._actions_section = QWidget(self)
        self.layout().addWidget(self._actions_section)

        self._setup_continue_buttons()

    def _setup_continue_buttons(self):
        self._actions_section.setLayout(QHBoxLayout())
        self.select_all_and_continue_button = QPushButton("Select all and continue", parent=self)
        self.continue_button = QPushButton("Continue with selected results", parent=self)

        self._actions_section.layout().addWidget(self.select_all_and_continue_button)
        self._actions_section.layout().addWidget(self.continue_button)

    def set_selected_results_section(self, view):
        self._content_section.layout().removeWidget(self._selected_results)
        self._selected_results.deleteLater()
        self._selected_results = view
        self._selected_results.setParent(self)
        self._content_section.layout().addWidget(self._selected_results, 0, 4, 1, 1, Qt.AlignTop)

    def set_analysis_overview_section(self, view):
        self._content_section.layout().removeWidget(self._analysis_results_overview)
        self._analysis_results_overview.deleteLater()
        self._analysis_results_overview = view
        self._analysis_results_overview.setParent(self)
        self._content_section.layout().addWidget(self._analysis_results_overview, 0, 0, 1, 3, Qt.AlignTop)
        self._analysis_results_overview.currentChanged.emit(0)

    def show_no_selected_result(self):
        NeedToSelectResult().exec()


class NeedToSelectResult(QDialog):

    def __init__(self):
        super(self.__class__, self).__init__()

        self.setWindowTitle("CardiAP")

        label = QLabel(
            'You need to select at least one image to continue, or if you want to select all the images please use the "Select all and continue" button')
        label.setWordWrap(True)
        button = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(button)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        self.layout.addWidget(label)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
