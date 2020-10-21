from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from app.selected_result_item import SelectedResultItem


class SelectedResults(QWidget):
    result_removed = pyqtSignal(int)

    def __init__(self):
        super(SelectedResults, self).__init__()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel("Selected images for result"), Qt.AlignTop)
        self._selected_results_container = QWidget(parent=self)
        self.layout().addWidget(self._selected_results_container, Qt.AlignTop)

        self._selected_results_container.setLayout(QVBoxLayout())
        self._selected_results = []

    def set_selected_results(self, selected_results):
        for selected_result in self._selected_results:
            selected_result.deleteLater()

        self._selected_results = []

        for selected_result in selected_results:
            selected_result_item = SelectedResultItem(self._selected_results_container, selected_result)
            selected_result_item.remove_clicked.connect(lambda result_id: self.result_removed.emit(result_id))
            self._selected_results_container.layout().addWidget(selected_result_item, Qt.AlignTop)
            self._selected_results.append(selected_result_item)