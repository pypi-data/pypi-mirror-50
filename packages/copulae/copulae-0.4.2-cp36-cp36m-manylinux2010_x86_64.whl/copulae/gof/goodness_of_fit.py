import numpy as np
from copy import deepcopy

from copulae.copula import AbstractCopula
from copulae.core import pseudo_obs


def gof_copula(copula: AbstractCopula, data: np.ndarray, reps: int, ties="average", fit_ties="average"):
    _check_arguments(copula, data, reps)

    u_hat = pseudo_obs(data, ties=ties)
    u_hat_fitted = pseudo_obs(data, ties=fit_ties) if _has_duplicates(data) and fit_ties != ties else deepcopy(u_hat)

    cop = type(copula)(dim=data.shape[2])
    cop.fit(u_hat_fitted)

    u = u_hat
    # T =


def _check_arguments(copula: AbstractCopula, x: np.ndarray, reps: int):
    assert isinstance(reps, int) and reps >= 1, "reps must be an integer with value >= 1"

    assert x.ndim == 2 and x.shape[1] == copula.dim, \
        "Data must be a matrix where the number of columns matches the copula's dimension"


def _has_duplicates(data: np.ndarray):
    nrow, ncol = data.shape
    for i in range(ncol):
        if len(np.unique(data[:, i])) != nrow:
            return True
    return False


def gof_t_stat(data: np.ndarray, ties="average"):
    u = pseudo_obs(data, ties)
