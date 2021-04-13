from app.models.images_refinement import ImagesRefinement
from app.views.images_refinement import ImageData, Tabs, SelectedImages, \
    ImagesRefinement as ImagesRefinementView, ImageSection


class Controller:
    @classmethod
    def for_parametrizations(cls, flow_controller, parametrizations, back_to):
        return cls(flow_controller, ImagesRefinement(parametrizations), back_to)

    @classmethod
    def from_state(cls, flow_controller, back_to, images_refinement):
        return cls(flow_controller, images_refinement, back_to)

    def __init__(self, flow_controller, image_refinement, back_to):
        self._back_to = back_to
        self._images_refinement = image_refinement
        self._flow_controller = flow_controller
        self._tabs = None
        self._image_data_widget = None
        self._selected_images_widget = None
        self._image_section = None

    def get_state(self):
        return self._images_refinement

    def show(self):
        self._tabs = Tabs(self._images_refinement.file_names())
        self._tabs.tab_changed_to.connect(
            lambda image_name: self._show_image(image_name))

        self._image_data_widget = ImageData()

        self._image_section = ImageSection(self._tabs, self._image_data_widget)
        self._image_section.current_image_selected.connect(
            lambda: self._current_image_selected())

        self._selected_images_widget = SelectedImages()
        self._selected_images_widget.image_removed.connect(
            lambda image_name: self._image_removed_from_selected(image_name))

        images_refinement = ImagesRefinementView(self._image_section,
                                             self._selected_images_widget,
                                             lambda: self._images_refinement.any_selected_file())
        images_refinement.select_all_and_continue.connect(
            lambda: self._select_all_images_and_continue())
        images_refinement.continue_with_selected.connect(
            lambda: self._continue_with_selected_images())
        self._tabs.show()
        self._tabs.show_first_tab()
        self._flow_controller.show_widget(images_refinement)

    def _show_image(self, image_name):
        image = self._images_refinement.get_image(image_name)
        self._image_data_widget.show_image(image.data, image.slices_data)

    def _current_image_selected(self):
        image_name = self._tabs.current_tab_name()
        self._images_refinement.select_image(image_name)
        self._selected_images_widget.set_selected_images(
            self._images_refinement.selected_image_names())

    def _image_removed_from_selected(self, image_name):
        self._images_refinement.image_unselected(image_name)
        self._selected_images_widget.set_selected_images(
            self._images_refinement.selected_image_names())

    def _select_all_images_and_continue(self):
        self._images_refinement.select_all_images()
        self._flow_controller.images_refinement_finished(self._images_refinement)

    def _continue_with_selected_images(self):
        self._flow_controller.images_refinement_finished(self._images_refinement)
