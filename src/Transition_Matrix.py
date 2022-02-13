import numpy as np
from Misc import states_within_range, parse_mudirac_file, normalise1d, parse_transition, State_objects_within_range


class EnergyLevelTransitionMatrix(object):

    def __init__(self, energy_level_start, energy_level_stop):
        self.n1 = energy_level_start
        self.n2 = energy_level_stop
        self.matrix_size = int(states_within_range(self.n1, self.n2))
        self.states_in_matrix = State_objects_within_range(self.n1, self.n2)
        self.state_dict = {state: index for (state, index) in zip(self.states_in_matrix, list(range(len(self.states_in_matrix))))}
        self.transition_matrix = np.zeros((self.matrix_size, self.matrix_size), dtype=float)
        self.steady_state = np.zeros(self.matrix_size, dtype=float)
        self.steady_state = np.transpose(self.steady_state)
        #print(len(self.states_in_matrix), self.matrix_size)

    def read_from_file(self, path):
        transitions, rates, _ = parse_mudirac_file(path, self.n1, self.n2)
        for i in range(len(transitions)):
            transition = transitions[i]
            rate = rates[i]
            s1, s2 = parse_transition(transition)
            index1, index2 = self.state_dict[s1], self.state_dict[s2]
            self.transition_matrix[index1, index2] = rate

    def get_steady_state_population_levels(self):
        return self.steady_state

    def calculate_steady_state(self, passes=1000):
        for i in range(passes):
            self.steady_state[0] = self.steady_state[0] + 1
            self.steady_state = np.matmul(self.transition_matrix, self.steady_state)
            #self.steady_state[-1] = 0
        self.steady_state = normalise1d(self.steady_state)
        #temp_matrix = self.transition_matrix - np.identity(self.matrix_size)
        #self.steady_state = np.linalg.solve(temp_matrix, np.zeros((self.matrix_size, 1)))

    def get_transition_matrix(self):
        return self.transition_matrix

    def get_energy_level_info(self):
        return [self.n1, self.n2, self.matrix_size]
