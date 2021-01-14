from app.views.analysis_parametrization import AnalysisParametrizationForm


class Controller:
    FILES_VALIDATION_ERROR = 'The files parameter must be a list of existing files'

    @classmethod
    def to_parametrize(cls, main_widget, files, back_to):
        if len(files) > 1:
            return MultipleFilesController(main_widget, files, back_to)
        elif len(files) == 1:
            return SigleFileController(main_widget, files, back_to)
        else:
            raise ValueError(
                "The files parameter must be a list of at least one file")

    def __init__(self, main_widget, files, back_to):
        self._validate_files(files)
        self._files = files
        self._back_to = back_to
        self._main_widget = main_widget

    def _build_widget_for(self, file):
        widget = AnalysisParametrizationForm(file)
        widget.go_back.connect(self._back_to)
        return widget

    def _validate_files(self, files):
        assert all(map(lambda file: file.is_file(),
                       files)), self.FILES_VALIDATION_ERROR


class MultipleFilesController(Controller):
    def __init__(self, main_widget, files, back_to):
        super().__init__(main_widget, files, back_to)
        self._parametrizations = []
        self._current_image_index = 0
        self._start_requesting_the_parametrization()

    def _start_requesting_the_parametrization(self):
        self._current_widget = self._build_widget_for(self._files[0])
        self._current_widget.analysis_parametrization_finished.connect(
            lambda parametrization: self._first_image_parametrization_finished(
                parametrization))
        self._main_widget.replace_central_widget(self._current_widget)

    def _first_image_parametrization_finished(self, parametrization):
        errors = parametrization.validate()
        if errors.any():
            self._current_widget.handle_validation_errors(errors)
        else:
            self._current_widget.customization_strategy().apply_to(self, parametrization)

    def use_different_parametrization_for_each(self, parametrization):
        self._current_image_parametrization_finished(parametrization)

    def _current_image_parametrization_finished(self, parametrization):
        self._parametrizations.append(parametrization)
        self._show_next_image_to_parametrize()

    def _show_next_image_to_parametrize(self):
        self._current_image_index += 1
        if self._is_last_image():
            self._request_parametrization_for_last_file()
        else:
            self._request_parametrization_for_current_image()

    def _request_parametrization_for_current_image(self):
        self._request_parametrization_for_file(
            self._files[self._current_image_index],
            lambda parametrization: self._current_image_parametrization_finished(parametrization)
        )

    def _is_last_image(self):
        return len(self._files) - 1 == self._current_image_index

    def use_same_parametrization_for_all(self, parametrization):
        self._parametrizations = self._copy_parametrizaton_for_all_files_from(
            parametrization)
        # TODO aca habria que seguir con la siguiente pantalla

    def _request_parametrization_for_last_file(self):
        self._request_parametrization_for_file(self._files[-1], lambda p: 1)
        # TODO aca habira que seguir con la siguiente pantalla

    def _request_parametrization_for_file(self, file, on_parametrization_success):
        self._current_widget = self._build_widget_for(file)
        self._current_widget.analysis_parametrization_finished.connect(
            lambda parametrization: self._image_parametrization_finished(
                parametrization, on_parametrization_success))
        self._main_widget.replace_central_widget(self._current_widget)

    def _image_parametrization_finished(self, parametrization, on_parametrization_success):
        errors = parametrization.validate()
        if errors.any():
            self._current_widget.handle_validation_errors(errors)
        else:
            on_parametrization_success(parametrization)

    def _copy_parametrizaton_for_all_files_from(self, parametrization):
        return [parametrization.copy_for(file) for file in self._files]


class SigleFileController(Controller):
    def __init__(self, main_widget, files, back_to):
        super().__init__(main_widget, files, back_to)
        self._widget = self._build_widget_for(files[0])
        self._widget.analysis_parametrization_finished.connect(
            lambda parametrization: self._parametrization_finished(
                parametrization))
        self._main_widget.replace_central_widget(self._widget)

    def _parametrization_finished(self, parametrization):
        errors = parametrization.validate()
        if errors.any():
            self._widget.handle_validation_errors(errors)
        else:
            # TODO aca habria que crear el controller que sigue y pasarle la parametrizacion
            pass
