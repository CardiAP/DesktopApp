import cv2
from dapp.image_raw_data import ImageRawData


class GreyScaleImage:
    def __init__(self, name):
        self.image_name = name
        self.image = cv2.imread(name, cv2.IMREAD_GRAYSCALE)

    def crop_vertical(self, pixel_start, pixel_end):
        self.image = self.image[pixel_start:pixel_end]

    def crop_horizontal(self, pixel_start, pixel_end):
        self.image = self.image[0:len(self.image), pixel_start:pixel_end]

    def smooth(self):
        cv2.bilateralFilter(self.image, 20, 300, 300)

    def get_raw_data(self):
        return ImageRawData(self.image)
