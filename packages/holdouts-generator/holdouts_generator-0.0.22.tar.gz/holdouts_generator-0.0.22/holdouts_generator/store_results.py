from typing import Dict
import os
import pandas as pd
import numpy as np
from .utils import results_path, hyper_parameters_path, parameters_path, history_path, trained_model_path, true_labels_path, predictions_labels_path
from .utils import build_keys, build_query
from keras import Model
import shutil
from json import dump
import humanize


def store_result(key: str, new_results: Dict, time:int, hyper_parameters: Dict = None, parameters: Dict = None, results_directory: str = "results"):
    """Store given results in a standard way, so that the skip function can use them.
        key: str, key identifier of holdout to be skipped.
        new_results: Dict, results to store.
        hyper_parameters: Dict, hyper parameters to check for.
        parameters: Dict, parameters used for tuning the model.
        results_directory: str = "results", directory where to store the results.
    """
    hppath = None if hyper_parameters is None else hyper_parameters_path(
        results_directory, hyper_parameters)
    ppath = None if parameters is None else parameters_path(
        results_directory, parameters)
    rpath = results_path(results_directory)
    results = pd.DataFrame({
        **new_results,
        **build_keys(key, hyper_parameters),
        "hyper_parameters_path": hppath,
        "parameters_path": ppath,
        "required_time": time,
        "human_required_time": humanize.naturaldelta(time)
    }, index=[0])
    if hyper_parameters:
        with open(hppath, "w") as f:
            dump(hyper_parameters, f)
    if parameters:
        with open(ppath, "w") as f:
            dump(parameters, f)
    if os.path.exists(rpath):
        results = pd.concat([pd.read_csv(rpath), results])
    results.to_csv(rpath, index=False)


def store_keras_result(key: str, history: Dict, x_test: np.ndarray, y_test_true: np.ndarray, model: Model, time:int, informations:Dict = None, hyper_parameters: Dict = None, parameters: Dict = None, save_model: bool = True, results_directory: str = "results"):
    """Store given keras model results in a standard way, so that the skip function can use them.
        key: str, key identifier of holdout to be skipped.
        history: Dict, training history to store.
        x_test:np.ndarray, input test values for the model.
        y_test_true:np.ndarray, true output test values.
        model:Model, model to save if save_model is True, used to predict the value.
        hyper_parameters: Dict, hyper parameters to check for.
        parameters: Dict, parameters used for tuning the model.
        save_model:bool=True, whetever to save or not the model.
        results_directory: str = "results", directory where to store the results.
    """
    y_pred = model.predict(x_test)

    hpath = history_path(results_directory, history)
    mpath = trained_model_path(results_directory, key, hyper_parameters)
    plpath = predictions_labels_path(results_directory, y_pred)
    tlpath = true_labels_path(results_directory, y_test_true)

    informations = {} if informations is None else informations
    dfh = pd.DataFrame(history)
    store_result(key, {
        **dfh.iloc[-1].to_dict(),
        **informations,
        "history_path": hpath,
        "model_path": mpath if save_model else None,
        "predictions_labels_path": plpath,
        "true_labels_path": tlpath
    }, time, hyper_parameters, parameters, results_directory)
    dfh.to_csv(hpath, index=False)
    pd.DataFrame(y_pred).to_csv(plpath, index=False)
    pd.DataFrame(y_test_true).to_csv(tlpath, index=False)
    if save_model:
        model.save(mpath)


def load_results(results_directory: str = "results"):
    """Load standard results.
        results_directory: str = "results", directory where results are stored.
    """
    return pd.read_csv(results_path(results_directory))


def load_result(key: str, hyper_parameters: Dict = None, results_directory: str = "results"):
    """Load standard results corresponding at given key and hyper_parameters.
        key: str, key identifier of holdout to be skipped.
        hyper_parameters: Dict, hyper parameters to check for.
        results_directory: str = "results", directory where to store the results.
    """
    return load_results(results_directory).query(
        build_query(build_keys(key, hyper_parameters))
    ).to_dict('records')[0]


def delete_results(results_directory: str = "results"):
    """Delete the results stored in a given directory.
        results_directory: str = "results", directory where results are stores.
    """
    if os.path.exists(results_directory):
        shutil.rmtree(results_directory)
