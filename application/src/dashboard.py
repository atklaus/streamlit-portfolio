"""
Instantiate Dash apps.
"""
from dash_html_components.Br import Br
from dash_html_components.Div import Div
from plotly.validators.scatter import marker
from plotly.validators.scatter.marker import SymbolValidator
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import dash
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
# from ..projects.happy_prime import HappyPrime
# from ..projects.AreaOfEllipse import Point, Ellipse, OverlapOfEllipses
# from ..projects.GameofLife import GameOfLife
# from ..models.data_pipeline import GoogleAPI
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container

# sys.path.append(os.path.join(BASE_DIR,models)
# from ..models import google_drive_api 
# gdrive = google_drive_api.DriveAPI

############################
#Application 1
############################


def new_layout(server):

    # 2. Create a Dash app instance
    app = dash.Dash(name=__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],assets_folder=os.getcwd() +'/application/assets')


    navbar = dbc.Navbar(
    [
        html.Div(
            dbc.Row(
                [
                    dbc.Col(html.Img(src = app.get_asset_url("/images/final_adsc_logo.png"), height= "120px"),width=12,style={"border":"2px black solid"}),      
                ]

            )
        ),
        dbc.NavbarToggler(id="navbar-toggler2"),
        dbc.Collapse(
            dbc.Nav(
                # right align dropdown menu with ml-auto className
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("More pages", header=True),
                    dbc.DropdownMenuItem("Page 2", href="#"),
                    dbc.DropdownMenuItem("Page 3", href="#"),
                ],
                nav=True,
                in_navbar=True,
                label="More",
            ), className="ml-auto", navbar=True
            ),
            id="navbar-collapse2",
            navbar=True,
            ),

    ]
    ,id='navbar_item'
    ,color="#3F5D70"
    )

    app.layout = navbar

    # 5. Start the Dash server
    if __name__ == "__main__":
        app.run_server()
    
    return app.server



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
            html.H3("Happy Prime Calculator"),

            html.P("For an initial integer number, if you take the sum of the square of the individual digits in that number you get a new number. Now take that number and continue this process. The number will either eventually equal 1 or continue in a never-ending loop. Numbers that end in a 1 are considered" + ' "Happy" numbers.'),
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
        routes_pathname_prefix='/ellipses/'
    )

    dash_app.index_string = HTML_LAYOUT

    dash_app.layout = html.Div(
        [
            html.H3("Area of Overlapping Ellipses"),
            html.P("Starting with a point on the curve of an ellipse, the sum of the distance between that point and the focal points of the ellipse will be the same compared to any other point on the ellipse curve. As a result of this, the width of the ellipse will equal the sum of the distances between the focal points and a point on the curve of the ellipse."),
            html.Br(),
            html.P("With this in mind, given two ellipses, we can determine if any random point is within one of the ellipses, both of the ellipses or neither by calculating the sum of the distance between that random point and the focal points of each ellipse. This is demonstrated below by showing where random points fell. Additionally, the numbers are generated by a custom built Pseudo Random Number Generator that can use any text data (this version is using a text document of the novel 'War and Peace') to generate a random number between 0 and 1. More specifically, the generator does a Bitwise comparison of 16 pairs of characters and takes the sum product of the resulting binary list."),
            html.Br(),
            html.P("The default example is two concentric circles and the area should be close to π (Pi)."),

            html.H4("Enter inputs for Ellipse 1"),

            html.Div(children=[

                html.H5("Focal Point 1"),
                dcc.Input(id="focal_pt_1", type="text", value='1,1',className='ellipse_input'),
                html.H5("Focal Point 2"),
                dcc.Input(id="focal_pt_2", type="text", value='1,1',className='ellipse_input'),
                html.H5("Ellipse Width"),
                dcc.Input(id="width_1", type="text", value='2',className='ellipse_input'),
            ], style={'columnCount': 3}
            ),

            html.H4("Enter inputs for Ellipse 2"),
            html.Div(children=[

                html.H5("Focal Point 1"),
                dcc.Input(id="focal_pt_3", type="text", value='0,0',className='ellipse_input'),
                html.H5("Focal Point 2"),
                dcc.Input(id="focal_pt_4", type="text", value='0,0',className='ellipse_input'),
                html.H5("Ellipse Width"),
                dcc.Input(id="width_2", type="text", value='2',className='ellipse_input'),
            ], style={'columnCount': 3}
            ),

            html.Br(),
            html.H5("Random Number Iterations"),
            dcc.Input(id="n_iterations", type="text", value='5000',className='ellipse_input'),                  
            html.Button(id='submit-button-state', n_clicks=0, children='Submit'),

            # html.Br(),
            html.Div(children=[
                html.H4("Estimation of the Overlapping Area between Ellipse 1 and 2:"),            
            ], style={'columnCount': 2}),
            html.Div(children=[
                html.Div(id="overlap_area"),
            ], style={'columnCount': 2}),


            dcc.Graph(id="ellipse_plot"),
        ]
    )

    @dash_app.callback(
        [Output("ellipse_plot", "figure"),
        Output("overlap_area", "children")], 
        [Input("submit-button-state", "n_clicks")],
        [State("focal_pt_1", "value"),
        State("focal_pt_2", "value"),
        State("width_1", "value"),
        State("focal_pt_3", "value"),
        State("focal_pt_4", "value"),
        State("width_2", "value"),
        State("n_iterations", "value")])

    def update_ellipse(n_clicks,input1,input2,width1,input3,input4,width2,input5):
        if n_clicks > 0:
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
            e1 = Ellipse(p1,p2, int(width1))
            e2 = Ellipse(p3,p4, int(width2))

            EllObj = OverlapOfEllipses(seed = 20, iters = int(input5))
            EllObj.computeOverlapOfEllipses(e1,e2)

            points_df = EllObj.points_df.copy()
            points_df['point_number'] = range(0,len(points_df))
            ell_fig = px.scatter(
            points_df, x="x", y="y", 
            # height=600, width=600,
            color="Location", hover_data=['point_number'])
            ell_fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
            ))
            
            return ell_fig, EllObj.overlap_area
        else:
            ell_fig = px.scatter(height=600, width=600)
            return ell_fig, ''

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
        routes_pathname_prefix='/life/'
    )

    dash_app.index_string = HTML_LAYOUT

    # fig.show()

    dash_app.layout = html.Div([
            html.H3("Conway's Game of Life"),
            html.P("Game of Life is a popular programming problem that can be set with unlimited initial configurations to display exciting graphics. Starting with a two-dimensional grid, the highlighted cells will change with each iteration based on the following rules:"),
            dcc.Markdown('''
            1. Any live cell with two or three live neighbors survives. 
            2. Any dead cell with three live neighbors becomes a live cell. 
            3. All other live cells die in the next generation. Similarly, all other dead cells stay dead.

            You can find more details about the game [here](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).
            '''),
            # html.A("Wikipedia Explanation",href='https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life',target='_blank'),
            html.H4("Enter inputs"),
            html.Div(children=[

                html.H5("Start Probability"),
                dcc.Input(id="prob", type="int", value=.1,className='life_input'),
                html.H5("Board Size"),
                dcc.Input(id="board_size", type="int", value=30,className='life_input'),
                html.H5("Iterations"),
                dcc.Input(id="iters", type="int", value=30,className='life_input'),
            ], style={'columnCount': 3}
            ),
            html.H4("OR"),
            html.H5("Choose a popular scenario"),
            html.Div(id='life-dropdown',children=[
            dcc.Dropdown(
                id='seed-dropdown',
                options=[
                    {'label': 'Beacon', 'value': 'beacon'},
                    {'label': 'Blinker', 'value': 'blinker'},
                    {'label': 'Toad', 'value': 'toad'},
                    {'label': 'Oscillator', 'value': 'oscilator'},
                    {'label': 'Growth', 'value': 'growth'},
                    ],
                    value=None
                ),
            ],style={'marginRight':'300'}),
            html.P(id='placeholder'),
            html.Br(),
            html.Button(id='submit-button-state', n_clicks=0, children='Create New Board'),
        dcc.Graph(id="life_plot"),
    ])

    #FIGURE OUT HOW TO HAVE EMPTY INPUT
    @dash_app.callback(
        Output("life_plot", "figure"), 
        [Input("placeholder", "value"),
        Input("submit-button-state", "n_clicks")],
        [State("prob", "value"),
        State("board_size", "value"),
        State("iters", "value"),
        State("seed-dropdown", "value")])
    def display_animated_graph(input1,input2,input3,input4,input5,input6):
        prob = input3
        board_size = int(input4)
        iters = int(input5)
        shape = input6

        GameObj = GameOfLife(board_size, prob, shape)
        board_size = len(GameObj.b)
        GameObj.advance(iters)

        fig = go.Figure(
            data=[go.Heatmap(
                x = list(range(0, board_size)),
                y = list(range(0, board_size)),
                z = GameObj.grids[0],
                colorscale=[[0.0, '#D3D3D3'], 
                         [1.0, '#191970']]
                )],
            layout=go.Layout(
                xaxis=dict(range=[0, board_size], autorange=False),
                yaxis=dict(range=[0, board_size], autorange=False),
                showlegend = False,
                updatemenus=[dict(
                    type="buttons",
                    buttons=[dict(label="Run Simulation",
                                method="animate",
                                args=[None])])]
            ),
            frames=[go.Frame(
                data=[go.Heatmap(x = list(range(0, board_size)),
                y = list(range(0, board_size)),
                z = GameObj.grids[k])])
                for k in range(iters)]
        )
        axis_template = dict(range = [0-1,board_size+1], autorange = False,
            showgrid = False, zeroline = False, showticklabels = False,
            ticks = '' )
        
        fig.update_layout(showlegend = False,autosize = False,xaxis = axis_template,yaxis = axis_template)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',transition = {'duration': 1000})
        fig.update_traces(showscale=False)
        fig.update_layout(width=800,height=800
        # ,transition = {'duration': 1000}
        )

        # fig.update_yaxes(range=[0-.5, board_size-.5])
        # fig.update_xaxes(nticks=10)
        return fig

    if __name__ == '__main__':
        dash_app.run_server(debug=True)
        
    return dash_app.server

