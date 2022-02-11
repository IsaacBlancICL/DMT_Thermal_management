# copied from tutorial: https://dash.plotly.com/layout
# run the code and go to http://127.0.0.1:8050/ in your web browser.


# IMPORTING LIBRARIES
# data handling libraries
import numpy as np
import pandas as pd
import serial
import time
# calculations Python file
import Calculations as calc
# figure making libraries
import plotly.graph_objects as go
# dash libraries
from dash import Dash, html, dcc
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate


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


# DATA SETUP
ser = serial.Serial('COM3', baudrate=9600, timeout=None)
df = pd.DataFrame(columns = ['Time', 'Sensor 1', 'Sensor 2', 'Sensor 3', 'Sensor 4', 'Sensor 5', 'Sensor 6', 'Sensor 7', 'Sensor 8', 'Solid fraction', 'Liquid fraction', 'Stored'])

# START THE APP
app = Dash(__name__, update_title=None, external_stylesheets=[dbc.themes.DARKLY]) # maybe change to FLATLY?


# LAYOUT
app.layout = dbc.Container([
    # title and intro text
    dbc.Row(html.Br()),
    dbc.Row(dbc.Col(html.H1("Thermal management dashboard"),width=6)),
    dbc.Row(dbc.Col(html.P("This is very much a work-in-progress, but I'm hoping to have lots of nice graphs here. For now, I want a colourplot with a slider for adjusting depth, a multi-series line graph where you can choose which sensors to look at, and a pie chart for phase fractions. Also maybe another line graph showing history of phase fractions. Maybe also some state of charge estimation."),width=6)),
    dbc.Row(html.Br()),
    # first row - colourplot and sensor temps line graph
    dbc.Row([
        # colourplot
        dbc.Col(
            [
            dcc.Slider(id='SLIDER_colourplot', min=0, max=100, step=1, value=50, marks={0:'0mm', 25:'42mm', 50:'84mm', 75:'126mm', 100:'168mm'}),
            dcc.Graph(id='FIGURE_colourplot', figure={})
            ],
            width=6),
        # 3D volume (not done yet)
        ]),
    # gap
    dbc.Row(html.Br()),
    # second row
    dbc.Row([
        # sensor temps line graph
        dbc.Col(
            [
            dcc.Dropdown(id='DROPDOWN_temps_line', options=['Sensor 1', 'Sensor 2', 'Sensor 3', 'Sensor 4', 'Sensor 5', 'Sensor 6', 'Sensor 7', 'Sensor 8'], value=[], multi=True, placeholder="Select which temperature sensors you want to view data for..."),
            dcc.Graph(id='FIGURE_temps_line', figure={})
            ],
            width=6)
        # pie chart (not done yet)
        ]),
    # interval for live updates
    dcc.Interval(id='INTERVAL', interval=1900) # fires a callback causing app to update every 'interval' milliseconds
], fluid=True)


# CALLBACKS (finish once I've got data coming into pandas ready to graph)    
# colourplot
@app.callback(
    Output('FIGURE_colourplot', 'figure'),
    Input('SLIDER_colourplot', 'value')
)
def update_graph(value):
    # serial
    serialLine = ser.readline().decode('ascii').rstrip().split(',')
    sensor_list = list(map(int,serialLine))
    sensor_vals = np.array(sensor_list).transpose()
    # interp
    interp_vals = calc.domain_interp(X,Y,Z, x,y,z, sensor_vals)
    # figure
    fig = go.Figure(data=go.Contour(
                                     x=X[:,0,0],
                                     y=Y[0,:,0],
                                     z=interp_vals[:,:,int(value/stepsize)].transpose(), # not sure why you have to transpose this, but you do otherwise graph comes out reversed lol
                                     # formating options
                                     line_smoothing=0.85,
                                     contours={'coloring':'heatmap',
                                               'showlabels':True,
                                               'labelfont':{'color':'white'} }))
    fig.update_layout(xaxis_title="x position",
                       yaxis_title="y position")
    return fig

             
# RUNNING DASHBOARD
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)