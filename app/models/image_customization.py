import cv2

DEFAULT_SIGMA_SPATIAL = 1

DEFAULT_SIGMA_COLOR = 1

DEFAULT_FILTER_DIAMETER = 1

DEFAULT_BRIGHT_VALUE = 0

DEFAULT_CONTRAST_VALUE = 0


class ImageCustomizationErrors(object):
    def __init__(self, image_customization):
        self._image_customization = image_customization

    def any(self):
        return False

    def send_details_to(self, receiver):
        # TODO We don't have validations here,
        pass


class ImageCustomization(object):
    @classmethod
    def default(cls):
        return cls(DEFAULT_CONTRAST_VALUE, DEFAULT_BRIGHT_VALUE,
                   DEFAULT_FILTER_DIAMETER, DEFAULT_SIGMA_COLOR,
                   DEFAULT_SIGMA_SPATIAL)

    def __init__(self, contrast_value, bright_value, filter_diameter,
                 sigma_color, sigma_spatial):
        self.sigma_spatial = sigma_spatial
        self.sigma_color = sigma_color
        self.filter_diameter = filter_diameter
        self.bright_value = bright_value
        self.contrast_value = contrast_value

    def apply_to(self, image_data):
        alpha_contrast = float(131 * (self.contrast_value + 127)) / (
                127 * (131 - self.contrast_value))
        gamma_contrast = 127 * (1 - alpha_contrast)

        if self.bright_value > 0:
            shadow = self.bright_value
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + self.bright_value

        alpha_brightness = (highlight - shadow) / 255
        gamma_brightness = shadow

        customized_image = cv2.addWeighted(image_data, alpha_brightness,
                                           image_data, 0, gamma_brightness)
        customized_image = cv2.addWeighted(customized_image, alpha_contrast,
                                           customized_image, 0, gamma_contrast)
        customized_image = cv2.bilateralFilter(customized_image,
                                               self.filter_diameter,
                                               self.sigma_color,
                                               self.sigma_spatial)
        return customized_image

    @classmethod
    def none(cls):
        return cls(0, 0, 1, 1, 1)

    def validate(self):
        return ImageCustomizationErrors(self)

    def copy(self):
        return self.__class__(self.contrast_value, self.bright_value,
                              self.filter_diameter, self.sigma_color,
                              self.sigma_spatial)
