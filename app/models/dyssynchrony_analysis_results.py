from lib.analysis.dyssynchrony_analysis import analyze_image
from lib.image.image_data import apply_settings_to_image


class DyssynchronyAnalysisResults(object):
    VALID_DATA_POINTS = {
        'max_peaks_positions': 'Max peaks positions',
        'max_peaks_intensities': 'Max peaks intensities',
        'min_peaks_positions': 'Min peaks positions',
        'min_peaks_intensities': 'Min peaks intensities',
        'amplitudes': 'Amplitudes',
        'times_to_peaks': 'Time to peak',
        'times_to_half_peaks': 'Time to half peak',
        'tau_s': 'Tau'
    }

    def __init__(self):
        super(DyssynchronyAnalysisResults, self).__init__()
        self._results = {}
        self._settings = None
        self._selected_results = {}
        self._selected_image_data_points = []
        self._selected_slices_data_points = []
        self._observers = []

    def image_data_points(self):
        return self._selected_image_data_points

    def image_data_points_data_for_selected_result(self, selected_result_id, with_humanized_data_points=False):
        self._check_existent_selected_result_id(selected_result_id)
        image_data_result = self._selected_results[selected_result_id]['image']
        results_for_data_points = {}
        for data_point in self._selected_image_data_points:
            if with_humanized_data_points:
                results_for_data_points[self.VALID_DATA_POINTS[data_point]] = image_data_result[data_point]
            else:
                results_for_data_points[data_point] = image_data_result[data_point]
        return results_for_data_points

    def slices_data_points_data_for_selected_result(self, selected_result_id, with_humanized_data_points=False):
        self._check_existent_selected_result_id(selected_result_id)
        slices = self._selected_results[selected_result_id]['slices']
        slices_results_for_data_points = []
        for slice in slices:
            results_for_data_points = {}
            for data_point in self._selected_slices_data_points:
                if with_humanized_data_points:
                    results_for_data_points[self.VALID_DATA_POINTS[data_point]] = slice[data_point]
                else:
                    results_for_data_points[data_point] = slice[data_point]
            slices_results_for_data_points.append(results_for_data_points)
        return slices_results_for_data_points

    def slices_data_points(self):
        return self._selected_slices_data_points

    def set_selected_image_data_points(self, selected_data_points):
        self._check_valid_data_points(selected_data_points)
        self._selected_image_data_points = selected_data_points

    def set_selected_slices_data_points(self, selected_data_points):
        self._check_valid_data_points(selected_data_points)
        self._selected_slices_data_points = selected_data_points

    def for_configuration(self, analysis_configuration):
        self._settings = analysis_configuration.images_settings()

    def results_ids_and_names(self):
        return [(index, settings['file'].split('/')[-1]) for index, settings in enumerate(self._settings)]

    def selected_results_ids_and_names(self):
        return [(result_id, self._settings[result_id]['file'].split('/')[-1]) for result_id in self._selected_results]

    def any_selected_result(self):
        return len(self._selected_results) > 0

    def select_all_results(self):
        self.precalculate_all_results()
        self._selected_results = self._results.copy()

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
        except ValueError:
            pass

    def _check_valid_data_points(self, data_points):
        for data_point in data_points:
            self._check_valid_data_point(data_point)

    def _check_valid_data_point(self, data_point):
        if data_point not in self.VALID_DATA_POINTS:
            raise ValueError(f"Invalid data point {data_point}")

    def data_point_human_name(self, data_point):
        self._check_valid_data_points(data_point)
        return self.VALID_DATA_POINTS[data_point]

    def _check_existent_selected_result_id(self, selected_result_id):
        if selected_result_id not in self._selected_results:
            raise ValueError(f"Id {selected_result_id} not found in selected results")
