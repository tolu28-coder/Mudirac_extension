from IntensityCalculator import IntensityCalculator
from Misc import parse_mudirac_file, State_objects_in_shell, parse_transition
import numpy as np
from Transition_Matrix import EnergyLevelTransitionMatrix
import matplotlib.pyplot as plt

path1 = r"C:\Users\Tolu\Documents\Mudirac data\mudirac_output_file\Gold.out"
path2 = r"C:\Users\Tolu\Documents\Mudirac_extension\Mudirac_data\Gold22.out"
path3 = r"C:\Users\Tolu\Documents\Mudirac_extension\Mudirac_data\Gold20_1.out"
path4 = r"C:\Users\Tolu\Documents\Mudirac_extension\Mudirac_data\Aluminium20.out"
path5 = r"C:\Users\Tolu\Documents\Mudirac_extension\Mudirac_data\Carbon20.out"
path6 = r"C:\Users\Tolu\Documents\Mudirac_extension\Mudirac_data\Gold16.out"
path7 = r"C:\Users\Tolu\Documents\Mudirac_extension\Mudirac_data\Gold20Ideal.out"
path8 = r"C:\Users\Tolu\Documents\Mudirac_extension\Mudirac_data\Iodine20Ideal.out"

matrix = EnergyLevelTransitionMatrix(22, 1)
matrix.read_from_file(path2)
matrix.calculate_steady_state(100)
a = matrix.steady_state
#a = matrix.transition_matrix+1
#a = np.log(np.abs(a))
plt.plot(a)
#plt.imshow(a)
plt.show()


#Gold = IntensityCalculator("linear", 20, path7, params=[])
#Gold.calculate_intensities()
"""
t1, r1, e1 = parse_mudirac_file(path1, 12, 0)
t2, r2, e2 = parse_mudirac_file(path3, 12, 0)

data1 = np.array([r1, e1], dtype=float)
data2 = np.array([r2, e2], dtype=float)

#print(np.allclose(data1, data2, rtol = 0.01))
diff = list(set(t1) - set(t2))
print(len(diff))
print(diff)

for a in t2:
    if a not in t1:
        print(a)

for a in diff:
    state1, state2 = parse_transition(a)
    for b in diff:
        if state1 in b and state2 in b and not (a == b):
            print(a + " and " + b)

"""






