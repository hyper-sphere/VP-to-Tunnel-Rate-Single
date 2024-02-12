## Apparently the smoothing function can be obtain using the savgol filter, as per chris
from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.signal import savgol_filter as savgol
import numpy as np





# def smooth(z, w):
#     if w <= 0 or w > len(z):
#         raise ValueError("Window size must be positive and less than or equal to the length of the data.")

#     if w == 1:  # No smoothing needed for window size 1
#         return z

#     # Prepare the window; no need for two separate convolutions
#     window = np.ones(w) / w

#     # Apply convolution
#     zSmooth = np.convolve(z, window, 'same')

#     return zSmooth



def smooth(z, w): 
    
    padding = np.full(w-1, np.nan)
    
    # Moving Average with Right NaNs
    zLeft  = np.convolve(z, np.ones(w), 'valid') / w
    zLeft  = np.append( zLeft, padding )
    
    # Moving Average with Left NaNs
    zRight = np.convolve( np.flip(z), np.ones(w), 'valid') / w
    zRight = np.append( zRight, padding )
    zRight = np.flip(zRight)
  
    zSmooth = (zLeft + zRight)/2
    
    return zSmooth



def baseline(y, lam, p, niter=10):
    L = len(y)
    D = sparse.diags([1,-2,1],[0,-1,-2], shape=(L,L-2))
    w = np.ones(L)
    for i in range(niter):
        W = sparse.spdiags(w, 0, L, L)
        Z = W + lam * D.dot(D.transpose())
        z = spsolve(Z, w*y)
        w = p * (y > z) + (1-p) * (y < z)
    return z





















