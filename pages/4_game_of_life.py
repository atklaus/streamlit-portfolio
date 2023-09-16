import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time
from projects.GameofLife import GameOfLife

from layout.header import page_header, set_page_container_style
import config as c
import math

# The `page_header('Game of Life')` function is likely a custom function defined in the
# `layout.header` module. It is used to display a header or title for the Game of Life page in the
# Streamlit application.
# page_header('Game of Life')

import streamlit as st
from streamlit_option_menu import option_menu
import lib.st_utils as stu
from streamlit.runtime.scriptrunner import RerunData, RerunException
from streamlit.source_util import get_pages

page_header('Game of Life',container_style=False)

st.title("Conway's Game of Life")
st.write("""
Game of Life is a popular programming problem that can be set with unlimited initial configurations to display exciting graphics. Starting with a two-dimensional grid, the highlighted cells will change with each iteration based on the following rules:
""")
st.write('''
1. Any live cell with two or three live neighbors survives. 
2. Any dead cell with three live neighbors becomes a live cell. 
3. All other live cells die in the next generation. Similarly, all other dead cells stay dead.

[More details about the game](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).
''')

# Create columns for the inputs
col1, col2, col3 = st.columns(3)
prob = col1.number_input("Start Probability", min_value=0.0, max_value=1.0, value=0.1)
board_size = col2.number_input("Board Size", min_value=5, max_value=100, value=30)
iters = col3.number_input("Iterations", min_value=1, max_value=100, value=10)

# Create a row for the seed selection
seed_col = st.columns(1)
seed_options = ['None', 'Beacon', 'Blinker', 'Growth']
# , 'Toad', 'Oscillator'
seed_choice = seed_col[0].selectbox("Choose a popular scenario", seed_options, index=0)
if st.button('Create New Board'):
    shape = None if seed_choice == 'None' else seed_choice.lower()
    GameObj = GameOfLife(board_size, prob, shape)
    board_size = len(GameObj.b)
    GameObj.advance(iters)
     # Adjust the margin of the Plotly chart container
    st.markdown('<style>#root .stPlotly > div { margin-top: 0px !important; }</style>', unsafe_allow_html=True)
    # Create a persistent placeholder for the plot immediately after the button
    plot = st.empty()
    for k in range(iters):
        fig = go.Figure(
            data=[go.Heatmap(
                x=list(range(0, board_size)),
                y=list(range(0, board_size)),
                z=GameObj.grids[k],
                colorscale=[[0.0, '#D3D3D3'],
                            [1.0, '#191970']]
            )],
            layout=go.Layout(
                xaxis=dict(range=[0, board_size], autorange=False, showgrid=False, zeroline=False),
                yaxis=dict(range=[0, board_size], autorange=False, showgrid=False, zeroline=False),
                showlegend=False,
                margin=dict(t=10, b=10, l=10, r=10),  # Reducing margins
                font=dict(size=10)  # Adjust font size if needed
            )
        )
        axis_template = dict(range=[0 - 1, board_size + 1], autorange=False,
                            showgrid=False, zeroline=False, showticklabels=False,
                            ticks='')
        fig.update_layout(showlegend=False, autosize=True, xaxis=axis_template, yaxis=axis_template)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', transition={'duration': 1000})
        fig.update_traces(showscale=False)
        
        # Update the plot using the persistent placeholder
        plot.plotly_chart(fig, use_container_width=True)
        time.sleep(0.5)  # Adding a delay to create an animation effect
