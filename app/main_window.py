from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QAction, \
    QMenuBar, QMenu

from app.controllers.new_analysis import Controller as NewAnalysis
from app.welcome_view import WelcomeView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CardiAP')

        self._setup_menu_bar()
        self._setup_layout()
        self.replace_central_widget(WelcomeView())

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
        menu_bar.setGeometry(QRect(0, 0, 800, 20))

        menu_analysis_selection = QMenu(menu_bar)
        menu_bar.addAction(menu_analysis_selection.menuAction())
        menu_analysis_selection.setTitle("Analysis")

        new_analysis = QAction(self)
        new_analysis.triggered.connect(lambda: self._new_analysis())
        new_analysis.setText("New")
        menu_analysis_selection.addAction(new_analysis)

        load_analysis = QAction(self)
        load_analysis.triggered.connect(lambda: self._load_analysis())
        load_analysis.setText("Load")
        menu_analysis_selection.addAction(load_analysis)

        save_analysis = QAction(self)
        save_analysis.triggered.connect(lambda: self._save_analysis())
        save_analysis.setText("Save")
        save_analysis.setDisabled(True)
        menu_analysis_selection.addAction(save_analysis)

        self.setMenuBar(menu_bar)

    def _new_analysis(self):
        NewAnalysis(self)

    def _load_analysis(self):
        pass

    def _save_analysis(self):
        pass
