from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QPushButton

from app.analysis_result_overview import AnalysisResultOverview
from app.controllers.analysis_results_overview_controller import AnalysisResultOverviewController
from app.selected_results import SelectedResults
from app.controllers.selected_results_controller import SelectedResultsController


class DyssynchronyAnalysisResultsRefinement(QWidget):
    def __init__(self, analysis_results):
        super(DyssynchronyAnalysisResultsRefinement, self).__init__()
        self._analysis_results = analysis_results
        self.setLayout(QVBoxLayout())

        self._content_section = QWidget()
        self.layout().addWidget(self._content_section)
        self._content_section.setLayout(QHBoxLayout())

        self._analysis_results_overview = QWidget(self)
        self._content_section.layout().addWidget(self._analysis_results_overview)
        self._selected_results = QWidget(self)
        self._content_section.layout().addWidget(self._selected_results)

        self._actions_section = QWidget(self)
        self.layout().addWidget(self._actions_section)

        self._setup_analysis_overview_section()
        self._setup_selected_results_section()
        self._setup_continue_buttons()

    def _setup_continue_buttons(self):
        self._actions_section.setLayout(QHBoxLayout())
        self._select_all_and_continue_button = QPushButton("Select all and continue", parent=self)
        self._continue_button = QPushButton("Continue with selected results", parent=self)

        self._actions_section.layout().addWidget(self._select_all_and_continue_button)
        self._actions_section.layout().addWidget(self._continue_button)

    def _setup_selected_results_section(self):
        layout = QVBoxLayout()
        self._selected_results.setLayout(layout)
        view = SelectedResults(self._selected_results)
        SelectedResultsController(self._analysis_results, view)
        layout.addWidget(view)

    def _setup_analysis_overview_section(self):
        layout = QVBoxLayout()
        self._analysis_results_overview.setLayout(layout)
        tabs_widget = QTabWidget(self._analysis_results_overview)
        layout.addWidget(tabs_widget)

        for result_id, result_name in self._analysis_results.results_ids_and_names():
            view = AnalysisResultOverview(self)
            controller = AnalysisResultOverviewController(result_id, result_name, self._analysis_results, view)
            index = tabs_widget.addTab(view, result_name)

            tabs_widget.currentChanged.connect(self._connect_overview_controller(index, controller))

        tabs_widget.currentChanged.emit(0)

    def _connect_overview_controller(self, target_index, controller):
        return lambda index: controller.opened() if index == target_index else None
