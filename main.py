# %%
from visualize import plot_2_tiff
from utils import draw_all_roms, draw_interception, perform_all
from matplotlib import pyplot as plt


# %%
def perform_overlall_rom(ft=16):
    xlab = 'Distance fingertip to MCP joint in x-direction [mm]'
    ylab = 'Distance fingertip to MCP joint in y-direction [mm]'
    fig = plt.figure(figsize=(24, 8))

    plt.subplot(131)
    plt.title('ROM Finger 1')
    plt.ylabel(ylab, fontsize=ft)
    draw_all_roms('niko_rom.txt', 1, color='blue')
    plt.xlabel(xlab, fontsize=ft)

    plt.subplot(132)
    plt.title('ROM Finger 2')
    plt.xlabel(xlab, fontsize=ft)
    draw_all_roms('tina_rom.txt', 0, color='green')

    plt.subplot(1, 3, 3)
    plt.title('ROM Finger 3')
    plt.plot([0, 0], [0.1, 0.1], color='black', label='Overall ROM')
    plt.xlabel(xlab, fontsize=ft)
    draw_all_roms('chrissi_rom.txt', 1, color='orangered')


perform_overlall_rom()
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
draw_interception(idxs=[14])
# %%
plt.figure(figsize=(12, 10))
draw_all_roms('tina_rom.txt', 1, color='green')

# %%
