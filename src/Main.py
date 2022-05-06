from IntensityCalculator import IntensityCalculator
from ElementIntensities import Element
from Misc import parse_mudirac_file, State_objects_in_shell, parse_transition
import numpy as np
from Transition_Matrix import EnergyLevelTransitionMatrix
from Ldistribution_calculator import LdistributionCalculator
import matplotlib.pyplot as plt
import tkinter
from GUI import MuonicXrayCalculatorGUI
from graphs import create_graphs


path1 = r"C:\Users\Tolu\Documents\Mudirac data\mudirac_output_file\Gold.out"
path2 = r"C:\Users\Tolu\Documents\Mudirac_extension\Mudirac_data\Gold22.out"
path3 = r"C:\Users\Tolu\Documents\Mudirac_extension\Mudirac_data\Gold20_1.out"
path4 = r"C:\Users\Tolu\Documents\Mudirac_extension\Mudirac_data\Aluminium20.out"
path5 = r"C:\Users\Tolu\Documents\Mudirac_extension\Mudirac_data\Carbon20.out"
path6 = r"C:\Users\Tolu\Documents\Mudirac_extension\Mudirac_data\Gold16.out"
path7 = r"C:\Users\Tolu\Documents\Mudirac_extension\Mudirac_data\Gold20Ideal.out"
path8 = r"C:\Users\Tolu\Documents\Mudirac_extension\Mudirac_data\Iodine20Ideal.out"
path9 = r"C:\Users\Tolu\Documents\Mudirac_extension\Mudirac_data\Gold_40ideal.out"
path10 = r"C:\Users\Tolu\Documents\Mudirac_extension\Mudirac_data\Gold40_T.xr.out"
path11 = r"C:\Users\Tolu\Documents\Mudirac_extension\Mudirac_data\Iodine_40T.out"
path12 = r"C:\Users\Tolu\Documents\Mudirac_extension\Mudirac_data\Iodine_40Ideal.out"

#matrix = EnergyLevelTransitionMatrix(40, 1)
#matrix.read_from_file(path9, True)
#matrix.calculate_steady_state(100)
#a = matrix.steady_state
#a = matrix.transition_matrix+1
#a = np.log(np.abs(a))
#plt.plot(a)
#plt.imshow(a)
#plt.show()

#save_file = "Gold_output.txt"
save_file = "Gold_output_linear_20.txt"
#save_file = ""

#Gold = IntensityCalculator("quadratic", 20, path10, neural_net=True, params=[-0.01561566,  0.00111518])
#Gold.calculate_intensities()

#Gold = LdistributionCalculator(path9, "quadratic", 40, 1, True)
#ldistribution = Gold.get_Ldistribution(40, 20)
#print(ldistribution.parameters)

#gold = Element(path9, "linear", 20, 40, 20)
#gold.calculate_intensity(save_file)
#print(gold.intensity_calculator.ldistribution.parameters)
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
root = tkinter.Tk()
GUI = MuonicXrayCalculatorGUI(root)
GUI.pack()
root.wm_title("Muonic x-ray intensity calculator")
root.mainloop()
"""
A1 = [0.539315575, 0.138893002, 0.812821431, 0.630394309, 0.590660186, 0.748208731, 0.585820269, 1, 0.707175343]
x1 = [57.48766279, 84.3850765, 130.0393123, 216.0979856, 217.5551904, 399.8465051, 405.3630541, 870.2007695,
      899.3442365]
e1 = [3.33E-02, 1.32E-02, 3.45E-02, 2.98E-02, 2.72E-02, 3.35E-02, 2.76E-02, 5.28E-02, 4.39E-02]
e1 = [0]*len(x1)
A1 = [0.25833216, 0.066529748, 0.389341465, 0.301958874, 0.282926229, 0.358391982, 0.280607909, 0.479, 0.338736989]
x2 = [864.36, 381.354, 215.684, 129.837, 57.6772, 84.3869, 130.338, 217.144, 386.78, 892.96]
A2 = [1, 0.969735819, 0.94807018, 0.930047892, 0.895304828, 0.831697605, 0.826354682, 0.813141511, 0.788061505,
      0.740162557]
e2 = [0]*len(x2)
x2 = [864.36, 381.354, 215.684, 892.96, 386.78, 129.837, 217.144, 130.338, 84.1837, 57.6772]
A2 = [1, 0.896713185, 0.797605764, 0.758336782, 0.74359224, 0.702666854, 0.695577672, 0.632876542, 0.613077005, 0.530237197 ]
A2  = "0.482286006
0.432472221
0.384674099
0.365735218
0.358624132
0.338886391
0.335467378
0.3052275
0.295678461
0.25572598
"
A2 = A2.split("\n")
A2 = [float(x) for x in A2]
create_graphs(x1, A1, e1, x2, A2, e2)"""

