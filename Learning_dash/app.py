# copied from tutorial: https://dash.plotly.com/layout
# run the code and go to http://127.0.0.1:8050/ in your web browser.


# IMPORTING LIBRARIES
# data handling libraries
import pandas as pd
# figure making libraries
import plotly.graph_objects as go
import plotly.express as px
# dash libraries
from dash import Dash, html, dcc
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc


# START THE APP
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])


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
        # sensor temps line graph
        dbc.Col(
            [
            dcc.Dropdown(id='DROPDOWN_temps_line', options=['Sensor 1', 'Sensor 2', 'Sensor 3', 'Sensor 4', 'Sensor 5', 'Sensor 6', 'Sensor 7', 'Sensor 8'], value=[], multi=True, placeholder="Select which temperature sensors you want to view data for..."),
            dcc.Graph(id='FIGURE_temps_line', figure={})
            ],
            width=6)
        ])
    # second row - pie chart - to be done later
    # dbc.Row([])
], fluid=True)


# CALLBACKS


             
# RUNNING DASHBOARD
if __name__ == '__main__':
    app.run_server(debug=True)