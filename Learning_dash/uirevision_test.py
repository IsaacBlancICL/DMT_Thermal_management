'''
copied from: https://iotespresso.com/preserving-zoom-settings-across-data-refresh-in-dash/
'''


#Callback to update the line-graph
@app.callback(Output('plot', 'figure'),
              [Input('intermediate-value', 'children')])
def update_realtime_fig(json1):
    df_go = pd.read_json(json1, orient='split').tail(500)
    fig = make_subplots()
    fig.add_trace(go.Scatter(x=df_go['time'], y=df_go['rate'],
                        mode='lines+markers',
                        name='Devices'))
    fig.update_layout(
        title_text="Rate in last 100 readings", uirevision="Don't change"
    )
    fig.update_yaxes(title_text="Rate", secondary_y=False)
    return fig