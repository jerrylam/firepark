import streamlit as st
import pandas
import time
import datetime

import plotly.graph_objects as go
from scipy.sparse import coo_matrix
import plotly.express as px
import numpy as np
from numpy.random import randint
import copy
import itertools

from firepark.game.life import ProbabilisticGameOfLife
from firepark.game.pattern import Pattern

st.title('Probabilistic Game of Life')
st.subheader('Rules:')
st.markdown(
    "Given that  $t$ represents a small probability (0.01), the rules for this game are:  \n"
    "- Any live cell with fewer than two live neighbors dies with probability (1−$t$)  \n"
    "- Any live cell with two or three live neighbors lives with probability (1−$t$) on to the next generation  \n"
    "- Any live cell with more than three live neighbors dies with probability (1−$t$)  \n"
    "- Any dead cell with exactly three live neighbors becomes a live cell with probability (1−$t$) otherwise they becomes a live cell with probability $t$  \n"
    "- (Special) Any cells within the radius of x cells of an active cell also have the probability of being alive with probability $t$"
    )

pattern_selection = st.sidebar.radio('Starting Pattern', ('Blinker', 'Boat', 'Beacon', 'Glider'))
probability = st.sidebar.slider('Probability (t)', 0.0, 0.5, 0.02)
radius = st.sidebar.slider('Radius of Influence', 2, 10, 2)
board_size = st.sidebar.slider('Board Size', 10, 100, 50)
num_iterations = st.sidebar.slider('Iterations', 10, 1000, 1000)
speed = st.sidebar.slider('Speed', 0.0, 1.0, 0.1)

board_center = int(board_size/2)

pattern = Pattern(board_center, board_center)

patterns = {'Blinker': pattern.blinker,
            'Boat': pattern.boat,
            'Beacon': pattern.beacon,
            'Glider': pattern.glider}

active_cells = patterns[pattern_selection]
n_rows = board_size
n_cols = board_size
game = ProbabilisticGameOfLife(active_cells, n_rows, n_cols, probability, leak_radius=radius)

if st.sidebar.button('Start Simulation'):
    heatmap_location = st.empty()
    alive_prob_location = st.empty()
    bar = st.sidebar.progress(0)
    board = game.get_board()
    board_fig = px.imshow(board, color_continuous_scale='gray', zmin=0, zmax=1)
    heatmap_location.plotly_chart(board_fig)
    iterations = []
    alive_probs = []
    for i in range(num_iterations):
        iterations.append(i)
        alive_probs.append(len(game.active_cells)/(board_size*board_size))
        alive_fig = go.Figure(data=go.Scatter(x=iterations, y=alive_probs))
        alive_fig.update_layout(title='Alive Probability over Time',
                                xaxis_title='Iteration',
                                yaxis_title='Alive Probability') 
        board, is_dead = game.get_next_board()
        board_fig = px.imshow(board, color_continuous_scale='gray', zmin=0, zmax=1)
        heatmap_location.plotly_chart(board_fig)
        alive_prob_location.plotly_chart(alive_fig)
        if is_dead:
            break
        time.sleep(speed)
        bar.progress((i+1)/num_iterations)
    bar.progress(100)