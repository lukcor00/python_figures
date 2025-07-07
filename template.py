#%%
import numpy as np
import matplotlib.pyplot as plt
from src import styles as st
from src import utils as ut
from pathlib import Path

## global variables by default
WORKING_DIRECTORY = Path(__file__).parent
FIGURE_DIRECTORY = WORKING_DIRECTORY / "figures" 
DATA_DIRECTORY = WORKING_DIRECTORY / "data"
fig, ax = plt.subplots()


## global variables to set
main_style_config = {}
x_tick, y_tick = 1, 10
x_lim, y_lim = (0, 8), (40, 140)


## basic configuration
st.basic_style()
st.main_style(main_style_config)
st.set_ticks(ax, x_tick, y_tick)
st.set_limits(ax, x_lim, y_lim)
st.set_legend(ax)


## main
plt.show()

