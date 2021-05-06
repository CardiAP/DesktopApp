from app.controllers.analysis import Controller as AnalysisController
from app.views.new_analysis import View


class Controller:
    def __init__(self, main_window):
        self.__main_window = main_window
        self.__view = View()
        self.__view.finished.connect(
            lambda new_analysis_parametrization: self.__start_analysis(
                new_analysis_parametrization))
        self.__main_window.replace_central_widget(self.__view)

    def __start_analysis(self, new_analysis_parametrization):
        if new_analysis_parametrization.is_valid():
            AnalysisController.controller_for_type(
                self.__main_window, new_analysis_parametrization)
        else:
            self.__view.show_errors(new_analysis_parametrization.errors())
