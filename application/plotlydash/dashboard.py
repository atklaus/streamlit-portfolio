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
from dash.dependencies import Input, Output, State
import pandas as pd
from ..config import BASE_DIR
import sys
import os
from ..projects.happy_prime import HappyPrime
from ..projects.AreaOfEllipse import Point, Ellipse, OverlapOfEllipses
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


    # points_df = points_df[points_df['overlap'] == True]

    # animations = {
    #     'Scatter': px.scatter(
    #         points_df, x="x", y="y", animation_frame="group", color='overlap',
    #         animation_group="count", hover_name="count", size_max=(len(points_df)),
    #         range_x=[0,1], range_y=[0,1])
    # }

    # # EXAMPLE
    # df = px.data.gapminder()
    # animations = {
    #     'Scatter': px.scatter(
    #         points_df, x="x", y="y", animation_frame="group", color='overlap',
    #         animation_group="count", hover_name="count", size_max=(len(points_df)),
    #         range_x=[0,1], range_y=[0,1]),
    # }

    # dash_app.layout = html.Div([
    #     html.P("Select an animation:"),
    #     dcc.RadioItems(
    #         id='selection',
    #         options=[{'label': x, 'value': x} for x in animations],
    #         value='Scatter'
    #     ),
    #     dcc.Graph(id="graph"),
    # ])

    dash_app.layout = html.Div(
        [
            html.H3("Area of Overlapping Ellipse"),
            html.P("Define math for overlapping ellipses"),
            html.Br(),

            html.H5("Coordinates of focal points for Ellipse 1"),
            html.Br(),

            dcc.Input(id="focal_pt_1", type="text", placeholder='2,3'),
            dcc.Input(id="focal_pt_2", type="text", placeholder='2,3'),
            html.Br(),
            html.Br(),

            html.H5("Coordinates of focal points for Ellipse 2"),
            html.Br(),

            dcc.Input(id="focal_pt_3", type="text", placeholder='2,3'),
            dcc.Input(id="focal_pt_4", type="text", placeholder='2,3'),                  
            html.Br(),
            html.Br(),

            html.H5("Number of Iterations"),
            html.Br(),

            dcc.Input(id="n_iterations", type="int", placeholder=1000),                  

            html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
            dcc.Graph(id="ellipse_plot"),
        ]
    )

    @dash_app.callback(
        Output("ellipse_plot", "figure"), 
        [Input("submit-button-state", "n_clicks")],
        [State("focal_pt_1", "value"),
        State("focal_pt_2", "value"),
        State("focal_pt_3", "value"),
        State("focal_pt_4", "value"),
        State("iterations", "value")])
    def update_ellipse(n_clicks,input1,input2,input3,input4, n_iterations):
        x1 = int(input1.split(',')[0])
        y1 = int(input1.split(',')[1])
        x2 = int(input2.split(',')[0])
        y2 = int(input2.split(',')[1])
        x3 = int(input3.split(',')[0])
        y3 = int(input3.split(',')[1])
        x4 = int(input4.split(',')[0])
        y4 = int(input4.split(',')[1])

        p1 = Point(x1,y1)
        p2 = Point(x2,y2)
        p3 = Point(x3,y3)
        p4 = Point(x4,y4)
        e1 = Ellipse(p1,p2, 2)
        e2 = Ellipse(p3,p4, 2)

        EllObj = OverlapOfEllipses(seed = 20, iters = n_iterations)
        EllObj.computeOverlapOfEllipses(e1,e2)

        points_df = EllObj.points_df.copy()
        # points_df['group'] = 'one'
        points_df['count'] = range(0,len(points_df))
        ell_fig = px.scatter(
        points_df, x="x", y="y", 
        color="overlap", hover_data=['count'])
        
        return ell_fig

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

    gdrive = GoogleAPI()
    df = gdrive.sheet_to_df("IPEDS Data", "IPEDS Data")
    df['PDI_Tier'] = df['PDI_Tier'].replace('',None)
    df['Apps_Tot_FT'] = df['Apps_Tot_FT'].replace('',None)
    df['Adm_Tot_FT'] = df['Adm_Tot_FT'].replace('',None)

    df = df.dropna()
    df['PDI_Tier']= df['PDI_Tier'].astype(float)
    df['Apps_Tot_FT']= df['Apps_Tot_FT'].astype(float)
    df['Adm_Tot_FT']= df['Adm_Tot_FT'].astype(float)


    # df = px.data.iris()
    # GameObj = GameOfLife(10, .5)
    # GameObj.advance(30)
    # data = GameObj.grids[0]
    # df = pd.DataFrame(data)


    dash_app.layout = html.Div([
        dcc.Graph(id="scatter-plot"),
        html.P("Petal Width:"),
        dcc.RangeSlider(
            id='range-slider',
            min=0, max=7, step=1,
            marks={0: '0', 2.5: '2.5'},
            value=[0, 7]
        ),
    ])

    @dash_app.callback(
        Output("scatter-plot", "figure"), 
        [Input("range-slider", "value")])
    def update_bar_chart(slider_range):
        low, high = slider_range
        mask = (df['PDI_Tier'] > low) & (df['PDI_Tier'] < high)
        fig = px.scatter(
            df[mask], x="Apps_Tot_FT", y="Adm_Tot_FT", 
            color="PDI_Tier", size='Apps_Tot_FT', 
            hover_data=['PDI_Tier'])
        return fig

    if __name__ == '__main__':
        dash_app.run_server(debug=True)
        
    return dash_app.server



