import numpy as np

from dapp.peaks_detector import PeaksDetector


class ImageRawData:
    def __init__(self, image_matrix):
        self.image_matrix = image_matrix

    def split_vertically_by(self, width):
        # TODO: Validar que la cantiad de columnas es divisible por el with
        return CompoundedImageRawData([ImageRawData(column) for column in np.hsplit(self.image_matrix, width)])

    def sum_columns(self):
        self.image_matrix = np.sum(self.image_matrix, axis=1)

class CompoundedImageRawData:
    def __init__(self, image_raw_data_array):
        self.image_raw_data_array = image_raw_data_array

    def sum_columns(self):
        for image_raw_data in self.image_raw_data_array:
            image_raw_data.sum_columns()

    def get_peaks_detector(self):
        slices = [image_raw_data.image_matrix for image_raw_data in self.image_raw_data_array]
        return PeaksDetector(slices)
