from app.controllers.analysis_parametrization import \
    Controller as AnalysisParametrizationController
from app.controllers.images_selection import \
    Controller as ImagesSelectionController
from app.models.analysis_parametrization import AnalysisParametrization
from app.controllers.images_refinement import Controller as ImagesRefinementController

class PreviousStep:
    def __init__(self, controller):
        self._state = controller.get_state()
        self._step_class = controller.__class__

    def regenerate_step(self, flow_controller):
        return self._step_class.from_state(flow_controller, self._state)


class Controller:
    def __init__(self, main_window):
        self._main_window = main_window
        self._selected_files = []
        self._parametrizations = []
        self._previous_steps = []
        self._show_images_selection_step()

    def show_widget(self, widget):
        self._main_window.replace_central_widget(widget)

    def _change_current_step_to(self, controller):
        self._current_controller = controller
        self._current_controller.show()

    def _to_previous_step(self):
        previous_step = self._previous_steps.pop()
        self._change_current_step_to(previous_step.regenerate_step(self))

    def _show_images_selection_step(self):
        self._change_current_step_to(ImagesSelectionController(self))

    def images_selection_finished(self, files):
        self._selected_files = files
        self.save_step()
        self._show_analysis_parametrization_step()

    def save_step(self):
        previous_step = PreviousStep(self._current_controller)
        self._previous_steps.append(previous_step)

    def _show_analysis_parametrization_step(self):
        #TODO mover la cracion de las parametrizaciones default al controller
        controller = AnalysisParametrizationController.to_parametrize(
            self,
            self._default_parametrizations(),
            lambda: self._to_previous_step()
        )
        self._change_current_step_to(controller)

    def _default_parametrizations(self):
        return [AnalysisParametrization.default(file) for file in self._selected_files]

    def analysis_parametrization_finished(self, parametrizations):
        self._parametrizations = parametrizations
        self.save_step()
        self._show_image_refinement_step()

    def _show_image_refinement_step(self):
        controller = ImagesRefinementController.for_parametrizations(self, self._parametrizations, lambda: self._to_previous_step())
        self._change_current_step_to(controller)

    def images_refinement_finished(self, images_refinement):
        self._images_refinement = images_refinement
        self.save_step()
        #TODO SEGUIR CON LA SIGUIENTE PANTALLA