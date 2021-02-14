"""
Instantiate Dash apps.
"""
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
        title='Project',
        external_stylesheets=external_stylesheets,
        server=server,
        url_base_pathname='/project1/'
        # routes_pathname_prefix='/project1/'
    )

    dash_app.index_string = HTML_LAYOUT

    #DONT CHANGE ANYTHING BEFORE THIS
    #NEED TO PUT INPUTS IN LIST

    dash_app.layout = html.Div(
        [
            html.H3("Welcome to the Happy Prime Calculator."),

            html.H5("For an initial integer, consider the sum of the square of the individual digits. The number will either eventually equal 1 or continue in a never-ending loop."),
            html.H5("Numbers that end in a 1 are considered 'Happy' numbers"),
            html.Br(),
            html.H5("Example: 13"),
            html.H5("1^2 + 3^2 = 10"),
            html.H5("1^2 + 0^2 = 1"),

            html.Br(),
            dcc.Input(id="hp_input", type="text", placeholder="Enter an integer", debounce=True),
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

    # dash_app.index_string = HTML_LAYOUT

    # temp_drive = gdrive()
    # filename = 'SunriseEventsCategories'
    # df = temp_drive.download(filename)

    # dash_app.layout = dash_table.DataTable(
    #     id='table',
    #     columns=[{"name": i, "id": i} for i in df.columns],
    #     data=df.to_dict('records'),
    # )

    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

    dash_app.layout = html.Div([
        dcc.Graph(id='graph-with-slider'),
        dcc.Slider(
            id='year-slider',
            min=df['year'].min(),
            max=df['year'].max(),
            value=df['year'].min(),
            marks={str(year): str(year) for year in df['year'].unique()},
            step=None
        ),

    ])

    @dash_app.callback(
        Output('graph-with-slider', 'figure'),[
        Input('year-slider', 'value')])
    def update_figure(selected_year):
        filtered_df = df[df.year == selected_year]

        fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                        size="pop", color="continent", hover_name="country",
                        log_x=True, size_max=55)

        fig.update_layout(transition_duration=500)

        return fig


    if __name__ == '__main__':
        dash_app.run_server(debug=True)
    
    return dash_app.server



