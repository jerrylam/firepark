import streamlit as st
import pandas
import time
import datetime

from scipy.sparse import coo_matrix
import plotly.express as px

import numpy as np
from numpy.random import randint

import copy
import itertools
from firepark.game.life import ProbabilisticGameOfLife
from firepark.game.pattern import Blinker, Glider, Boat, Beacon


st.title('Probabilistic Game of Life')
st.subheader('Rules:')
st.markdown(
    "Given that  $t$ represents a small probability (0.01), the rules for this game are:  \n"
    "- Any live cell with fewer than two live neighbours dies with probability (1−$t$)  \n"
    "- Any live cell with two or three live neighbours lives with probability (1−$t$) on to the next generation  \n"
    "- Any live cell with more than three live neighbours dies with probability (1−$t$)  \n"
    "- Any dead cell with exactly three live neighbours becomes a live cell with probability (1−$t$) otherwise they becomes a live cell with probability $t$  \n"
    "- (Special) Any cells within the radius of x cells of an active cell also have the probability of being alive with probability $t$"
    )

pattern_selection = st.sidebar.radio('Starting Pattern', ('Blinker', 'Boat', 'Beacon', 'Glider'))
probability = st.sidebar.slider('Probability (t)', 0.0, 0.5, 0.02)
radius = st.sidebar.slider('Radius of Influence', 2, 10, 2)
board_size = st.sidebar.slider('Board Size', 10, 100, 50)
num_iterations = st.sidebar.slider('Iterations', 10, 1000, 1000)
speed = st.sidebar.slider('Speed', 0.0, 1.0, 0.1)

board_center = int(board_size/2)

patterns = {'Blinker': Blinker(board_center, board_center),
            'Boat': Boat(board_center, board_center),
            'Beacon': Beacon(board_center, board_center),
            'Glider': Glider(board_center, board_center),
           }
active_cells = patterns[pattern_selection].pattern
n_rows = board_size
n_cols = board_size
game = ProbabilisticGameOfLife(active_cells, n_rows, n_cols, probability, leak_radius=radius)
heatmap_location = st.empty()
if st.sidebar.button('Start Simulation'):
    board = game.get_board()
    fig = px.imshow(board, color_continuous_scale='gray', zmin=0, zmax=1)
    heatmap_location.plotly_chart(fig)
    for _ in range(num_iterations):
        board, is_dead = game.get_next_board()
        fig = px.imshow(board, color_continuous_scale='gray', zmin=0, zmax=1)
        heatmap_location.plotly_chart(fig)
        if is_dead:
            break
        time.sleep(speed)