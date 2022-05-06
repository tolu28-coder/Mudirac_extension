from Transition_Matrix import EnergyLevelTransitionMatrix
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from Misc import normalise1d
import math
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split

from graphs import create_graphs, create_bar_graph
from Neural_net import NeuralNetwork

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
path12 = r"C:\Users\Tolu\Documents\Mudirac_extension\Mudirac_data\Silver_40ideal.out"

def linear(x):
    y = []
    for i in range(len(x)):
        y.append(2*int(math.ceil(x[i]/2)) + 1)
    return normalise1d(y)


def exponential(x, a):
    y = []
    for i in range(len(x)):
        k = int(math.ceil(x[i]/2))
        y.append((2*k + 1)*np.exp(a*k))
    return normalise1d(y)


def quadratic(x, a, b, c):
    y = []
    for i in range(len(x)):
        k = int(math.ceil(x[i] / 2))
        y.append(a + b*k + c*k*k)
    return normalise1d(y)

def constant(x):
    y = [1]*len(x)
    return normalise1d(y)


def efficiency(x):
    y = (-1.79 + (0.805*np.log(x)) + (-0.0711*np.log(x)*np.log(x)) )/x
    return y


k = 0.2771353
d = [-77756.2456934, 31574.78120367, -2192.49348176]

"""
matrix = EnergyLevelTransitionMatrix(40, 1)
matrix.read_from_file(path9, False)
matrix.calculate_steady_state(100)
#a = matrix.steady_state
#a = matrix.transition_matrix+1
#a = np.log(np.abs(a))
a = matrix.seperate_steady_state_by_n()
x, y = a[20]
fig, ax = plt.subplots(1)
ax.plot(x, normalise1d(y), label="Steady state")
ax.plot(x, quadratic(x, *d), label="Quadratic", ls="-.")
ax.plot(x, linear(x), label="Linear", ls= ":")
ax.plot(x, exponential(x, k), label="Exponential", ls="--")
ax.plot(x, constant(x), label="Constant")
ax.set_title("Steady state population at n=20")
ax.set_xlabel(r'Angular momentum(' + r'$\hslash$' ')')
ax.set_ylabel("Population")
plt.legend()
plt.show()
#fig, ax = plt.subplots(1)
#x = np.linspace(22, 1000, 1000)
#ax.plot(x, efficiency(x))
#ax.set_title("Efficiency of detector")
#ax.set_ylabel("Absolute Efficiency")
#ax.set_xlabel("Energy (KeV)")
plt.tick_params(left=False, right=False, labelleft=False, labelbottom=False, bottom=False)
#plt.show()"""

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
"""
#A2 = A2.split("\n")

#A2 = [float(x) for x in A2]
#create_graphs(x1, A1, e1, x2, A2, e2)

au_exp = {"O9-N7": 0.969735819, "P11-O9": 0.94807018, "Q13-P11": 0.930047892, "S17-R15": 1.726,
          "R14-Q12": 1.744, "P10-O8": 0.813141511, "O8-N6": 0.788061505, "N6-M4": 0.740162557}

au_real = {"O9-N7": 0.748208731, "P11-O9": 0.630394309, "Q13-P11": 0.812821431, "S17-R15": 0.539315575,
           "R14-Q12": 0.138893002, "P10-O8": 0.590660186, "O8-N6": 0.585820269, "N6-M4": 0.707175343}

au_errors= {"O9-N7": 0.0335, "P11-O9": 0.0298, "Q13-P11": 0.0345, "S17-R15": 0.033,
            "R14-Q12": 0.0132, "P10-O8": 0.0272, "O8-N6": 0.0276, "N6-M4": 0.0439}

au_const= {"O9-N7": 0.846227, "P11-O9": 0.715691, "Q13-P11": 1.146, "S17-R15": 0.818,
           "R14-Q12": 0.972, "P10-O8": 0.627, "O8-N6": 0.707, "N6-M4": 0.768}

au_linear = {"O9-N7": 0.896, "P11-O9": 0.797, "Q13-P11": 1.335, "S17-R15": 1.026,
               "R14-Q12": 1.177, "P10-O8": 0.695, "O8-N6": 0.743, "N6-M4": 0.758}

au_quad = {"O9-N7": 0.925, "P11-O9": 0.849, "Q13-P11": 1.463, "S17-R15": 1.190,
           "R14-Q12": 1.328, "P10-O8": 0.737, "O8-N6": 0.763, "N6-M4": 0.753}

c_real = {"M3-K1": 0.361, "N3-K1": 0.164, "O3-K1": 0.0974}
c_errors = {"M3-K1": 0.00770, "N3-K1": 0.00697, "O3-K1": 0.0595}
c_const = {"M3-K1": 0.115, "N3-K1": 0.0350, "O3-K1": 0.0206}
c_exp = {"M3-K1": 0.000412, "N3-K1": 0.00000608, "O3-K1": 0.0000000933}
c_linear = {"M3-K1": 0.0382, "N3-K1": 0.00722, "O3-K1": 0.00343}
c_quad = {"M3-K1": 0.0169, "N3-K1": 0.00201, "O3-K1": 0.000796}

cu_real = {"M5-L3":0.835, "M4-L2":0.397, "P7-M5":0.126, "O7-M5": 0.237, "O9-N7":0.108}
cu_errors = {"M5-L3":0.048, "M4-L2":0.0343, "P7-M5":0.0132, "O7-M5": 0.0137, "O9-N7":0.0110}
cu_const = {"M5-L3":0.686, "M4-L2":0.416, "P7-M5":0.0198, "O7-M5": 0.0748, "O9-N7":0.883}
cu_exp = {"M5-L3":0.607, "M4-L2":0.344, "P7-M5":0.00000738, "O7-M5": 0.00169, "O9-N7":1.01}
cu_linear = {"M5-L3":0.641, "M4-L2":0.384, "P7-M5":0.00926, "O7-M5": 0.0449, "O9-N7":0.935}
cu_quad = {"M5-L3":0.618, "M4-L2":0.368, "P7-M5":0.00424, "O7-M5": 0.0276, "O9-N7": 0.955}

ag_real = {"P11-O9": 0.429, "N7-N5": 0.541, "N6-N4": 0.354, "M5-L3": 0.646, "M4-L2": 0.388}
ag_errors = {"P11-O9": 0.0096, "N7-N5": 0.0142, "N6-N4": 0.0171, "M5-L3": 0.0263, "M4-L2": 0.0246}
ag_const = {"P11-O9": 1.583, "N7-N5": 1.178, "N6-N4": 0.897, "M5-L3": 1.408, "M4-L2": 0.866}
ag_exp = {"P11-O9": 1.815, "N7-N5": 1.03, "N6-N4": 0.759, "M5-L3": 1.0869, "M4-L2": 0.640}
ag_linear = {"P11-O9": 1.663, "N7-N5": 1.115, "N6-N4": 0.841, "M5-L3": 1.25, "M4-L2": 0.758}
ag_quad = {"P11-O9": 1.712, "N7-N5": 1.081, "N6-N4": 0.809, "M5-L3": 1.178, "M4-L2": 0.705}


pb_real = {"P11-09": 1.313, "O9-N7":0.797, "O8-N6":0.709, "N6-M4": 0.744}
pb_errors = {"P11-09": 0.0659, "O9-N7":0.0322, "O8-N6":0.0296, "N6-M4": 0.0395}
pb_const = {"P11-09": 1.343, "O9-N7":0.847, "O8-N6":0.707, "N6-M4": 0.770}
pb_exp = {"P11-09": 1.761, "O9-N7":0.970, "O8-N6":0.789, "N6-M4": 0.740}
pb_linear = {"P11-09": 1.333, "O9-N7":0.800, "O8-N6":0.665, "N6-M4": 0.678}
pb_quad = {"P11-09": 1.583, "O9-N7":0.923, "O8-N6":0.762, "N6-M4": 0.752}

si_real ={"P5-L3": 0.228,"L3-K1": 1.278, "M3-K1": 0.225}
si_errors ={"P5-L3": 0.00378,"L3-K1": 0.0158, "M3-K1": 0.0116}
si_const ={"P5-L3": 0.00671,"L3-K1": 1.195, "M3-K1": 0.0379}
si_exp ={"P5-L3": 0.0000000338,"L3-K1": 1.073, "M3-K1": 0.00015}
si_linear ={"P5-L3": 0.0025,"L3-K1": 1.125, "M3-K1": 0.0150}
si_quad ={"P5-L3": 0.000775,"L3-K1": 1.096, "M3-K1": 0.00627}




#create_bar_graph(si_real, si_exp, si_linear, si_quad, si_const,  "Silicon Muonic Xray Intensities", errors=si_errors)
#create_bar_graph(exp, calc_linear, "Muonic Xray from Gold with linear l-distribution")

"""
# Testing neural net
x = []
y = []
neural_net = NeuralNetwork(path12)
neural_net.process_data()
input1, output1 = neural_net.training_input, neural_net.training_output
train_x, test_x, train_y, test_y = train_test_split(input1, output1, test_size=0.25)
for hidden in range(1, 41):
    x.append(hidden)
    neural_net = NeuralNetwork(path12, hidden=hidden)
    #neural_net.process_data()
    #input1, output1 = neural_net.training_input, neural_net.training_output
    #train_x, test_x, train_y, test_y = train_test_split(input1, output1, test_size=0.25)
    neural_net.neural_net.fit(train_x, train_y)
    a = neural_net.neural_net.score(test_x, test_y)
    #print(a)
    y.append(a)
