# %%

import pandas as pd
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly
import numpy as np
import os

cur_path = os.getcwd()
addon = 'poti_kalib'
filename = 'poti_calibration.xlsx'
filename = filename if addon in cur_path else f'{addon}/{filename}'
df = pd.read_excel(filename)
a_arr = np.array(df['Neu A'])
b_arr = np.array(df['Neu B'])
k_arr = np.array(df['K'])
k_arr = k_arr[k_arr < 1e5]
grad = np.array(df['Grad'])


def fit_poti(grad_arr, poti_arr, poly_deg=3, offset=0):
    grad_arr = grad_arr[:len(poti_arr)]
    coefficients = poly.polyfit(poti_arr, grad_arr, poly_deg)
    ffit = poly.Polynomial(coefficients)

    plt.grid(0.25)
    plt.plot(poti_arr, grad_arr, label='True Value', linestyle='-.')
    plt.plot(poti_arr, ffit(poti_arr), label='Measured Value')
    plt.xlabel('Raw Value []')
    plt.ylabel('Degree [°]')
    plt.xlim([0, 3500])
    plt.ylim([0, 180])
    plt.legend()

    # apply offset:
    coefficients[0] += offset
    ffit = poly.Polynomial(coefficients)

    coefficients_lin = poly.polyfit(poti_arr, grad_arr, 1)
    print('Coefficients: ', coefficients_lin)

    return ffit


# %%
poti_polys = {}
plt.figure(figsize=(8, 12))
plt.subplot(3, 1, 1)
poti_polys['B'] = fit_poti(grad, b_arr, offset=-99.719)
plt.subplot(3, 1, 2)
poti_polys['A'] = fit_poti(grad, a_arr, offset=-48.569)
plt.subplot(3, 1, 3)
poti_polys['K'] = fit_poti(grad, k_arr, offset=-36)  # -16 original!
# %%
#poti_polys['K'](2257) - 90
# %%
poti_polys['B'](3740) - 90
# %%
poti_polys['A'](2817) - 90
# %%
poti_polys['B'](2260) - 0
# %%
