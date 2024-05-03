import cv2 as cv
import numpy as np

image_orig = cv.imread("balls_and_rects.png")



image = cv.bitwise_not(image_orig)

image = cv.GaussianBlur(image,(9,9),0)


gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)


_, thrash = cv.threshold(gray_image, 240, 255, cv.THRESH_BINARY)
contours, _ = cv.findContours(thrash, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
color_circle = {}
color_rect = {}

for contour in contours[1:]:
    shape = cv.approxPolyDP(contour, 0.01*cv.arcLength(contour, True), True)  

    x, y, w, h = cv.boundingRect(contour)

    cropped_image = image[y:y+h, x:x+w]
    color = cropped_image.shape
    if len(shape) <= 8:
        if color in color_rect:
            color_rect[color] += 1
        else:
            color_rect[color] = 1
    else:
        if color in color_circle:
            color_circle[color] += 1
        else:
            color_circle[color] = 1
print('Всего фигур: ',sum(color_rect.values()) + sum(color_circle.values()))
print('Rect: ')
print(color_rect)
print('Circle: ')
print(color_circle)