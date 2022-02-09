# learning how interpn function works
# example from: https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interpn.html

# importing libraries
from scipy.interpolate import interpn
import numpy as np

# creating 3D space
x = np.linspace(0, 4, 5)
y = np.linspace(0, 5, 6)
z = np.linspace(0, 6, 7)
points = (x, y, z)

# creating values in that space
def value_func_3d(x, y, z):
    return 2 * x + 3 * y - z
values = value_func_3d(*np.meshgrid(*points, indexing='ij'))

# using interpn function
point = np.array([2.21, 3.12, 1.15])
print(interpn(points, values, point))