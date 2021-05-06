from PySide6.QtWidgets import QTabWidget

from app.analysis_result_overview import AnalysisResultOverview
from app.controllers.analysis_results_overview_controller import AnalysisResultOverviewController
from app.controllers.selected_results_controller import SelectedResultsController
from app.selected_results import SelectedResults


class AnalysisResultsRefinementController(object):
    def __init__(self, results, view):
        self._results = results
        self._view = view

        selected_results = SelectedResults()
        SelectedResultsController(self._results, view, selected_results)

        self._view.set_selected_results_section(selected_results)

        tabs_widget = QTabWidget()

        for result_id, result_name in self._results.results_ids_and_names():
            view = AnalysisResultOverview(tabs_widget)
            controller = AnalysisResultOverviewController(result_id, result_name, self._results, view)
            index = tabs_widget.addTab(view, result_name)

            tabs_widget.currentChanged.connect(self._connect_overview_controller(index, controller))

        self._view.set_analysis_overview_section(tabs_widget)

        self._view.select_all_and_continue_button.clicked.connect(lambda: self._select_all_and_continue_clicked())
        self._view.continue_button.clicked.connect(lambda: self._continue_with_selected_clicked())

    def _select_all_and_continue_clicked(self):
        self._results.select_all_results()
        self._view.finished.emit()

    def _continue_with_selected_clicked(self):
        if self._results.any_selected_result():
            self._view.finished.emit()
        else:
            self._view.show_no_selected_result()

    def _connect_overview_controller(self, target_index, controller):
        return lambda index: controller.opened() if index == target_index else None