# %%
from force_kalib.eval_forces import force_polys
from poti_kalib.poti_eval import poti_polys
import matplotlib.pyplot as plt
import numpy as np
from exo_workflow import KinExoParams
from ipywidgets import widgets
import pandas as pd
from math import pi


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


def plot_data(data_list: list, index=0):
    data = data_list[index]
    plt.figure(figsize=(14, 14))
    time = [ele / 1000 for ele in data['ms']]
    plt.subplot(2, 1, 1)
    plt.grid(0.25)
    plt.plot(time, data['A'], label='A')
    plt.plot(time, data['B'], label='B')
    plt.plot(time, data['K'], label='K')
    plt.legend()
    plt.xlabel('Time [s]')
    plt.ylabel('Degree [°]')

    plt.subplot(2, 1, 2)
    plt.grid(0.25)
    plt.plot(time, data['ZUG'], label='ZUG', linestyle='-.')
    plt.plot(time, data['DRUCK'], label='DRUCK', linestyle='-.')
    plt.plot(time, np.array(data['DRUCK']) -
             np.array(data['ZUG']), label='external', color='red')
    plt.legend()
    plt.xlabel('Time [s]')
    plt.ylabel('Force [N]')


def perform_model_analysis(model: KinExoParams, data_list: list, index: int):
    """perform the elementwise analysis of the model"""
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

    deg_max = max(max(phi_pip_arr), max(phi_mcp_arr), max(phi_dip_arr)) + 10
    deg_min = min(min(phi_pip_arr), min(phi_mcp_arr), min(phi_dip_arr)) - 10

    m_max = max(max(m_pip_arr), max(m_mcp_arr), max(m_dip_arr)) + 0.02
    m_min = min(min(m_pip_arr), min(m_mcp_arr), min(m_dip_arr)) - 0.02

    plt.figure(figsize=(12, 8))

    plt.subplot(2, 3, 1)
    plt.title('Angle Trajectory MCP')
    plt.grid(0.25)
    plt.plot(time, phi_mcp_arr)
    plt.ylim([deg_min, deg_max])
    #plt.xlabel('Time [s]')
    plt.ylabel('Joint Angle [deg]')

    plt.subplot(2, 3, 2)
    plt.title('Angle Trajectory PIP')
    plt.grid(0.25)
    plt.plot(time, phi_pip_arr, color='green')
    plt.ylim([deg_min, deg_max])
    #plt.xlabel('Time [s]')
    #plt.ylabel('Joint Angle [deg]')

    plt.subplot(2, 3, 3)
    plt.title('Angle Trajectory DIP')
    plt.grid(0.25)
    plt.plot(time, phi_dip_arr, color='red')
    plt.ylim([deg_min, deg_max])
    #plt.xlabel('Time [s]')
    #plt.ylabel('Joint Angle [deg]')

    plt.subplot(2, 3, 4)
    plt.title('Torque Trajectory MCP')
    plt.grid(0.25)
    plt.plot(time, m_mcp_arr)
    plt.ylim([m_min, m_max])
    plt.xlabel('Time [s]')
    plt.ylabel('Joint Torque [Nm]')

    plt.subplot(2, 3, 5)
    plt.title('Torque Trajectory PIP')
    plt.grid(0.25)
    plt.plot(time, m_dip_arr, color='green')
    plt.ylim([m_min, m_max])
    plt.xlabel('Time [s]')
    #plt.ylabel('Joint Torque [Nm]')

    plt.subplot(2, 3, 6)
    plt.title('Torque Trajectory DIP')
    plt.grid(0.25)
    plt.plot(time, m_pip_arr, color='red')
    plt.ylim([m_min, m_max])
    plt.xlabel('Time [s]')
    #plt.ylabel('Joint Torque [Nm]')


PATH = './measure_forces'

with open(f'{PATH}/log_1.txt') as f:
    lines = f.readlines()

all_polys = concat_polys(poti_polys, force_polys)
all_data = lines2data(lines, all_polys)
data_list = all_data_2_list(all_data)
model = KinExoParams()

# %%


def update(index=110):
    #plot_data(data_list, index)
    perform_model_analysis(model, data_list, index)


widgets.interactive(update)
# %%