# p=.3
# b=6
# t=30

# GameObj = GameOfLife(b, p)
# universe = np.zeros((6, 6))
# beacon = [[1, 1, 0, 0],
#           [1, 1, 0, 0],
#           [0, 0, 1, 1],
#           [0, 0, 1, 1]]
# universe[1:5, 1:5] = beacon
# GameObj.b = universe

# GameObj.advance(t)
# GameObj.grids

# df = pd.DataFrame(columns = ['x','y','value','step'])

# for i in range(GameObj.steps):
#     temp_df = pd.DataFrame(data=GameObj.grids[i])
#     temp_df = temp_df.reset_index()
#     temp_df = temp_df.rename(columns={"index":"x"})
#     temp_df = pd.melt(temp_df, id_vars=['x'], value_vars=list(range(0,b)))
#     temp_df = temp_df.rename(columns={"variable":"y"})
#     temp_df = temp_df[temp_df.value ==1]
#     temp_df['step'] = i
#     df = pd.concat([df,temp_df])

# df['x'] = df['x'] + .5
# df['y'] = df['y'] + .5


#############
# GOOGLE DRIVE EXAMPLE
#############

# def create_project3(server):
#     """Create a Plotly Dash dashboard."""

#     external_stylesheets = []

#     dash_app = dash.Dash(__name__,
#         title='Project',
#         external_stylesheets=external_stylesheets,
#         server=server,
#         routes_pathname_prefix='/life/'
#     )

