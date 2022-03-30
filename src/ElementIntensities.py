from IntensityCalculator import IntensityCalculator
from Ldistribution_calculator import LdistributionCalculator

class Element(object):

    def __init__(self, path, function_type, cascade_start, matrix_start, matrix_stop):
        self.type = function_type
        self.path = path
        params = []
        if function_type == "linear":
            params = []
        elif function_type == "exponential":
            params = [1]
        elif function_type == "quadratic":
            params = [1,1]
        elif function_type == "constant":
            params = []
        self.cascade_start = cascade_start
        self.matrix_stop = matrix_stop
        self.matrix_start = matrix_start
        self.Intensity_calculator = IntensityCalculator(self.type, self.cascade_start, True, params)
        self.l_distribution_calculator = LdistributionCalculator(path, function_type, matrix_start, matrix_stop, True)

    def calculate_intensity(self, file_name=""):
        ldistribution = self.l_distribution_calculator.get_Ldistribution(self.matrix_start, self.cascade_start)
        self.Intensity_calculator.calculate_intensities(file_name)
