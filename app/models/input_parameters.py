DEFAULT_SLICE_WIDTH = 0
DEFAULT_CALIBRATION = None
DEFAULT_MIN_DIST = None


class InputParametersErrors(object):
    def __init__(self, input_parameters):
        self._input_parameters = input_parameters

    def any(self):
        return self._slice_width_invalid() or self._calibration_invalid() or self._min_dist_invalid()

    def _slice_width_invalid(self):
        slice_width = self._input_parameters.slice_width
        return slice_width is None or slice_width < 0

    def send_details_to(self, receiver):
        if self._slice_width_invalid():
            receiver.error_in_slice_width()

        if self._calibration_invalid():
            receiver.error_in_calibration()

        if self._min_dist_invalid():
            receiver.error_in_min_dist()

    def _min_dist_invalid(self):
        min_dist = self._input_parameters.min_dist
        valid = min_dist is None or min_dist <= 0
        return valid

    def _calibration_invalid(self):
        calibration = self._input_parameters.calibration
        valid = calibration is None or calibration <= 0
        return valid


class InputParameters(object):
    @classmethod
    def default(cls):
        return cls(DEFAULT_MIN_DIST, DEFAULT_CALIBRATION, DEFAULT_SLICE_WIDTH)

    def __init__(self, min_dist, calibration, slice_width):
        self.slice_width = slice_width
        self.calibration = calibration
        self.min_dist = min_dist

    def validate(self):
        return InputParametersErrors(self)

    def copy(self):
        return self.__class__(self.min_dist, self.calibration,
                              self.slice_width)
