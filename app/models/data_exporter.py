import json
import os
from pathlib import Path

import numpy as np
import pandas


class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


class DataExporter(object):
    def __init__(self, results, directory):
        self._results = results
        self._directory = Path(directory)

    def _ensure_image_directory_exists(self, name):
        if not os.path.isdir(self._directory / name):
            os.mkdir(self._directory / name)

    def save_csv(self):
        slices_data_points = self._results.slices_data_points()
        for (result_id, name) in self._results.selected_results_ids_and_names():
            self._ensure_image_directory_exists(name)
            image_data = self._results.image_data_points_data_for_selected_result(result_id)
            #TODO sacar esto de aca, abria que reificar los resultados del analisisz
            peaks_number = max([ len(image_data[data_point]) for data_point in image_data])
            peaks = [f"Peak {peak}" for peak in range(0, peaks_number)]
            pandas.DataFrame.from_dict(image_data, orient='index', columns=peaks).to_csv(self._directory / name / 'image.csv')

            slices_data = self._results.slices_data_points_data_for_selected_result(result_id)
            slices_by_metric = np.array([list(slice_data.values()) for slice_data in slices_data], ndmin=2).transpose(1, 0)
            for (index, slices) in enumerate(slices_by_metric):
                # TODO sacar esto de aca, abria que reificar los resultados del analisisz
                df_columns = [f"Peak {peak}" for peak in range(0, max([len(slice) for slice in slices]))]
                df_index = [f"Slice {slice_number}" for slice_number in range(0, len(slices))]
                pandas.DataFrame(list(slices), index=df_index, columns=df_columns).to_csv(self._directory / name / f"{slices_data_points[index]}.csv")

    def save_json(self):
        data = [{name: {
            "image": self._results.image_data_points_data_for_selected_result(result_id),
            "slices": self._results.slices_data_points_data_for_selected_result(result_id)
        }} for (result_id, name) in self._results.selected_results_ids_and_names()]
        self._save_file('analysis_results.json',
                        json.dumps(data, cls=NumpyEncoder))

    def _save_file(self, file_name, data):
        with open(self._directory / file_name, "w") as file_handle:
            file_handle.write(data)