from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QAction, \
    QMenuBar, QMenu

from dyssynchrony_analysis_form import DyssynchronyAnalysisForm
from welcome_view import WelcomeView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CardiAP')

        self._setup_menu_bar()
        self._setup_layout()
        self.change_current_view_to(WelcomeView())

    def change_current_view_to(self, new_view):
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
        action_dyssynchrony_analysis.setObjectName(u"action_dyssynchrony_analysis")
        menu_analysis_selection.addAction(action_dyssynchrony_analysis)
        action_dyssynchrony_analysis.triggered.connect(lambda _: self.change_current_view_to(
            DyssynchronyAnalysisForm()))
        action_dyssynchrony_analysis.setText(u"Dyssynchrony Analysis")

        self.setMenuBar(menu_bar)
