'''
functions for inter/extrapolating temperature distribution throughout
PCM and using this to calculate useful things like solid volume fraction,
liquid volume fraction, state of charge etc...
'''


# IMPORTING LIBRARIES
import numpy as np
from scipy.interpolate import Rbf
import plotly.graph_objects as go


# DOMAIN
# domain size is from the CAD and in mm
# the +1 is because np.arange is an exclusive (ie: not inclusive) range
stepsize = 5
X,Y,Z = np.meshgrid(np.arange(0,427+1,stepsize), # domain X axis
                    np.arange(0,294+1,stepsize), # domain Y axis
                    np.arange(0,168+1,stepsize), # domain Z axis
                    indexing='ij')


# SENSOR LOCATIONS
x = np.array([60,  60, 140, 140, 220, 220, 300, 300])
y = np.array([72, 177, 124, 229,  72, 177, 124, 229])
z = np.array([49,  49,  97,  97,  49,  49,  97,  97])


# DEMO READINGS
readings = [95,55,76,25,47,97,52,94]
sensor_vals = np.array(readings).transpose()


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


# TESTING FUNCTIONS
interp_vals = domain_interp(X,Y,Z, x,y,z, sensor_vals)


# PLOTTING VOLUME
# interpolated field
fig1 = go.Figure(data=go.Volume(
    x=X.flatten(),
    y=Y.flatten(),
    z=Z.flatten(),
    value=interp_vals.flatten(),
    # formating options
    isomin=0,
    isomax=150,
    opacity=0.1, # needs to be small to see through all surfaces
    surface_count=17 # needs to be a large number for good volume rendering
    ))
# sensor locations
fig1.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='markers', marker={'color':'green'}))
# save the result
fig1.write_html("volume.html")


# PLOTTING PLANE
z_slice = 169 # this refers to the dimensional location
fig2 = go.Figure(data=go.Contour(
                                 x=X[:,0,0],
                                 y=Y[0,:,0],
                                 z=interp_vals[:,:,int(z_slice/stepsize)].transpose(), # not sure why you have to transpose this, but you do otherwise graph comes out reversed lol
                                 # formating options
                                 line_smoothing=0.85,
                                 contours={'coloring':'heatmap',
                                           'showlabels':True,
                                           'labelfont':{'color':'white'} }))
fig2.update_layout(xaxis_title="x position",
                   yaxis_title="y position")
fig2.write_html("plane.html")