#%%
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Rectangle
from matplotlib.ticker import MultipleLocator
from pathlib import Path

WORKING_DIRECTORY = Path(__file__).parent
DATA_DIRECTORY = WORKING_DIRECTORY / "data"
FILE = DATA_DIRECTORY / "V.txt"
# Чтение данных из файла (предполагается CSV-формат)
data = pd.read_csv(FILE)  # замените "data.txt" на имя вашего файла

# Создаем фигуру и оси
fig, ax = plt.subplots(figsize=(10, 6))

# Список для хранения прямоугольников (для легенды)
rectangles = []

# Проходим по всем строкам в данных
for _, row in data.iterrows():
    # Получаем параметры прямоугольника
    name = row["name"]
    x_min, x_max = row["Vmin"], row["Vmax"]
    y_min, y_max = row["BSAmin"], row["BSAmax"]
    width = x_max - x_min
    height = y_max - y_min
    
    # Создаем прямоугольник с уникальным цветом и прозрачностью
    rect = Rectangle(
        (x_min, y_min), 
        width, 
        height, 
        linewidth=5, 
        edgecolor=f"C{len(rectangles)}",  # автоматический выбор цвета
        facecolor=f"C{len(rectangles)}", 
        alpha=0.3, 
        label=name
    )
    
    # Добавляем прямоугольник на график и в список
    ax.add_patch(rect)
    rectangles.append(rect)

rect=Rectangle(
        (0.3, 0.2), 
        1.9, 
        0.6, 
        linewidth=1, 
        fill=None, 
        hatch='/', 
        color="lime",
        label="рабочий диапазон №1")
ax.add_patch(rect)
rectangles.append(rect)
rect=Rectangle(
        (0.3, 0.8), 
        2.7, 
        0.7, 
        linewidth=1, 
        fill=None, 
        hatch='/', 
        color="b",
        label="рабочий диапазон №2")
ax.add_patch(rect)
rectangles.append(rect)


# Настройка осей и легенды
ax.xaxis.set_major_locator(MultipleLocator(1)) 
ax.set_xlim(-0.1, data["Vmax"].max() + 0.1)  # +-0.1 для отступов
ax.set_ylim(data["BSAmin"].min() - 0.1, 1.8)
ax.set_xlabel(r'$\dot{V}$, л/мин')
ax.set_ylabel(r'BSA, $м^2$')
ax.axvline(x=1.8, color='purple', linestyle=':', linewidth=3, label='Подача рабочей точки')
ax.axvline(x=1.3,ymax=0.4, color='purple', linestyle=':', linewidth=3)
plt.axhline(y=0.2, color='r', linestyle='--', linewidth=2)
plt.axhline(y=1.5, color='r', linestyle='--', linewidth=2)
plt.axhline(y=0.8, color='r', linestyle='--', linewidth=2)
plt.axhline(y=1.5, color='r', linestyle='--', linewidth=2)
plt.axvline(x=2.2, ymin=0, ymax=0.4, color='g', linestyle='--', linewidth=2)
plt.axvline(x=0.3, color='g', linestyle='--', linewidth=2)
plt.axvline(x=3, color='g', linestyle='--', linewidth=2)
ax.text(1.8, 0, '1,8', ha='center', va='top')
ax.text(1.3, 0, '1,3', ha='center', va='top')
# ax.set_title("Зависимость ра")
ax.grid(True)

# Добавляем легенду
ax.legend(handles=rectangles)

plt.tight_layout()
plt.savefig('figures/BSA-V.jpg')
plt.show()
# %%
