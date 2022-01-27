from Ldistribution import Ldistribution
from Transition_Matrix import EnergyLevelTransitionMatrix
from Misc import get_filepath_for_element


class LdistributionCalculator(object):

    def __init__(self, element, type, n1, n2):
        self.set_up_transition_matrix(element, n1, n2)
        if type == "constant" or type == "linear":
            params = []
        elif type == "exponential":
            params = [0]
        elif type == "quadratic":
            params = [0, 0]
        self.ldistribution = Ldistribution(type, params)

    def set_up_transition_matrix(self, element, n1,n2):
        get_filepath_for_element(element)
        self.transition_matrix = EnergyLevelTransitionMatrix(n1, n2)
        self.transition_matrix.calculate_steady_state()


    def get_Ldistribution(self):
        # calculate l-distribution and return l-distribution object
        pass

