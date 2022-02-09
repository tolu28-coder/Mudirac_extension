import csv
import numpy as np


def population_in_energy_level(energy_level):
    return 2 * (pow(energy_level, 2))


def states_within_range(energy_level_start, energy_level_stop):
    number_of_levels = energy_level_start-energy_level_stop
    return (states_in_energy_level(energy_level_start)+states_in_energy_level(energy_level_stop))*0.5*number_of_levels


def states_in_energy_level(energy_level):
    return 2*(energy_level - 1) + 1


def parse_mudirac_file(path, n_start=np.inf, n_stop=0):
    transitions = []
    transition_rates = []
    energy = []
    with open(path, "r") as file:
        csv_file = csv.reader(file, delimiter="\t")
        next(csv_file)
        next(csv_file)
        for row in csv_file:
            transition = row[0]
            #print(row)
            state1, state2 = parse_transition(transition)
            n1, _ = parse_Iupac_notation(state1)
            n2, _ = parse_Iupac_notation(state2)
            if n1 > n_start or n2 > n_start:
                continue
            if n1 < n_stop or n2 < n_stop:
                continue
            transitions.append(row[0])
            energy.append(float(row[1])/1000)
            transition_rates.append(float(row[3]))

    return transitions, transition_rates, energy


def parse_transition(transition):
    states = transition.split('-')
    return states[0].strip(), states[1].strip()


def parse_Iupac_notation(state):
    if state == "K":
        n = 1
        l = 0
        return n, l

    else:
        shell = state[0]
        subshell = state[1:]
        n = int(ord(shell) - ord("J"))
        l = int(float(subshell)/2)
        return n, l


def get_filepath_for_element(element):
    pass


def shell_to_IUPAC(n):
    shell = int(ord(n) - ord("J"))
    return shell


def normalise1d(array):
    result = array/np.sum(array)
    return result


def State_objects_below_range(n):
    states = []
    for i in range(1, n+1):
        for j in range(1, states_in_energy_level(i) + 1):
            shell = str(chr(i + ord("J")))
            subshell = str(j)
            state = shell + subshell
            states.append(state)
    return list(reversed(states))


def State_objects_in_shell(n):
    states = []
    for j in range(1, states_in_energy_level(n)+1):
        shell = str(chr(n + ord("J")))
        subshell = str(j)
        state = shell + subshell
        states.append(state)
    return states