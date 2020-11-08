import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

import bitmap_helper


t = np.linspace(0, 2 * np.pi)
x = np.sin(t)
y = np.cos(t)

# Create & save plot
fig = plt.figure(figsize=(4, 4))
plt.plot(x, y, 'k')
plt.savefig('plot.png')

# Load plot & rotate to fix image reading
img = Image.open('plot.png').rotate(90)

pixels = img.load()
width, height = img.size
print(width, height)

all_pixels = []
for x in range(width):
    for y in range(height):
        _pix = pixels[x, y]
        mono_pix = 1 if round(sum(_pix)/float(len(_pix))) > 127 else 0
        all_pixels.append(mono_pix)

img.close()

# Write bitmap
file_name = 'plot_bitmap.bmp'
bitmap_helper.create_monochrome_bitmap(file_name, all_pixels, width, height)
