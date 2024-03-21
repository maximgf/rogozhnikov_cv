import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label

image = np.load('ps.npy')

labeled = label(image)

result = {}

for l in np.unique(labeled)[1:]:
    
    x, y = np.where(labeled == l)
    x = x - x.min()
    y = y - y.min()
    k = (str(x), str(y))

    if k not in result.keys():
        result[k] = 1
    else:
        result[k] += 1



for i, (fi, coun) in enumerate(result.items()):

    plt.subplot(1, 5, i + 1)

    fi = (np.fromstring(fi[0][1:-1], dtype=int, sep=" "),np.fromstring(fi[1][1:-1], dtype=int, sep=" "),)
    fig = np.zeros((max(fi[0]) + 1, max(fi[1]) + 1))
    fig[fi[0], fi[1]] = 1

    plt.title(f"{coun}")
    plt.imshow(fig)

plt.suptitle(f"Всего: {len(result.items())}")
plt.show()