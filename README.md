import covforge as cf
import pandas as pd

rd = pd.read_csv("./data/return/return_d.csv").set_index("Date")
k = 10
t_min = 42
h_cov = 126
h_var = 42

rm_fctr = cf.IEWMAFactorModel(k, t_min, h_cov, h_var)
rm_fctr.fit(rd)

path = "./data/test.npz"
rm_fctr.save(path)
rm_new = cf.IEWMAFactorModel.load(path)