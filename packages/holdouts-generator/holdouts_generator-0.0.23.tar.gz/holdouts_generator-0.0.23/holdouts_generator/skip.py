from typing import Dict
from os.path import exists
from pandas import read_csv
from .utils import build_query, build_keys, results_path


def skip(key: str, hyper_parameters: Dict, results_directory: str)->bool:
    """Default function to choose to load or not a given holdout.
        key: str, key identifier of holdout to be skipped.
        hyper_parameters: Dict, hyper parameters to check for.
        results_directory: str = "results", directory where to store the results.
    """
    path = results_path(results_directory)
    return exists(path) and not read_csv(path).query(build_query(build_keys(key, hyper_parameters))).empty
