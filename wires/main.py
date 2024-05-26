import numpy as np
from skimage.measure import label
import matplotlib.pyplot as plt

def dillation(arr, struct):
    res = np.zeros_like(arr)
    for y in range(1, arr.shape[0] - 1):
        for x in range(1, arr.shape[1] - 1):
            sub = arr[y - 1 : y + 2, x - 1 : x + 2]
            rsub = np.logical_and(arr[y, x], struct)
            res[y - 1 : y + 2, x - 1 : x + 2] = np.logical_or(
                res[y - 1 : y + 2, x - 1 : x + 2], rsub
            )
    return res

def erosian(arr, struct):
    result = np.zeros_like(arr)
    for y in range(1, arr.shape[0] - 1):
        for x in range(1, arr.shape[1] - 1):
            sub = arr[y - 1 : y + 2, x - 1 : x + 2]
            if np.all(sub >= struct):
                result[y, x] = 1
    return result

def closing(arr, struct):
    return dillation(erosian(arr, struct), struct)

m = np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]])

for i in range(1, 6 + 1):  # Измените диапазон на количество файлов, которые у вас есть
    img = np.load(f"wires{i}.npy")
    labeled = label(img)
    for wire_label in np.unique(labeled):
        if wire_label != 0:  # 0 - это фон
            wire = np.where(labeled == wire_label,1,0)
            wire_closed = closing(wire, m)

            if np.max(label(wire_closed)) == 0:
                print("Провод разорван")
            else:
                print(f"img:{i} Провод{(np.max(wire_label))} Дырок: {np.max(label(wire_closed)) - 1}")
                plt.imshow(wire_closed)
                plt.show()