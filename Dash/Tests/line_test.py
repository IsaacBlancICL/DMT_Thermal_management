import pandas as pd
import plotly.express as px


df = pd.read_csv('filename.csv')


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
temps_line.update_xaxes(color='white')
temps_line.update_yaxes(color='white')


temps_line.write_html('line.html')