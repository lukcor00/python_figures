#%%
import numpy as np
import matplotlib.pyplot as plt
from src import styles as st
from src import utils as ut
from pathlib import Path

def convert_to_mmHg(p):
    return -p*1035*1000/13600/9.81

def convert_to_lmin(q):
    return -q*60000

def prepare_point_data(X, Y):
    X = np.array(X)
    Y = np.array(Y)
    X = convert_to_lmin(X)
    Y = convert_to_mmHg(Y)
    return X, Y

def style(ax):
    main_style_config = {}
    x_tick, y_tick = 1, 10
    x_lim, y_lim = (0, 6), (40, 120)
    st.basic_style()
    st.main_style(main_style_config)
    st.set_ticks(ax, x_tick, y_tick)
    st.set_limits(ax, x_lim, y_lim)
    ax.set_xlabel(r'$\dot{V}$, л/мин')
    ax.set_ylabel(r'$\Delta p$, мм рт.ст.')

def list_of_substrings_in_string(str, str_list):
    return [s for s in str_list if s in str]

def one_param_sample(input, start_index, end_index):
    used_data = []
    result = []
    for i in input:
        if i in used_data:
            continue
        data = []
        list_of_substring = [i[0:start_index], i[end_index: -1]]
        for j in input:
            if j in used_data:
                continue
            if list_of_substring == list_of_substrings_in_string(j, list_of_substring):
                if j in used_data:
                    continue
                data.append(j)
                data.append(j+"ЛН")
        if len(data) <= 2:
            continue
        used_data += data
        result.append(data)
    return result

def export_figures(input, export_dir="figures/"):
    data, keys, data_enumeration = input
    for i in keys.keys():
        for j in keys[i]:
            for k in j:
                clor = data_enumeration[k]
                if "ЛН" in clor:
                    clor = clor[:-3]
                clor = clor[1:]
                clor = int(clor)
                red = clor % 5 * 35/255
                green = clor % 7 * 25/255
                blue = clor % 3 * 56/255
                if "ЛН" in data_enumeration[k]:
                    ax.plot(data[k][0], data[k][1], linewidth=2, label=data_enumeration[k], color=(red+0.3, green+0.3, blue+0.3), linestyle='--')
                else:
                    ax.plot(data[k][0], data[k][1], label=data_enumeration[k], color=(red, green, blue))
            ax.plot([1.8], [77], marker="X", markersize=10, linestyle='None',     label='Раб. Т')
            style(ax)
            st.set_legend(ax)
            plt.savefig(f"{export_dir}/{i}{data_enumeration[j[0]]}_scaled")
            plt.cla()
        # plt.show()

def scale_to_regime(coeffs, f1, point, max_power):
    X = point[0] 
    Y = point[1]
    new_coeffs = []
    n_coeffs = ut.prepare_coeffs(coeffs, X, Y)
    n = ut.get_roots(n_coeffs)
    n = ut.find_nearest(n, 1)
    for i in range(max_power+1):
        new_coeffs.append(coeffs[i] * (pow(n,2)/pow(n, i)))
    return new_coeffs, n*f1
        
## global variables by default
WORKING_DIRECTORY = Path(__file__).parent
FIGURE_DIRECTORY = WORKING_DIRECTORY / "figures" 
DATA_DIRECTORY = WORKING_DIRECTORY / "data"
fig, ax = plt.subplots()

## main
INPUT_FILE = open(f"{DATA_DIRECTORY}/p.txt", "r")
INPUT_DATA = {}
INPUT_DATA = ut.read_data_unstructured(INPUT_FILE)
INPUT_FILE.close()
INPUT_DATA_SORTED_KEYS = ut.sort_keys(INPUT_DATA)
INPUT_DATA_SORTED_ENUMERATION = {}
for counter, key in enumerate(INPUT_DATA_SORTED_KEYS):
    INPUT_DATA_SORTED_ENUMERATION[key] = f"№{counter+1}"
# ax.plot([1.2, 1.8, 2.5, 4, 5], [70, 77, 85, 100, 120], marker="X", markersize=10, linestyle='None', label='Рабочие точки')

prepared_data = {}
prepared_data_linear = {}
f = []
equation_export_data = []
for i in INPUT_DATA_SORTED_KEYS:
    X, Y = prepare_point_data(INPUT_DATA[i][0], INPUT_DATA[i][1])
    polynom_coeffs = ut.execute(Y, X)
    polynom_coeffs, f2 = scale_to_regime(polynom_coeffs, 10000, [1.8, 77], 3)
    f.append(f2)
    equation = f"P = {polynom_coeffs[0]} + {polynom_coeffs[1]}*V + {polynom_coeffs[2]}*(V)^2 + {polynom_coeffs[3]}*(V)^3"
    equation_export_data.append(equation)
    X_approx = np.arange(0, 8, 0.4)
    X_linear_approx = np.arange(0.3, 3, 0.3)
    Y_approx = []
    Y_linear_approx = []
    for point in X_approx:
        Y_approx.append(ut.calculate_polynom(point, polynom_coeffs))
    for point in X_linear_approx:
        Y_linear_approx.append(ut.calculate_polynom(point, polynom_coeffs))
    prepared_data[i] = [X_approx, Y_approx]
    prepared_data_linear[i] = [X_linear_approx, Y_linear_approx]

for i in range(len(f)):
    print(f'{equation_export_data[i]:.2f}\t{str(f[i]):.2f}')

linear_data = {}
for i in INPUT_DATA_SORTED_KEYS:
    X, Y = prepared_data_linear[i][0], prepared_data_linear[i][1]
    polynom_coeffs = ut.execute(Y, X, polinom_power=1)
    X_approx = np.arange(0.3, 3, 0.3)
    Y_approx = []
    new_key = i + "ЛН"
    for point in X_approx:
        Y_approx.append(ut.calculate_polynom(point, polynom_coeffs))
    linear_data[new_key] = [X_approx, Y_approx]

export_keys = {}
export_keys["SD"] = one_param_sample(INPUT_DATA_SORTED_KEYS, 6, 8)
export_keys["HD"] = one_param_sample(INPUT_DATA_SORTED_KEYS, 8, 10)
export_keys["HPhi"] = one_param_sample(INPUT_DATA_SORTED_KEYS, -3, -1)

export_data = linear_data | prepared_data
for counter, i in enumerate(linear_data.keys()): 
    INPUT_DATA_SORTED_ENUMERATION[i] = f"№{counter+1} ЛН"
    INPUT_DATA_SORTED_KEYS.append(i)

export_figures([export_data, export_keys, INPUT_DATA_SORTED_ENUMERATION])

# %%
