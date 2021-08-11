# %%


import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import numpy.polynomial.polynomial as poly
import os
from visualize import plot_2_tiff


def read_file(filename: str, active_id=5):
    """read the file and extract the values and time signal of the sensor"""
    cur_path = os.getcwd()
    addon = 'force_kalib'
    filename = filename if addon in cur_path else f'{addon}/{filename}'

    with open(filename) as f:
        lines = f.readlines()

    values = [int(line.split(';')[active_id].strip('\n')) for line in lines]
    time = [int(line.split(';')[0].strip('\n')) for line in lines]

    return time, values


def long_arr_2_arrs(time, values, counts, excludes):
    """split the long arr into multiple small arrays depending on the time signal"""
    len_count = int(len(time) / counts)

    new_time = time[:len_count]

    value_arrs = []

    for count in range(counts):
        if count in excludes:
            continue
        loc_values = values[len_count * count: len_count*(count+1)]
        value_arrs.append(loc_values)

    return new_time, value_arrs


def plot_arrs(value_arrs):
    plt.figure(figsize=(12, 12))
    plt.grid(0.25)

    for i, arr in enumerate(value_arrs):

        plt.plot(arr, label=i)
    plt.legend()


def print_errors(value_arrs_fitted, soll_arr):
    errs = [abs(np.array(loc_arr) - np.array(soll_arr))
            for loc_arr in value_arrs_fitted]

    # print single tests
    for idx, (m, std) in enumerate(zip(np.mean(errs, axis=1), np.std(errs, axis=1))):
        print(f'Test {idx}: {round(m,2)} ± {round(std, 2)} N')

    # overall tests:
    overall = np.array(errs).flatten()
    m_all = np.mean(overall)
    std_all = np.std(overall)
    print(f'Overall: {round(m_all,2)} ± {round(std_all, 2)} N')


def std_plot(value_arrs, poly_deg=2, show_poly=False, index=0, longval=True, ft=14):

    plt.grid(0.25)

    mean_arr = np.mean(value_arrs, axis=0)
    soll_arr = define_soll_arr(mean_arr)

    # fit the polygon:
    slope, intercept, _, _, _ = stats.linregress(
        mean_arr, soll_arr)

    if longval:
        long_values = np.array(value_arrs).flatten()
        long_soll = np.array(
            [soll_arr for _ in range(len(value_arrs))]).flatten()
        coefficients = poly.polyfit(long_values, long_soll, poly_deg)
    else:
        coefficients = poly.polyfit(mean_arr, soll_arr, poly_deg)

    print('polynom of degree: ', poly_deg)
    print('Coefficients: ', coefficients)
    ffit = poly.Polynomial(coefficients)

    print('SCALE: ', slope)
    print('OFFSET: ', intercept)

    value_arrs_fitted = [ffit(np.array(loc_arr)) for loc_arr in value_arrs]
    print_errors(value_arrs_fitted, soll_arr)

    mean_arr = np.mean(value_arrs_fitted, axis=0)
    std_arr = np.std(value_arrs_fitted, axis=0)

    time = np.array(range(len(mean_arr))) / 10
    plt.plot(time, mean_arr, label='mean ± std of measurements')
    plt.fill_between(time, mean_arr + std_arr, mean_arr -
                     std_arr, facecolor='blue', interpolate=True, alpha=0.2)
    plt.plot(time, soll_arr, color='red', linestyle='-.', label='target value')

    plt.xlabel('Time [s]', fontsize=ft) if index > 0 else ''
    plt.ylabel('Force [N]', fontsize=ft)
    plt.ylim([0, 12])
    plt.title(f'Sensor {index+1}: Drift and hysteresis',
              fontweight='bold', fontsize=ft)

    if show_poly:
        plt.subplot(2, 2, index * 2 + 2)
        plt.grid(0.25)
        addon = 500
        raw = np.linspace(np.min(value_arrs) - addon,
                          np.max(value_arrs) + addon, 1000)
        fitted = ffit(raw)
        plt.plot(raw, fitted)
        [plt.scatter(value_arr, soll_arr, color='red')
         for value_arr in value_arrs]
        plt.xlabel('Raw Values []')
        plt.ylabel('Force [N]')

    return ffit


def define_soll_arr(arr):
    """define the array of the value we need"""
    hook = 0.14
    bottle = 3.33
    grams = [hook, hook + 1 * bottle,
             hook + 2*bottle, hook + 3 * bottle, hook + 2 * bottle, hook + 1 * bottle, hook]

    # define the lengths
    len_g = len(grams)
    num_plateus = len_g - 1
    len_arr = len(arr)
    plateau_len = int(len_arr / num_plateus)
    startend_len = int(plateau_len / 2)

    id_list = []
    start_id = 0

    for i in range(len_g):
        loc_len = startend_len if i in [0, num_plateus] else plateau_len
        loc_ids = [start_id, start_id + loc_len]
        start_id += loc_len
        id_list.append(loc_ids)

    soll_arr = arr.copy()
    soll_arr[:] = hook

    # create array
    for loc_ids, gram in zip(id_list, grams):
        soll_arr[loc_ids[0]:loc_ids[1]] = gram

    return soll_arr


def perform_analysis(poly_deg=2, show_poly=False, longval=True):
    fig = plt.figure(figsize=(8, 10))

    name_mapping = {
        'blau.txt': 'DRUCK',
        'gelb.txt': 'ZUG'
    }
    force_polys = {}

    for index, filename in enumerate(['blau.txt', 'gelb.txt']):
        if show_poly:
            plt.subplot(2, 2, index * 2 + 1)
        else:
            plt.subplot(2, 1, index+1)

        print(filename)
        active_id = 5 if 'blau' in filename else 4
        time, values = read_file(filename, active_id=active_id)
        _, value_arrs = long_arr_2_arrs(time, values, 10, excludes=[0, 1])
        force_polys[name_mapping[filename]] = std_plot(value_arrs, poly_deg=poly_deg,
                                                       show_poly=show_poly, index=index, longval=longval)
    ax = plt.subplot(2, 1, 2)
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', ncol=2, fontsize=14)
    plot_2_tiff(fig, 'force')

    return force_polys


force_polys = perform_analysis(poly_deg=3, show_poly=False)


# %%
