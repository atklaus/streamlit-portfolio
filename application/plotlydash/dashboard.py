"""Instantiate a Dash app."""
import numpy as np
import pandas as pd
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from .layout import html_layout
import plotly.express as px
from dash.dependencies import Input, Output 

external_stylesheets = []

def create_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
        server=server,
        routes_pathname_prefix='/dashapp/'
    )

    # Custom HTML layout
    dash_app.index_string = html_layout


    dash_app.layout = html.Div([
    html.H6("Change the value in the text box to see callbacks in action!"),
    html.Div(["Input: ",
            dcc.Input(id='my-input', value='initial value', type='text')]),
    html.Br(),
    html.Div(id='my-output'),

    ])

    @dash_app.callback(
    dash.dependencies.Output('my-output','children'),
    [dash.dependencies.Input('my-input','value')
    ])
    def update_output_div(input_value):
        return 'Output: {}'.format(input_value)

    #     @dash_app.callback(
    #     dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    #     [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
    #     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
    #     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
    #     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
    #     dash.dependencies.Input('crossfilter-year--slider', 'value')])
    # def update_graph(xaxis_column_name, yaxis_column_name,


    if __name__ == '__main__':
        dash_app.run_server(debug=True)

    # df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

    # available_indicators = df['Indicator Name'].unique()


    # dash_app.layout = html.Div([
    #     html.Div([

    #         html.Div([
    #             dcc.Dropdown(
    #                 id='crossfilter-xaxis-column',
    #                 options=[{'label': i, 'value': i} for i in available_indicators],
    #                 value='Fertility rate, total (births per woman)'
    #             ),
    #             dcc.RadioItems(
    #                 id='crossfilter-xaxis-type',
    #                 options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
    #                 value='Linear',
    #                 labelStyle={'display': 'inline-block'}
    #             )
    #         ],
    #         style={'width': '49%', 'display': 'inline-block'}),

    #         html.Div([
    #             dcc.Dropdown(
    #                 id='crossfilter-yaxis-column',
    #                 options=[{'label': i, 'value': i} for i in available_indicators],
    #                 value='Life expectancy at birth, total (years)'
    #             ),
    #             dcc.RadioItems(
    #                 id='crossfilter-yaxis-type',
    #                 options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
    #                 value='Linear',
    #                 labelStyle={'display': 'inline-block'}
    #             )
    #         ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    #     ], style={
    #         'borderBottom': 'thin lightgrey solid',
    #         'backgroundColor': 'rgb(250, 250, 250)',
    #         'padding': '10px 5px'
    #     }),

    #     html.Div([
    #         dcc.Graph(
    #             id='crossfilter-indicator-scatter',
    #             hoverData={'points': [{'customdata': 'Japan'}]}
    #         )
    #     ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    #     html.Div([
    #         dcc.Graph(id='x-time-series'),
    #         dcc.Graph(id='y-time-series'),
    #     ], style={'display': 'inline-block', 'width': '49%'}),

    #     html.Div(dcc.Slider(
    #         id='crossfilter-year--slider',
    #         min=df['Year'].min(),
    #         max=df['Year'].max(),
    #         value=df['Year'].max(),
    #         marks={str(year): str(year) for year in df['Year'].unique()},
    #         step=None
    #     ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
    # ])


    # @dash_app.callback(
    #     dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    #     [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
    #     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
    #     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
    #     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
    #     dash.dependencies.Input('crossfilter-year--slider', 'value')])
    # def update_graph(xaxis_column_name, yaxis_column_name,
    #                 xaxis_type, yaxis_type,
    #                 year_value):
    #     dff = df[df['Year'] == year_value]

    #     fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
    #             y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
    #             hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name']
    #             )

    #     fig.update_traces(customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])

    #     fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')

    #     fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')

    #     fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    #     return fig


    # def create_time_series(dff, axis_type, title):

    #     fig = px.scatter(dff, x='Year', y='Value')

    #     fig.update_traces(mode='lines+markers')

    #     fig.update_xaxes(showgrid=False)

    #     fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    #     fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
    #                     xref='paper', yref='paper', showarrow=False, align='left',
    #                     bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    #     fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    #     return fig


    # @dash_app.callback(
    #     dash.dependencies.Output('x-time-series', 'figure'),
    #     [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
    #     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
    #     dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
    # def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    #     country_name = hoverData['points'][0]['customdata']
    #     dff = df[df['Country Name'] == country_name]
    #     dff = dff[dff['Indicator Name'] == xaxis_column_name]
    #     title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    #     return create_time_series(dff, axis_type, title)


    # @dash_app.callback(
    #     dash.dependencies.Output('y-time-series', 'figure'),
    #     [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
    #     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
    #     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
    # def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    #     dff = df[df['Country Name'] == hoverData['points'][0]['customdata']]
    #     dff = dff[dff['Indicator Name'] == yaxis_column_name]
    #     return create_time_series(dff, axis_type, yaxis_column_name)


    # if __name__ == '__main__':
    #     dash_app.run_server(debug=True)
    
    return dash_app.server

