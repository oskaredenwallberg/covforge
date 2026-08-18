import numpy as np
import pandas as pd
from covforge.modules.factor import covariance_factor_iewma
from covforge.modules.simple import covariance_rolling_window, covariance_ewma

# abstract base class
class RiskModel:
    def __init__(self):
        self.Sigma: np.ndarray = None
        self.assets: np.ndarray = None
        self.timeline: pd.DatetimeIndex = None

    def fit(self, ret_d: pd.DataFrame) -> None:
        raise NotImplementedError

    def save(self, filepath: str):
        state = self.__getstate__()
        np.savez(filepath, **state, allow_pickle=True)

    @classmethod
    def load(cls, filepath: str):
        data = np.load(filepath, allow_pickle=True)
        state = { k: v.item() if v.ndim == 0 else v for k, v in data.items() }
        rm = cls.__new__(cls)
        rm.__dict__.update(state)
        return rm


class RollingWindowModel(RiskModel):
    def __init__(
            self,
            lookback: int,
            ):
        super().__init__()
        self.l = lookback

    def fit(self, ret_d: pd.DataFrame):
        self.Sigma = covariance_rolling_window(
            Xx=ret_d.to_numpy(), 
            l=self.l
        )
        self.assets = ret_d.columns
        self.timeline = ret_d.index


class EWMAModel(RiskModel):
    def __init__(
            self,
            min_samples: int,
            halflife: int,
            ):
        super().__init__()
        self.t_min = min_samples
        self.h = halflife

    def fit(self, ret_d: pd.DataFrame):
        self.Sigma = covariance_ewma(
            Xx=ret_d.to_numpy(), 
            t_min=self.t_min,
            h=self.h
        )
        self.assets = ret_d.columns
        self.timeline = ret_d.index


class GARCH(RiskModel):
    ...


class IEWMAFactorModel(RiskModel):
    def __init__(
            self,
            k: int,             # 10
            min_samples: int,   # 126
            halflife_cov: int,  # 126
            halflife_var: int,  # 42
        ):
        self.k = k
        self.t_min = min_samples
        self.h_cov = halflife_cov
        self.h_var = halflife_var

        self.F_cov = None
        self.d_var = None

    def fit(self, ret_d: pd.DataFrame):
        F_cov, d_var, Sigma = covariance_factor_iewma(
            Xx=ret_d.to_numpy(),
            k=self.k,
            t_min=self.t_min,
            h_cov=self.h_cov,
            h_var=self.h_var,
        )
        super().__init__()
        self.F_cov = F_cov
        self.d_var = d_var
        self.Sigma = Sigma
        self.assets = ret_d.columns.to_numpy()
        self.timeline = ret_d.index.to_numpy()
