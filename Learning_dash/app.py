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
import plotly.express as px
# dash libraries
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform


# DOMAIN
# domain size is from the CAD and in mm
# the +1 is because np.arange is an exclusive (ie: not inclusive) range
stepsize = 5
X,Y,Z = np.meshgrid(np.arange(0,427+1,stepsize), # domain X axis
                    np.arange(0,294+1,stepsize), # domain Y axis
                    np.arange(0,168+1,stepsize), # domain Z axis
                    indexing='ij')
# for colourplot
Z_slice = 0.5 # initial slice (as a fraction of full depth)
Z_total = len(Z[0,0,:])-1


# SENSOR LOCATIONS
x = np.array([60,  60, 140, 140, 220, 220, 300, 300])
y = np.array([72, 177, 124, 229,  72, 177, 124, 229])
z = np.array([49,  49,  97,  97,  49,  49,  97,  97])


# DATA SETUP
ser = serial.Serial('COM3', baudrate=9600, timeout=None)
df = pd.DataFrame(columns = ['Time', 'Sensor 1', 'Sensor 2', 'Sensor 3', 'Sensor 4', 'Sensor 5', 'Sensor 6', 'Sensor 7', 'Sensor 8', 'Solid fraction', 'Liquid fraction', 'Stored'])


# START THE APP
app = DashProxy(prevent_initial_callbacks=True, transforms=[MultiplexerTransform()], update_title=None, external_stylesheets=[dbc.themes.DARKLY])

# LAYOUT
app.layout = dbc.Container([
    # title and intro text
    dbc.Row(html.Br()),
    dbc.Row(dbc.Col(html.H1("Thermal management dashboard"),width=6)),
    dbc.Row(dbc.Col(html.P("The Arduino reads the 8 temperature sensors using the OneWire library and sends the values to my laptop via serial. A Python running on my laptop script recieves these values using Pyserial and inter/extrapolates the temperature field across the whole volume of PCM. This inter/extrapolation is done using the Rbf (radial basis function) method from scipy.interpolate. I won't say here what function Rbf is set to use, since it was a total guess and I'll likely change it once I try using the code on some real data. From this interpolated temperature field (which is just a big array of grid points), the script estimates the fractions of solid and liquid phase by volume (proportions of points below and above the fusion temperature), as well as the energy stored (not coded yet). The temperature sensor results and the subsequent calculated results are saved into a Pandas DataFrame, which is re-saved to a .csv file each time new data is added, for security. The temperature sensor readings, interpolated field and calculated results are all graphed below. Graphs were made with plotly.graph_objects and plotly.express. The graphs are somewhat interactive and automatically update each time new data is recieved from the Arduino. Currently, this is set to happen every 10 seconds, so the graphs are 'real-time' to within that period. This dashboard was made with Dash. All the libraries mentioned are Python, apart from the OneWire Arduino library."),width=12)),
    dbc.Row(html.Br()),
    dbc.Row(html.Br()),
    # first row titles
    dbc.Row([
        dbc.Col(html.H4("2D slice distribution", className='text-center'),width=6),
        dbc.Col(html.H4("3D volume distribution", className='text-center'),width=6)
        ]),
    # first row - colourplot and sensor temps line graph
    dbc.Row([
        # colourplot
        dbc.Col(
            [
            dcc.Slider(id='SLIDER_colourplot',
                       min=0,
                       max=1,
                       step=0.01,
                       value=Z_slice, # initial value
                       marks={0:'0mm', 0.25:'42mm', 0.50:'84mm', 0.75:'126mm', 1:'168mm'},
                       updatemode='drag'),
            dcc.Graph(id='FIGURE_colourplot', figure={})
            ],
            width=6),
        # 3D volume
        dbc.Col(
            dcc.Graph(id='FIGURE_volume', figure={}),
            width=6)
        ]),
    # gap
    dbc.Row(html.Br()),
    # second row titles
    dbc.Row([
        dbc.Col(html.H4("Sensor temperatures", className='text-center'),width=6),
        dbc.Col(html.H4("Phase volume fractions", className='text-center'),width=6)
        ]),
    # second row
    dbc.Row([
        # sensor temps line graph
        dbc.Col( dcc.Graph(id='FIGURE_temps_line', figure={}), width=6),
        # pie chart
        dbc.Col( dcc.Graph(id='FIGURE_pie', figure={}), width=6)
        ]),
    # interval for live updates
    dcc.Interval(id='INTERVAL', interval=9900) # fires a callback causing app to update every 'interval' milliseconds
], fluid=True)


# CALLBACKS (finish once I've got data coming into pandas ready to graph)    
# interval
@app.callback( [Output('FIGURE_colourplot', 'figure'),
                Output('FIGURE_volume', 'figure'),
                Output('FIGURE_temps_line', 'figure'),
                Output('FIGURE_pie', 'figure')],
                Input('INTERVAL', 'n_intervals') )
