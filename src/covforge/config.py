FIRST_DATE     = "1954-01-03"  # first date
FINAL_DATE     = "2026-03-25"  # final date
FIRST_DATE_BTC = "2017-09-07"  # according to Kasper's paper
AUTO_ADJUST = True

D0 = "2005-01-03"
D1 = "2024-12-31"

sbg  = ["SPY", "AGG", "GLD"]
indx = ["SPY", "QQQ", "VTV", "VUG", "MDY", "IWM", "IWD", "SCHD", "USMV", "QUAL"]  # market
bond = ["AGG", "TLT", "IEF", "TIP", "LQD", "LQDH", "HYG", "MUB", "BNDX", "EMB", "IAGG", "VWOB"]  # bonds
sect = ["XLK", "XLV", "XLF", "XLY", "XLI", "XLP", "XLE", "XLU", "XLB", "IBB", "IYR"]  # sectors
intn = ["EWJ", "EWG", "EWU", "EWA", "EWH", "EWS", "EWZ", "EWT", "EWY", "EWP", "EWW", "EWI", "EWD", "EWL", "EWC"]  # international "EEM"
comd = ["GLD", "SLV", "CPER", "USO", "UGA", "CORN", "WEAT", "SOYB", "CANE"]  # commodities COTN.L, "DBC", "DBA", 
extr = []
# metl = ["GLD", "SLV", "CPER"]  # precious metals  "DBB"
# crpt = ["BTC-USD"]  # crypto
universe = sorted([*indx, *sect, *intn, *bond, *comd, *extr])

# Time periods
_1W   = 5
_2W   = 10
_4W   = _1M  = 21
_12W  = _3M  = _1Q  = 63
_26W  = _6M  = _2Q  = 126
_52W  = _12M = _4Q  = _1Y = 252
_104W = _24M = _8Q  = _2Y = 504
_156W = _36M = _12Q = _3Y = 756
