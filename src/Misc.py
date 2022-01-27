import csv


def population_in_energy_level(energy_level):
    return 2 * (pow(energy_level, 2))


def states_within_range(energy_level_start, energy_level_stop):
    number_of_levels = energy_level_start-energy_level_stop
    return (states_in_energy_level(energy_level_start)+states_in_energy_level(energy_level_stop))*0.5*number_of_levels


def states_in_energy_level(energy_level):
    return 2*(energy_level - 1) + 1


def parse_mudirac_file(path, n_start, n_stop=0):
    transitions = []
    transition_rates = []
    energy = []
    with open(path, "r") as file:
        csv_file = csv.reader(file, delimiter="\t")
        next(csv_file)
        next(csv_file)
        for row in csv_file:
            transitions.append(row[0])
            energy.append(float(row[1])/1000)
            transition_rates.append(float(row[2]))

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
        subshell = state[-1:]
        n = int(ord(shell) - ord("J"))
        l = int(float(subshell)/2)
        return n, l


def get_filepath_for_element(element):
    pass


def shell_to_IUPAC(n):
    n = int(ord(n) - ord("J"))


def normalise1d(array):
    pass


def State_objects_below_range(n):
    states = []
    for i in range(1, n+1):
        for j in range(1, states_in_energy_level(i)):
            shell = str(chr(i + ord("J")))
            subshell = str(j)
            state = shell + subshell
            states.append(state)
    return reversed(states)


def State_objects_in_shell(n):
    states = []
    for j in range(1, states_in_energy_level(n)):
        shell = str(chr(n + ord("J")))
        subshell = str(j)
        state = shell + subshell
        states.append(state)
    return states