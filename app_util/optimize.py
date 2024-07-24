from inspect import signature
import numpy as np
from galibrate.sampled_parameter import SampledParameter
from galibrate import GAO
from app_util import measure


X_BOUND = ["ec50", "ic50", "kd", "ki"]
Y_BOUND = ["emax", "emin", "fret_ratio_max"]
ZERO_TO_INF = ["n", "tau"]
ZERO_TO_ONE = ["epsilon"]
ONE_TO_INF = ["gamma"]


def get_bounds(arg_name, xdata, ydata):
    if arg_name in X_BOUND:
        return np.min(xdata), np.max(xdata)
    elif arg_name in Y_BOUND:
        y_max = np.max(ydata)
        return 0.0, y_max + 0.1 * y_max
    elif arg_name in ZERO_TO_INF:
        return 0.0, 100.0
    elif arg_name in ONE_TO_INF:
        return 1.0, 100.0
    else:
        return 0.0, 1.0


def response_fit(response_function, xdata, ydata, sigma=None):
    """Use Genetic Algorithm Optimization to fit an exposure-response function to data."""
    sign = signature(response_function)
    func_args = list(sign.parameters.keys())[1:]
    sampled_parameters = list()
    for arg in func_args:
        lower_bound, upper_bound = get_bounds(arg, xdata, ydata)
        sampled_parameters.append(
            SampledParameter(
                name=arg, loc=lower_bound, width=(upper_bound - lower_bound)
            )
        )

    def fitness(chromosome):
        y_pred = response_function(xdata, *chromosome)
        sse = measure.ss_error(ydata, y_pred)
        return -sse
    
    pop_size = np.max([len(func_args) * 10, 200])
    gao = GAO(sampled_parameters, fitness, pop_size, generations=200)
    best_chromo, best_chromo_fitness = gao.run()
    args_best = dict()
    for i in range(len(func_args)):
        args_best[func_args[i]] = best_chromo[i]
    return args_best, np.abs(best_chromo_fitness)
