from PySide6.QtCore import QPoint


class ImageSelectionErrors(object):
    def __init__(self, image_selection):
        self._image_selection = image_selection

    def any(self):
        return self._image_selection.x_start is None or \
               self._image_selection.x_end is None or \
               self._image_selection.y_start is None or \
               self._image_selection.y_end is None

    def send_details_to(self, receiver):
        if self.any():
            receiver.incomplete_selection()


class ImageSelection(object):
    @classmethod
    def default(cls):
        return cls(None, None, None, None)

    @classmethod
    def from_qt_points(cls, point1, point2):
        if point1 is not None and point2 is not None:
            x_start = int(min(point1.x(), point2.x()))
            y_start = int(min(point1.y(), point2.y()))
            x_end = int(max(point1.x(), point2.x()))
            y_end = int(max(point1.y(), point2.y()))
            return cls(x_start, x_end, y_start, y_end)
        else:
            return cls(None, None, None, None)

    def __init__(self, x_start, x_end, y_start, y_end):
        self.y_end = y_end
        self.y_start = y_start
        self.x_end = x_end
        self.x_start = x_start

    def as_qt_points(self):
        point1 = QPoint(self.x_start, self.y_start) if self.x_start is not None and self.y_start is not None else None
        point2 = QPoint(self.x_end, self.y_end) if self.x_end is not None and self.y_end is not None else None
        return point1, point2

    def apply_to(self, image_data):
        return image_data[self.x_start:self.x_end][self.y_start:self.y_end]

    def validate(self):
        return ImageSelectionErrors(self)

    def copy(self):
        return self.__class__(self.x_start, self.x_end, self.y_start, self.y_end)
