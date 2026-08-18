import numpy as np
from covforge.config import EPS


def scale_returns(xt, ewma_var, mask):
    vol_t = ewma_var[mask]
    vol_t = np.sqrt(np.clip(vol_t, min=EPS**2))  # avoid extreme scaling

    xt = xt / vol_t
    xt = np.clip(xt, min=-3.0, max=3.0)
    return xt, vol_t


def scale_momentum(ewma_mom, mask_ix):
    diag = np.sqrt(np.diag(ewma_mom[mask_ix]))
    scale_t = np.outer(diag, diag)
    scale_t = np.clip(scale_t, min=EPS)

    Ct: np.ndarray = ewma_mom[mask_ix] / scale_t
    Ct = 0.5 * (Ct + Ct.T)  # pseudo correlation matrix
    return Ct, scale_t


def em_initialization(Ct, k):
    d, Qt = np.linalg.eigh(Ct)
    dk = np.clip(d[-k:], min=EPS)
    Qk = Qt[:,-k:]

    Ft = Qk * np.sqrt(dk)[None,:]
    dt = np.diag(Ct - Ft @ Ft.T)
    dt = np.clip(dt, min=EPS)
    return Ft, dt


def expectation_maximisation(Ft, dt, Ct):
    Ik = np.eye(Ft.shape[1])
    max_iter = 10
    tol = 1e-4

    for _ in range(max_iter):
        F_prev = Ft
        d_prev = dt

        # E step
        D_inv = np.diag(1.0/dt)
        Cov_z = np.linalg.solve(Ft.T @ D_inv @ Ft + Ik, Ik)  # Cov[z|x]
        Beta = Cov_z @ Ft.T @ D_inv                          # E[z|x] = Beta @ x
        M_xz = Ct @ Beta.T                                   # E[xz']
        M_zz = Beta @ Ct @ Beta.T + Cov_z                    # E[zz']

        # M step
        Ft = M_xz @ np.linalg.solve(M_zz, Ik)
        dt = np.diag(Ct - 2 * M_xz @ Ft.T + Ft @ M_zz @ Ft.T)
        dt = dt.clip(min=EPS)

        # Convergence
        dF = np.linalg.norm(Ft - F_prev) / np.linalg.norm(F_prev)
        dD = np.linalg.norm(dt - d_prev) / np.linalg.norm(d_prev)
        if dF < tol and dD < tol:
            break

    return Ft, dt


def covariance_factor_iewma(
        Xx: np.ndarray, 
        k: int, 
        t_min: int,
        h_cov: int, 
        h_var: int
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    T, N = Xx.shape  # T timesteps, N assets
    assert t_min < T, T
    assert k < N, N
    nans = np.isnan(Xx)
    mask = np.zeros((N,), dtype=bool)
    Xx = np.nan_to_num(Xx, nan=0.0)

    F_cov = np.full((T, N, k), np.nan)  # factor loading matrix of covariance
    d_var = np.full((T, N), np.nan)     # idiosyncratic variance of covariance
    Sigma = np.full((T, N, N), np.nan)  # combined covariance matrix

    # ewma_t = lamda * ewma_tm1 + (1-lamda) * xt
    lamda_cov = 0.5**(1/h_cov)
    lamda_var = 0.5**(1/h_var)
    ewma_mom = np.zeros((N, N))
    ewma_var = np.zeros((N,))

    for t in range(T):
        mask |= ~nans[t]  # at least one day of returns
        n = mask.sum()
        k_ = min(k, n)

        if n == 0:
            continue

        # Standard scale returns
        xt = Xx[t, mask]
        var_t = xt**2
        ewma_var[mask] = lamda_var * ewma_var[mask] + (1 - lamda_var) * var_t
        xt, vol_t = scale_returns(xt, ewma_var, mask)

        # Standard scale second moment matrix into correlation matrix
        mask_ix = np.ix_(mask, mask)
        mom_t = np.outer(xt, xt)
        ewma_mom[mask_ix] = lamda_cov * ewma_mom[mask_ix] + (1 - lamda_cov) * mom_t
        Ct, _ = scale_momentum(ewma_mom, mask_ix)

        if t < t_min:
            continue

        # Eigen decomposition to init F and D for EM
        Ft, dt = em_initialization(Ct, k_)
    
        # EM to regularize F and D after PCA
        if n >= k+1:
            Ft, dt = expectation_maximisation(Ft, dt, Ct)

        Ft = Ft * vol_t[:, None]
        dt = dt * vol_t**2

        F_cov[t, mask, :k_] = Ft
        d_var[t, mask]      = dt
        Sigma[t][mask_ix]   = Ft @ Ft.T + np.diag(dt)

    return F_cov, d_var, Sigma
