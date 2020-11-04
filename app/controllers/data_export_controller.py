from PyQt5.QtWidgets import QTabWidget

from app.result_data_visualization import ResultDataVisualization


class DataExportController(object):
    def __init__(self, results, view):
        self._view = view
        self._results = results

        tabs_widget = QTabWidget()

        for result_id, result_name in self._results.selected_results_ids_and_names():
            view = ResultDataVisualization(tabs_widget)
            view.set_data(
                self._results.image_data_points_data_for_selected_result(result_id, with_humanized_data_points=True),
                self._results.slices_data_points_data_for_selected_result(result_id, with_humanized_data_points=True),
            )
            tabs_widget.addTab(view, result_name)

        self._view.set_results_data(tabs_widget)

        self._view.export_button.clicked.connect(lambda: self._show_export_settings())

    def _show_export_settings(self):
        print("clickea-:ditto:")