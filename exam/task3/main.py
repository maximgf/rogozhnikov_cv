import cv2
import numpy as np
from skimage.measure import label
image = cv2.imread('img.png')

image_orig = image

image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

fon = image[0][0]

mask = np.where(image == fon, 0, 255)

image = np.where(mask == 0, 0, 255).astype(np.uint8)

'''cv2.imshow('Image',image)
cv2.waitKey(0)
cv2.destroyAllWindows()'''

contours,_ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
counter = {"L":0,"J":0,"D":0,"K":0,"R":0}
for countour in contours:
    x,y,w,h = cv2.boundingRect(countour)
    labeled = label(image[y+1:y+h - 1,x+1:x+w - 1],background=255)
    holes = np.max(labeled)
    if holes == 1:
        if image[y+1][x+w-1] == 0:
            #print("L")
            counter["L"] += 1
        else:
            #print("J")
            counter["J"] += 1
    else:
        if image[y+1][x+w-1] == 0:
            #print("D")
            counter["D"] += 1
        elif image[y+h//2][x+w-1] == 0:
            #print("K")
            counter["K"] += 1
        else:
            #print("R")
            counter["R"] += 1
    '''cv2.imshow('Image',image[y+1:y+h - 1,x+1:x+w - 1])
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''
print(counter)