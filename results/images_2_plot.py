# %%

import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import numpy as np


fig = plt.figure(figsize=(20, 30))
name = 'true_hands'
ft = 26


ax2 = plt.subplot(3, 1, 1)
im1 = np.array(Image.open('./niko.png'))
plt.imshow(im1)
x_axis = ax2.axes.get_xaxis()
x_axis.set_visible(False)
y_axis = ax2.axes.get_yaxis()
y_axis.set_visible(False)
plt.title('(a)', y=-0.15, fontsize=ft)

ax3 = plt.subplot(3, 1, 2)
im1 = np.array(Image.open('./tina.png'))
plt.imshow(im1)
x_axis = ax3.axes.get_xaxis()
x_axis.set_visible(False)
y_axis = ax3.axes.get_yaxis()
y_axis.set_visible(False)
plt.title('(b)', y=-0.15, fontsize=ft)

ax4 = plt.subplot(3, 1, 3)
im1 = np.array(Image.open('./chrissi.png'))
plt.imshow(im1)
x_axis = ax4.axes.get_xaxis()
x_axis.set_visible(False)
y_axis = ax4.axes.get_yaxis()
y_axis.set_visible(False)
plt.title('(c)', y=-0.15, fontsize=ft)


png1 = BytesIO()
fig.savefig(png1, format='png')

# (2) load this image into PIL
png2 = Image.open(png1)

# (3) save as TIFF
png2.save(f'./{name}.tiff')
png1.close()

# %%
fig = plt.figure(figsize=(30, 20))
name = 'true_hands'
ft = 30

ax2 = plt.subplot(2, 1, 1)
im1 = np.array(Image.open('./rendered.png'))
plt.imshow(im1)
x_axis = ax2.axes.get_xaxis()
x_axis.set_visible(False)
y_axis = ax2.axes.get_yaxis()
y_axis.set_visible(False)
plt.title('(a)', y=-0.15, fontsize=ft)

ax2 = plt.subplot(3, 3, 7)
im1 = np.array(Image.open('./niko.png'))
plt.imshow(im1)
x_axis = ax2.axes.get_xaxis()
x_axis.set_visible(False)
y_axis = ax2.axes.get_yaxis()
y_axis.set_visible(False)
plt.title('(b)', y=-0.15, fontsize=ft)

ax3 = plt.subplot(3, 3, 8)
im1 = np.array(Image.open('./tina.png'))
plt.imshow(im1)
x_axis = ax3.axes.get_xaxis()
x_axis.set_visible(False)
y_axis = ax3.axes.get_yaxis()
y_axis.set_visible(False)
plt.title('(c)', y=-0.15, fontsize=ft)

ax4 = plt.subplot(3, 3, 9)
im1 = np.array(Image.open('./chrissi.png'))
plt.imshow(im1)
x_axis = ax4.axes.get_xaxis()
x_axis.set_visible(False)
y_axis = ax4.axes.get_yaxis()
y_axis.set_visible(False)
plt.title('(d)', y=-0.15, fontsize=26)


png1 = BytesIO()
fig.savefig(png1, format='png')

# (2) load this image into PIL
png2 = Image.open(png1)

# (3) save as TIFF
png2.save(f'./{name}.tiff')
png1.close()
# %%
png2 = Image.open('all_in_one.png')

# (3) save as TIFF
png2.save(f'./{name}.tiff')
png1.close()
# %%
