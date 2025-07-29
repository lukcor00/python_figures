import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as interp1d
from src import styles as st
from src import utils as ut
from pathlib import Path
from pprint import pprint
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LightSource
from scipy.interpolate import griddata
from skimage.measure import marching_cubes
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.interpolate import RegularGridInterpolator

def main():
    data = read_delimited_file_to_dict("linear_approx_3d.txt")
    Point = set_main_point()
    Other_points = set_other_points()
    D_points = []
    d_points = []
    phi_points = []
    alpha_points = []
    for i in data.keys():
        D, d, phi = get_Ddphi_from_name(i)
        D_points.append(D)
        d_points.append(d)
        phi_points.append(phi)
        alpha_points.append(tan_to_angle_deg(float(data[i][0])))
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    norm = Normalize(vmin=min(alpha_points), vmax=max(alpha_points))
    scatter = ax.scatter(
        D_points, d_points, phi_points,
        c = alpha_points,          
        cmap='jet',
        norm=norm,         
        s=30,             
        alpha=0.7,
        edgecolor='k',
        linewidth=0.3     
    )

    cbar = fig.colorbar(
        ScalarMappable(norm=norm, cmap='viridis'),
        ax=ax,
        shrink=0.7,
        label='$\\alpha$, °'
    )   
    
    add_default_plane(ax, "Z", D_points, d_points, phi_points, 20)
    add_default_plane(ax, "Z", D_points, d_points, phi_points, 45)
    add_default_plane(ax, "Z", D_points, d_points, phi_points, 60)
    # add_countours(ax, D_points, d_points, phi_points, alpha_points, 3)
    add_intrpol_plane(ax, D_points, d_points, phi_points, alpha_points, 32)
    ax.grid(True)
    ax.set_xlabel('$D$, мм', fontsize=12)
    ax.set_ylabel('$d$, мм', fontsize=12)
    ax.set_zlabel('$\\varphi$, °', fontsize=12)
    ax.view_init(elev=10, azim=60)
    plt.tight_layout()
    plt.show()

def add_default_plane(ax, axis, X, Y, Z, level, values = 1):
    match axis:
        case "X":
            Y, Z = np.meshgrid(Y, Z)
            X = np.full_like(Y, level)
        case "Y":
            X, Z = np.meshgrid(X, Z)
            Y = np.full_like(X, level)
        case "Z":
            X, Y = np.meshgrid(X, Y)
            Z = np.full_like(X, level)
    if values == 1:
        ax.plot_surface(
            X, Y, Z,
            linewidth=0.5,
            facecolor='gray',
            edgecolor='gray',
            alpha=0.2)
    else:
        ax.plot_surface(
            X, Y, Z,
            linewidth=0.5,
            facecolors=plt.cm.viridis(values),
            edgecolor='gray',
            alpha=0.2)
    return

