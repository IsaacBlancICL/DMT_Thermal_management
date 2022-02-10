'''
copied from https://plotly.com/python/3d-volume-plots/
trying to export to html, as described in https://plotly.com/python/interactive-html-export/

Figured it all out - see description of previous commit for details.
'''

import plotly.graph_objects as go
import numpy as np

X, Y, Z = np.mgrid[-8:8:40j, -8:8:40j, -8:8:40j]
values = np.sin(X*Y*Z) / (X*Y*Z)

fig = go.Figure(data=go.Volume(
    x=X.flatten(),
    y=Y.flatten(),
    z=Z.flatten(),
    value=values.flatten(),
    isomin=0.1,
    isomax=0.8,
    opacity=0.1, # needs to be small to see through all surfaces
    surface_count=17, # needs to be a large number for good volume rendering
    ))

fig.write_html("volume.html")