from app.views.analysis_parametrization import AnalysisParametrizationForm


class Controller:
    FILES_VALIDATION_ERROR = 'The files parameter must be a list of existing files'

    @classmethod
    def from_state(cls, flow_controller, back_to, state):
        return cls.to_parametrize(flow_controller, state, back_to)

    @classmethod
    def to_parametrize(cls, flow_controller, parametrizations, back_to):
        if len(parametrizations) > 1:
            return MultipleFilesController(flow_controller, parametrizations,
                                           back_to)
        elif len(parametrizations) == 1:
            return SingleFileController(flow_controller, parametrizations,
                                        back_to)
        else:
            raise ValueError(
                "The files parameter must be a list of at least one file")

    def __init__(self, flow_controller, parametrizations, back_to):
        self._validate_files(parametrizations)
        self._input_parametrizations = parametrizations
        self._back_to = back_to
        self._flow_controller = flow_controller

    def _build_widget_for(self, parametrization):
        widget = AnalysisParametrizationForm(parametrization)
        widget.go_back.connect(self._back_to)
        return widget

    def _validate_files(self, parametrizations):
        # TODO handlear este error
        assert all(
            map(lambda parametrization: parametrization.with_existent_file(),
                parametrizations)), self.FILES_VALIDATION_ERROR

    def get_state(self):
        raise NotImplementedError()

    def show(self):
        raise NotImplementedError()


class MultipleFilesController(Controller):
    def __init__(self, flow_controller, parametrizations, back_to):
        super().__init__(flow_controller, parametrizations, back_to)
        self._parametrizations = []
        self._current_image_index = 0

    def show(self):
        self._start_requesting_the_parametrization()

    def _start_requesting_the_parametrization(self):
        self._current_widget = self._build_widget_for(
            self._input_parametrizations[0])
        self._current_widget.analysis_parametrization_finished.connect(
            lambda parametrization: self._first_image_parametrization_finished(
                parametrization))
        self._flow_controller.show_widget(self._current_widget)

    def _first_image_parametrization_finished(self, parametrization):
        errors = parametrization.validate()
        if errors.any():
            self._current_widget.handle_validation_errors(errors)
        else:
            self._current_widget.customization_strategy().apply_to(self,
                                                                   parametrization)

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
            self._input_parametrizations[self._current_image_index],
            lambda
                parametrization: self._current_image_parametrization_finished(
                parametrization)
        )

    def _is_last_image(self):
        return len(
            self._input_parametrizations) - 1 == self._current_image_index

    def use_same_parametrization_for_all(self, parametrization):
        self._parametrizations = self._copy_parametrization_for_all_files_from(
            parametrization)
        self._flow_controller.analysis_parametrization_finished(
            self._parametrizations)

    def _request_parametrization_for_last_file(self):
        self._request_parametrization_for_file(
            self._input_parametrizations[-1],
            lambda parametrization: self._last_image_parametrization_finished(
                parametrization))

    def _last_image_parametrization_finished(self, parametrization):
        self._parametrizations.append(parametrization)
        self._flow_controller.analysis_parametrization_finished(
            self._parametrizations)

    def _request_parametrization_for_file(self, file,
                                          on_parametrization_success):
        self._current_widget = self._build_widget_for(file)
        self._current_widget.analysis_parametrization_finished.connect(
            lambda parametrization: self._image_parametrization_finished(
                parametrization, on_parametrization_success))
        self._flow_controller.show_widget(self._current_widget)

    def _image_parametrization_finished(self, parametrization,
                                        on_parametrization_success):
        errors = parametrization.validate()
        if errors.any():
            self._current_widget.handle_validation_errors(errors)
        else:
            on_parametrization_success(parametrization)

    def _copy_parametrization_for_all_files_from(self, parametrization):
        return [parametrization.copy_for(input_parametrization.file) for
                input_parametrization in self._input_parametrizations]

    def get_state(self):
        return self._parametrizations


class SingleFileController(Controller):
    def __init__(self, main_widget, parametrizations, back_to):
        super().__init__(main_widget, parametrizations, back_to)
        self._parametrization = None

    def show(self):
        self._widget = self._build_widget_for(self._input_parametrizations[0])
        self._widget.analysis_parametrization_finished.connect(
            lambda parametrization: self._parametrization_finished(
                parametrization))
        self._flow_controller.show_widget(self._widget)

    def _parametrization_finished(self, parametrization):
        errors = parametrization.validate()
        if errors.any():
            self._widget.handle_validation_errors(errors)
        else:
            self._parametrization = parametrization
            self._flow_controller.analysis_parametrization_finished(
                [parametrization])

    def get_state(self):
        return [self._parametrization]
