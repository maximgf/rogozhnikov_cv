import cv2 as cv
import numpy as np

image_orig = cv.imread("balls_and_rects.png")



image = cv.bitwise_not(image_orig)

image = cv.GaussianBlur(image,(3,3),0)


gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)


_, thrash = cv.threshold(gray_image, 127, 255, cv.THRESH_BINARY)
contours, _ = cv.findContours(thrash, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
color_circle = {}
color_rect = {}
for contour in contours[1:]:
    x, y, w, h = cv.boundingRect(contour)
    cropped_image = image_orig[y:y+h, x:x+w]
    center_x = w // 2
    center_y = h // 2
    color = tuple(cropped_image[center_y, center_x])

    color_rect[color]=1
    break
for contour in contours[2:]:
    #shape = cv.approxPolyDP(contour, 0.01*cv.arcLength(contour, True), True)  

    x, y, w, h = cv.boundingRect(contour)
    cv.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 1)
    cropped_image = image_orig[y:y+h, x:x+w]
    area = cv.contourArea(contour)
    center_x = w // 2
    center_y = h // 2
    color = tuple(cropped_image[center_y, center_x])
    if (((w-1)*(h-1))-area) <= 2:
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