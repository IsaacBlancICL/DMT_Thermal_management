'''
functions for inter/extrapolating temperature distribution throughout
PCM and using this to calculate useful things like solid volume fraction,
liquid volume fraction, state of charge etc...
'''


# IMPORTING LIBRARIES
import numpy as np
from scipy.interpolate import Rbf
import plotly.graph_objects as go


# MAKING DEMO READINGS
readings = [4,5,7,2,4,6,5,7]


# MAKING DOMAIN
# domain size is from the CAD and in mm
# the +1 is because np.arange is an exclusive (ie: not inclusive) range
stepsize = 5 # used to reduce the number of points in the domain
X = np.arange(0,427+1,stepsize)
Y = np.arange(0,294+1,stepsize)
Z = np.arange(0,168+1,stepsize)
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
    rbf = Rbf(sensor_locs[:,0],
              sensor_locs[:,1],
              sensor_locs[:,2],
              sensor_vals)
    interp_vals = rbf(domain[0].flatten(),
                      domain[1].flatten(),
                      domain[2].flatten())
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


# TESTING FUNCTIONS
result = domain_interp(domain, sensor_locs, readings)


# # PLOTTING VOLUME
# # interpolated field
# fig1 = go.Figure(data=go.Volume(
#     x=domain[0].flatten(),
#     y=domain[1].flatten(),
#     z=domain[2].flatten(),
#     value=result.flatten(),
#     isomin=0,
#     isomax=10,
#     opacity=0.1, # needs to be small to see through all surfaces
#     surface_count=17, # needs to be a large number for good volume rendering
#     ))
# # sensor locations
# fig1.add_trace(go.Scatter3d(x=sensor_locs[:,0], y=sensor_locs[:,1], z=sensor_locs[:,2], mode='markers', marker={'color':'green'}))
# # save the result
# fig1.write_html("volume.html")


# # PLOTTING PLANE
# z_slice = 30 # note that this refers to slice index, not to dimensional location
# fig2 = go.Figure(data=go.Heatmap(x=domain[0][0,:,0], y=domain[1][:,0,0], z=result[:,:,z_slice], zsmooth='best'))
# fig2.write_html("plane.html")