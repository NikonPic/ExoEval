# %%
import numpy as np
import matplotlib.pyplot as plt
from math import pi

fac_dip = 2 / 3

R_all = {
    'mcp': [-14, 86.5],
    'pip': [0, 102, 5],
    'dip': [0, 102, 5*fac_dip]
}

R_func = {
    'mcp': [23.5, 62.5],
    'pip': [23, 86],
    'dip': [23*fac_dip, 86*fac_dip]
}

# process:
# run: mcpmin -> mcpmax -> pipmin and dipmin -> pipmax and dipmax - and back


def deg_2_pos(l_pp, l_pm, l_pd, mcp, pip, dip, mult=False):
    mcp = -(pi/180)*mcp
    pip = mcp-(pi/180)*pip
    dip = pip-(pi/180)*dip

    xpip = l_pp*np.cos(mcp)
    ypip = l_pp*np.sin(mcp)

    xdip = xpip+l_pm*np.cos(pip)
    ydip = ypip+l_pm*np.sin(pip)

    xtip = xdip+l_pd*np.cos(dip)
    ytip = ydip+l_pd*np.sin(dip)

    if mult:
        return xpip, ypip, xdip, ydip, xtip, ytip

    return xtip, ytip


def plot_br(l_pp, l_pm, l_pd, r_rel, steps=1000, color='black'):
    """plot the ROM depending on the measured values"""
    # allocate empty
    fs = [[], []]

    # flex mcp
    pip = r_rel['pip'][0]
    dip = r_rel['dip'][0]
    mcp_arr = np.linspace(r_rel['mcp'][0], r_rel['mcp'][1], steps)

    for mcp in mcp_arr:
        xtip, ytip = deg_2_pos(l_pp, l_pm, l_pd, mcp, pip, dip)
        fs[0].append(xtip)
        fs[1].append(ytip)

    # flex pip and dip
    mcp = r_rel['mcp'][1]
    pip_arr = np.linspace(r_rel['pip'][0], r_rel['pip'][1], steps)
    dip_arr = np.linspace(r_rel['dip'][0], r_rel['dip'][1], steps)

    for pip, dip in zip(pip_arr, dip_arr):
        xtip, ytip = deg_2_pos(l_pp, l_pm, l_pd, mcp, pip, dip)
        fs[0].append(xtip)
        fs[1].append(ytip)

    # extend mcp
    pip = r_rel['pip'][1]
    dip = r_rel['dip'][1]
    mcp_arr = np.linspace(r_rel['mcp'][1], r_rel['mcp'][0], steps)
    for mcp in mcp_arr:
        xtip, ytip = deg_2_pos(l_pp, l_pm, l_pd, mcp, pip, dip)
        fs[0].append(xtip)
        fs[1].append(ytip)

    # extend pip and dip
    mcp = r_rel['mcp'][0]
    pip_arr = np.linspace(r_rel['pip'][1], r_rel['pip'][0], steps)
    dip_arr = np.linspace(r_rel['dip'][1], r_rel['dip'][0], steps)
    for pip, dip in zip(pip_arr, dip_arr):
        xtip, ytip = deg_2_pos(l_pp, l_pm, l_pd, mcp, pip, dip)
        fs[0].append(xtip)
        fs[1].append(ytip)

    plt.plot(fs[0], fs[1], color=color)


def plot_finger(l_pp, l_pm, l_pd, r_rel):
    """draw the finger in the starting position"""
    mcp = r_rel['mcp'][0]
    pip = r_rel['pip'][0]
    dip = r_rel['dip'][0]

    xpip, ypip, xdip, ydip, xtip, ytip = deg_2_pos(
        l_pp, l_pm, l_pd, mcp, pip, dip, mult=True)

    x_arr = [0, xpip, xdip, xtip]
    y_arr = [0, ypip, ydip, ytip]

    plt.plot(x_arr, y_arr, color='black')
    plt.scatter(x_arr, y_arr, color='black')


def perform_br_plot(l_pp, l_pm, l_pd, r_extra=0):
    plt.ylim([-110, 40])
    plt.xlim([-50, 100])
    plt.grid(0.25)
    plot_finger(l_pp, l_pm, l_pd, R_all)
    plot_br(l_pp, l_pm, l_pd, R_all)
    plot_br(l_pp, l_pm, l_pd, R_func, color='darkred')

    if r_extra != 0:
        plot_br(l_pp, l_pm, l_pd, r_extra)


def plot_br_fitted(l_pp, l_pm, l_pd, fd, color, filename):
    pt1 = 0.99
    mcp_arr, pip_arr, dip_arr = filt_d(fd['deg_1']), filt_d(
        fd['deg_2'], u_lim=-10, pt1=pt1), filt_d(fd['deg_3'])

    r_extra = {
        'mcp': [-min(mcp_arr), -max(mcp_arr)],
        'pip': [-min(pip_arr), -max(pip_arr)],
        'dip': [-min(dip_arr), -max(dip_arr)]
    }

    perform_br_plot(l_pp, l_pm, l_pd, r_extra=0)

    fs = [[], []]
    for (mcp, pip, dip) in zip(fd['deg_1'], fd['deg_2'], fd['deg_3']):
        xtip, ytip = deg_2_pos(l_pp, l_pm, l_pd, mcp, pip, dip)
        fs[0].append(xtip)
        fs[1].append(-ytip)
    plt.plot(fs[0], fs[1], color=color, linewidth=2)


def filt_d(deg_arr, u_lim=30, pt1=0.95):
    deg_old = deg_arr[0]

    # exclude 0s
    for i, deg in enumerate(deg_arr):
        if deg == 0:
            deg_arr[i] = deg_old
        elif deg < -220:
            deg_arr[i] = deg_old
        elif deg > 200:
            deg_arr[i] = deg_old
        else:
            deg_old = deg

    for i, deg in enumerate(deg_arr):
        if deg > 30:
            deg = deg - 180
        if deg > u_lim:
            deg = deg - 180
        if deg < -220:
            deg = deg + 180
        if deg < -140:
            deg = -140

        deg_arr[i] = deg

    deg_old = deg_arr[0]

    # exclude 0s
    for i, deg in enumerate(deg_arr):
        if abs(deg - deg_old) > 50:
            deg = deg_old
        else:
            deg_old = deg
        deg_arr[i] = deg

    deg_old = deg_arr[0]

    for i, deg in enumerate(deg_arr):
        deg_old = pt1 * deg_old + (1-pt1) * deg
        deg_arr[i] = deg_old

    return deg_arr


if __name__ == '__main__':
    l_pp = 45
    l_pm = 25
    l_pd = 24
    perform_br_plot(l_pp, l_pm, l_pd)

# %%
