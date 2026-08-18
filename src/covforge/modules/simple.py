import numpy as np
from covforge.config import EPS

def covariance_rolling_window(
        Xx: np.ndarray,
        l: int,
    ) -> np.ndarray:
    T, N = Xx.shape
    assert l < T, T
    Sigma = np.full((T, N, N), np.nan)  # combined covariance matrix
    nans = np.isnan(Xx)
    mask = np.zeros((N,), dtype=bool)
    Xx = np.nan_to_num(Xx, nan=0.0)
    
    for t in range(l, T):
        mask |= ~nans[t]
        mask_ix = np.ix_(mask, mask)
        
        xt = Xx[t-l:t, mask]  # [l, n]
        Sigma[t][mask_ix] = xt.T @ xt / l

    return Sigma


def covariance_ewma(
        Xx: np.ndarray,
        t_min: int,
        h: int,
    ) -> np.ndarray:
    T, N = Xx.shape
    assert t_min < T, T
    lamda = 0.5**(1/h)
    ewma = np.zeros((N, N))

    nans = np.isnan(Xx)
    Xx = np.nan_to_num(Xx, nan=0.0)
    mask = np.zeros((N,), dtype=bool)
    Sigma = np.full((T, N, N), np.nan)  # combined covariance matrix

    for t in range(T):
        mask |= ~nans[t]
        mask_ix = np.ix_(mask, mask)

        xt = Xx[t, mask]
        cov_t = np.outer(xt, xt)
        ewma[mask_ix] = lamda * ewma[mask_ix] + (1 - lamda) * cov_t

        if t < t_min:
            continue
        Sigma[t] = ewma

    return Sigma
