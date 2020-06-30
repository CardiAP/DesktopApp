import numpy as np
import peakutils
from peakutils.peak import indexes

class Slice:
    def __init__(self, slice):
        self.intencities = slice
        self.max_peaks = []
        self.min_peaks = []

    def calculate_max_peaks(self, min_dist_between_maxs):
        max_peaks = indexes(self.intencities, thres=2.5 / max(self.intencities), min_dist=min_dist_between_maxs)
        max_peak_avg = sum(max_peaks) / len(max_peaks)
        for max_peak in max_peaks:
            if self.intencities[max_peak] > max_peak_avg:
                self.max_peaks.append(max_peak)

    def calculate_min_peaks(selfs):
        return 1
