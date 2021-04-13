from app.models.image_data_extraction import ImageDataExtraction


class ImagesRefinement(object):
    def __init__(self, parametrizations):
        self._parametrizations_per_file = {}
        for parametrization in parametrizations:
            self._parametrizations_per_file[parametrization.file_name()] = parametrization
        self._selected_files = []

    def file_names(self):
        return list(self._parametrizations_per_file.keys())

    def any_selected_file(self):
        return len(self._selected_files) > 0

    def get_image(self, image_name):
        return ImageDataExtraction(self._parametrizations_per_file[image_name])

    def select_all_images(self):
        for file_name in self._parametrizations_per_file.keys():
            self._selected_files.append(file_name)
