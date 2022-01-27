import numpy as np
from Transition_Matrix import EnergyLevelTransitionMatrix
from Ldistribution import Ldistribution
from Probability_tree import ProbabilityTree
from Misc import State_objects_below_range, parse_mudirac_file, State_objects_in_shell, parse_Iupac_notation


class IntensityCalculator(object):

    def __init__(self, type, n_start, file_path, params= []):
        self.ldistribution = Ldistribution(type, params)
        states = State_objects_below_range(n_start)
        transitions,rates, energy = parse_mudirac_file(file_path, n_start)
        l_distribution = self.calculate_ldistribution(n_start)
        self.probability_tree = ProbabilityTree(states, transitions, rates, energy, l_distribution)

    def calculate_intensities(self):
        self.probability_tree.calculate_rel_probabilty()
        self.probability_tree.calculate_abs_probabilty()
        self.probability_tree.display_data()

    def calculate_ldistribution(self, n_start):
        states = State_objects_in_shell(n_start)
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



