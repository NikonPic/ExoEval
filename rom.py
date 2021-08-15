# %%
import numpy as np
import matplotlib.pyplot as plt
from math import pi
from shapely.geometry import Polygon

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


def plot_br(l_pp, l_pm, l_pd, r_rel, steps=1000, color='black', label=''):
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

    plt.plot(fs[0], fs[1], color=color, label=label)

    return fs_2_poly(fs)


def fs_2_poly(fs):
    poly_arr = []
    for x, y in zip(fs[0], fs[1]):
        poly_arr.append([x, y])
    poly = Polygon(poly_arr)
    return poly.buffer(0)


def plot_finger(l_pp, l_pm, l_pd, r_rel):
    """draw the finger in the starting position"""
    mcp = r_rel['mcp'][0]
    pip = r_rel['pip'][0]
    dip = r_rel['dip'][0]

    xpip, ypip, xdip, ydip, xtip, ytip = deg_2_pos(
        l_pp, l_pm, l_pd, mcp, pip, dip, mult=True)

    x_arr = [0, xpip, xdip, xtip]
    y_arr = [0, ypip, ydip, ytip]

    plt.plot(x_arr, y_arr, color='black', label='_Hidden')
    plt.scatter(x_arr, y_arr, color='black', label='_Hidden')


def perform_br_plot(l_pp, l_pm, l_pd, r_extra=0):
    plt.ylim([-110, 40])
    plt.xlim([-50, 100])
    plt.grid(0.25)
    plot_finger(l_pp, l_pm, l_pd, R_all)
    poly_all = plot_br(l_pp, l_pm, l_pd, R_all, label='Overall ROM')
    poly_func = plot_br(l_pp, l_pm, l_pd, R_func,
                        color='darkred', label='Functional ROM')

    if r_extra != 0:
        plot_br(l_pp, l_pm, l_pd, r_extra)

    return poly_all, poly_func


def plot_br_fitted(l_pp, l_pm, l_pd, fd, color, label=''):
    pt1 = 0.99
    mcp_arr, pip_arr, dip_arr = filt_d(fd['deg_1']), filt_d(
        fd['deg_2'], u_lim=-10, pt1=pt1), filt_d(fd['deg_3'])

    poly_all, poly_func = perform_br_plot(l_pp, l_pm, l_pd, r_extra=0)

    fs = [[], []]
    for (mcp, pip, dip) in zip(mcp_arr, pip_arr, dip_arr):
        xtip, ytip = deg_2_pos(l_pp, l_pm, l_pd, -mcp, -pip, -dip)
        fs[0].append(xtip)
        fs[1].append(ytip)
    plt.plot(fs[0], fs[1], color=color, linewidth=2, label=label)

    poly_exo = fs_2_poly(fs)
    plot_inter_infos(poly_all, poly_func, poly_exo)


def plot_inter_infos(poly_all: Polygon, poly_func: Polygon, poly_exo: Polygon):
    print('Overall ROM: ', round(poly_all.intersection(
        poly_exo).area / poly_all.area, 2), ' %')
    print('Functional ROM: ', round(poly_func.intersection(
        poly_exo).area / poly_func.area, 2), ' %')
    print('Area Overall: ', round(poly_all.area, 2))
    print('Area Func: ', round(poly_func.area, 2))
    print('Area Exo: ', round(poly_exo.area, 2))


def pt1_filt(deg_arr, pt1):
    deg_old = deg_arr[0]

    for i, deg in enumerate(deg_arr):
        deg_old = pt1 * deg_old + (1-pt1) * deg
        deg_arr[i] = deg_old

    return deg_arr


def filt_values(deg_arr, val1=0, val_high=200, val_low=-220):
    deg_old = deg_arr[0]

    # exclude 0s
    for i, deg in enumerate(deg_arr):
        if deg == val1:
            deg_arr[i] = deg_old
        elif deg < val_low:
            deg_arr[i] = deg_old
        elif deg > val_high:
            deg_arr[i] = deg_old
        else:
            deg_old = deg

    return deg_arr


def filt_d(deg_arr, u_lim=30, pt1=0.95):
    deg_arr = filt_values(deg_arr)

    for i, deg in enumerate(deg_arr):
        if deg > 30:
            deg = deg - 180
        if deg > u_lim:
            deg = deg - 180
        if deg < -220:
            deg = deg + 180
        if deg < -130:
            deg = -130

        deg_arr[i] = deg

    deg_old = deg_arr[0]

    # exclude 0s
    for i, deg in enumerate(deg_arr):
        if abs(deg - deg_old) > 50:
            deg = deg_old
        else:
            deg_old = deg
        deg_arr[i] = deg

    return pt1_filt(deg_arr, pt1)


if __name__ == '__main__':
    l_pp = 45
    l_pm = 25
    l_pd = 24
    perform_br_plot(l_pp, l_pm, l_pd)

# %%
