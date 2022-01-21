# %%
from scipy import signal
from rom import perform_br_plot, plot_br_fitted
from visualize import plot_data, plot_fitted_arrs
from force_kalib.eval_forces import force_polys
from poti_kalib.poti_eval import poti_polys
import numpy as np
from exoskeleton.individual_params import get_model_by_filename
import pandas as pd
import matplotlib.pyplot as plt

PATH = './measure_forces'

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

    off_b = 0
    off_a = 0
    off_k = 0

    jump = 2000
    b_old = int(lines[0].replace('\n', '').split(';')[1])
    a_old = int(lines[0].replace('\n', '').split(';')[2])
    k_old = int(lines[0].replace('\n', '').split(';')[3])

    for line in lines:
        # take the local elements from the array
        # raw_data = ms, angleB, angleA, angleK, forceB, forceA
        # Kraft Druck: forceB
        # Kraft Zug: forceA
        raw_data = [int(ele) for ele in line.replace('\n', '').split(';')]

        ms, b, a, k, fa, fb = raw_data

        b = b + off_b
        if abs(b - b_old) > jump:
            print('JUMP B')
            off_b = b - b_old

        a = a + off_a
        if abs(a - a_old) > jump:
            print('JUMP A')
            off_a = a - a_old

        k = k + off_k
        if abs(k - k_old) > jump:
            print('JUMP K')
            off_k = k - k_old

        raw_data = ms, b, a, k, fa, fb

        b_old, a_old, k_old = b, a, k

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


def get_mindiff(arr):
    """get the minimum difference between two values"""
    if len(arr) > 4:
        arr = arr[:4]
    diffs = np.diff(arr[1:])
    #diffs = list(diffs)
    # diffs.remove(np.min(diffs))
    return np.min(diffs)


def all_data_2_list_synchro(all_data, refill=1):
    """split th dictionary into multipl dictionary, by synchronising the start-time"""
    data_list = []

    # set start-time to 0
    loc_dict = {
        ele: [] for ele in all_data.keys()
    }
    ms0 = all_data['ms'][0]
    ms_add = 0
    ms_prev = 0

    for index, ms in enumerate(all_data['ms']):
        # avoid time jumps
        if ms_prev > ms:
            ms_add += ms_prev - ms

        # create new dict and save old if this happens
        for key in all_data.keys():
            if key == 'ms':
                loc_dict[key].append(ms - ms0 + ms_add)
            else:
                loc_dict[key].append(all_data[key][index])
        ms_prev = ms

    if refill:
        # fill the rest of the data
        for key in all_data.keys():
            if key == 'ms':
                loc_dict[key] = signal.resample(
                    loc_dict[key], int(len(loc_dict[key])*2)) * 2
            else:
                loc_dict[key] = signal.resample(
                    loc_dict[key], int(len(loc_dict[key])*2))

    # synchronise the arrays using the angleB
    if refill:
        b, a = signal.butter(5, 0.01, btype='lowpass')
    else:
        b, a = signal.butter(5, 0.005, btype='lowpass')

    bfilt = np.array(signal.filtfilt(b, a, loc_dict['B']))
    minbs = signal.argrelextrema(bfilt, np.greater)[0]
    indexdiff = get_mindiff(minbs)
    indexdiff = indexdiff + 140 if refill else indexdiff

    # now rebuilt the single ararys:
    for cur_min in minbs[:-1]:
        # create new dict
        loc_dict_sync = {
            ele: [] for ele in all_data.keys()
        }
        cur_min0 = loc_dict['ms'][cur_min]
        # copy the values until maxindex
        for index in range(indexdiff):
            for key in all_data.keys():
                if key == 'ms':
                    loc_dict_sync[key].append(
                        loc_dict[key][cur_min + index] - cur_min0)
                else:
                    loc_dict_sync[key].append(loc_dict[key][cur_min + index])
        data_list.append(loc_dict_sync)

    return data_list


def perform_model_analysis(model, data_list: list, index: int, true_data=False, plotit=True, ymax=False):
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
    m_akt_arr = np.zeros(len(data))

    for index in range(len(data)):
        ele = data.iloc[index]

        try:
            output_arr = model(ele.A, ele.B, ele.K, -(ele.DRUCK - ele.ZUG))
            phi_mcp, phi_pip, phi_dip, m_mcp, m_pip, m_dip = output_arr

            # assign
            phi_mcp_arr[index] = phi_mcp
            phi_pip_arr[index] = phi_pip
            phi_dip_arr[index] = phi_dip
            m_mcp_arr[index] = m_mcp
            m_pip_arr[index] = m_pip
            m_dip_arr[index] = m_dip
            m_akt_arr[index] = model.m_b_nm
        except:
            pass

    fitted_data = {
        'time': time,
        'deg_1': phi_mcp_arr,
        'deg_2': phi_pip_arr,
        'deg_3': phi_dip_arr,
        'm_1': m_mcp_arr,
        'm_2': m_pip_arr,
        'm_3': m_dip_arr,
        'm_akt': m_akt_arr,
    }

    if plotit:
        plot_fitted_arrs(fitted_data, buil_ymax=ymax)

    return fitted_data


