import numpy as np
from scipy.optimize import curve_fit
from collections import OrderedDict
from Misc import normalise1d


class Ldistribution(object):

    def __init__(self, function_type, parameters):
        self.parameters = parameters
        self.type = function_type
        function_type = function_type.lower()
        if function_type == "linear":
            self._distribution = self.linear
        elif function_type == "exponential":
            self._distribution = self.exponential
        elif function_type == "quadratic":
            self._distribution = self.quadratic
        elif function_type == "constant":
            self._distribution = self.constant

    def distribution(self, X):
        return self._distribution(X, *self.parameters)

    def linear(self, X):
        initial_population = np.zeros(len(X), dtype=float)
        for i in range(len(X)):
            l, n = X[i]
            if l > 0:
                initial_population[i] = (2*l + 1)
            else:
                initial_population[i] = 1

        return normalise1d(initial_population)

    def exponential(self, X, alpha):
        initial_population = np.zeros(len(X), dtype=float)
        for i in range(len(X)):
            l, n = X[i]
            if l > 0:
                initial_population[i] = ((2*l+1)*np.exp(alpha*l))
            else:
                initial_population[i] = 1
        return normalise1d(initial_population)

    def quadratic(self, X, b, c):
        initial_population = np.zeros(len(X), dtype=float)
        for i in range(len(X)):
            l, n = X[i]
            if l != 1:
                initial_population[i] = (1/n + b*(l - 0.5 *(n - 1)) + c*(l*l - (n - 1)*(2*n - 1)/6))
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
        X, steady_state = self.sort_steady_state_by_energy_level(X, steady_state)
        number_of_shells = self.get_number_of_shells(X)
        popt, pcov = curve_fit(self.to_minimise, X, steady_state, [1]*number_of_shells+self.parameters)
        self.parameters = popt[number_of_shells:]
        return self.parameters

    def to_minimise(self, X, *args):
        n_dict = self.split_by_energy_level(X)
        other_arg = args[len(n_dict):]
        i = 0
        entire_y =[]
        for key in n_dict:
            x, state = n_dict[key]
            y = args[i]*self._distribution(x, *other_arg)
            i += 1
            entire_y += y
        return entire_y

    def split_by_energy_level(self, X):
        l, n = X[:, 0], X[:, 1]
        set_of_n = sorted(list(set(n)))
        n_dict = OrderedDict()
        for x in set_of_n:
            n_dict[x] = []
        for i in range(len(l)):
            n_dict[n[i]].append([l[i], n[i]])
        for key in n_dict:
            n_dict[key][0] = np.array(n_dict[key][0])
        return n_dict

    def sort_steady_state_by_energy_level(self, X, steady_state):
        l, n = X[:, 0], X[:, 1]
        set_of_n = sorted(list(set(n)))
        n_dict = OrderedDict()
        for x in set_of_n:
            n_dict[x] = [[],[]]
        for i in range(len(l)):
            n_dict[n[i]][0].append([l[i], n[i]])
            n_dict[n[i]][1].append(steady_state[i])
        entire_steady_state = []
        entire_X = []
        for key in n_dict:
            entire_X += n_dict[key][0]
            entire_steady_state += n_dict[key][1]
        return np.array(entire_X), np.array(entire_steady_state)

    def get_number_of_shells(self, X):
        l, n = X[:, 0], X[:, 1]
        set_of_n = list(set(n))
        return len(set_of_n)
