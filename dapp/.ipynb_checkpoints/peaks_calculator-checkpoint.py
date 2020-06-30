from dapp.slice import Slice


class PeaksCalculator:
    def __init__(self, slices):
        self.slices = self.create_slices(slices)

    def create_slices(self, slices):
        def create_slice(slice): return Slice(slice)
        return map(create_slice, slices)

    def calculate_max_peaks(self, min_dist_between_maxs):
        for slice in self.slices:
            slice.calculate_max_peaks(min_dist_between_maxs)
