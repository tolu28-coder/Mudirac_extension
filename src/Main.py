from IntensityCalculator import IntensityCalculator
from Misc import parse_mudirac_file, State_objects_in_shell, parse_transition
import numpy as np

path1 = r"C:\Users\Tolu\Documents\Mudirac data\mudirac_output_file\Gold.out"
path2 = r"C:\Users\Tolu\Documents\Mudirac_extension\Mudirac_data\Gold22.out"

#Gold = IntensityCalculator("linear", 12, path2)
#Gold.calculate_intensities()

t1, r1, e1 = parse_mudirac_file(path1, 12, 0)
t2, r2, e2 = parse_mudirac_file(path2, 12, 0)

data1 = np.array([r1, e1], dtype=float)
data2 = np.array([r2, e2], dtype=float)

#print(np.allclose(data1, data2, rtol = 0.01))
diff = list(set(t1) - set(t2))
print(len(diff))
print(diff)

for a in t2:
    if a not in t1:
        print(a)

"""for a in diff:
    state1, state2 = parse_transition(a)
    for b in diff:
        if state1 in b and state2 in b and not (a == b):
            print(a + " and " + b)"""




