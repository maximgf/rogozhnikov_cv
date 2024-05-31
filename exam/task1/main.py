import cv2
import numpy as np

image = cv2.imread('img.png')
# Целевой цвет (например, зеленый)
image_orig = image

image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

fon = image[0][0]

# Создание маски для изменения цветов пикселей
mask = np.where(image == fon, 0, 255)

# Применение маски к изображению
image = np.where(mask == 0, 0, 255).astype(np.uint8)
'''cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()'''
contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

max_area = 0
max_contour = None

for contour in contours:
    '''x, y, w, h = cv2.boundingRect(contour)
    cv2.imshow('Contour', image_orig[y:y+h,x:x+w])
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''
    area = cv2.contourArea(contour)
    
    perimeter = cv2.arcLength(contour, True)
    
    internal_area = area - perimeter
    
    if internal_area > max_area:
        max_area = internal_area
        max_contour = contour

if max_contour is not None:
    x, y, w, h = cv2.boundingRect(max_contour)
    cv2.rectangle(image_orig,(x,y),(x+w,y+h),(0,0,0))
    cv2.imshow('Image without perimetr with max area figure', image_orig)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No contours found.")
 

 