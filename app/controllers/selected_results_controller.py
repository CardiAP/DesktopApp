class SelectedResultsController(object):
    def __init__(self, results, parent_view, view):
        self._results = results
        self._view = view
        self._view.setParent(parent_view)
        self._results.add_observer(self)
        self._view.result_removed.connect(self.result_removed)
        self._view.set_selected_results(self._results.selected_results_ids_and_names())
        parent_view.finished.connect(lambda: self._results.remove_observer(self))

    def result_removed(self, result_id):
        self._results.remove_result(result_id)

    def results_changed_in_observable(self):
        self._view.set_selected_results(self._results.selected_results_ids_and_names())