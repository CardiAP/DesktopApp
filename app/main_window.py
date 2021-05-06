from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, \
    QMenuBar, QMenu, QScrollArea

from app.controllers.new_analysis import Controller as NewAnalysis
from app.welcome_view import WelcomeView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CardiAP')

        self.__setup_menu_bar()

        self.__scroll = QScrollArea()
        self.__scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.__scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.__scroll.setWidgetResizable(True)
        self.setCentralWidget(self.__scroll)

        self.__setup_layout()
        self.replace_central_widget(WelcomeView())

    def replace_central_widget(self, widget):
        old_view = self.__current_view
        self._mainLayout.replaceWidget(old_view, widget)
        self.__current_view.close()
        self.__current_view = widget

    def __setup_layout(self):
        self._mainWidget = QWidget()
        self._mainLayout = QVBoxLayout()
        self._mainWidget.setLayout(self._mainLayout)
        self.__current_view = QWidget()
        self._mainLayout.addWidget(self.__current_view)
        self.__scroll.setWidget(self._mainWidget)

    def __setup_menu_bar(self):
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
