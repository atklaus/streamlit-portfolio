"""
Instantiate Dash apps.
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from .layout import HTML_LAYOUT
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
from ..config import BASE_DIR
import sys
import os
from ..projects.happy_prime import HappyPrime
from ..projects.GameofLife import GameOfLife
from ..models.data_pipeline import GoogleAPI
import matplotlib.pyplot as plt


# sys.path.append(os.path.join(BASE_DIR,models)
# from ..models import google_drive_api 
# gdrive = google_drive_api.DriveAPI

############################
#Application 1
############################

def create_project1(server):
    """
    Create a Plotly Dash dashboard.
    """
    external_stylesheets = []

    dash_app = dash.Dash(__name__,
        title='Math',
        external_stylesheets=external_stylesheets,
        server=server,
        url_base_pathname='/math/'
        # routes_pathname_prefix='/project1/'
    )

    dash_app.index_string = HTML_LAYOUT

    #DONT CHANGE ANYTHING BEFORE THIS
    #NEED TO PUT INPUTS IN LIST

    dash_app.layout = html.Div(
        [
            html.H3("Happy Prime Calculator."),

            html.P("For an initial integer, consider the sum of the square of the individual digits. Continue this process and the number will either eventually equal 1 or continue in a never-ending loop. Numbers that end in a 1 are considered" + ' "Happy" numbers.'),
            html.Br(),
            html.H5("Example: 13"),
            html.H5("1\u00b2 + 3\u00b2 = 10"),
            html.H5("1\u00b2 + 0\u00b2 = 1"),

            html.Br(),
            dcc.Input(id="hp_input", type="text", placeholder="Enter an integer", debounce=True),
            html.Button('Enter', id='btn-1'),
            html.Div(id="hp_output"),
        ]
    )

    @dash_app.callback(
        Output("hp_output", "children"),
        [Input("hp_input", "value")]
    )
    def update_output(input1):
        hpObj = HappyPrime(input1)
        return hpObj.result

    if __name__ == '__main__':
        dash_app.run_server(debug=True)
    
    return dash_app.server


############################
#Applicaiton 2
############################


def create_project2(server):
    """Create a Plotly Dash dashboard."""

    external_stylesheets = []

    dash_app = dash.Dash(__name__,
        title='Project',
        external_stylesheets=external_stylesheets,
        server=server,
        routes_pathname_prefix='/project2/'
    )

    dash_app.index_string = HTML_LAYOUT

    df = px.data.gapminder()
    animations = {
        'Scatter': px.scatter(
            df, x="gdpPercap", y="lifeExp", animation_frame="year", 
            animation_group="country", size="pop", color="continent", 
            hover_name="country", log_x=True, size_max=55,
            range_x=[100,100000], range_y=[25,90]),
        'Bar': px.bar(
            df, x="continent", y="pop", color="continent", 
            animation_frame="year", animation_group="country", 
            range_y=[0,4000000000]),
    }

    dash_app.layout = html.Div([
        html.P("Select an animation:"),
        dcc.RadioItems(
            id='selection',
            options=[{'label': x, 'value': x} for x in animations],
            value='Scatter'
        ),
        dcc.Graph(id="graph"),
    ])

    @dash_app.callback(
        Output("graph", "figure"), 
        [Input("selection", "value")])
    def display_animated_graph(s):
        return animations[s]

    if __name__ == '__main__':
        dash_app.run_server(debug=True)
        
    return dash_app.server

def create_project3(server):
    """Create a Plotly Dash dashboard."""

    external_stylesheets = []

    dash_app = dash.Dash(__name__,
        title='Project',
        external_stylesheets=external_stylesheets,
        server=server,
        routes_pathname_prefix='/project3/'
    )

    dash_app.index_string = HTML_LAYOUT

    df = px.data.iris()
    GameObj = GameOfLife(10, .5)
    GameObj.advance(30)
    data = GameObj.grids[0]
    df = pd.DataFrame(data)


    dash_app.layout = html.Div([
        dcc.Graph(id="scatter-plot"),
        html.P("Petal Width:"),
        dcc.RangeSlider(
            id='range-slider',
            min=0, max=2.5, step=0.1,
            marks={0: '0', 2.5: '2.5'},
            value=[0.5, 2]
        ),
    ])

    @dash_app.callback(
        Output("scatter-plot", "figure"), 
        [Input("range-slider", "value")])
    def update_bar_chart(slider_range):
        low, high = slider_range
        mask = (df['petal_width'] > low) & (df['petal_width'] < high)
        fig = px.scatter(
            df[mask], x="sepal_width", y="sepal_length", 
            color="species", size='petal_length', 
            hover_data=['petal_width'])
        return fig

    if __name__ == '__main__':
        dash_app.run_server(debug=True)
        
    return dash_app.server



