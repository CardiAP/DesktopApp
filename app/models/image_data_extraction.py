import cv2
import numpy as np

class ImageDataExtraction(object):
    def __init__(self, analysis_parametrization):
        self._slice_width = analysis_parametrization.input_parameters.slice_width
        self._image_data = np.array(self._get_data_from(analysis_parametrization))

    def _get_data_from(self, analysis_parametrization):
        image_data = cv2.imread(str(analysis_parametrization.file))
        image_data = analysis_parametrization.image_customization.apply_to(image_data)
        image_data = analysis_parametrization.image_selection.apply_to(image_data)
        return cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)

    def data(self):
        return np.mean(self._image_data, 1)

    def slices_data(self):
        return np.mean(self._split_vertically(self._image_data, self._slice_width), 2)

    def _split_vertically(self, image_data, slice_width):
        image_width = len(image_data[0])
        if slice_width > image_width:
            raise ValueError(
                "The value of the slice width needs to be smaller than the len of the x axis"
            )

        left_over_width = image_width % slice_width
        amount_of_slices = image_width // slice_width
        width_to_split = image_width - left_over_width

        transposed = np.transpose(image_data)
        todo_menos_el_resto = np.transpose(np.vsplit(transposed[0:width_to_split], amount_of_slices), (0, 2, 1))
        el_resto = transposed[width_to_split:]
        return np.concatenate((todo_menos_el_resto, el_resto))

