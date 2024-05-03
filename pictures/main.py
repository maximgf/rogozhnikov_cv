import cv2
from skimage.measure import label
import numpy as np
video = 'pictures.avi'
cap = cv2.VideoCapture(video)
count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    else:
        print(ret)
        if (np.max(label(frame))) == 71356:
            count += 1
'''Программа долго работает. Ответ для моей картинки 95'''
print(count)

