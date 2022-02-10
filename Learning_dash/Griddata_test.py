'''
example from: https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.griddata.html
playing around to get a feel for the function
'''

import numpy as np
from scipy.interpolate import griddata

def func(x, y, z):
    return x+y+z

x = np.linspace(0,1,100)
y = np.linspace(0,1,100)
z = np.linspace(0,1,100)

grid_x, grid_y, grid_z = np.meshgrid(x,y,z)

rng = np.random.default_rng()
points = rng.random((1000, 3))
values = func(points[:,0], points[:,1], points[:,2])

grid = griddata(points, values, (grid_x, grid_y, grid_z), method='nearest')