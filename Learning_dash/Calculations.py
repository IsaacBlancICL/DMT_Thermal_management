'''
functions for inter/extrapolating temperature distribution throughout
PCM and using this to calculate useful things like solid volume fraction,
liquid volume fraction, state of charge etc...
'''


# IMPORTING LIBRARIES
import numpy as np
from scipy.interpolate import griddata
import plotly.graph_objects as go


# MAKING DEMO READINGS
readings = [4,5,7,2,4,6,5,7]


# MAKING DOMAIN
# domain size is from the CAD and in cm (rounded)
# the +1 is because np.arange is an exclusive (ie: not inclusive) range
X = np.arange(0,43+1,1)
Y = np.arange(0,29+1,1)
Z = np.arange(0,17+1,1)
domain = tuple(np.meshgrid(X,Y,Z))


# SENSOR LOCATIONS
# stored as coordinates [x,y,z]
sensor_locs = np.array( [[ 6,  7,  5],
                         [ 6, 18,  5],
                         [14, 12,  10],
                         [14, 23,  10],
                         [22,  7,  5],
                         [22, 18,  5],
                         [30, 12,  10],
                         [30, 23,  10]] )


# DECLARING FUNCTIONS
def domain_interp(domain, sensor_locs, readings):
    # sensor values
    sensor_vals = np.array(readings).transpose()
    # interpolation
    interp_vals = griddata(sensor_locs, sensor_vals, domain, method='nearest')
    return interp_vals


# TESTING FUNCTIONS
result = domain_interp(domain, sensor_locs, readings)


# PLOTTING
# interpolated field
fig = go.Figure(data=go.Volume(
    x=domain[0].flatten(),
    y=domain[1].flatten(),
    z=domain[2].flatten(),
    value=result.flatten(),
    isomin=0,
    isomax=10,
    opacity=0.1, # needs to be small to see through all surfaces
    surface_count=17, # needs to be a large number for good volume rendering
    ))
# sensor locations
fig.add_trace(go.Scatter3d(x=sensor_locs[:,0], y=sensor_locs[:,1], z=sensor_locs[:,2], mode='markers', marker={'color':'green'}))
# save the result
fig.write_html("volume.html")