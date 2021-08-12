# %%
from visualize import plot_2_tiff
from utils import draw_all_roms, draw_interception, perform_all
from matplotlib import pyplot as plt


# %%

fig = plt.figure(figsize=(24, 8))
plt.subplot(131)
plt.ylabel('Distance fingertip to MCP joint in y-direction [mm]')
draw_all_roms('niko_rom.txt', 1, color='blue')
plt.xlabel('Distance fingertip to MCP joint in x-direction [mm]')
plt.subplot(132)
plt.xlabel('Distance fingertip to MCP joint in x-direction [mm]')
draw_all_roms('tina_rom.txt', 0, color='green')
plt.subplot(133)
plt.xlabel('Distance fingertip to MCP joint in x-direction [mm]')
draw_all_roms('chrissi_rom.txt', 1, color='orangered')
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

# %%
draw_interception(idxs=[14])
# %%
plt.figure(figsize=(12, 10))
draw_all_roms('tina_rom.txt', 1, color='green')

# %%
