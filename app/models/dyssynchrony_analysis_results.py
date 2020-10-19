from lib.analysis.dyssynchrony_analysis import analyze_image
from lib.image.image_data import apply_settings_to_image


class DyssynchronyAnalysisResults(object):
    def __init__(self):
        super(DyssynchronyAnalysisResults, self).__init__()
        self._results = {}
        self._settings = None
        self._selected_results = {}
        self._observers = []

    def for_configuration(self, analysis_configuration):
        self._results = {}
        self._settings = analysis_configuration.images_settings()

    def results_ids_and_names(self):
        return [(index, settings['file'].split('/')[-1]) for index, settings in enumerate(self._settings)]

    def selected_results_ids_and_names(self):
        return [(result_id, self._settings[result_id]['file'].split('/')[-1]) for result_id in self._selected_results]

    def result_for_id(self, result_id):
        if not (0 <= result_id < len(self._settings)):
            raise Exception("Id not found")
        elif result_id in self._results:
            return self._results[result_id]
        else:
            result = self._analyze_image(self._settings[result_id])
            self._results[result_id] = result
            return result

    def _analyze_image(self, settings):
        image_customization_settings = settings['image_settings']
        analysis_settigns = settings['analysis_settigns']
        return analyze_image(apply_settings_to_image(settings['file'], image_customization_settings),
                             analysis_settigns["min_dist_between_maxs"], analysis_settigns["calibration"],
                             analysis_settigns["slice_width"])

    def precalculate_all_results(self):
        for index, settings in enumerate(self._settings):
            if index not in self._results:
                self.result_for_id(index)

    def select_result(self, image_id):
        if image_id in self._results:
            self._selected_results[image_id] = self._results[image_id]
            self._notify_change()
        else:
            raise Exception("Id not found in results")

    def remove_result(self, image_id):
        if image_id in self._selected_results:
            del (self._selected_results[image_id])
            self._notify_change()

    def _notify_change(self):
        for observer in self._observers:
            observer.results_changed_in_observable()

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        try:
            self._observers.remove(observer)
        except:
            pass