fig, ax = plt.subplots(1)
ax.plot(x, y)
ax.set_title("Effect of changing size of hidden layers")
ax.set_xlabel("Size of hidden layer")
ax.set_ylabel("Perfomance")
plt.show()
"""


def exp_perform(x, a, b, c):
    return a*np.exp(b*x)  + c


def factorial(x):
    n = 1
    for i in range(1, int(x)+1):
        n = n*i
    return n


def quatric(x, a, b):
    return a*np.power(x, 4) + b



def fact_perform(x, a, b):
    y = []
    for i in x:
        y.append(a*factorial(i) + b)
    return np.array(y)

fig, ax = plt.subplots(1)
x = np.array(range(2,29,2), dtype="int32")

y = np.array([0.5782499313354492, 1.3876409530639648, 1.2508745193481445, 1.6396598815917969, 2.2722620964050293,
              3.110476016998291, 4.373539924621582, 6.88287091255188, 10.084136962890625, 15.05847430229187,
              23.928719520568848, 42.479217767715454, 79.77801895141602, 171.88315796852112])

popt_exp, pcov_exp = curve_fit(exp_perform, x, y)
popt_fact, pcov_fact = curve_fit(fact_perform, x, y)
popt, pcov = curve_fit(quatric, x, y)

ax.plot(x, y, label="Measured data", linestyle="", marker=".")
ax.plot(x, exp_perform(x, *popt_exp), label="Fitted function: Exponential")
#ax.plot(x, quatric(x, *popt), label="Fitted function: quatric")
ax.set_xlabel("Energy Levels n to calculate")
ax.set_ylabel("Time taken to calculate (seconds)")
ax.set_title("Time complexity of Mudirac software")
print(popt_exp)
print(exp_perform(40, *popt_exp))
print(exp_perform(50, *popt_exp))
plt.legend()
plt.show()


