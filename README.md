# CovForge

This library serves as a minimalistic tool to create risk models used for quantitative portfolio construction. It is part of an open software package presented in the paper: \ref{...}{...}. A risk model is a series of covariance matricies constructed from historical returns. Risk models can be constructed using many different methods. The three methods used in this project are: rolling window covariance, exponentially weighted moving average (EWMA), and iterated EWMA (IEWMA) factor model. 

## Risk averse strategies
Many simple investment strategies such as volatility control, minimum volatility, risk parity, and maximum diversification require access to a risk model. Using a risk averse strategy does however usually come at a cost of portfolio return and whether it is correct to use a risk averse strategy depends on your investment goals and risk appetite. Without a mechanism to protect against volatility much is left to chance and performance will fluctuate from year to year. Risk preserves much of its structure, meaning simple return histories can produce useful and practical estimates, without access to proprietary data. 


## Installation
```Bash
pip install covforge
```

## Example usage
```Python
import covforge as cf
import pandas as pd

return_data = pd.read_csv(".../return_data.csv")

# riskmodel
rm = cf.IEWMAFactorModel(
    k = 10,                 # num factors
    min_samples = 42,       # num days
    halflife_cov = 126,     # num days
    halflife_var = 42       # num days
)
rm.fit(return_data)

# access the covariance matrix series
rm.Sigma

# acces the decomposed version
rm.F_cov, rm.d_var  # Sigma = F_cov @ F_cov.T + np.diag(d_var)

# store the risk model
rm.save(filepath=".../risk_model.npz")

# load a risk model
rm = IEWMAFactorModel.load(filepath=".../risk_model.npz")
```

