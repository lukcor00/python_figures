import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from skimage.measure import marching_cubes  # или from scipy.ndimage import marching_cubes
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Пример данных (замените на свои)
np.random.seed(42)
points = np.random.rand(21, 3) * 10  # x, y, z в диапазоне [0, 10]
c = np.sin(points[:, 0]) + np.cos(points[:, 1]) + np.tan(points[:, 2] / 5)  # Пример c

# Создаем регулярную сетку
grid_size = 20
x_grid = np.linspace(min(points[:, 0]), max(points[:, 0]), grid_size)
y_grid = np.linspace(min(points[:, 1]), max(points[:, 1]), grid_size)
z_grid = np.linspace(min(points[:, 2]), max(points[:, 2]), grid_size)
X, Y, Z = np.meshgrid(x_grid, y_grid, z_grid)

# Интерполяция (заменяем NaN на 0 или ближайшее значение)
C_interp = griddata(points, c, (X, Y, Z), method='linear')
C_interp = np.nan_to_num(C_interp)  # Заменяем NaN на 0

# Альтернатива: method='nearest' (нет NaN, но менее гладко)
# C_interp = griddata(points, c, (X, Y, Z), method='nearest')

# Визуализация
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Изоповерхности
levels = np.linspace(np.min(c), np.max(c), 5)  # 5 уровней
for level in levels:
    try:
        verts, faces, _, _ = marching_cubes(C_interp, level=level)
        # Масштабируем вершины в исходные координаты
        verts[:, 0] = x_grid[(verts[:, 0]).astype(int)]
        verts[:, 1] = y_grid[(verts[:, 1]).astype(int)]
        verts[:, 2] = z_grid[(verts[:, 2]).astype(int)]
        mesh = Poly3DCollection(verts[faces], alpha=0.5, edgecolor='k')
        mesh.set_facecolor(plt.cm.viridis(level / np.max(levels)))
        ax.add_collection3d(mesh)
    except ValueError as e:
        print(f"Не удалось построить изоповерхность для уровня {level}: {e}")

# Исходные точки
ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=c, s=50, cmap='viridis', edgecolor='k')

# Настройки
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.colorbar(plt.cm.ScalarMappable(cmap='viridis'), ax=ax, label='Значение c')
plt.title('3D изоповерхности')
plt.show()