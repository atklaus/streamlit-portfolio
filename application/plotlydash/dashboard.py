"""Instantiate a Dash app."""
import numpy as np
import pandas as pd
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from .layout import HTML_LAYOUT
import plotly.express as px
from dash.dependencies import Input, Output 
import pandas as pd


external_stylesheets = []
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def create_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
        server=server,
        routes_pathname_prefix='/dashapp/'
    )

    dash_app.index_string = HTML_LAYOUT

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
        )
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

