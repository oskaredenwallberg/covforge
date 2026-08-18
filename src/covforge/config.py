FIRST_DATE     = "1954-01-03"  # first date
FINAL_DATE     = "2026-03-25"  # final date
FIRST_DATE_CRYPTO =  "2017-09-07"  # according to Kasper's paper
AUTO_ADJUST = True

D0 = "2005-01-03"
D1 = "2024-12-31"

# Equity (Eq.)
mrkt = ["SPY", "QQQ", "VTV", "VUG", "MDY", "IWM", "SCHD", "USMV", "QUAL"]
sect = ["XLK","XLV","XLF","XLY","XLI","XLP","XLE","XLU","XLB","IBB","IYR"]
ctry = ["EWJ", "EWG", "EWU", "EWA", "EWH", "EWS", "EWZ", "EWT", "EWY", "EWP", "EWW", "EWI", "EWD", "EWL", "EWC"]
eqty = [*mrkt, *sect, *ctry]

# Fixed Income (FI)
govm = ["AGG","TLT","IEF","TIP","MUB"]
corp = ["LQD","LQDH","HYG"]
glob = ["BNDX","EMB","IAGG","VWOB"]
fixd = [*govm, *corp, *glob]

# Alternatives (Alt.)
phys = ["GLD", "SLV", "PPLT"]
futr = ["CPER", "USO", "UGA", "CORN", "WEAT", "SOYB", "CANE"]
cryp = ["BTC-USD", "ETH-USD"]
alts = [*phys, *futr, *cryp]

universe = sorted([*mrkt, *sect, *ctry, *govm, *corp, *glob, *phys, *futr, *cryp])

# Time periods
_1W = 5
_2W = 10
_3W = 15
_1M = 21
_2M = 42
_3M = _1Q = 63
_6M = _2Q = 126
_1Y = 252
_2Y = 504
_3Y = 756

EPS = 1e-8
