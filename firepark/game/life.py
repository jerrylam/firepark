import pandas
import numpy as np
import copy
import itertools

class ProbabilisticGameOfLife(object):

    def __init__(self, active_cells, num_rows, num_cols, probability, leak_radius=3):
        self.active_cells = active_cells
        self.M = num_rows
        self.N = num_cols
        self.probability = probability
        self.leak_radius = leak_radius
        self.__initialize_board()

    def __initialize_board(self):
        self.board = np.zeros([self.M, self.N])
        for i, j in self.active_cells:
            self.board[i, j] = 1

    def get_board(self):
        return self.board

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

    def get_next_board(self):
        candidates = self.find_candidates()
        is_alive = 0
        for (k, v) in candidates.items():
            if abs(v) == 3 or v == 4:
                is_alive = np.random.choice([0, 1], p=[self.probability, 1-self.probability])
            else:
                is_alive = np.random.choice([0, 1], p=[1-self.probability, self.probability])

            if is_alive:
                self.active_cells.update({k: 1})
                self.board[k[0], k[1]] = 1
            else:
                self.active_cells.pop(k, 0)
                self.board[k[0], k[1]] = 0
        is_dead = False if len(self.active_cells) else True
        return self.board, is_dead 