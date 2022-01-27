import numpy as np
from Misc import states_within_range, parse_mudirac_file, parse_Iupac_notation


class EnergyLevelTransitionMatrix(object):

    def __init__(self, energy_level_start, energy_level_stop):
        self.n1 = energy_level_start
        self.n2 = energy_level_stop
        self.matrix_size = states_within_range(self.n1, self.n2)
        self.transition_matrix = np.zeros((self.matrix_size, self.matrix_size), dtype=float)
        self.steady_state = np.zeros((self.matrix_size, 1), dtype=float)

    def read_from_file(self, path):
        transition, rates, _ = parse_mudirac_file(path)



    def get_steady_state_population_levels(self):
        return self.steady_state

    def calculate_steady_state(self):
        temp_matrix = self.transition_matrix - np.identity(self.matrix_size)
        self.steady_state = np.linalg.solve(temp_matrix, np.zeros((self.matrix_size, 1)))

    def get_transition_matrix(self):
        return self.transition_matrix

    def get_energy_level_info(self):
        return [self.n1, self.n2, self.matrix_size]
