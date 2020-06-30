import numpy as np
from peakutils.peak import indexes


class PeaksDetector:
    def __init__(self, slices, min_dist_between_maxs):
        self.min_dist_between_maxs = min_dist_between_maxs
        self.slices = self.__create_slices(slices)

    def __create_slices(self, slices):
        def create_slice(slice): return SlicePeaksDetector(slice, self.min_dist_between_maxs)
        return map(create_slice, slices)

    def max_peaks_positions(self):
        return [a_slice.max_peaks_positions() for a_slice in self.slices]

    def max_peks_intensities(self):
        return [a_slice.max_peaks_intencities() for a_slice in self.slices]

    def min_peaks_positions(self):
        return [a_slice.min_peaks_positions() for a_slice in self.slices]

    def min_peaks_intensities(self):
        return [a_slice.min_peks_intensities() for a_slice in self.slices]

class SlicePeaksDetector:
    def __init__(self, a_slice, min_dist_between_maxs):
        self.intensities = a_slice
        self.min_dist_between_maxs = min_dist_between_maxs

    def max_peaks_positions(self):
        max_peaks = indexes(self.intensities, thres=2.5 / max(self.intensities), min_dist=self.min_dist_between_maxs)
        max_peak_avg = sum(max_peaks) / len(max_peaks)
        return [ max_peak for max_peak in max_peaks if self.intensities[max_peak] > max_peak_avg]

    def max_peaks_intensities(self):
        return [self.intensities[max_peak] for max_peak in self.max_peaks_positions()]

    def min_peaks_positions(self):
        intensities_between_max_peaks = self.__get_intensities_between_max_peaks
        all_minumum_candidates = self.__get_all_minumum_candidates(intensities_between_max_peaks)
        return self.__select_mininum_peaks(all_minumum_candidates)

    def min_peaks_intensities(self):
        return [self.intensities[min_peak] for min_peak in self.min_peaks_positions()]

    #Here we are calculating the candidates to be a minumum intensity for a givven array.
    #This method will return an array of the indexes of the minumum candidates
    # F.g minumum_candidates([4,3,2,1,2,3,2,1,0,1,2,3]) will return [3,8]
    def __minimum_candidates(self, offset_and_intensities):
        offset = offset_and_intensities[0]
        intensities = offset_and_intensities[1]
        return ((np.diff(np.sign(np.diff(intensities))) > 0).nonzero()[0] + 1) + offset

    def __get_intensities_between_max_peaks(self):
        intensities_between_max_peaks = []
        max_peaks = self.max_peaks_positions()
        for i in range(0, len(max_peaks) - 2):
            current_max_peak = max_peaks[i]
            next_max_peak = max_peaks[i + 1]

            intensities_between_max_peaks.append((current_max_peak, self.intensities[current_max_peak + 1:next_max_peak]))

        return intensities_between_max_peaks

    def __get_all_minumum_candidates(self, intensities_between_max_peaks):
        return [ self.__minimum_candidates(offset_and_intensities) for offset_and_intensities in intensities_between_max_peaks]

    def __select_mininum_peaks(self, all_minimum_candidates):
        return [self.__minimum_peak(candidates) for candidates in all_minimum_candidates]

    def __minimum_peak(self, minimum_candidates):
        winner = minimum_candidates[0]
        for candidate in minimum_candidates:
            winner_intensity = self.intensities[winner]
            candidate_intensity = self.intensities[candidate]
            winner = winner if winner_intensity < candidate_intensity else candidate

        return winner