#     dash_app.index_string = HTML_LAYOUT

#     gdrive = GoogleAPI()
#     df = gdrive.sheet_to_df("IPEDS Data", "IPEDS Data")
#     df['PDI_Tier'] = df['PDI_Tier'].replace('',None)
#     df['Apps_Tot_FT'] = df['Apps_Tot_FT'].replace('',None)
#     df['Adm_Tot_FT'] = df['Adm_Tot_FT'].replace('',None)

#     df = df.dropna()
#     df['PDI_Tier']= df['PDI_Tier'].astype(float)
#     df['Apps_Tot_FT']= df['Apps_Tot_FT'].astype(float)
#     df['Adm_Tot_FT']= df['Adm_Tot_FT'].astype(float)

#     # df = px.data.iris()
#     # GameObj = GameOfLife(10, .5)
#     # GameObj.advance(30)
#     # data = GameObj.grids[0]
#     # df = pd.DataFrame(data)

#     dash_app.layout = html.Div([
#         dcc.Graph(id="scatter-plot"),
#         html.P("Petal Width:"),
#         dcc.RangeSlider(
#             id='range-slider',
#             min=0, max=7, step=1,
#             marks={0: '0', 2.5: '2.5'},
#             value=[0, 7]
#         ),
#     ])

#     @dash_app.callback(
#         Output("scatter-plot", "figure"), 
#         [Input("range-slider", "value")])
#     def update_bar_chart(slider_range):
#         low, high = slider_range
#         mask = (df['PDI_Tier'] > low) & (df['PDI_Tier'] < high)
#         fig = px.scatter(
#             df[mask], x="Apps_Tot_FT", y="Adm_Tot_FT", 
#             color="PDI_Tier", size='Apps_Tot_FT', 
#             hover_data=['PDI_Tier'])
#         return fig

#     if __name__ == '__main__':
#         dash_app.run_server(debug=True)
        
#     return dash_app.server
