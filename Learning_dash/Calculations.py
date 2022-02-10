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
# domain size is from the CAD and in mm
# the +1 is because np.arange is an exclusive (ie: not inclusive) range
X = np.arange(0,427+1,1)
Y = np.arange(0,294+1,1)
Z = np.arange(0,168+1,1)
domain = tuple(np.meshgrid(X,Y,Z))


# DECLARING FUNCTION
def domain_interp(readings, domain):
    
    # SENSOR LOCATIONS
    # stored as coordinates [x,y,z]
    sensor_locs = np.array( [[ 60,  72,  49],
                             [ 60, 177,  49],
                             [140, 124,  97],
                             [140, 229,  97],
                             [220,  72,  49],
                             [220, 177,  49],
                             [300, 124,  97],
                             [300, 229,  97]] )
    
    # PLOTTING SENSOR LOCATIONS
    # fig_locs = go.Figure(data=[go.Scatter3d(x=sensor_locs[:,0], y=sensor_locs[:,1], z=sensor_locs[:,2], mode='markers')])
    # fig_locs.update_layout(scene={  'xaxis': {'nticks': 3, 'range': [0, np.max(domain[0])]},
    #                                 'yaxis': {'nticks': 3, 'range': [0, np.max(domain[1])]},
    #                                 'zaxis': {'nticks': 3, 'range': [0, np.max(domain[2])]}   })
    # fig_locs.write_html("sensor_locations.html")
    
    # SENSOR VALUES
    sensor_vals = np.array(readings).transpose()
    
    # INTERPOLATION
    interp_vals = griddata(sensor_locs, sensor_vals, domain, method='nearest')
    return interp_vals


# TESTING FUNCTIONS
result = domain_interp(readings, domain)


# PLOTTING INTERPOLATED FIELD
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
fig.write_html("volume.html")