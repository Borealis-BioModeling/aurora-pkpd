"""
Adopted from https://github.com/NTBEL/diffusion-fit/blob/main/diffusionfit/measure.py
"""

import numpy as np
import numba


@numba.njit(cache=True)
def ss_error(observed_values, estimated_values):
    """Sum of squared error function."""
    sse = np.sum((observed_values - estimated_values) ** 2)
    return sse


@numba.njit(cache=True)
def sse_to_rmse(sse, N_values):
    """Sum of squared error function."""
    rmse = np.sqrt(sse / N_values)
    return rmse


@numba.njit(cache=True)
def rms_error(observed_values, estimated_values):
    """Root-mean-squared Error function."""
    N_values = np.prod(observed_values.shape)
    sse = ss_error(observed_values, estimated_values)
    rmse = sse_to_rmse(sse, N_values)
    return rmse


@numba.njit(cache=True)
def ma_error(observed_values, estimated_values):
    """Mean absolute error function."""
    mae = np.mean(np.abs(observed_values - estimated_values))
    return mae


@numba.njit(cache=True)
def akaike_ic(maximum_loglikelihood, N_params):
    """Akaike information criterion."""
    return 2 * N_params - 2 * maximum_loglikelihood


@numba.njit(cache=True)
def bayesian_ic(maximum_loglikelihood, N_params, N_data):
    """Bayesian information criterion."""
    return np.log(N_data) * N_params - 2.0 * maximum_loglikelihood