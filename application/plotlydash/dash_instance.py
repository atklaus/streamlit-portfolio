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

class DashModule:
    def __init__(self, param_dict):
    self.param_dict = param_dict



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

    if __name__ == '__main__':
        dash_app.run_server(debug=True)
    
    return dash_app.server

