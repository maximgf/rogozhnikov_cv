import cv2
import numpy as np
image = cv2.imread('img.png')

image_orig = image

image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

fon = image[0][0]

# Создание маски для изменения цветов пикселей
mask = np.where(image == fon, 0, 255)

# Применение маски к изображению
image = np.where(mask == 0, 0, 255).astype(np.uint8)
'''cv2.imshow('Image',image)
cv2.waitKey(0)
cv2.destroyAllWindows()'''

hsv_image = cv2.cvtColor(image_orig, cv2.COLOR_BGR2HSV)

contours,_ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

max_saturetion = 0
circle = 0
for countour in contours:
    x,y,w,h = cv2.boundingRect(countour)
    _, saturation, _ = cv2.split(hsv_image[y:y+h,x:x+w])
    average = np.mean(saturation[saturation > 0])
    '''cv2.imshow('Image',image_orig[y:y+h,x:x+w])
    cv2.waitKey(0)'''
    if max_saturetion < average:
        max_saturetion = average
        circle = countour

x,y,w,h = cv2.boundingRect(circle)
cv2.imshow('Circle',image_orig[y:y+h,x:x+w])
cv2.waitKey(0)

