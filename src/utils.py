import pandas as pd
import numpy as np
from typing import List, Dict, Tuple

def read_data_csv(PATH : str):
    return pd.read_csv(PATH)

def is_empty_line(str : str):
    return not str.strip()

def is_header(line : str):
    if not line:
        return False
    first_char = line[0]
    if first_char.isdigit() or first_char in {'-', '.'}:
        return False
    return True

def extract_point_data(data : str) -> List[str]:
    return data.split("\t")
    
def sort_keys(dict):
    return sorted(dict.keys())

def get_LSM_matrix(X, max_power):
    coefficient_matrix = []
    for i in X:
        coefficient_line = []
        for j in range(max_power+1):
            coefficient_line.append(pow(i, j))
        coefficient_matrix.append(coefficient_line)
    return np.array(coefficient_matrix)

def calculate_polynom(x, coeffs : List[float]) -> float:
    result = 0
    for i in range(len(coeffs)):
        result += pow(x, i) * coeffs[i]
    return result

def read_data_unstructured(input):
    data = {}
    for i in input:
        if is_empty_line(i):
            continue
        if is_header(i):
            data[i] = [[],[]]
            header = i
            continue
        points = extract_point_data(i)
        X = float(points[0])
        Y = float(points[1])
        data[header][0].append(X)
        data[header][1].append(Y)
    return data
    

def file_clear(name):
    with open(name, 'w') as file:
        pass

def prepare_coeffs(coeffs, X, Y):
    new_coeffs = np.zeros((len(coeffs), 1))
    for i in range(len(coeffs)):
        new_coeffs[i] = (coeffs[i]*X**i)
    new_coeffs[2] -= Y
    return new_coeffs

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def get_roots(coeffs):
    new_coeffs = np.poly1d(coeffs.ravel())
    return new_coeffs.r

def execute(Y, X, polinom_power = 3):
    A = get_LSM_matrix(X, polinom_power)
    coeffs = np.linalg.lstsq(A, Y, rcond=None)[0]
    return coeffs