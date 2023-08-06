# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines helpful model wrapper and utils for implicitly rewrapping the model to conform to explainer contracts."""

import numpy as np

from azureml.explain.model.common.constants import ModelTask

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', 'Starting from version 2.2.1', UserWarning)
    from shap.common import DenseData


def _convert_to_two_cols(function, examples):
    """In classification case, convert the function's output to two columns if it outputs one column.

    :param function: The prediction function to evaluate on the examples.
    :type function: function
    :param examples: The model evaluation examples.
    :type examples: np.array or list
    :return: The function chosen from given model and classification domain.
    :rtype (function, str)
    """
    # Add wrapper function to convert output to 2D array, check values to decide on whether
    # to throw, or create two columns [1-p, p], or leave just one in multiclass one-class edge-case
    result = function(examples)
    # If the function gives a 2D array of one column, we will need to reshape it prior to concat
    is_2d_result = len(result.shape) == 2
    convert_to_two_cols = False
    for value in result:
        if value < 0 or value > 1:
            raise Exception("Probability values outside of valid range: " + str(value))
        if value < 1:
            convert_to_two_cols = True
    if convert_to_two_cols:
        # Create two cols, [1-p, p], from evaluation result
        if is_2d_result:
            def function_2D_two_cols_wrapper_2D_result(dataset):
                result = function(dataset)[:, 0]
                return np.stack([1 - result, result], axis=-1)
            return (function_2D_two_cols_wrapper_2D_result, ModelTask.Classification)
        else:
            def function_2D_two_cols_wrapper_1D_result(dataset):
                result = function(dataset)
                return np.stack([1 - result, result], axis=-1)
            return (function_2D_two_cols_wrapper_1D_result, ModelTask.Classification)
    else:
        if is_2d_result:
            return (function, ModelTask.Classification)
        else:
            def function_2D_one_col_wrapper(dataset):
                result = function(dataset)
                # Create one col in rare edge case scenario for multiclass one-class result
                return result.reshape(result.shape[0], 1)
            return (function_2D_one_col_wrapper, ModelTask.Classification)


class WrappedClassificationModel(object):
    """A class for wrapping a classification model."""

    def __init__(self, model, eval_function):
        """Initialize the WrappedClassificationModel with the model and evaluation function."""
        self._eval_function = eval_function
        self._model = model

    def predict(self, dataset):
        """Predict the output using the wrapped classification model.

        :param dataset: The dataset to predict on.
        :type dataset: DatasetWrapper
        """
        if str(type(self._model)).endswith("tensorflow.python.keras.engine.sequential.Sequential'>"):
            return self._model.predict_classes(dataset)
        return self._model.predict(dataset)

    def predict_proba(self, dataset):
        """Predict the output probability using the wrapped model.

        :param dataset: The dataset to predict_proba on.
        :type dataset: DatasetWrapper
        """
        return self._eval_function(dataset)


class WrappedRegressionModel(object):
    """A class for wrapping a regression model."""

    def __init__(self, model, eval_function):
        """Initialize the WrappedRegressionModel with the model and evaluation function."""
        self._eval_function = eval_function
        self._model = model

    def predict(self, dataset):
        """Predict the output using the wrapped regression model.

        :param dataset: The dataset to predict on.
        :type dataset: DatasetWrapper
        """
        return self._eval_function(dataset)


def _wrap_model(model, examples, model_task, is_function):
    """If needed, wraps the model or function in a common API based on model task and prediction function contract.

    :param model: The model or function to evaluate on the examples.
    :type model: function or model with a predict or predict_proba function
    :param examples: The model evaluation examples.
    :type examples: DatasetWrapper
    :param model_task: Optional parameter to specify whether the model is a classification or regression model.
        In most cases, the type of the model can be inferred based on the shape of the output, where a classifier
        has a predict_proba method and outputs a 2 dimensional array, while a regressor has a predict method and
        outputs a 1 dimensional array.
    :type model_task: str
    :return: The function chosen from given model and chosen domain, or model wrapping the function and chosen domain.
    :rtype (function, str) or (model, str)
    """
    if is_function:
        return _eval_function(model, examples, model_task)
    else:
        eval_function, eval_ml_domain = _eval_model(model, examples, model_task)
        if eval_ml_domain == ModelTask.Classification:
            return WrappedClassificationModel(model, eval_function), eval_ml_domain
        else:
            return WrappedRegressionModel(model, eval_function), eval_ml_domain


