import numpy as np
from peakutils import indexes

from DesktopApp.lib.image.image_data import split_vertically_by


def analyze_image(image, min_dist_between_max_peaks, slice_width=0):
    image_analysis = _analyze_matrix(image, min_dist_between_max_peaks)
    slices_analysis = [_analyze_matrix(matrix, min_dist_between_max_peaks) for matrix in
                       split_vertically_by(image, slice_width)] if slice_width > 0 else []

    return ({
        "hole_image": image_analysis,
        "slices": slices_analysis
    })


# PRIVATE FUNCTIONS


def _analyze_matrix(matrix, min_dist_between_max_peaks):
    intensities = np.asarray(_sum_columns(matrix), dtype=np.int16)
    max_peaks_positions = _max_peaks_positions(intensities, min_dist_between_max_peaks)
    max_peaks_intensities = _intensities_in_positions(intensities, max_peaks_positions)
    min_peaks_positions = _min_peaks_positions(intensities, max_peaks_positions)
    min_peaks_intensities = _intensities_in_positions(intensities, min_peaks_positions)

    return ({
        "intensities": intensities,
        "max_peaks_positions": max_peaks_positions,
        "max_peaks_intensities": max_peaks_intensities,
        "min_peaks_positions": min_peaks_positions,
        "min_peaks_intensities": min_peaks_intensities,
        "amplitudes": _calculate_amplitudes(max_peaks_intensities, min_peaks_intensities),
        "times_to_peaks": _calculate_time_to_peaks(max_peaks_positions, min_peaks_positions),
        "times_to_half_peaks": _calculate_times_to_half_peaks(intensities, max_peaks_positions, min_peaks_positions)

    })


def _calculate_times_to_half_peaks(intensities, max_peaks_positions, min_peaks_positions):
    half_time_to_peaks = []
    for max_min in np.column_stack((max_peaks_positions[0:len(max_peaks_positions) - 1], min_peaks_positions)):
        max_index = max_min[0]
        min_index = max_min[1]

        half_intensity_between_peaks = intensities[max_index] - ((intensities[max_index] - intensities[min_index]) / 2)
        intensities_between_peaks = intensities[max_index:min_index]
        half_max_index = None

        for i in range(0, len(intensities_between_peaks)):
            if intensities_between_peaks[i] < half_intensity_between_peaks:
                half_max_index = i
                break

        half_time_to_peaks.append(abs(max_min[0] - half_max_index + max_min[0]))

    return half_time_to_peaks


def _calculate_time_to_peaks(max_peaks_positions, min_peaks_positions):
    return [abs(max_min[0] - max_min[1]) for max_min in
     np.column_stack((max_peaks_positions[0:len(max_peaks_positions) - 1], min_peaks_positions,))]


def _calculate_amplitudes(max_peaks_intensities, min_peaks_intensities):
    amplitudes = []
    for i in range(0, len(min_peaks_intensities)):
        amplitude = (max_peaks_intensities[i] - min_peaks_intensities[i]) / min_peaks_intensities[i]
        amplitudes.append(amplitude)
    return amplitudes


def _sum_columns(slice):
    return [np.sum(row) for row in slice]


def _max_peaks_positions(a_slice, min_dist_between_max_peaks):
    max_peaks = indexes(a_slice, thres=1.0 / max(a_slice), min_dist=min_dist_between_max_peaks)
    intensity_avg = sum(a_slice) / len(a_slice)
    return [max_peak for max_peak in max_peaks if a_slice[max_peak] > intensity_avg]


def _intensities_in_positions(intensities, positions):
    return [intensities[position] for position in positions]


def _min_peaks_positions(intensities, max_peaks):
    all_minumum_candidates = _all_minimum_candidates(intensities, max_peaks)
    return _select_minimum_peaks(all_minumum_candidates, intensities)


# Here we are calculating the candidates to be a minumum intensity for a givven array.
# This method will return an array of the indexes of the minumum candidates
# F.g minumum_candidates(0, [4,3,2,1,2,3,2,1,0,1,2,3]) will return [3,8]
def _minimum_candidates(offset, intensities):
    return ((np.diff(np.sign(np.diff(intensities))) > 0).nonzero()[0] + 1) + offset


def _all_minimum_candidates(intensities, max_peaks_positions):
    all_minimum_candidates = []
    for i in range(0, len(max_peaks_positions) - 1):
        current_peak = max_peaks_positions[i]
        next_peak = max_peaks_positions[i + 1]
        intensities_between_peaks = intensities[current_peak:next_peak]
        all_minimum_candidates.append(_minimum_candidates(current_peak, intensities_between_peaks))

    return all_minimum_candidates


def _select_minimum_peaks(all_minimum_candidates, intensities):
    return [_minimum_peak(candidates, intensities) for candidates in all_minimum_candidates]


def _minimum_peak(minimum_candidates, intensities):
    winner = minimum_candidates[0]
    for candidate in minimum_candidates:
        winner_intensity = intensities[winner]
        candidate_intensity = intensities[candidate]
        winner = winner if winner_intensity < candidate_intensity else candidate

    return winner
