This project is motivated by a post from facebook page "เนิร์ดไฟแนนซ์" (https://www.facebook.com/permalink.php?story_fbid=pfbid07yUMyLABLprkQaSu8KStBH4KqruovKSXYr22HWb8HRXLLeJugTXvmMqxZNPSEjvol&id=61558121405445)

The aim is to maximize the interest profit from portfolio where each asset is stepwise interest rate.

# How to use

1. Define a dictionary of interest rate as `{bankName: ([rate(1), rate(2), ..., rate(k+1)],[bound(1), bound(2), ..., bound(k)])}` where the interest rate of the given bank is `rate(i)` for the amount of money in the interval `(bound(i-1), bound(i))` where `bound(0)` is 0.