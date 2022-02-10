'''
example from: https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.griddata.html
playing around to get a feel for the function
'''

import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def func(x, y, z):
    return x+y+z

x = np.linspace(0,1,40)
y = np.linspace(0,1,40)
z = np.linspace(0,1,40)

grid_x, grid_y, grid_z = np.meshgrid(x,y,z)

rng = np.random.default_rng()
points = rng.random((100, 3))
values = func(points[:,0], points[:,1], points[:,2])

interp_values = griddata(points, values, (grid_x, grid_y, grid_z), method='nearest')


# plotting data points in 3D graph
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(points[:,0], points[:,1], points[:,2])


# plotting interpolated field in 3D graph
fig = go.Figure(data=go.Volume(
    x=grid_x.flatten(),
    y=grid_y.flatten(),
    z=grid_z.flatten(),
    value=interp_values.flatten(),
    isomin=0,
    isomax=3,
    opacity=0.1, # needs to be small to see through all surfaces
    surface_count=17, # needs to be a large number for good volume rendering
    ))

fig.write_html("volume.html")