
# coding: utf-8

# In[6]:


import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv('nama_10_gdp_1_Data.csv')
df = df[~df['GEO'].str.contains('Euro')]
df = df.drop(['Flag and Footnotes'], axis=1)

app = dash.Dash(__name__)
    server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

available_indicators = df['NA_ITEM'].unique()
countries = df['GEO'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='a_xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
            dcc.RadioItems(
                id='a_xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='a_yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Value added, gross'
            ),
            dcc.RadioItems(
                id='a_yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='a_indicator-graphic'),

    dcc.Slider(
        id='a_year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    ),
    
    html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='b_country',
                options=[{'label': i, 'value': i} for i in countries],
                value='Spain'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='b_yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Value added, gross'
            ),
            dcc.RadioItems(
                id='b_yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='b_indicator-graphic'),

    
])
])

@app.callback(
    dash.dependencies.Output('a_indicator-graphic', 'figure'),
    [dash.dependencies.Input('a_xaxis-column', 'value'),
     dash.dependencies.Input('a_yaxis-column', 'value'),
     dash.dependencies.Input('a_xaxis-type', 'value'),
     dash.dependencies.Input('a_yaxis-type', 'value'),
     dash.dependencies.Input('a_year--slider', 'value')])
def a_update_graph(a_xaxis_column_name, a_yaxis_column_name,
                 a_xaxis_type, a_yaxis_type,
                 a_year_value):
    a_dff = df[df['TIME'] == a_year_value]
    
    return {
        'data': [go.Scatter(
            x=a_dff[a_dff['NA_ITEM'] == a_xaxis_column_name]['Value'],
            y=a_dff[a_dff['NA_ITEM'] == a_yaxis_column_name]['Value'],
            text=a_dff[a_dff['NA_ITEM'] == a_yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': a_xaxis_column_name,
                'type': 'linear' if a_xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': a_yaxis_column_name,
                'type': 'linear' if a_yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }
@app.callback(
    dash.dependencies.Output('b_indicator-graphic', 'figure'),
    [dash.dependencies.Input('b_country', 'value'),
     dash.dependencies.Input('b_yaxis-column', 'value'),
     dash.dependencies.Input('b_yaxis-type', 'value')
     ])
def b_update_graph(b_country_name, b_yaxis_column_name,
                b_yaxis_type,
                 ):
    b_dff = df[df['GEO'] == b_country_name]
    
    return {
        'data': [go.Scatter(
            x=b_dff[b_dff['NA_ITEM'] == b_yaxis_column_name]['TIME'],
            y=b_dff[b_dff['NA_ITEM'] == b_yaxis_column_name]['Value'],
            text=b_dff[b_dff['NA_ITEM'] == b_yaxis_column_name]['GEO'],
            mode='lines+markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Year',
                'type': 'linear'
            },
            yaxis={
                'title': b_yaxis_column_name,
                'type': 'linear' if b_yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()

