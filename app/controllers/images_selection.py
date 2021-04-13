from pathlib import Path

from app.views.anaysis_selection_form import AnalysisSelectionForm


class Controller(object):

    def __init__(self, flow_controller):
        self._selected_path = ''
        self._flow_controller = flow_controller

    @classmethod
    def from_state(cls, flow_controller, path):
        instance = cls(flow_controller)
        instance._selected_path = path
        return instance

    def show(self):
        widget = AnalysisSelectionForm(self._selected_path)
        self._flow_controller.show_widget(widget)
        widget.form_submitted.connect(lambda path: self._path_selected(path))

    def _path_selected(self, selected_path):
        # TODO cambiar esta chota cuando cambiemos el input a un file selector y tambien validar algo
        self._selected_path = selected_path
        path = Path(selected_path)
        if path.is_file():
            files = [path]
        else:
            files = list(path.glob('*.tif'))

        self._flow_controller.images_selection_finished(files)

    def get_state(self):
        return self._selected_path
