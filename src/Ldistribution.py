import numpy as np
from scipy.optimize import curve_fit
from Misc import normalise1d


class Ldistribution(object):

    def __init__(self, function_type, parameters):
        self.parameters = parameters
        self.type = function_type
        if function_type == "linear":
            self._distribution = self.linear
        elif function_type == "exponential":
            self._distribution = self.exponential
        elif function_type == "quadratic":
            self._distribution = self.quadratic
        elif function_type == "constant":
            self._distribution = self.constant

    def distribution(self, X):
        self._distribution(X, *self.parameters)

    def linear(self, X):
        initial_population = np.zeros(len(X), dtype=float)
        for i in range(len(X)):
            l, n = X[i]
            if l > 0:
                initial_population[i] = (2*l + 1)/2
            else:
                initial_population[i] = 1
        return normalise1d(initial_population)

    def exponential(self, X, alpha):
        initial_population = np.zeros(len(X), dtype=float)
        for i in range(len(X)):
            l, n = X[i]
            if l > 0:
                initial_population[i] = ((2*l+1)*np.exp(alpha*l))/2
            else:
                initial_population[i] = 1
        return normalise1d(initial_population)

    def quadratic(self, X, b, c):
        initial_population = np.zeros(len(X), dtype=float)
        for i in range(len(X)):
            l, n = X[i]
            if l != 1:
                initial_population[i] = (1/n + b*(l - 0.5 *(n - 1)) + c*(l*l - (n - 1)*(2*n - 1)/6))/2
            else:
                initial_population[i] = 1/n + b*(l - 0.5 *(n - 1)) + c*(l*l - (n - 1)*(2*n - 1)/6)
        return normalise1d(initial_population)

    def constant(self, X):
        l, n = X[:, 0], X[:, 1]
        initial_population = np.ones(len(l), dtype=float)
        return normalise1d(initial_population)

    def get_params(self):
        return self.parameters

    def get_type(self):
        return self.type

    def fit(self, X, steady_state):
        if self.type == "constant" or self.type == "linear":
            return self.parameters

        popt, pcov = curve_fit(self._distribution, X, steady_state, self.parameters)
        self.parameters = popt
        return self.parameters