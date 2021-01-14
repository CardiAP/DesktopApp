from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QAction, \
    QMenuBar, QMenu

from app.controllers.basic_analysis import Controller as BasicAnalysis
from app.models.dyssynchrony_analysis_results import \
    DyssynchronyAnalysisResults
from app.welcome_view import WelcomeView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CardiAP')

        self._setup_menu_bar()
        self._setup_layout()
        self.replace_central_widget(WelcomeView())
        self._dyssynchrony_analysis_result = DyssynchronyAnalysisResults()

    def replace_central_widget(self, widget):
        old_view = self._current_view
        self._mainLayout.replaceWidget(old_view, widget)
        self._current_view.close()
        self._current_view = widget

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
        menu_bar.addAction(menu_analysis_selection.menuAction())
        menu_analysis_selection.setTitle("Analysis Selection")

        action_basic_analysis = QAction(self)
        menu_analysis_selection.addAction(action_basic_analysis)

        action_basic_analysis.triggered.connect(
            lambda _: self._start_basic_analysis())
        action_basic_analysis.setText(u"Basic Analysis")

        self.setMenuBar(menu_bar)

    def _start_basic_analysis(self):
        BasicAnalysis(self)