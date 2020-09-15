import os


class DyssynchronyConfiguration:
    NO_CUSTOMIZATION_STRATEGY = -1
    SINGLE_IMAGE_CUSTOMIZATION_STRATEGY = 1
    MULTIPLE_IMAGE_CUSTOMIZATION_STRATEGY = 0

    def __init__(self):
        self._path = None
        self._images_paths = None
        self._is_single_file = None
        self._current_image_index = None
        self._image_customization_strategy = -1
        self._images_settings = []

    def set_image_path(self, path):
        self._path = path
        self._is_single_file = os.path.isfile(self._path)
        self._current_image_index = -1
        if self._is_single_file:
            self._images_paths = [self._path]
            self._image_customization_strategy = self.MULTIPLE_IMAGE_CUSTOMIZATION_STRATEGY
        else:
            self._images_paths = [f'{path}/{file}' for file in os.listdir(path) if file.endswith(".tif")]

    def need_to_select_customization_strategy(self):
        return self._image_customization_strategy is self.NO_CUSTOMIZATION_STRATEGY

    def set_image_customization_strategy(self, strategy):
        self._image_customization_strategy = strategy

    def next_image_path(self):
        if self.are_there_more_images():
            self._current_image_index += 1
            current_image_path = self._images_paths[self._current_image_index]
            return current_image_path
        else:
            raise Exception("No images left")

    def are_there_more_images(self):
        has_not_read_first_image = self._current_image_index < 0
        has_not_read_all_images = (self._current_image_index < len(self._images_paths) - 1)
        return (self._is_single_image_strategy() and has_not_read_first_image) or \
               (self.need_to_select_customization_strategy() and has_not_read_first_image) or \
               (self._is_multiple_image_strategy() and has_not_read_all_images)

    def _is_multiple_image_strategy(self):
        return (self._image_customization_strategy == self.MULTIPLE_IMAGE_CUSTOMIZATION_STRATEGY)

    def _is_single_image_strategy(self):
        return self._image_customization_strategy == self.SINGLE_IMAGE_CUSTOMIZATION_STRATEGY

    def _current_image_path(self):
        return self._images_paths[self._current_image_index]

    def current_image_name(self):
        path_list = self._current_image_path().split("/")
        path_list.reverse()
        return path_list[0]

    def settings_for_current_image(self, settings):
        if self._is_single_image_strategy():
            self._images_settings = [{"file": file_path, "settings": settings} for file_path in self._images_paths]

        if self._is_multiple_image_strategy():
            self._images_settings.append({"file": self._images_paths[self._current_image_index], "settings": settings})
