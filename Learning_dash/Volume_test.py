'''
copied from https://plotly.com/python/3d-volume-plots/
trying to export to html, as described in https://plotly.com/python/interactive-html-export/

Figured it all out - see description of previous commit for details.
'''

import plotly.graph_objects as go
import numpy as np
import Calculations as calc

# DOMAIN
# domain size is from the CAD and in mm
# the +1 is because np.arange is an exclusive (ie: not inclusive) range
stepsize = 5
X,Y,Z = np.meshgrid(np.arange(0,427+1,stepsize), # domain X axis
                    np.arange(0,294+1,stepsize), # domain Y axis
                    np.arange(0,168+1,stepsize), # domain Z axis
                    indexing='ij')
# initial z_slice (for colourplot)
z_slice = 84


# SENSOR LOCATIONS
x = np.array([60,  60, 140, 140, 220, 220, 300, 300])
y = np.array([72, 177, 124, 229,  72, 177, 124, 229])
z = np.array([49,  49,  97,  97,  49,  49,  97,  97])


# DATA
sensor_vals = [76,45,67,78,81,45,67,92]
interp_vals = calc.domain_interp(X,Y,Z, x,y,z, sensor_vals)


# FIGURE
volume = go.Figure(data=go.Volume(
    x=X.flatten(),
    y=Y.flatten(),
    z=Z.flatten(),
    value=interp_vals.flatten(),
    # formating options
    isomin=0,
    isomax=150,
    opacity=0.1, # needs to be small to see through all surfaces
    surface_count=5 # needs to be a large number for good volume rendering
    ))
volume.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='markers', marker={'color':'green'}))
volume.update_layout(margin={'l':10, 'r':10, 't':5, 'b':5},
                     scene_camera={'up':     {'x':0,   'y':0,   'z':1    },
                                   'center': {'x':0,   'y':-0.2,'z':-0.1 },
                                   'eye':    {'x':1.5, 'y':1.5, 'z':0.4  }},
                     uirevision="Don't change")

volume.write_html("volume.html")