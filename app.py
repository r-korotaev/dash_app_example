
# coding: utf-8

# In[6]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

df = pd.read_csv('nama_10_gdp_1_Data.csv')
df = df[~df['GEO'].str.contains('Euro')]
df = df.drop(['Flag and Footnotes'], axis=1)


available_indicators = df['NA_ITEM'].unique()
countries = df['GEO'].unique()

app.layout = html.Div([
                       html.Div([
                                 
                                 html.Div([
                                           dcc.Dropdown(
                                                        id='crossfilter-xaxis-column',
                                                        options=[{'label': i, 'value': i} for i in available_indicators],
                                                        value='Gross domestic product at market prices'
                                                        ),
                                           dcc.RadioItems(
                                                          id='crossfilter-xaxis-type',
                                                          options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                                                          value='Linear',
                                                          labelStyle={'display': 'inline-block'}
                                                          )
                                           ],
                                          style={'width': '49%', 'display': 'inline-block'}),
                                 
                                 html.Div([
                                           dcc.Dropdown(
                                                        id='crossfilter-yaxis-column',
                                                        options=[{'label': i, 'value': i} for i in available_indicators],
                                                        value='Value added, gross'
                                                        ),
                                           dcc.RadioItems(
                                                          id='crossfilter-yaxis-type',
                                                          options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                                                          value='Linear',
                                                          labelStyle={'display': 'inline-block'}
                                                          )
                                           ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
                                 ], style={
                                'borderBottom': 'thin lightgrey solid',
                                'backgroundColor': 'rgb(250, 250, 250)',
                                'padding': '10px 5px'
                                }),
                       
                       html.Div([
                                 dcc.Graph(
                                           id='crossfilter-indicator-scatter',
                                           hoverData={'points': [{'customdata': 'Spain'}]}
                                           )
                                 ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
                       html.Div([
                                 dcc.Graph(id='x-time-series'),
                                 dcc.Graph(id='y-time-series'),
                                 ], style={'display': 'inline-block', 'width': '49%'}),
                       
                       html.Div(dcc.Slider(
                                           id='crossfilter-year--slider',
                                           min=df['TIME'].min(),
                                           max=df['TIME'].max(),
                                           value=df['TIME'].max(),
                                           marks={str(year): str(year) for year in df['TIME'].unique()}
                                           ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
                       ])


@app.callback(
              dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
              [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
               dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
               dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
               dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
               dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
                            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
                            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
                            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
                            customdata=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
                            mode='markers',
                            marker={
                            'size': 15,
                            'opacity': 0.5,
                            'line': {'width': 0.5, 'color': 'white'}
                            }
                            )],
                            'layout': go.Layout(
                                                xaxis={
                                                'title': xaxis_column_name,
                                                'type': 'linear' if xaxis_type == 'Linear' else 'log'
                                                },
                                                yaxis={
                                                'title': yaxis_column_name,
                                                'type': 'linear' if yaxis_type == 'Linear' else 'log'
                                                },
                                                margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
                                                height=450,
                                                hovermode='closest'
                                                )
                 }


def create_time_series(dff, axis_type, title):
    return {
        'data': [go.Scatter(
                            x=dff['TIME'],
                            y=dff['Value'],
                            mode='lines+markers'
                            )],
                            'layout': {
                                'height': 225,
                                    'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
                                        'annotations': [{
                                                        'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                                                        'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                                                        'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                                                        'text': title
                                                        }],
                                            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
                                                'xaxis': {'showgrid': False}
    }
}


@app.callback(
              dash.dependencies.Output('x-time-series', 'figure'),
              [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
               dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
               dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['GEO'] == country_name]
    dff = dff[dff['NA_ITEM'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)


@app.callback(
              dash.dependencies.Output('y-time-series', 'figure'),
              [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
               dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
               dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = df[df['GEO'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['NA_ITEM'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)


if __name__ == '__main__':
    app.run_server()
