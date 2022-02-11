'''
functions for inter/extrapolating temperature distribution throughout
PCM and using this to calculate useful things like solid volume fraction,
liquid volume fraction, state of charge etc...
'''


# IMPORTING LIBRARIES
import numpy as np
from scipy.interpolate import Rbf


# DECLARING FUNCTIONS
def domain_interp(X,Y,Z, x,y,z, sensor_vals):
    rbf = Rbf(x,y,z,sensor_vals)
    interp_vals = rbf(X,Y,Z)
    return interp_vals

def SoC(interp_vals):
    # temperature of fusion
    t_fusion = 74
    # total number of points in domain
    total_parts  = np.prod(np.shape(interp_vals))
    # liquid phase
    liquid_parts = np.count_nonzero(interp_vals > t_fusion)
    liquid_frac  = liquid_parts/total_parts
    # solid phase
    solid_parts  = np.count_nonzero(interp_vals < t_fusion)
    solid_frac   = solid_parts/total_parts
    # energy stored (not done yet)
    stored = 1000
    # return values
    return [solid_frac, liquid_frac, stored]