def _eval_model(model, examples, model_task):
    """Return function from model and specify the ML Domain using model evaluation on examples.

    :param model: The model to evaluate on the examples.
    :type model: model with a predict or predict_proba function
    :param examples: The model evaluation examples.
    :type examples: DatasetWrapper
    :param model_task: Optional parameter to specify whether the model is a classification or regression model.
        In most cases, the type of the model can be inferred based on the shape of the output, where a classifier
        has a predict_proba method and outputs a 2 dimensional array, while a regressor has a predict method and
        outputs a 1 dimensional array.
    :type model_task: str
    :return: The function chosen from given model and chosen domain.
    :rtype (function, str)
    """
    # TODO: Add more pytorch model types here
    if str(type(model)).endswith("tensorflow.python.keras.engine.sequential.Sequential'>"):
        if model_task == ModelTask.Regression:
            return _eval_function(model.predict, examples, ModelTask.Regression)
        result = model.predict_proba(examples.typed_wrapper_func(examples.dataset[0:1]))
        if result.shape[1] == 1 and model_task == ModelTask.Unknown:
            raise Exception("Please specify model_task to disambiguate model type since "
                            "result of calling function is 2D array of one column.")
        else:
            return _eval_function(model.predict_proba, examples, ModelTask.Classification)
    else:
        has_predict_proba = hasattr(model, "predict_proba")
        # Note: Allow user to override default to use predict method for regressor
        if has_predict_proba and model_task != ModelTask.Regression:
            return _eval_function(model.predict_proba, examples, model_task)
        else:
            return _eval_function(model.predict, examples, model_task)


def _eval_function(function, examples, model_task, wrapped=False):
    """Return function and specify the ML Domain using function evaluation on examples.

    :param function: The prediction function to evaluate on the examples.
    :type function: function
    :param examples: The model evaluation examples.
    :type examples: DatasetWrapper
    :param model_task: Optional parameter to specify whether the model is a classification or regression model.
        In most cases, the type of the model can be inferred based on the shape of the output, where a classifier
        has a predict_proba method and outputs a 2 dimensional array, while a regressor has a predict method and
        outputs a 1 dimensional array.
    :type model_task: str
    :param wrapped: Indicates if function has already been wrapped.
    :type wrapped: bool
    :return: The function chosen from given model and chosen domain.
    :rtype (function, str)
    """
    # Try to run the function on a single example - if it doesn't work wrap
    # it in a function that converts a 1D array to 2D for those functions
    # that only support 2D arrays as input
    examples_dataset = examples.dataset
    if isinstance(examples_dataset, DenseData):
        examples_dataset = examples_dataset.data
    try:
        result = function(examples.typed_wrapper_func(examples_dataset[0]))
    except ValueError as ex:
        # If function has already been wrapped, re-throw error to prevent stack overflow
        if wrapped:
            raise ex

        def function_input_1D_wrapper(dataset):
            if len(dataset.shape) == 1:
                dataset = dataset.reshape(1, -1)
            return function(dataset)

        return _eval_function(function_input_1D_wrapper, examples, model_task, wrapped=True)
    if len(result.shape) == 2:
        # If the result of evaluation the function is a 2D array of 1 column,
        # and they did not specify classifier or regressor, throw exception
        # to force the user to disambiguate the results.
        if result.shape[1] == 1:
            if model_task == ModelTask.Unknown:
                raise Exception("Please specify model_task to disambiguate model type since "
                                "result of calling function is 2D array of one column.")
            elif model_task == ModelTask.Classification:
                return _convert_to_two_cols(function, examples_dataset)
            else:
                # model_task == ModelTask.Regression
                # In case user specified a regressor but we have a 2D output with one column,
                # we want to flatten the function to 1D
                def function_flatten(dataset):
                    return function(dataset).flatten()
                return (function_flatten, model_task)
        else:
            if model_task == ModelTask.Unknown or model_task == ModelTask.Classification:
                return (function, ModelTask.Classification)
            else:
                raise Exception("Invalid shape for prediction: "
                                "Regression function cannot output 2D array with multiple columns")
    elif len(result.shape) == 1:
        if model_task == ModelTask.Unknown:
            return (function, ModelTask.Regression)
        elif model_task == ModelTask.Classification:
            return _convert_to_two_cols(function, examples_dataset)
        return (function, model_task)
