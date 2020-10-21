class AnalysisResultOverviewController:
    def __init__(self, image_id, image_name, analysis_results, view):
        self._image_id = image_id
        self._image_name = image_name
        self._analysis_results = analysis_results
        self._view = view
        self._view.result_selected.connect(lambda: self._analysis_results.select_result(self._image_id))
        self._already_opened = False

    def opened(self):
        if not self._already_opened:
            self._view.set_analysis_results(self._analysis_results.result_for_id(self._image_id))
        self._already_opened = True
