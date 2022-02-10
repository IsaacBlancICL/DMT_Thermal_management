'''
example from: https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.griddata.html
playing around to get a feel for the function
'''

import numpy as np
from scipy.interpolate import griddata

def func(x, y):
    return x+y

grid_x, grid_y = np.mgrid[0:1:100j, 0:1:200j]

rng = np.random.default_rng()
points = rng.random((1000, 2))
values = func(points[:,0], points[:,1])

grid_z0 = griddata(points, values, (grid_x, grid_y), method='nearest')