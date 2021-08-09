# %%
import matplotlib.pyplot as plt
import numpy as np


timelab = 'Time [s]'
torquelab = 'Joint Torque [Nm]'
deglab = 'Joint Angle [deg]'


def plot_fitted_arrs(fitted_data: dict, stats=False, buil_ymax=False, plot=plt.figure(figsize=(12, 8)), color='none', filename='none'):
    """plot the arrays fitted to the model"""

    time = fitted_data['time']

    if stats:
        phi_mcp_arr = fitted_data['deg_1_m']
        phi_pip_arr = fitted_data['deg_2_m']
        phi_dip_arr = fitted_data['deg_3_m']

        phi_mcp_arr_std = fitted_data['deg_1_std']
        phi_pip_arr_std = fitted_data['deg_2_std']
        phi_dip_arr_std = fitted_data['deg_3_std']

        m_mcp_arr = fitted_data['m_1_m']
        m_pip_arr = fitted_data['m_2_m']
        m_dip_arr = fitted_data['m_3_m']

        m_mcp_arr_std = fitted_data['m_1_std']
        m_pip_arr_std = fitted_data['m_2_std']
        m_dip_arr_std = fitted_data['m_3_std']

    else:
        phi_mcp_arr = fitted_data['deg_1']
        phi_pip_arr = fitted_data['deg_2']
        phi_dip_arr = fitted_data['deg_3']

        m_mcp_arr = fitted_data['m_1']
        m_pip_arr = fitted_data['m_2']
        m_dip_arr = fitted_data['m_3']

    if buil_ymax:
        deg_max = max(max(phi_pip_arr), max(
            phi_mcp_arr), max(phi_dip_arr)) + 10
        deg_min = min(min(phi_pip_arr), min(
            phi_mcp_arr), min(phi_dip_arr)) - 10

        m_min = min(min(m_pip_arr), min(m_mcp_arr), min(m_dip_arr)) - 0.05
        m_max = max(max(m_pip_arr), max(m_mcp_arr), max(m_dip_arr)) + 0.05

    else:
        deg_min = -80
        deg_max = 20

        m_min = -0.15
        m_max = 0.10

    cur_color = 'blue' if color == 'none' else color

    plt.subplot(2, 3, 1)
    plt.title('Angle Trajectory MCP')
    plt.grid(0.25)
    plt.plot(time, phi_mcp_arr, color=cur_color)
    if stats:
        plt.fill_between(time, phi_mcp_arr + phi_mcp_arr_std, phi_mcp_arr -
                         phi_mcp_arr_std, facecolor=cur_color, interpolate=True, alpha=0.2)
    plt.ylim([deg_min, deg_max])
    plt.ylabel(deglab)

    cur_color = 'green' if color == 'none' else color
    plt.subplot(2, 3, 2)
    plt.title('Angle Trajectory PIP')
    plt.grid(0.25)
    plt.plot(time, phi_pip_arr, color=cur_color)
    if stats:
        plt.fill_between(time, phi_pip_arr + phi_pip_arr_std, phi_pip_arr -
                         phi_pip_arr_std, facecolor=cur_color, interpolate=True, alpha=0.2)
    plt.ylim([deg_min, deg_max])

    cur_color = 'red' if color == 'none' else color
    plt.subplot(2, 3, 3)
    plt.title('Angle Trajectory DIP')
    plt.grid(0.25)
    plt.plot(time, phi_dip_arr, color=cur_color)
    if stats:
        plt.fill_between(time, phi_dip_arr + phi_dip_arr_std, phi_dip_arr -
                         phi_dip_arr_std, facecolor=cur_color, interpolate=True, alpha=0.2)
    plt.ylim([deg_min, deg_max])

    cur_color = 'blue' if color == 'none' else color
    plt.subplot(2, 3, 4)
    plt.title('Torque Trajectory MCP')
    plt.grid(0.25)
    plt.plot(time, m_mcp_arr, color=cur_color)
    if stats:
        plt.fill_between(time, m_mcp_arr + m_mcp_arr_std, m_mcp_arr -
                         m_mcp_arr_std, facecolor=cur_color, interpolate=True, alpha=0.2)
    plt.ylim([m_min, m_max])
    plt.xlabel(timelab)
    plt.ylabel(torquelab)

    cur_color = 'green' if color == 'none' else color
    plt.subplot(2, 3, 5)
    plt.title('Torque Trajectory PIP')
    plt.grid(0.25)
    plt.plot(time, m_dip_arr, color=cur_color)
    if stats:
        plt.fill_between(time, m_dip_arr + m_dip_arr_std, m_dip_arr -
                         m_dip_arr_std, facecolor=cur_color, interpolate=True, alpha=0.2)
    plt.ylim([m_min, m_max])
    plt.xlabel(timelab)

    if filename != 'none':
        filename = filename.split('_')[0]

    cur_color = 'red' if color == 'none' else color
    plt.subplot(2, 3, 6)
    plt.title('Torque Trajectory DIP')
    plt.grid(0.25)
    plt.plot(time, m_pip_arr, color=cur_color, label=filename)
    if stats:
        plt.fill_between(time, m_pip_arr + m_pip_arr_std, m_pip_arr -
                         m_pip_arr_std, facecolor=cur_color, interpolate=True, alpha=0.2)
    plt.ylim([m_min, m_max])
    plt.xlabel(timelab)
    return plt


def plot_data(data_list: list, index=0):
    """plot the measured angle and force data"""
    data = data_list[index]
    plt.figure(figsize=(14, 14))
    time = [ele / 1000 for ele in data['ms']]
    plt.subplot(2, 1, 1)
    plt.grid(0.25)
    plt.plot(time, data['A'], label='A')
    plt.plot(time, data['B'], label='B')
    plt.plot(time, data['K'], label='K')
    plt.legend()
    plt.xlabel(timelab)
    plt.ylabel('Degree [°]')

    plt.subplot(2, 1, 2)
    plt.grid(0.25)
    plt.plot(time, data['ZUG'], label='ZUG', linestyle='-.')
    plt.plot(time, data['DRUCK'], label='DRUCK', linestyle='-.')
    plt.plot(time, np.array(data['DRUCK']) -
             np.array(data['ZUG']), label='external', color='red')
    plt.legend()
    plt.xlabel(timelab)
    plt.ylabel('Force [N]')
