import numpy as np


# from:
#   https://stackoverflow.com/questions/12269834/is-there-any-numpy-autocorrellation-function-with-standardized-output
def autocorr(x):
    x = x.flatten()
    res = np.correlate(x, x, mode='full')
    max_corr = np.argmax(res)
    res = res / res[max_corr]
    return res[round(res.size / 2):]
