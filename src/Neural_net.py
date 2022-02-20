from sklearn.neural_network import MLPRegressor
import numpy as np



class NeuralNetwork(object):

    def __init__(self, path):
        self.neural_net = MLPRegressor((4,20), learning_rate="adaptive")
        self.path = path
        self.read_file()
        self.train_data()

    def read_file(self):
        pass

    def train_data(self):
        pass

    def predict_unknown_data(self):
        pass


