import pandas as pd
import plotly.express as px

df = pd.read_csv('filename.csv')

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

pie.write_html('pie.html')