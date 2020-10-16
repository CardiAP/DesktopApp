from lib.image.image_data import apply_settings_to_image
from lib.analysis.dyssynchrony_analysis import analyze_image


class DyssynchronyAnalysisCalculation:
    def __init__(self, dyssynchrony_configuration):
        self._results = []
        self._dyssynchrony_configuration = dyssynchrony_configuration

    def execute_for_all(self):
        [
            image_settings for image_setting in self._images_settings()
            if not any(image_settings['file'] == result['file']
                       for result in results)
        ]
        self._results = [
            self._analyze_image(image_settings) for image_settings in
            self._dyssynchrony_configuration.images_settings
        ]
        return self

    def analyze_image(self, settings):
        image_customization_settings = settings['image_settings']
        analysis_settigns = settings['analysis_settigns']
        return analyze_image(
            apply_settings_to_image(settings['file'],
                                    image_customization_settings),
            analysis_settigns["min_dist_between_maxs"],
            analysis_settigns["calibration"], analysis_settigns["slice_width"])

    def get_image_names(self):
        return [
            image_settings['file'].split('/')[-1]
            for image_settings in self._images_settings
        ]
