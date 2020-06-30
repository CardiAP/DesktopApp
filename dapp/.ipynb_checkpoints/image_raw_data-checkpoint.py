import numpy as np

from dapp.peaks_calculator import PeaksCalculator


class ImageRawData:
    def __init__(self, image_matrix):
        self.image_matrix = image_matrix

    def split_vertically_by(self, width):
        # TODO: Validar que la cantiad de columnas es divisible por el with
        def image_raw_data(column): return ImageRawData(column)
        return CompoundedImageRawData(map(image_raw_data, np.hsplit(self.image_matrix, width)))

    def sum_columns(self):
        self.image_matrix = np.sum(self.image_matrix, axis=1)


class CompoundedImageRawData:
    def __init__(self, image_raw_data_array):
        self.image_raw_data_array = image_raw_data_array

    def sum_columns(self):
        for image_raw_data in self.image_raw_data_array:
            image_raw_data.sum_columns()

    def get_peaks_calculator(self):
        def get_slice(raw_data): return raw_data.image_matrix
        return PeaksCalculator(map(get_slice, self.image_raw_data_array))
