from typing import Callable, List, Dict
from .paths import pickle_path, info_path
from .various import odd_even_split, build_query
from .hash import hash_file
import os
import pandas as pd
import zlib
import pickle
import compress_pickle


def uncached(generator: Callable, dataset: List, *args, **kwargs):
    return odd_even_split(generator(dataset)), None


def cached(generator: Callable, dataset: List, cache_dir: str, **parameters: Dict):
    path = pickle_path(cache_dir, **parameters)
    try:
        key = pd.read_csv(info_path(cache_dir)).query(
            build_query({"path": path})
        )["key"].values[0]
        if key != hash_file(path):
            raise ValueError("Holdout has been tempered.")
        return compress_pickle.load(path), key
    except (pickle.PickleError, FileNotFoundError, AttributeError,  EOFError, ImportError, IndexError, zlib.error):
        data = odd_even_split(generator(dataset))
    key = dump(data, cache_dir, path, **parameters)
    return (data, key)


def build_info(path: str, parameters: Dict, key: str)->pd.DataFrame:
    return pd.DataFrame({
        "path": path,
        "key": key,
        **parameters
    }, index=[0])


def dump(data, cache_dir: str, path: str, **parameters: Dict)->str:
    compress_pickle.dump(data, path)
    key = hash_file(path)
    info_file = info_path(cache_dir)
    info = build_info(path, parameters, key)
    if os.path.exists(info_file):
        info = pd.concat([pd.read_csv(info_file), info])
    info.to_csv(info_file, index=False)
    return key


def get_holdout_key(cache_dir: str, **parameters: Dict)->str:
    """Return key, if cached, for given holdout else return None.
        cache_dir:str, cache directory to load data from
        parameters:Dict, parameters used to generated the holdout.
    """
    try:
        return pd.read_csv(info_path(cache_dir)).query(build_query(parameters))["key"].values[0]
    except (FileNotFoundError, IndexError):
        return None