def add_countours(ax, x, y, z, values, levels):
    points = np.zeros((21,3))
    values = np.array(values)
    for i in range(len(points)):
        points[i][0] = x[i]
        points[i][1] = y[i]
        points[i][2] = z[i]

    sorted_indices = np.lexsort((points[:, 2], points[:, 1], points[:, 0]))
    points_sorted = points[sorted_indices]
    values_sorted = values[sorted_indices]

    x_grid = np.unique(points_sorted[:, 0])
    y_grid = np.unique(points_sorted[:, 1])
    z_grid = np.unique(points_sorted[:, 2])

    grid_values = np.full((len(x_grid), len(y_grid), len(z_grid)), np.nan)
    for (x, y, z), val in zip(points_sorted, values_sorted):
        i = np.where(x_grid == x)[0][0]
        j = np.where(y_grid == y)[0][0]
        k = np.where(z_grid == z)[0][0]
        grid_values[i, j, k] = val

    interp = RegularGridInterpolator(
        (x_grid, y_grid, z_grid),
        grid_values,
        method='nearest'
    )

    X_vis = np.linspace(min(x_grid), max(x_grid), 30) 
    Y_vis = np.linspace(min(y_grid), max(y_grid), 30) 
    Z_vis = np.linspace(min(z_grid), max(z_grid), 30) 
    X, Y, Z = np.meshgrid(
        X_vis, Y_vis, Z_vis)
    
    V = interp((X, Y, Z))
    V = np.nan_to_num(V, nan=np.nanmin(V))

    levels = np.linspace(np.min(V), np.max(V), levels)
    print(levels)
    for level in levels:
        try:
            verts, faces, _, _ = marching_cubes(V, level=level, spacing=(X_vis[1]-X_vis[0], Y_vis[1]-Y_vis[0], Z_vis[1]-Z_vis[0]))
            verts = verts + [X_vis[0], Y_vis[0], Z_vis[0]]  # Сдвигаем в исходные координаты
            ax.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2], alpha=0.5)
            verts, faces, _, _ = marching_cubes(V, level=level)
            verts[:, 0] = X[(verts[:, 0]).astype(int)]
            verts[:, 1] = Y[(verts[:, 1]).astype(int)] 
            verts[:, 2] = Z[(verts[:, 2]).astype(int)]
            mesh = Poly3DCollection(verts[faces], alpha=0.5, edgecolor='k')
            mesh.set_facecolor(plt.cm.viridis(level / np.max(levels)))
            ax.add_collection3d(mesh)
        except Exception as e:
            print(f"Не удалось построить изоповерхность для level={level}: {e}")

def add_intrpol_plane(ax, x, y, z, values, level):
    points = np.zeros((21,3))
    values = np.array(values)
    for i in range(len(points)):
        points[i][0] = x[i]
        points[i][1] = y[i]
        points[i][2] = z[i]

    sorted_indices = np.lexsort((points[:, 2], points[:, 1], points[:, 0]))
    points_sorted = points[sorted_indices]
    values_sorted = values[sorted_indices]

    x_grid = np.unique(points_sorted[:, 0])
    y_grid = np.unique(points_sorted[:, 1])
    z_grid = np.unique(points_sorted[:, 2])

    grid_values = np.full(
        (len(x_grid), len(y_grid), len(z_grid)), 
        np.nan)
    for (x, y, z), val in zip(points_sorted, values_sorted):
        i = np.where(x_grid == x)[0][0]
        j = np.where(y_grid == y)[0][0]
        k = np.where(z_grid == z)[0][0]
        grid_values[i, j, k] = val

    interp = RegularGridInterpolator(
        (x_grid, y_grid, z_grid),
        grid_values,
        method='nearest'
    )

    X_vis = np.linspace(min(x_grid), max(x_grid), 30) 
    Y_vis = np.linspace(min(y_grid), max(y_grid), 30) 
    Z_vis = np.linspace(min(z_grid), max(z_grid), 30) 
    X, Y = np.meshgrid(
        X_vis, Y_vis)
    V = interp((X, Y, np.full_like(X, level)))
    norm = Normalize(vmin=np.min(V), vmax=np.max(V))
    # print(V)
    ax.plot_surface(X, Y, np.full_like(X, level), 
                    facecolors=plt.cm.viridis(norm(V)), 
                    shade=False)


def set_main_point()->list:
    return [1.8, 77]
def set_other_points()->list:
    return [
    [1.8, 77],
    [2.5, 85],
    [4, 100],
    [5, 120]
]
def tan_to_angle_deg(tan_value : float):
    rad_value = -np.atan(tan_value)
    deg_value = rad_value / np.pi * 180
    return deg_value
def read_delimited_file_to_dict(filepath, delimiter='\t'):
    data_dict = {}
    with open(filepath, 'r', encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(delimiter)
                key = parts[0].strip()
                value = [parts[1].strip(), parts[2].strip()]
                data_dict[key] = value
    return data_dict
def scale_tan_alpha(tan_alpha, n1, n2):
    return tan_alpha*(n2/n1)**2
def scale_to_regime():
    pass
def get_Ddphi_from_name(name : str) -> list[3]:
    parts = name.split('-')[2:]
    for i in range(len(parts)):
        parts[i] = int(parts[i])
    return parts

if __name__=='__main__':
    main()
