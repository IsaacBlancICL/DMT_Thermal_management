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
scale = 5 # used to reduce the number of points in the domain
X = np.arange(0,427+1,scale)
Y = np.arange(0,294+1,scale)
Z = np.arange(0,168+1,scale)
domain = tuple(np.meshgrid(X,Y,Z))


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


# DECLARING FUNCTIONS
def domain_interp(domain, sensor_locs, readings):
    # sensor values
    sensor_vals = np.array(readings).transpose()
    # interpolation
    interp_vals = griddata(sensor_locs, sensor_vals, domain, method='linear')
    return interp_vals

def phase_fractions(interp_vals):
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
    # return fractions
    return solid_frac, liquid_frac


# TESTING FUNCTIONS
result = domain_interp(domain, sensor_locs, readings)


# PLOTTING VOLUME
# interpolated field
fig1 = go.Figure(data=go.Volume(
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
fig1.add_trace(go.Scatter3d(x=sensor_locs[:,0], y=sensor_locs[:,1], z=sensor_locs[:,2], mode='markers', marker={'color':'green'}))
# save the result
fig1.write_html("volume.html")


# PLOTTING PLANE
z_slice = int(65/scale)
fig2 = go.Figure(data=go.Heatmap(x=domain[0][0,:,0], y=domain[1][:,0,0], z=result[:,:,z_slice], zsmooth='best'))
fig2.write_html("plane.html")