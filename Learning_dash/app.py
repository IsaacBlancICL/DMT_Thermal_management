# copied from tutorial: https://dash.plotly.com/layout
# run the code and go to http://127.0.0.1:8050/ in your web browser.


# IMPORTING LIBRARIES
from dash import Dash, html, dcc
import plotly.graph_objects as go


# CREATING DATA AND FIGURE
fig = go.Figure(data =
    go.Contour(
        z=[[10, 10.625, 12.5, 15.625, 20],
           [5.625, 6.25, 8.125, 11.25, 15.625],
           [2.5, 3.125, 5., 8.125, 12.5],
           [0.625, 1.25, 3.125, 6.25, 10.625],
           [0, 0.625, 2.5, 5.625, 10]]
    ))
fig.show()


# MAKING DASHBOARD
app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

             
# RUNNING DASHBOARD
if __name__ == '__main__':
    app.run_server(debug=True)