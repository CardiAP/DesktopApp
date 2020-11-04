from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QAction, \
    QMenuBar, QMenu

from app.analysis_results_refinement import AnalysisResultsRefinement
from app.controllers.analysis_results_refinment_controller import AnalysisResultsRefinementController
from app.controllers.data_export_controller import DataExportController
from app.controllers.data_points_selection_controller import DataPointsSelectionController
from app.data_export import DataExport
from app.data_points_selection import DataPointsSelection
from app.image_settings import ImageSettings
from app.images_selection_form import ImagesSelectionForm
from app.models.dyssynchrony_analysis_results import DyssynchronyAnalysisResults
from app.models.dyssynchrony_configuration import DyssynchronyConfiguration
from app.welcome_view import WelcomeView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CardiAP')

        self._setup_menu_bar()
        self._setup_layout()
        self._change_current_view_to(WelcomeView())
        self._dyssynchrony_configuration = DyssynchronyConfiguration()
        self._dyssynchrony_analysis_results = DyssynchronyAnalysisResults()

    def _change_current_view_to(self, new_view):
        old_view = self._current_view
        self._mainLayout.replaceWidget(old_view, new_view)
        self._current_view.close()
        self._current_view = new_view

    def _setup_layout(self):
        self._mainWidget = QWidget()
        self._mainLayout = QVBoxLayout()
        self._mainWidget.setLayout(self._mainLayout)
        self._current_view = QWidget()
        self._mainLayout.addWidget(self._current_view)
        self.setCentralWidget(self._mainWidget)

    def _setup_menu_bar(self):
        menu_bar = QMenuBar(self)
        menu_bar.setObjectName(u"menuBar")
        menu_bar.setGeometry(QRect(0, 0, 800, 20))

        menu_analysis_selection = QMenu(menu_bar)
        menu_analysis_selection.setObjectName(u"menu_analysis_selection")
        menu_bar.addAction(menu_analysis_selection.menuAction())
        menu_analysis_selection.setTitle("Analysis Selection")

        action_dyssynchrony_analysis = QAction(self)
        action_dyssynchrony_analysis.setObjectName(
            u"action_dyssynchrony_analysis")
        menu_analysis_selection.addAction(action_dyssynchrony_analysis)

        action_dyssynchrony_analysis.triggered.connect(
            lambda _: self._go_to_image_selection())
        action_dyssynchrony_analysis.setText(u"Dyssynchrony Analysis")

        self.setMenuBar(menu_bar)

    def _go_to_image_selection(self):
        self._dyssynchrony_configuration.reset()
        image_selection = ImagesSelectionForm(self._dyssynchrony_configuration)
        image_selection.finished.connect(self._go_to_image_settings)
        self._change_current_view_to(image_selection)

    def _go_to_image_settings(self):
        image_settings = ImageSettings(self._dyssynchrony_configuration)
        image_settings.finished.connect(self._go_to_dyssynchrony_analysis_results)
        self._change_current_view_to(image_settings)

    def _go_to_dyssynchrony_analysis_results(self):
        self._dyssynchrony_analysis_results.for_configuration(self._dyssynchrony_configuration)
        results_refinement = AnalysisResultsRefinement()
        AnalysisResultsRefinementController(self._dyssynchrony_analysis_results, results_refinement)
        results_refinement.finished.connect(self._go_to_data_selection)
        self._change_current_view_to(results_refinement)

    def _go_to_data_selection(self):
        data_selection = DataPointsSelection()
        DataPointsSelectionController(self._dyssynchrony_analysis_results, data_selection)
        data_selection.finished.connect(self._go_to_data_export)
        self._change_current_view_to(data_selection)

    def _go_to_data_export(self):
        data_export = DataExport()
        DataExportController(self._dyssynchrony_analysis_results, data_export)
        self._change_current_view_to(data_export)
