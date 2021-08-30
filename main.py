# %%
from visualize import plot_2_tiff
from utils import draw_all_roms, draw_interception, perform_all
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np


# %%
def perform_overlall_rom(ft=18, vertical=True):
    xlab = 'Distance fingertip to MCP joint in x-direction [mm]'
    ylab = 'Distance fingertip to MCP joint in y-direction [mm]'

    fig = plt.figure(figsize=(8, 24)) if vertical else plt.figure(
        figsize=(24, 8))

    loc_diff = 3
    plt.subplot(311) if vertical else plt.subplot(131)
    plt.title('ROM Index Finger Subject 1', fontsize=ft)
    plt.ylabel(ylab, fontsize=ft)
    plt.ylabel(ylab, fontsize=ft) if vertical else plt.xlabel(
        xlab, fontsize=ft)
    draw_all_roms('niko_rom.txt', 1, color='blue')

    plt.legend(fontsize=ft-loc_diff)

    plt.subplot(312) if vertical else plt.subplot(132)
    plt.title('ROM Index Finger Subject 2', fontsize=ft)
    plt.ylabel(ylab, fontsize=ft) if vertical else plt.xlabel(
        xlab, fontsize=ft)
    draw_all_roms('tina_rom.txt', 1, color='green')
    plt.legend(fontsize=ft-loc_diff)

    plt.subplot(313) if vertical else plt.subplot(133)
    plt.title('ROM Index Finger Subject 3', fontsize=ft)
    plt.xlabel(xlab, fontsize=ft)
    plt.ylabel(ylab, fontsize=ft) if vertical else plt.xlabel(
        xlab, fontsize=ft)
    draw_all_roms('chrissi_rom.txt', 1, color='orangered')
    plt.legend(fontsize=ft-loc_diff)

    plot_2_tiff(fig, 'ROM_plot')

    offset = 200
    img = np.array(Image.open('results/ROM_plot.tiff'))
    sh = img.shape
    img = img[200:sh[0]-offset, :, :]
    img = Image.fromarray(img)
    img.save(f'./results/ROM_plot.tiff', bbox_inches='tight', pad_inches=0)


perform_overlall_rom(vertical=True)
# %%

if __name__ == '__main__':

    filenames = [
        'niko_ohne_inter.txt',
        'tina_ohne_inter.txt',
        'chrissi_ohne_inter.txt'
    ]

    colors = [
        'blue',
        'green',
        'orangered'
    ]

    plot = plt.figure(figsize=(12, 10))

    for filename, color in zip(filenames, colors):
        plot = perform_all(filename, color, plot)

    ax = plt.subplot(2, 3, 6)
    handles, labels = ax.get_legend_handles_labels()
    plot.legend(handles, labels, loc='upper center', ncol=3, fontsize=14)
    plot_2_tiff(plot, 'measurements_real')
    plot.show()

    draw_interception()

    perform_overlall_rom()

# %%
plot = plt.figure(figsize=(12, 10))
deglim = [-80, 20]
mlim = [-0.15, 0.1]
plot = draw_interception(filename='niko_inter_many.txt', idxs=[14, 15, 16])
for ind in range(1, 7):
    plt.subplot(2, 3, ind)
    plt.ylim(deglim)
    if ind > 3:
        plt.ylim(mlim)
    plt.vlines(7, -100, 30, linestyles='-.', linewidth=1, color='black')
    plt.vlines(22, -100, 30, linestyles='-.', linewidth=1, color='black')
ax = plt.subplot(2, 3, 6)
handles, labels = ax.get_legend_handles_labels()
plot.legend(handles, labels, loc='upper center', ncol=1, fontsize=14)
plot_2_tiff(plot, 'interception')
# %%

# %%
arr = [142, 145, 145, 161, 149, 170, 160]