import matplotlib.pyplot as plt
import numpy as np


def gaussian (x,a,w,center):
    exponent = -0.5 * np.power((x-center)/w,2)
    y = a*np.exp(exponent)
    return y


def create_gaussian_peak(a,w,peak_center,x_data,peak_range = 3):
    # a = Amplitude of peak
    # w = width of peak
    # peak_center = center of peak
    # peak_range = how peak width gaussian should be implemented
    x_data = np.array(x_data)
    y = np.zeros(x_data.shape)
    index = np.where(x_data >= peak_center-(peak_range*w),x_data,0)
    index = np.where(x_data <= peak_center+(peak_range*w),index,0)
    index = np.where(index > 0,True,False)
    y = np.where(index,y+gaussian(a,w,peak_center,x_data),y)
    return y


def add_peaks_to_data_set(x_data, centers, intensites):
    y_data = np.zeros(x_data.shape)
    for i in range(len(centers)):
        #y_data += create_gaussian_peak(intensites[i], 1, centers[i], x_data)
        y_data += gaussian(x_data, intensites[i], 0.3, centers[i])

    return y_data


def add_errors(x_data, centers, errors):
    error_data = np.zeros(x_data.shape)
    for i in range(len(centers)):
        center = centers[i]
        index_high, index_low =0, 0
        for j in range(len(x_data)):
            if x_data[j] > center:
                index_high = j
                index_low = j - 1
                if j == 0:
                    index_low = j
                break
        if index_high or index_low:
            high = x_data[index_high]
            low = x_data[index_high]
            if abs(high - center) > abs(low -center):
                error_data[index_low] = errors[i]
            else:
                error_data[index_high] = errors[i]
        else:
            error_data[0] = errors[i]
    return error_data


def create_graphs(x1, A1, e1, x2, A2, e2):
    fig, axis = plt.subplots(1)
    x_data = np.arange(0, 2000, 0.1)
    y1 = add_peaks_to_data_set(x_data, x1, A1)
    y2 = add_peaks_to_data_set(x_data, x2, A2)
    errors1 = add_errors(x_data, x1, e1)
    errors2 = add_errors(x_data, x2, e2)
    axis.errorbar(x_data, y1, yerr=errors1, ecolor="g")
    axis.plot(x_data, y2)
    plt.show()


def create_bar_graph(experimental, calculated_exp, calculated_linear, calculated_quad, calculated_const, title,
                     x_axis="Transition", y_axis="Intensity (arbitrary units)", literature=None, errors=None):
    fig, ax = plt.subplots(1)
    transitions = []
    if not literature:
        intensity = []
        error = []
        intensity_exp = []
        intensity_linear = []
        intensity_quad = []
        intensity_const = []
        for transition in experimental:
            transitions.append(transition)
            intensity_exp.append(calculated_exp[transition])
            intensity_linear.append(calculated_linear[transition])
            intensity_const.append(calculated_const[transition])
            intensity_quad.append(calculated_quad[transition])
            intensity.append(experimental[transition])
            if errors is not None:
                error.append(errors[transition])
        if not error:
            error = [0]*len(intensity)

        x = np.arange(0, 3 * len(intensity), 3)
        width = 0.4
        bar1 = ax.bar(x, intensity, yerr=error, width=width, label="Experimental", capsize=3)
        bar2 = ax.bar(x + width, intensity_exp, width=width, label="Calculated: exponential")
        bar3 = ax.bar(x + 2*width, intensity_linear, width=width, label="Calculated: linear")
        bar4 = ax.bar(x + 3*width, intensity_quad, width=width, label="Calculated: quadratic")
        bar5 = ax.bar(x + 4*width, intensity_const, width=width, label="Calculated: constant")

        exp_val = 100*sum(np.abs((np.array(intensity_exp)-np.array(intensity))/np.array(intensity_exp)))/len(intensity)
        quad_val = 100*sum(np.abs((np.array(intensity_quad) - np.array(intensity))/ np.array(intensity_quad)))/len(intensity)
        linear_val = 100*sum(np.abs((np.array(intensity_linear) - np.array(intensity))/ np.array(intensity_linear)))/len(intensity)
        const_val = 100*sum(np.abs((np.array(intensity_const)-np.array(intensity) )/ np.array(intensity_const)))/len(intensity)

        print({"Exponential": exp_val, "Quadratic": quad_val, "Linear": linear_val, "const_val": const_val})



    """
    else:
        intensity_exp = []
        intensity_calc = []
        intensity_lit = []
        for transition in experimental:
            transitions.append(transition)
            intensity_calc.append(calculated[transition])
            intensity_exp.append(experimental[transition])
            intensity_lit.append(literature[transition])

        width = 0.3
        ax.bar(np.arange(len(intensity_calc)), intensity_calc, width=width, label="Calculated")
        ax.bar(np.arange(len(intensity_exp)) + width, intensity_exp, width=width, label="Experimental")
        ax.bar(np.arange(len(intensity_lit)) + 2*width, intensity_lit, width=width, label="Literature")
    """
    ax.set_title(title)
    ax.set_ylabel(y_axis)
    ax.set_xlabel(x_axis)
    ax.set_xticks(x + 2*width, transitions)
    plt.legend(loc="best")
    plt.show()