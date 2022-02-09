from Misc import parse_Iupac_notation


class Transition(object):

    def __init__(self, transition, transition_rate, energy):
        self.transition = transition
        self.transition_rate = transition_rate
        self.energy = energy
        self.rel_probability = None
        self.abs_probability = None

    def set_relative_probability(self, rel_probability):
        self.rel_probability = rel_probability

    def set_absolute_probability(self, abs_probability):
        self.abs_probability = abs_probability


class State(object):

    def __init__(self, state):
        self.state = state
        self.previous_transitions = []
        self.transitions = []

    def calculate_rel_probability(self):
        sum_of_rates = sum([transition.transition_rate for transition in
                            self.transitions])

        for transition in self.transitions:
            rel_probability = transition.transition_rate / sum_of_rates
            transition.set_relative_probability(rel_probability)

    def calculate_abs_probability(self, start, proportion=0):
        self.calculate_rel_probability()
        if start:
            sum_of_abs = proportion
        else:
            previous_trans = [previous_transition.abs_probability for previous_transition in self.previous_transitions]
            sum_of_abs = proportion + sum(previous_trans)
        for transition in self.transitions:
            abs_probability = transition.rel_probability * sum_of_abs
            transition.set_absolute_probability(abs_probability)


class ProbabilityTree(object):

    def __init__(self, states, transition, transition_rate, energy,
                 initial_distribution):
        self.states = {}
        self.is_start = {}
        self.transitions = {}
        self.create_states(states)
        self.create_transitions(transition, transition_rate, energy)
        self.initial_distribution = initial_distribution

    def create_states(self, states):
        for state in states:
            self.states[state] = State(state)
            if self.is_start:
                self.is_start[state] = False
            else:
                self.is_start[state] = True

    def create_transitions(self, transitions, transition_rates, energies):
        for i in range(len(transitions)):
            start, stop = self.parse_transition(transitions[i])
            temp = Transition(transitions[i], transition_rates[i], energies[i])
            self.states[start].transitions.append(temp)
            self.states[stop].previous_transitions.append(temp)
            self.transitions[transitions[i]] = temp

    def calculate_rel_probabilty(self):
        for state in self.states:
            self.states[state].calculate_rel_probability()

    def calculate_abs_probabilty(self):
        for state in self.states:
            if state in self.initial_distribution:
                proportion = self.initial_distribution[state]
            else:
                proportion = 0
            self.states[state].calculate_abs_probability(bool(proportion), proportion)

    def display_data(self):
        for state in self.states:
            if not self.states[state].transitions:
                continue
            print('-' * 10 + state + '-' * 10)
            for transition in self.states[state].transitions:
                text = str(transition.transition + '  ,Relative Probability: ' +
                           str(transition.rel_probability) + '  ,Absolute Probability: ' +
                           str(transition.abs_probability) + '  ,Energy: ' +
                           str(transition.energy))
                print(text)
            print('')

    def parse_transition(self, transition):
        states = transition.split('-')
        s1 = states[0].strip()
        s2 = states[1].strip()
        n1, l1 = parse_Iupac_notation(s1)
        n2, l2 = parse_Iupac_notation(s2)
        if n1 < n2:
            s1, s2 = s2, s1
        if n1 == n2:
            if l1 < l2:
                s1, s2 = s2, s1

        return s1, s2


if __name__ == "__main__":
    teststate = ['A', 'B', 'C', 'D']
    testtransitions = ['A-B', 'A-C', 'A-D', 'B-C', 'B-D', 'C-D']
    testrates = [6, 2, 2, 5, 5, 4]
    testenergies = [10, 20, 30, 40, 50, 60]
    test = ProbabilityTree(teststate, testtransitions, testrates, testenergies)
    test.calculate_rel_probabilty()
    test.calculate_abs_probabilty()
    test.display_data()