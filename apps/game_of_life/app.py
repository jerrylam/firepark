import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import pandas
import time
import datetime

from scipy.sparse import coo_matrix
import plotly.express as px

import numpy as np
from numpy.random import randint

import copy
import itertools

class ProbabilisticGameOfLife(object):

    def __init__(self, active_cells, num_rows, num_cols, probability, leak_radius=3):
        self.active_cells = active_cells
        self.M = num_rows
        self.N = num_cols
        self.probability = probability
        self.leak_radius = leak_radius

    def find_candidates(self):
        def encode(cell_value):
            if cell_value <=0:
                return cell_value - 1
            else:
                return cell_value + 1

        def get_neighbor_cells(current_cell):
            i, j = current_cell
            
            true_neighbors = [-1, 0, 1]
            true_neighbors = set(itertools.product(true_neighbors, true_neighbors)) - {(0, 0)}
            probable_neighbors = []
            if self.leak_radius:
                num_potential_neighbors = ((self.leak_radius * 2 + 1)**2) - 9
                num_resurrections = np.random.binomial(num_potential_neighbors, self.probability, 1)[0]

                neighbor_bound = list(range(-self.leak_radius, self.leak_radius+1))
                probable_neighbors = set(itertools.product(neighbor_bound, neighbor_bound)) - {(0, 0)}
                probable_neighbors = np.array(list(probable_neighbors - true_neighbors))
                
                if num_resurrections:
                    probable_neighbor_idx = np.random.choice(len(probable_neighbors), size=num_resurrections, replace=False)
                    probable_neighbors = probable_neighbors[probable_neighbor_idx, :].tolist()
                else:
                    probable_neighbors = []
            
            neighbors = list(true_neighbors) + probable_neighbors
            return [((i + v) % self.M, (j + h) % self.N) for (h, v) in neighbors]
        
        candidates = copy.deepcopy(self.active_cells)
        for ((i, j), v)  in self.active_cells.items():
            for neighbor in get_neighbor_cells((i, j)):
                value = candidates.get(neighbor, 0)
                candidates.update({neighbor: encode(value)})
        return candidates

    def get_next(self):
        candidates = self.find_candidates()
        is_alive = 0
        for (k, v) in candidates.items():
            if abs(v) == 3 or v == 4:
                is_alive = np.random.choice([0, 1], p=[self.probability, 1-self.probability])
            else:
                is_alive = np.random.choice([0, 1], p=[1-self.probability, self.probability])
            if is_alive:
                self.active_cells.update({k: 1})
            else:
                self.active_cells.pop(k, 0)
        return self.active_cells


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

pattern = st.sidebar.radio('Starting Pattern', ('Blinker', 'Boat', 'Beacon', 'Glider'))
probability = st.sidebar.slider('Probability', 0.0, 0.5, 0.02)
radius = st.sidebar.slider('Radius of Influence', 0, 10, 0)
board_size = st.sidebar.slider('Board Size', 10, 200, 50)
num_iterations = st.sidebar.slider('Iterations', 10, 1000, 1000)
speed = st.sidebar.slider('Speed', 0.0, 1.0, 0.1)

board_center = board_size/2
blinker = {(board_center, board_center): 1,
           (board_center - 1, board_center): 1,
           (board_center + 1, board_center): 1}

boat = {(board_center, board_center - 1): 1,
        (board_center - 1, board_center - 1): 1,
        (board_center - 1, board_center): 1,
        (board_center + 1, board_center): 1,
        (board_center, board_center + 1): 1}

beacon = {(board_center - 1, board_center): 1,
          (board_center - 1, board_center - 1): 1,
          (board_center - 2, board_center): 1,
          (board_center - 2, board_center - 1): 1,
          (board_center, board_center + 1): 1,
          (board_center, board_center + 2): 1,
          (board_center + 1, board_center + 1): 1,
          (board_center + 1, board_center + 2): 1}

glider = {(board_center - 1, board_center): 1,
          (board_center + 1, board_center): 1,
          (board_center + 1, board_center - 1): 1,
          (board_center + 1, board_center + 1): 1,
          (board_center, board_center + 1): 1,
}

patterns = {'Blinker': blinker,
            'Boat': boat,
            'Beacon': beacon,
            'Glider': glider,
           }
active_cells = patterns[pattern]
n_rows = board_size
n_cols = board_size
game = ProbabilisticGameOfLife(active_cells, n_rows, n_cols, probability, leak_radius=radius)

heatmap_location = st.empty()
all_die_board = np.zeros((n_rows, n_cols))
if st.sidebar.button('Start Simulation'):
    for _ in range(num_iterations):
        board = game.get_next()
        if len(board):
            coordinates = np.array([*board.keys()])
            data = np.array([*board.values()])
            heatmap = coo_matrix((data, (coordinates[:, 0], coordinates[:, 1])), shape=(n_rows, n_cols)).toarray()
        else:
            heatmap = all_die_board

        fig = px.imshow(heatmap, color_continuous_scale='gray', zmin=0, zmax=1)
        heatmap_location.plotly_chart(fig)
        if len(board) == 0:
            break
        time.sleep(speed)