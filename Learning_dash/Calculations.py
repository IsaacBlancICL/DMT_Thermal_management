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


# DECLARING FUNCTION
def domain_interp(readings):
    
    # DOMAIN
    # domain size is from the CAD and in mm
    X = np.arange(0,427,1)
    Y = np.arange(0,294,1)
    Z = np.arange(0,168,1)
    X,Y,Z = np.meshgrid(X,Y,Z)
    
    # SENSORS
    # locations for all 8 sensors stored as coordinates [x,y,z]
    sensor_locs = np.array( [[ 60,  72,  49],
                             [ 60, 177,  49],
                             [140, 124,  97],
                             [140, 229,  97],
                             [220,  72,  49],
                             [220, 177,  49],
                             [300, 124,  97],
                             [300, 229,  97]] )
    # values from all 8 sensors
    sensor_vals = np.array(readings).transpose()
    
    # PLOTTING SENSOR LOCATIONS
    fig_locs = go.Figure(data=[go.Scatter3d(x=sensor_locs[:,0], y=sensor_locs[:,1], z=sensor_locs[:,2], mode='markers')])
    fig_locs.update_layout(scene={  'xaxis': {'nticks': 3, 'range': [0, 427]},
                                    'yaxis': {'nticks': 3, 'range': [0, 294]},
                                    'zaxis': {'nticks': 3, 'range': [0, 168]}   })
    fig_locs.write_html("sensor_locations.html")
    
    # INTERPOLATION
    interp_vals = griddata(sensor_locs, sensor_vals, (X,Y,Z), method='nearest')
    
    return interp_vals

# TESTING FUNCTIONS
result = domain_interp(readings)