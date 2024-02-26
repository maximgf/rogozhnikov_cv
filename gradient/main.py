import numpy as np
import matplotlib.pyplot as plt

def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1

size = 100
image = np.zeros((size, size, 3), dtype="uint8")
assert image.shape[0] == image.shape[1]

color1 = np.array([255, 128, 0])
color2 = np.array([0, 128, 255])

x = np.linspace(0, 1, size)
y = np.linspace(0, 1, size)

Ox, Oy = np.meshgrid(x, y)

t = (Ox + Oy)/2

colors = lerp(color2, color1, t[..., np.newaxis])
image[:, :, :] = colors.astype(np.uint8)

plt.figure(1)
plt.imshow(image)
plt.show()
