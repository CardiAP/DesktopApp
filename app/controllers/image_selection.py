from pathlib import Path

from app.controllers.analysis_parametrization import \
    Controller as AnalysisParametrizationController
from app.views.images_selection_form import ImagesSelectionForm


class Controller(object):
    def __init__(self, main_widget):
        self._widget = ImagesSelectionForm()
        self._main_widget = main_widget
        self._main_widget.replace_central_widget(self._widget)
        self._widget.form_submitted.connect(lambda files: self._open_configuration_widget(files))

    def _open_configuration_widget(self, files):
        # TODO cambiar esta chota cuando cambiemos el input a un file selector
        if isinstance(files, str):
            path = Path(files)
            if path.is_file():
                files = [path]
            else:
                files = list(path.glob('*.tif'))

        AnalysisParametrizationController.to_parametrize(self._main_widget, files, lambda: self.__class__(self._main_widget))