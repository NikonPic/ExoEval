# %%
from visualize import plot_2_tiff, plot_data, plot_fitted_arrs
from force_kalib.eval_forces import force_polys
from poti_kalib.poti_eval import poti_polys
import numpy as np
from exoskeleton.individual_params import get_model_by_filename
import pandas as pd
import matplotlib.pyplot as plt

timelab = 'Time [s]'
torquelab = 'Joint Torque [Nm]'
deglab = 'Joint Angle [deg]'


def concat_polys(poti_polys, force_polys):
    """make 1 dicitionary out of the two"""
    all_polys = {}
    for polys in [poti_polys, force_polys]:
        for loc_key in polys.keys():
            all_polys[loc_key] = polys[loc_key]
    return all_polys


def lines2data(lines: list, all_polys: dict) -> dict:
    """take the input lines and create a list of data measurement dictionary"""

    all_data = {
        'ms': [],
        'B': [],
        'A': [],
        'K': [],
        'DRUCK': [],
        'ZUG': [],
    }

    for line in lines:
        # take the local elements from the array
        # raw_data = ms, angleB, angleA, angleK, forceB, forceA
        # Kraft Druck: forceB
        # Kraft Zug: forceA
        raw_data = [int(ele) for ele in line.replace('\n', '').split(';')]

        for index, loc_key in enumerate(all_data.keys()):
            if loc_key in all_polys.keys():
                all_data[loc_key].append(all_polys[loc_key](raw_data[index]))
            else:
                all_data[loc_key].append(raw_data[index])

    return all_data


def all_data_2_list(all_data):
    """split th dictionary into multipl dictionary, if the next timestep is smaller than the previous"""
    data_list = []
    prev_ms = -1e5
    loc_dict = {
        ele: [] for ele in all_data.keys()
    }

    for index, ms in enumerate(all_data['ms']):
        # create new dict and save old if this happens
        if ms < prev_ms:
            data_list.append(loc_dict.copy())
            loc_dict = {
                ele: [] for ele in all_data.keys()
            }
        for key in all_data.keys():
            loc_dict[key].append(all_data[key][index])
        prev_ms = ms
    return data_list


def perform_model_analysis(model, data_list: list, index: int, true_data=False, plotit=True):
    """perform the elementwise analysis of the model"""
    if true_data:
        plot_data(data_list, index)

    data = pd.DataFrame(data_list[index])
    time = data_list[index]['ms']
    time = [ele / 1000 for ele in time]

    # preallocate:
    phi_mcp_arr = np.zeros(len(data))
    phi_pip_arr = np.zeros(len(data))
    phi_dip_arr = np.zeros(len(data))
    m_mcp_arr = np.zeros(len(data))
    m_pip_arr = np.zeros(len(data))
    m_dip_arr = np.zeros(len(data))

    for index in range(len(data)):
        ele = data.iloc[index]

        output_arr = model(ele.A, ele.B, ele.K, -(ele.DRUCK - ele.ZUG))
        phi_mcp, phi_pip, phi_dip, m_mcp, m_pip, m_dip = output_arr

        # assign
        phi_mcp_arr[index] = phi_mcp
        phi_pip_arr[index] = phi_pip
        phi_dip_arr[index] = phi_dip
        m_mcp_arr[index] = m_mcp
        m_pip_arr[index] = m_pip
        m_dip_arr[index] = m_dip

    fitted_data = {
        'time': time,
        'deg_1': phi_mcp_arr,
        'deg_2': phi_pip_arr,
        'deg_3': phi_dip_arr,
        'm_1': m_mcp_arr,
        'm_2': m_pip_arr,
        'm_3': m_dip_arr,
    }

    if plotit:
        plot_fitted_arrs(fitted_data)

    return fitted_data


def build_average_fitted_data(model, data_list, id_list, color='none', plot=plt.figure(figsize=(12, 8)), filename='none', ymax=False):
    """apply the model on the measurements acc to id list and plot the fitted arrays"""

    arr_fitted_data = []
    for idx in id_list:
        arr_fitted_data.append(perform_model_analysis(
            model, data_list, idx, plotit=False))

    avg_arrs = {
        'time': arr_fitted_data[0]['time']
    }

    # now build the means and stds
    keylist = list(arr_fitted_data[0].keys())
    keylist.remove('time')

    for key in keylist:
        loc_arrs = [np.array(arr_fitted_data[index][key])
                    for index in range(len(arr_fitted_data))]
        avg_arrs[f'{key}_m'] = np.mean(loc_arrs, axis=0)
        avg_arrs[f'{key}_std'] = np.std(loc_arrs, axis=0)

    plot = plot_fitted_arrs(avg_arrs, stats=True,
                            color=color, plot=plot, filename=filename, buil_ymax=ymax)
    return plot


def perform_all(filename, color, plot):
    with open(f'{PATH}/{filename}') as f:
        lines = f.readlines()

    all_polys = concat_polys(poti_polys, force_polys)
    all_data = lines2data(lines, all_polys)
    data_list = all_data_2_list(all_data)
    model = get_model_by_filename(filename)
    plot = build_average_fitted_data(
        model, data_list, [1, 2, 3, 4, 5, 7], color=color, plot=plot, filename=filename)
    return plot


def draw_interception():
    filename = 'niko_mit_inter.txt'
    with open(f'{PATH}/{filename}') as f:
        lines = f.readlines()
    plot = plt.figure(figsize=(12, 10))

    for ind in range(1, 7):
        plt.subplot(2, 3, ind)
        plt.vlines(5.1, -70, 30, linestyles='-.', linewidth=1, color='black')
        plt.vlines(8, -70, 30, linestyles='-.', linewidth=1, color='black')

        plt.vlines(18, -70, 30, linestyles='-.', linewidth=1, color='black')
        plt.vlines(20, -70, 30, linestyles='-.', linewidth=1, color='black')

    all_polys = concat_polys(poti_polys, force_polys)
    all_data = lines2data(lines, all_polys)
    data_list = all_data_2_list(all_data)
    model = get_model_by_filename(filename)
    plot = build_average_fitted_data(
        model, data_list, [1], color='blue', plot=plot, filename=filename, ymax=True)

# %%


if __name__ == '__main__':

    PATH = './measure_forces'

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
    # plt.legend()
    plot_2_tiff(plot, 'measurements_real')

    draw_interception()


# %%


# %%
