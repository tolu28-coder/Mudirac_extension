from sklearn.neural_network import MLPRegressor
import numpy as np
import csv
from Misc import parse_transition, parse_Iupac_notation


class NeuralNetwork(object):

    def __init__(self, path):
        size = [5] + [10]*20 + [1]
        self.neural_net = MLPRegressor(tuple(size), learning_rate="adaptive")
        self.path = path

    def read_file(self):
        transitions = []
        transition_rates = []
        energy = []
        with open(self.path, "r") as file:
            csv_file = csv.reader(file, delimiter="\t")
            next(csv_file)
            next(csv_file)
            for row in csv_file:
                transition = row[0]
                rate = float(row[3])
                state1, state2 = parse_transition(transition)
                if transition.find(state1) != 0:
                    rate = -rate
                transitions.append("-".join([state1, state2]))
                energy.append(float(row[1]) / 1000)
                if np.isnan(rate):
                    transition_rates.append(None)
                else:
                    transition_rates.append(rate)

        return transitions, transition_rates, energy

    def process_data(self):
        transitions, rates, energy = self.read_file()
        self.training_input = []
        self.training_output = []
        self.predict_input = []
        self.known_transitions = []

        for i in range(len(transitions)):
            s1, s2 = parse_transition(transitions[i])
            input = [0,0,0,0,0]
            input[0], input[1] = parse_Iupac_notation(s1)
            input[2], input[3] = parse_Iupac_notation(s2)
            input[4] = energy[i]
            if rates[i] is not None:
                self.training_input.append(np.array(input))
                self.training_output.append(rates[i])
            else:
                self.predict_input.append(np.array(input))
        self.training_input = np.array(self.training_input)
        self.training_output = np.array(self.training_output)

    def train_data(self):
        self.process_data()
        self.neural_net.fit(self.training_input, self.training_output)

    def predict_unknown_data(self, transitions, energy):
        inputs = []
        for i in range(len(transitions)):
            s1, s2 = parse_transition(transitions[i])
            input = [0, 0, 0, 0, 0]
            input[0], input[1] = parse_Iupac_notation(s1)
            input[2], input[3] = parse_Iupac_notation(s2)
            input[4] = energy[i]
            inputs.append(input)
        inputs = np.array(inputs)
        rates = self.neural_net.predict(inputs)
        return rates

