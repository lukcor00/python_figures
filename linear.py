#%%
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as interp1d
from src import styles as st
from src import utils as ut
from pathlib import Path
from pprint import pprint
st.basic_style()

def list_of_substrings_in_string(str, str_list):
    return [s for s in str_list if s in str]

def one_param_sample(input, start_index, end_index):
    used_data = []
    result = []
    for i in input:
        data = []
        if i in used_data:
            continue
        list_of_substring = [i[:start_index], i[end_index:]]
        for j in input:
            if list_of_substring == list_of_substrings_in_string(j, list_of_substring):
                data.append(j)
        if len(data) < 3:
            continue
        used_data += data
        result.append(data)
    return result

def export_figures(input, export_dir="figures/"):
    data, keys, data_enumeration = input
    for i in keys.keys():
        for j in keys[i]:
            if len(j) < 6:
                continue
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

def read_delimited_file_to_dict(filepath, delimiter='\t'):
    data_dict = {}
    with open(filepath, 'r', encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(delimiter, 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    data_dict[key] = value
    return data_dict

def tan_to_angle_deg(tan_value : float):
    rad_value = -np.atan(tan_value)
    deg_value = rad_value / np.pi * 180
    return deg_value

def graph(dict, data, labelX, labelY, rangeX, rangeY, tag, export_dir="figures/"):
    nomer = {}
    counter = 1
    for i in data.keys():
        nomer[i] = counter
        counter += 1
    X = np.array([1, 2, 3])
    X_fit = np.linspace(X.min(), X.max(), 100)
    for i in dict:
        names = ''
        for j in i:
            names += '№' + str(nomer[j]) + ' '
        X, Y = [1, 2, 3], []
        for j in i:
            Y.append(tan_to_angle_deg(float(data[j])))
        polynom = np.poly1d(np.polyfit(X, Y, 2))
        Y_fit = polynom(X_fit) 
        plt.plot(X_fit, Y_fit, label=names)
    plt.legend(frameon=False)
    plt.xticks(X, rangeX)
    plt.ylim(rangeY)
    plt.xlabel(labelX)
    plt.ylabel(labelY)
    plt.grid(0)
    plt.savefig(f"{export_dir}/{tag}")
    plt.show()
    pass

data = read_delimited_file_to_dict("linear_approx.txt")

export_keys = {}
export_keys["SD"] = one_param_sample(data, 6, 8)
export_keys["HD"] = one_param_sample(data, 9, 11) 
export_keys["HPhi"] = one_param_sample(data, -3, -1)

yRange = [75, 88]
graph(export_keys["HPhi"], data, '$\\varphi$, °', '$\\alpha$,°', [20, 45, 60], yRange, "HPhi")
graph(export_keys["HD"], data, '$d$, мм', '$\\alpha$,°', [8, 9, 10], yRange, "HD")
graph(export_keys["SD"], data, '$D$, мм', '$\\alpha$,°', [12, 13, 14], yRange, "SD")

#%%