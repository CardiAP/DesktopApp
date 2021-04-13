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


class AnalysisParametrization(object):
    @classmethod
    def default(cls, file):
        return cls(file, ImageCustomization.default(),
                   InputParameters.default(), ImageSelection.default())

    def __init__(self, file, image_customization, input_parameters,
                 image_selection):
        self.file = file
        self.image_selection = image_selection
        self.input_parameters = input_parameters
        self.image_customization = image_customization

    def with_existent_file(self):
        return self.file.exists()

    def validate(self):
        return AnalysisParametrizationErrors(self.image_selection.validate(),
                                             self.input_parameters.validate(),
                                             self.image_customization.validate())

    def copy_for(self, file):
        return self.__class__(file, self.image_customization.copy(),
                              self.input_parameters.copy(),
                              self.image_customization.copy())

    def file_name(self):
        return self.file.name


class ParametersCustomizationStrategy(object):
    SINGLE_IMAGE_CUSTOMIZATION_STRATEGY = 1
    MULTIPLE_IMAGE_CUSTOMIZATION_STRATEGY = 0

    def __init__(self, strategy_id):
        self._strategy_id = strategy_id

    def apply_to(self, analysis, parametrization):
        if self.use_same_parametrization_for_all():
            analysis.use_same_parametrization_for_all(parametrization)
        elif self.use_different_parametrization_for_each():
            analysis.use_different_parametrization_for_each(parametrization)

    def use_same_parametrization_for_all(self):
        return self.SINGLE_IMAGE_CUSTOMIZATION_STRATEGY == self._strategy_id

    def use_different_parametrization_for_each(self):
        return self.MULTIPLE_IMAGE_CUSTOMIZATION_STRATEGY == self._strategy_id
