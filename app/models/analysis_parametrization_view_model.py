from app.models.image_customization import ImageCustomization
from app.models.image_selection import ImageSelection
from app.models.input_parameters import InputParameters


class AnalysisParametrizationErrors(object):
    def __init__(self, image_selection_errors, input_parameters_errors,
                 image_customization_errors):
        self._image_customization_errors = image_customization_errors
        self._input_parameters_errors = input_parameters_errors
        self._image_selection_errors = image_selection_errors

    def any(self):
        return self._image_selection_errors.any() or \
               self._input_parameters_errors.any() or \
               self._image_customization_errors.any()

    def for_image_customization_form(self):
        return self._image_customization_errors

    def for_analysis_input_form(self):
        return self._input_parameters_errors

    def for_image_preview(self):
        return self._image_selection_errors


class TransitoryAnalysisConnector(object):
    def __init__(self, view, parametrization):
        self.view = view
        self.parametrization = parametrization

    