def print_data_infos(arr_fitted_data):
    """
    print all infos to angle and torque
    mcp - range - min - max
    pip - range - min - max 
    dip - range - min - max

    -> and mean ± std
    """
    rel_keys = list(arr_fitted_data[0].keys())
    rel_keys.remove('time')

    data_infos = {
        key: {
            'min': [],
            'max': [],
            'range': [],
        } for key in rel_keys
    }

    for fitted_data in arr_fitted_data:

        for key in rel_keys:
            loc_arr = fitted_data[key]
            loc_min = min(loc_arr)
            loc_max = max(loc_arr)
            loc_range = round(loc_max - loc_min, 2)

            data_infos[key]['min'].append(loc_min)
            data_infos[key]['max'].append(loc_max)
            data_infos[key]['range'].append(loc_range)

    # now print the overall result
    for key in rel_keys:
        print(key)
        for loc_key in ['min', 'max', 'range']:
            print(ret_m_std(data_infos[key], loc_key))


def ret_m_std(arr, loc_key):
    m = round(np.mean(arr[loc_key]), 2)
    st = round(np.std(arr[loc_key]), 2)
    return f'{loc_key}: ${m} \pm {st}$'


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

    # print_data_infos(arr_fitted_data)

    plot = plot_fitted_arrs(avg_arrs, stats=True,
                            color=color, plot=plot, filename=filename, buil_ymax=ymax)
    return plot


def perform_all(filename, color, plot):
    """perform the data analysis"""
    with open(f'{PATH}/{filename}') as f:
        lines = f.readlines()

    all_polys = concat_polys(poti_polys, force_polys)
    all_data = lines2data(lines, all_polys)
    data_list = all_data_2_list(all_data)
    model = get_model_by_filename(filename)
    plot = build_average_fitted_data(
        model, data_list, [1, 2, 3, 4, 5, 7], color=color, plot=plot, filename=filename)
    return plot


def perform_all_patients(filename, color, plot):
    """perform the data analysis"""
    with open(f'./patienten/{filename}') as f:
        lines = f.readlines()
    lines = lines[1:len(lines)-1]

    all_polys = concat_polys(poti_polys, force_polys)
    all_data = lines2data(lines, all_polys)
    if 'pat4/Messung_12' in filename:
        print('TRUE')
        data_list = all_data_2_list_synchro(all_data, refill=1)
    else:
        data_list = all_data_2_list_synchro(all_data, refill=0)
    model = get_model_by_filename(filename)
    plot = build_average_fitted_data(
        model, data_list, [2, 3], color=color, plot=plot, filename=filename)
    return plot


def draw_interception(filename='niko_mit_inter (2).txt', idxs=[1]):
    """take a file and perform analysis"""
    lines = filename_2_lines(filename)
    plot = plt.figure(figsize=(12, 10))

    all_polys = concat_polys(poti_polys, force_polys)
    all_data = lines2data(lines, all_polys)
    data_list = all_data_2_list(all_data)
    model = get_model_by_filename(filename)
    plot = build_average_fitted_data(
        model, data_list, idxs, color='blue', plot=plot, filename=filename, ymax=True)
    return plot


def filename_2_lines(filename):
    """read a file by lines"""
    with open(f'{PATH}/{filename}') as f:
        lines = f.readlines()
    return lines


def draw_all_roms(filename, index, color):
    """perform the Range of Motion (ROM) plots for all subjects"""
    lines = filename_2_lines(filename)
    all_polys = concat_polys(poti_polys, force_polys)
    all_data = lines2data(lines, all_polys)
    data_list = all_data_2_list(all_data)
    model = get_model_by_filename(filename)

    # get the lengths
    l_pp = model.l_pp
    l_pm = model.l_pm
    l_pd = model.l_pd

    # get the data
    fitted_data = perform_model_analysis(
        model, data_list, index, true_data=False, plotit=False, ymax=True)

    lab = 'Exoskeleton ROM'
    labelmap = {
        '': '',
        'niko': lab,
        'tina': lab,
        'chrissi': lab,
        'none': 'none',
    }
    label = labelmap[filename.split('_')[0]]
    plot_br_fitted(l_pp, l_pm, l_pd, fitted_data, color, label)


# %%
if __name__ == '__main__':

    filename = 'pat4/Messung_12.txt'
    with open(f'./patienten/{filename}') as f:
        lines = f.readlines()
    lines = lines[1:len(lines)-1]
    all_polys = concat_polys(poti_polys, force_polys)
    all_data = lines2data(lines, all_polys)
    b, a = signal.butter(5, 0.005, btype='lowpass')
    bfilt = np.array(signal.filtfilt(b, a, all_data['B']))
    minbs = signal.argrelextrema(bfilt, np.less)[0]
    zugd = all_data['ZUG'][minbs[0]:]
    zugd = signal.resample(zugd, int(len(zugd)*2))
    plt.plot(zugd)

    filename = 'pat2/Messung_21.txt'
    with open(f'./patienten/{filename}') as f:
        lines = f.readlines()
    lines = lines[1:len(lines)-1]
    all_polys = concat_polys(poti_polys, force_polys)
    all_data = lines2data(lines, all_polys)
    b, a = signal.butter(5, 0.005, btype='lowpass')
    bfilt = np.array(signal.filtfilt(b, a, all_data['B']))
    minbs = signal.argrelextrema(bfilt, np.less)[0]
    plt.plot(all_data['ZUG'][minbs[0]:])
# %%
