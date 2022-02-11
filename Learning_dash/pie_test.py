import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('filename.csv')

pie = go.Figure(data=go.Pie(
    labels=['Solid fraction','Liquid fraction'],
    values=df.iloc[-1][['Solid fraction','Liquid fraction']].tolist(),
    title='Volumetric phase fractions',
    # color_discrete_map={'Solid fraction' :'rgba(90,23,162,255)',
    #                     'Liquid fraction':'rgba(243,201,57,255)'},
    hole=0.4))

pie.write_html('pie.html')