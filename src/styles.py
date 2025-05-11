#%%
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.ticker as ticker

def basic_style():
    rcParams.update({
        'font.family': 'serif',         
        'font.serif': 'Times New Roman',
        'font.size': 14,                
        'axes.titlesize': 16,           
        'axes.labelsize': 14,           
        'xtick.labelsize': 12,          
        'ytick.labelsize': 12,          
        'legend.fontsize': 10,          
        'figure.figsize': (8.268, 11.693/2),       
        'grid.alpha': 1,                
        'axes.grid': True,              
        'savefig.dpi': 300,             
        'savefig.bbox': 'tight',        
        'mathtext.fontset': 'stix',     
    }) 

def main_style(*pairs):
    for pair in pairs:
        if len(pair) != 0:
            raise ValueError(f"Tuple {pair} is not a pair")
    basic_style()
    for pair in pair:
        rcParams.update({pair[0] : pair[1]})
    
def set_ticks(ax, x_step=None, y_step=None):
    if x_step:
        ax.xaxis.set_major_locator(ticker.MultipleLocator(x_step))
    if y_step:
        ax.yaxis.set_major_locator(ticker.MultipleLocator(y_step))

def set_limits(ax, xlim=None, ylim=None):
    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)
        
def set_legend(ax):
    ax.legend()
 

def main():
    
    plt.ion()
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [1, 4, 9, 16], label="arbuz")
    
    basic_style()
    
    main_style({})
    
    set_ticks(ax, x_step=0.5, y_step=1)
    set_legend(ax)
    set_limits(ax, xlim=(0,5), ylim=(0, 20))
    plt.ioff()
    
if __name__=="__main__":
    main()