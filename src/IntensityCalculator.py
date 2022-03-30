import numpy as np
from Transition_Matrix import EnergyLevelTransitionMatrix
from Neural_net import NeuralNetwork
from Ldistribution import Ldistribution
from Probability_tree import ProbabilityTree
from Misc import State_objects_below_range, parse_mudirac_file_completely, State_objects_in_shell, parse_Iupac_notation


class IntensityCalculator(object):

    def __init__(self, type, n_start, file_path, neural_net=False, params=[]):
        self.ldistribution = Ldistribution(type, params)
        states = State_objects_below_range(n_start)
        transitions,rates, energy, other_params = parse_mudirac_file_completely(file_path, n_start)
        self.neural_net = NeuralNetwork(file_path)
        if neural_net:
            self.neural_net.train_data()
            other_rates = self.neural_net.predict_unknown_data(other_params[0], other_params[1])
            transitions += other_params[0]
            energy += other_params[1]
            rates += list(other_rates)
        l_distribution = self.calculate_ldistribution(n_start)
        self.probability_tree = ProbabilityTree(states, transitions, rates, energy, l_distribution)

    def set_ldistribution(self, ldistribution):
        self.ldistribution = ldistribution

    def parse_mudirac_file(self, filepath, n_start):
        pass

    def calculate_intensities(self, file_name = ""):
        self.probability_tree.calculate_rel_probabilty()
        self.probability_tree.calculate_abs_probabilty()
        self.probability_tree.sort_and_display()
        if file_name:
            file = open(file_name, "w")
            file.write(self.get_file_data())

    def get_file_data(self):
        all_data = str(self.probability_tree.sorter)
        file_data= "Energy, Intensity, Transition \n"
        lines = all_data.split("\n")
        for line in lines:
            if not line:
                continue
            split_line = line.split(",")
            energy, intensity, transition = [x.split(":")[1] for x in split_line]
            final_line = "{}, {}, {}\n".format(energy, intensity, transition)
            file_data += final_line
        return file_data[:-1]

    def calculate_ldistribution(self, n_start):
        states = list(reversed(State_objects_in_shell(n_start)))
        X = []
        for state in states:
            n , l = parse_Iupac_notation(state)
            X.append([l,n])
        X = np.array(X)
        distribution = self.ldistribution.distribution(X)
        l_distribution = {}
        for i in range(len(states)):
            l_distribution[states[i]] = distribution[i]

        return l_distribution



