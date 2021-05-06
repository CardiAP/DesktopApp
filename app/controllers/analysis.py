from app.models.analysis_files import AnalysisFiles
from app.models.analysis_parametrization import AnalysisParametrization
from app.models.new_analysis_parametrization import NewAnalysisParametrization
from app.views.analysis import AnalysisView
from app.views.files_navigation import FilesNavigation
from app.views.image_analysis import TransitoryImageAnalysis


class Controller:
    @classmethod
    def controller_for_type(cls, main_window, new_analysis_parametrization):
        analysis_type = new_analysis_parametrization.analysis_type()
        files = AnalysisFiles.for_file_paths(
            new_analysis_parametrization.selected_files())

        controller = next(
            filter(
                lambda subclass: subclass.can_handle(analysis_type),
                cls.__subclasses__()),
            None
        )

        return controller(main_window, files)

    @classmethod
    def can_handle(cls, analysis_type):
        raise NotImplemented()

    def __init__(self, main_window, selected_files):
        self.__files_to_analyze = selected_files
        self.__current_file = None

        self.__main_window = main_window
        self.__files_navigation = FilesNavigation(self.__files_to_analyze)

        self.__image_analysis = self.build_image_analysis_widget()
        self.__image_analysis.accepted.connect(
            lambda: self.__current_file_accepted())
        self.__image_analysis.discard.connect(
            lambda: self.__current_image_discarded())
        self.__image_analysis.graphics_request(
            lambda: self.__show_graphics_for_current_image())
        self.__image_analysis.data_tables_request(
            lambda: self.__show_data_tables_for_current_image())

        self.__files_navigation.file_clicked.connect(
            lambda file: self.__send_file_to_analyze(file))

        main_window.replace_central_widget(
            AnalysisView(self.__image_analysis, self.__files_navigation))

    def build_image_analysis_widget(self):
        raise NotImplemented()

    def __send_file_to_analyze(self, file):
        self.__current_file.unselect()
        self.__current_file = file
        self.__current_file.select()
        self.__files_navigation.repaint()
        self.__image_analysis.set_for_analysis(file)

    def __current_file_accepted(self):
        parametrization = self.__image_analysis.get_parametrization()
        self.__current_file.parametrization = parametrization
        validation_errors = parametrization.validate()
        if validation_errors.any():
            self.__show_validation_errors(validation_errors)
        else:
            self.__current_file.accepted()
            self.__files_navigation.repaint()

    def __show_validation_errors(self, validation_errors):
        self.__image_analysis.show_validation_errors(validation_errors)


class TransitoryController(Controller):
    @classmethod
    def can_handle(cls, analysis_type):
        return analysis_type is NewAnalysisParametrization.TRANSITORY

    def __init__(self, main_window, selected_files):
        super().__init__(main_window, selected_files)

    def build_image_analysis_widget(self):
        return TransitoryImageAnalysis()


class WavesController(Controller):
    @classmethod
    def can_handle(cls, analysis_type):
        return analysis_type is NewAnalysisParametrization.WAVES

    def __init__(self, main_window, selected_files):
        super().__init__(main_window, selected_files)


class SparksController(Controller):
    @classmethod
    def can_handle(cls, analysis_type):
        return analysis_type is NewAnalysisParametrization.SPARKS

    def __init__(self, main_window, selected_files):
        super().__init__(main_window, selected_files)
