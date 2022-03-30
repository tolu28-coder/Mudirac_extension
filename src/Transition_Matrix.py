import numpy as np
from scipy.linalg import expm
from Neural_net import NeuralNetwork
from Misc import states_within_range, parse_mudirac_file_completely, normalise1d, parse_transition, State_objects_within_range,\
    states_in_energy_level, parse_mudirac_file_completely, parse_Iupac_notation


class EnergyLevelTransitionMatrix(object):

    def __init__(self, energy_level_start, energy_level_stop):
        self.n1 = energy_level_start
        self.n2 = energy_level_stop
        self.matrix_size = int(states_within_range(self.n1, self.n2))
        self.states_in_matrix = State_objects_within_range(self.n1, self.n2)
        self.state_dict = {state: index for (state, index) in zip(self.states_in_matrix, list(range(len(self.states_in_matrix))))}
        self.transition_matrix = np.zeros((self.matrix_size, self.matrix_size), dtype=float)
        self.normalised_transition_matrix = np.zeros((self.matrix_size, self.matrix_size), dtype=float)
        self.steady_state = np.zeros(self.matrix_size, dtype=float)
        self.state_leaving_transition = {}
        self.neural_net = None
        #self.steady_state = np.transpose(self.steady_state)
        #print(len(self.states_in_matrix), self.matrix_size)

    def read_from_file(self, path, neural_net=False):
        self.transitions, self.rates, self.energy, other_params = parse_mudirac_file_completely(path, self.n1, self.n2)
        self.neural_net = NeuralNetwork(path)
        if neural_net:
            self.neural_net.train_data()
            other_rates = self.neural_net.predict_unknown_data(other_params[0], other_params[1])
            self.transitions += other_params[0]
            self.energy += other_params[1]
            self.rates += list(other_rates)
        #self.get_emptying_rates(path)
        for i in range(len(self.transitions)):
            transition = self.transitions[i]
            rate = self.rates[i]
            s1, s2 = parse_transition(transition)
            index1, index2 = self.state_dict[s1], self.state_dict[s2]
            self.transition_matrix[index1, index2] = rate
        for i in range(len(self.transition_matrix)):
            sum_of_trans = np.sum(self.transition_matrix[i])
            if sum_of_trans == 0:
                continue
            self.normalised_transition_matrix[i] = self.transition_matrix[i] / sum_of_trans
            self.transition_matrix[i,i] = -sum_of_trans
            #self.normalised_transition_matrix[i,i] = -1
        #self.probability_matrix = expm(self.transition_matrix*10e-15)

    def get_steady_state_population_levels(self):
        return self.steady_state

    def calculate_steady_state(self, passes=1000):
        j = states_in_energy_level(self.n1)
        k = states_in_energy_level(self.n2)
        for i in range(passes):
            self.steady_state[0:j] = self.steady_state[0:j] + 1
            self.steady_state = np.matmul(self.steady_state, self.normalised_transition_matrix)
            self.steady_state[-k:] = 0

        #zero = np.zeros((self.matrix_size, 1))
        #zero[0:j] = zero[0:j] - 1
        #temp_matrix = self.normalised_transition_matrix - np.identity(self.matrix_size)
        #self.steady_state = np.linalg.solve(temp_matrix, zero)

        self.steady_state = normalise1d(self.steady_state)

    def get_transition_matrix(self):
        return self.transition_matrix

    def get_energy_level_info(self):
        return [self.n1, self.n2, self.matrix_size]

    def get_emptying_rates(self, path):
        all_transitions, all_rates, _ = parse_mudirac_file_completely(path)
        for i in range(len(all_transitions)):
            transition = all_transitions[i]
            s1, s2 = parse_transition(transition)
            if s1 not in self.state_dict:
                continue
            if s2 in self.state_dict or all_rates[i] > 0:
                continue
            if s1 in self.state_leaving_transition:
                self.state_leaving_transition[s1] -= all_rates[i]
            else:
                self.state_leaving_transition[s1] = -all_rates[i]

        for state in self.state_leaving_transition:
            index = self.state_dict[state]
            self.transition_matrix[index, index] = self.state_leaving_transition[state]

    def get_X_and_steady_states(self, n1, n2):
        all_states = State_objects_within_range(n1, n2)
        steady_state = []
        X = []
        for state in all_states:
            index = self.state_dict[state]
            steady_state.append(self.steady_state[index])
            n, l = parse_Iupac_notation(state)
            X.append([l,n])
        return np.array(X), np.array(steady_state)


