import os

from PyQt5.QtWidgets import QTabWidget

from app.models.data_exporter import DataExporter
from app.result_data_visualization import ResultDataVisualization


class DataExportController(object):
    JSON_FORMAT = 'json'
    CSV_FORMAT = 'csv'
    XLSX_FORMAT = 'xlsx'

    VALID_FORMATS = [JSON_FORMAT, CSV_FORMAT, XLSX_FORMAT]

    def __init__(self, results, view):
        self._view = view
        self._results = results
        self._directory = ''
        self._selected_formats = {
            self.CSV_FORMAT: False,
            self.JSON_FORMAT: False,
            self.XLSX_FORMAT: False
        }

        tabs_widget = QTabWidget()

        for result_id, result_name in self._results.selected_results_ids_and_names():
            view = ResultDataVisualization(tabs_widget)
            view.set_data(
                self._results.image_data_points_data_for_selected_result(
                    result_id, with_humanized_data_points=True),
                self._results.slices_data_points_data_for_selected_result(
                    result_id, with_humanized_data_points=True),
            )
            tabs_widget.addTab(view, result_name)

        self._view.set_results_data(tabs_widget)

        self._view.export_button.clicked.connect(
            lambda: self._show_export_settings())
        self._view.export_format_selected.connect(
            lambda selected_format: self._export_format_clicked(
                selected_format))
        self._view.directory_changed.connect(
            lambda directory: self._set_directory(directory))
        self._view.finish_with_settings.connect(
                lambda: self._save_results_if_possible())

    def _export_format_clicked(self, selected_format):
        if selected_format not in self.VALID_FORMATS:
            raise ValueError(f"Invalid format {selected_format}")
        self._selected_formats[selected_format] = not self._selected_formats[
            selected_format]

    def _set_directory(self, directory):
        self._directory = directory

    def _save_results_if_possible(self):
        valid_directory = os.path.isdir(self._directory)
        valid_formats = len(
            [output_format for output_format in self._selected_formats if
             self._selected_formats[output_format]]) > 0
        if not valid_formats:
            self._view.need_to_complete_export_format()
            return
        if not valid_directory:
            self._view.need_to_complete_directory()
            return

        self._export_selected_formats()

    def _export_selected_formats(self):
        exporter = DataExporter(self._results, self._directory)
        for format in self._selected_formats:
            if format is self.JSON_FORMAT:
                exporter.save_json()
            if format is self.CSV_FORMAT:
                exporter.save_csv()

            exporter.save_settings(self._results.settings())

    def _show_export_settings(self):
        self._view.complete_export_settings()
