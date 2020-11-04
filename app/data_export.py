from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QTabWidget, QHBoxLayout, QPushButton


class DataExport(QWidget):
    finished = pyqtSignal()

    def __init__(self):
        super(DataExport, self).__init__()
        self.setLayout(QVBoxLayout())

        self._content_section = QWidget()
        self.layout().addWidget(self._content_section)
        self._content_section.setLayout(QGridLayout())

        self._results_data = QTabWidget(self)
        self._content_section.layout().addWidget(self._results_data, 0, 0)

        self._actions_section = QWidget(self)
        self.layout().addWidget(self._actions_section)

        self._setup_continue_buttons()

    def _setup_continue_buttons(self):
        self._actions_section.setLayout(QHBoxLayout())
        self.export_button = QPushButton("Export results", parent=self)

        self._actions_section.layout().addWidget(self.export_button)

    def set_results_data(self, view):
        self._content_section.layout().removeWidget(self._results_data)
        self._results_data.deleteLater()
        self._results_data = view
        self._results_data.setParent(self)
        self._content_section.layout().addWidget(self._results_data, 0, 0)
        self._results_data.currentChanged.emit(0)