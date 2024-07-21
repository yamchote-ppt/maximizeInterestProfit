This project is motivated by a post from facebook page "เนิร์ดไฟแนนซ์" (https://www.facebook.com/permalink.php?story_fbid=pfbid07yUMyLABLprkQaSu8KStBH4KqruovKSXYr22HWb8HRXLLeJugTXvmMqxZNPSEjvol&id=61558121405445)

The aim is to maximize the interest profit from portfolio where each asset is stepwise interest rate.

# How to use

1. Define a dictionary of interest rate as `{bankName: ([rate(1), rate(2), ..., rate(k+1)],[bound(1), bound(2), ..., bound(k)])}` where the interest rate of the given bank is `rate(i)` for the amount of money in the interval `(bound(i-1), bound(i))` where `bound(0)` is 0.
For example, `inputDict = {
    'LH':([0.0025, 0.0175,0.0555,0.015,0.0025,0],[100000, 900000, 1000000, 3000000, 100000000]),
    'KPP':([0.02,0.04,0.02,0.0155,0.005],[5000,10000,50000,1500000]),
    'Dime':([0.03,0.015,0.005],[10000,1000000]),
    'CIMBChill': ([0.005,0.018,0.0288,0.002],[10000,50000,100000]),
    'Kept':([0.0175],[]),
    'TTB':([0.022,0.016,0.012],[100000,1000000]),
    'Alpha':([0.02,0.007],[500000]),
    'CIMBSpeed':([0.008,0.0188],[100000]),
}`

2. 