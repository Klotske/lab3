import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

t = np.linspace(0, 2 * np.pi)
x = np.sin(t)
y = np.cos(t)

# Create & save plot
fig = plt.figure(figsize=(6, 6))
plt.plot(x, y, 'k')
plt.savefig('plot.png')

# Load plot & convert to grayscale
img = Image.open('plot.png')
img = img.convert('1')
