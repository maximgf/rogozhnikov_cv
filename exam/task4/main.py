import cv2
import numpy as np
#The nominal resolution is a numerical value in pixels per inch
nominal = 1.05714
image = cv2.imread('img.jpg')

image_orig = image

hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_, image = cv2.threshold(image, 160, 255, cv2.THRESH_BINARY)
image = cv2.GaussianBlur(image,(21,21),1)
'''cv2.imshow('Image',image)
cv2.waitKey(0)
cv2.destroyAllWindows()'''

contours,_ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    x,y,w,h = cv2.boundingRect(contour)
    epsilon = 0.001 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    if len(approx) == 36:
        diameter_real = w / nominal
        print("\n",diameter_real,"inch")
        cv2.imshow('Image',image[y:y+h,x:x+w])
        cv2.waitKey(0)
        cv2.destroyAllWindows()