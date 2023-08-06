from typing import Dict
from .utils import build_query, build_keys
from .store_results import load_results, is_result_directory
from .work_in_progress import is_work_in_progress

def skip(key: str, hyper_parameters: Dict, results_directory: str)->bool:
    """Default function to choose to load or not a given holdout.
        key: str, key identifier of holdout to be skipped.
        hyper_parameters: Dict, hyper parameters to check for.
        results_directory: str = "results", directory where to store the results.
    """
    return is_result_directory(results_directory) and (
        not load_results(results_directory).query(build_query(build_keys(key, hyper_parameters))).empty or
        is_work_in_progress(key, results_directory)
    )