def update_general(n_intervals):
    # DATA
    # reading serial to list
    serialLine = ser.readline().decode('ascii').rstrip().split(',')
    sensor_list = [float(item) for item in serialLine]
    sensor_vals = np.array(sensor_list).transpose()
    # calculating stuff
    global interp_vals # because must be accessed by colourplot callback function
    interp_vals = calc.domain_interp(X,Y,Z, x,y,z, sensor_vals)
    calcs_list = calc.SoC(interp_vals)
    # putting calculation results in DataFrame
    df.loc[len(df.index)] = [time.strftime("%H:%M:%S", time.localtime())] + sensor_list + calcs_list
    # saving DataFrame to csv
    filename = 'filename.csv'
    df.to_csv(filename, index=False)
    
    # FIGURES
    # colourplot
    colourplot = go.Figure(data=go.Contour(
                                     x=X[:,0,0],
                                     y=Y[0,:,0],
                                     z=interp_vals[:,:,int(Z_slice*Z_total)].transpose(), # not sure why you have to transpose this, but you do otherwise graph comes out reversed lol
                                     # formating options
                                     line_smoothing=0.85,
                                     contours={'coloring':'heatmap',
                                               'showlabels':True,
                                               'labelfont':{'color':'white'} }))
    colourplot.update_layout(xaxis_title="x position",
                       yaxis_title="y position",
                       margin={'l':20, 'r':20, 't':5, 'b':20},
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       uirevision="Don't change")
    colourplot.update_xaxes(color='white',
                            linecolor='rgba(0,0,0,0)')
    colourplot.update_yaxes(color='white',
                            linecolor='rgba(0,0,0,0)')
    # volume
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
                                       'center': {'x':0,   'y':-0.2,'z':-0.2 },
                                       'eye':    {'x':1.5, 'y':1.5, 'z':0.4  }},
                         paper_bgcolor='rgba(0,0,0,0)',
                         plot_bgcolor='rgba(0,0,0,0)',
                         uirevision="Don't change")
    # temps line
    temps_line = px.line(df,
                         x="Time",
                         y=["Sensor 1","Sensor 2","Sensor 3","Sensor 4","Sensor 5","Sensor 6","Sensor 7","Sensor 8",])
    temps_line.update_layout(xaxis_title="Time",
                             yaxis_title="Temperature (deg C)",
                             margin={'l':20, 'r':20, 't':5, 'b':20},
                             paper_bgcolor='rgba(0,0,0,0)',
                             plot_bgcolor='rgba(0,0,0,0)',
                             legend={'title':None,
                                     'font':{'color':'white'},
                                     'y':0.5},
                             uirevision="Don't change")
    temps_line.update_xaxes(color='white',
                            showgrid=False)
    temps_line.update_yaxes(color='white',
                            showgrid=False)
    # pie
    pie = px.pie(values=df.iloc[-1][['Solid fraction','Liquid fraction']].tolist(),
                 names=['Solid fraction','Liquid fraction'],
                 color=['Solid fraction','Liquid fraction'],
                 color_discrete_map={'Solid fraction' :'#5A17A2',
                                     'Liquid fraction':'#F3C939'},
                 hole=0.4)
    pie.update_layout(showlegend=False,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')
    pie.update_traces(sort=False,
                      textposition='inside',
                      textinfo='percent+label',
                      hovertemplate=None,
                      hoverinfo='skip')
    
    # RETURN
    return colourplot, volume, temps_line, pie


# # colourplot z-position slider
@app.callback( Output('FIGURE_colourplot', 'figure'),
                Input('SLIDER_colourplot', 'value') )
def update_colourplot(value):
    # VARIABLE
    Z_slice = value
    
    # FIGURE
    # colourplot (copied from interval callback function - must be the same here!)
    colourplot = go.Figure(data=go.Contour(
                                      x=X[:,0,0],
                                      y=Y[0,:,0],
                                      z=interp_vals[:,:,int(Z_slice*Z_total)].transpose(), # not sure why you have to transpose this, but you do otherwise graph comes out reversed lol
                                      # formating options
                                      line_smoothing=0.85,
                                      contours={'coloring':'heatmap',
                                                'showlabels':True,
                                                'labelfont':{'color':'white'} }))
    colourplot.update_layout(xaxis_title="x position",
                        yaxis_title="y position",
                        margin={'l':20, 'r':20, 't':5, 'b':20},
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        uirevision="Don't change")
    colourplot.update_xaxes(color='white',
                            linecolor='rgba(0,0,0,0)')
    colourplot.update_yaxes(color='white',
                            linecolor='rgba(0,0,0,0)')
    
    # RETURN
    return colourplot
             



# RUNNING DASHBOARD
if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False)


# CLOSING SERIAL PORT
ser.close()